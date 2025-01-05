# Generated by Django 5.0.9 on 2025-01-05 12:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0046_alter_insuranceplan_insurancecompany'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insuranceplan',
            name='insuranceCompany',
        ),
        migrations.AddField(
            model_name='insuranceplan',
            name='insuranceCompany',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prodHCM.insurancecompany'),
        ),
    ]
