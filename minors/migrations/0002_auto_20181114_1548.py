# Generated by Django 2.1.1 on 2018-11-14 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='directcost',
            name='name',
            field=models.CharField(db_index=True, default=1, max_length=50, verbose_name='名称'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='directcost',
            name='supplier',
            field=models.CharField(db_index=True, max_length=50, verbose_name='付款单位'),
        ),
    ]