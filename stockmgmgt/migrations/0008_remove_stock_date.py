# Generated by Django 3.2.3 on 2021-06-03 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmgt', '0007_stock_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='date',
        ),
    ]
