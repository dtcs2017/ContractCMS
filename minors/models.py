from django.db import models
from contracts.models import Company, Subject
from django.db.models import Sum


class DirectCost(models.Model):
    name = models.CharField(max_length=50, verbose_name='名称', db_index=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='付款金额')
    supplier = models.CharField(max_length=50, verbose_name='付款单位', db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='directcosts', verbose_name='公司',
                                default=1)
    subject = models.ForeignKey(Subject, related_name='directcosts', on_delete=models.CASCADE, verbose_name='类别')
    text = models.TextField(blank=True, null=True, verbose_name='付款说明')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return "{}-{}".format(self.name, self.amount)

    @property
    def total_reqs(self):
        if self.directreqs.all().count():
            reqs = self.directreqs.all().aggregate(Sum('amount'))['amount__sum']
            return reqs
        else:
            return None

    @property
    def total_pays(self):
        if self.directpayments.all().count():
            pays = self.directpayments.all().aggregate(Sum('amount'))['amount__sum']
            return pays
        else:
            return None

    class Meta:
        ordering = ('subject', 'created')
        verbose_name = '非合同付款'
        verbose_name_plural = '非合同付款'


class DirectRequisition(models.Model):
    cost_record = models.ForeignKey(DirectCost, on_delete=models.CASCADE, related_name='directreqs',
                                    verbose_name='所属非合同付款记录')
    amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='请款金额')
    invoice = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='收到发票或凭证金额')
    payday = models.DateField(verbose_name='请款时间')
    text = models.TextField(blank=True, null=True, verbose_name='付款说明')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return "{:,.2f}".format(self.amount)

    class Meta:
        ordering = ('cost_record', 'created')
        verbose_name = '非合同付款请款记录'
        verbose_name_plural = '非合同付款请款记录'


class DirectPayment(models.Model):
    cost_record = models.ForeignKey(DirectCost, on_delete=models.CASCADE, related_name='directpayments',
                                    verbose_name='所属非合同付款记录')
    amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='付款金额')
    record = models.CharField(max_length=4, verbose_name='凭证号', null=True, blank=True)
    payday = models.DateField(verbose_name='付款时间')
    rate = models.DecimalField(max_digits=6, decimal_places=4, verbose_name='增值税率',default=0)
    text = models.TextField(blank=True, null=True, verbose_name='付款备注')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return "{:,.2f}".format(self.amount)

    class Meta:
        ordering = ('cost_record', 'created')
        verbose_name = '付款记录'
        verbose_name_plural = '付款记录'
