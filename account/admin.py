from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'email', 'is_contractor', 'is_engineer', 'is_frontier', 'is_designer',
                    'is_accountant', 'is_active']
