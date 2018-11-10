from django.db import models
from contracts.models import Contract


class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='payments', verbose_name='所属合同')
    amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='付款金额')
    record = models.CharField(max_length=4, verbose_name='凭证号', null=True, blank=True)
    payday = models.DateField(verbose_name='付款时间')
    text = models.TextField(blank=True, null=True, verbose_name='付款备注')
    rate = models.DecimalField(max_digits=6, decimal_places=4, verbose_name='增值税率')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return "{:,.2f}".format(self.amount)

    class Meta:
        ordering = ('contract', 'created')
        verbose_name = '付款记录'
        verbose_name_plural = '付款记录'
