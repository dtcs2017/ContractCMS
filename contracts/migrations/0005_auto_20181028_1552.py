# Generated by Django 2.1.1 on 2018-10-28 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0004_auto_20181028_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='definite',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True, verbose_name='决算金额'),
        ),
    ]
