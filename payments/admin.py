from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract', 'amount', 'payday', 'record', 'text')
