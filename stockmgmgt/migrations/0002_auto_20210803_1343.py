# Generated by Django 2.2.14 on 2021-08-03 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmgt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='supplier',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='stockhistory',
            name='supplier',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
