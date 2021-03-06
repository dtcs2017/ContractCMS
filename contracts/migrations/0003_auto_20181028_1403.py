# Generated by Django 2.1.1 on 2018-10-28 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_auto_20181028_1351'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'ordering': ('subject', 'index', 'created'), 'verbose_name': '合同'},
        ),
        migrations.AlterModelOptions(
            name='stamp',
            options={'ordering': ['created'], 'verbose_name': '印花税'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['created'], 'verbose_name': '合同种类'},
        ),
        migrations.AlterField(
            model_name='contract',
            name='active',
            field=models.BooleanField(default=True, verbose_name='有效'),
        ),
    ]
