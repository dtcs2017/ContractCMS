from django.contrib import admin
from .models import Requisition


@admin.register(Requisition)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract', 'amount', 'invoice', 'payday', 'text')
