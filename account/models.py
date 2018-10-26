from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_contractor = models.BooleanField(default=False, verbose_name='合约部')
    is_engineer = models.BooleanField(default=False, verbose_name='工程部')
    is_frontier = models.BooleanField(default=False, verbose_name='前期部')
    is_designer = models.BooleanField(default=False, verbose_name='设计部')
    is_accountant = models.BooleanField(default=False, verbose_name='财务部')

    class Meta(AbstractUser.Meta):
        pass
