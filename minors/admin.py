from django.contrib import admin
from .models import DirectPayment, DirectRequisition, DirectCost


@admin.register(DirectCost)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'supplier', 'company', 'subject', 'text']


@admin.register(DirectRequisition)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['cost_record', 'amount', 'invoice', 'payday', 'text']


@admin.register(DirectPayment)
class StampAdmin(admin.ModelAdmin):
    list_display = ['cost_record', 'amount', 'record', 'payday', 'rate', 'text']
