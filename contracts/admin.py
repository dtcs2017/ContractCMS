from django.contrib import admin
from .models import Subject, Stamp, Contract, Company
from requisitions.models import Requisition


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['subject', 'company', 'index', 'name', 'supplier', 'sign', 'amount', 'definite', 'active','is_cost', 'text',
                    'jgc', 'stamp', ]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Stamp)
class StampAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


class RequisitionInline(admin.StackedInline):
    model = Requisition
