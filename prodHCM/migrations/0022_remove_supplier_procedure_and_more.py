# Generated by Django 5.0.9 on 2024-11-22 20:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0021_supplier_procedure'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='procedure',
        ),
        migrations.AlterField(
            model_name='insurancecompanyprocedure',
            name='insuranceCompany',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prodHCM.insurancecompany'),
        ),
    ]
