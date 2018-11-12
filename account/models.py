from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    继承ABU替代默认User类。需配合settings.py中设置：AUTH_USER_MODEL = 'account.User'。
    is_为权限字段，目前实际用到合约部，工程部和财务部。
    单独某部门权限管理器位于accounts.permission_decortor
    多个部门权限管理在视图函数中使用具体逻辑确定
    权限不足，统一返回HttpResponse，不直接抛出异常
    """
    is_contractor = models.BooleanField(default=False, verbose_name='合约部')
    is_engineer = models.BooleanField(default=False, verbose_name='工程部')
    is_frontier = models.BooleanField(default=False, verbose_name='前期部')
    is_designer = models.BooleanField(default=False, verbose_name='设计部')
    is_accountant = models.BooleanField(default=False, verbose_name='财务部')

    class Meta(AbstractUser.Meta):
        pass
