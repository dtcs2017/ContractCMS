from django.db import models
from contracts.models import Contract


class Requisition(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='requisitions', verbose_name='所属合同')
    amount = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='请款金额')
    invoice = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='收到发票金额')
    payday = models.DateField(verbose_name='请款时间')
    text = models.TextField(blank=True, null=True, verbose_name='付款说明')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return "{:,.2f}".format(self.amount)

    class Meta:
        ordering = ('contract', 'created')
        verbose_name = '请款记录'
        verbose_name_plural = '请款记录'
