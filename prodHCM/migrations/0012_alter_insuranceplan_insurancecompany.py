# Generated by Django 5.0.9 on 2024-11-13 08:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0011_alter_insuranceplan_insurancecompany'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuranceplan',
            name='insuranceCompany',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prodHCM.insurancecompany'),
        ),
    ]
