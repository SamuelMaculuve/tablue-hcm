# Generated by Django 5.0.9 on 2025-01-07 19:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0048_remove_insuranceplan_hasplafonewqeq_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='insurancePlan',
            field=models.ManyToManyField(blank=True, null=True, related_name='client', to='prodHCM.insuranceplan'),
        ),
        migrations.AlterField(
            model_name='insurancecompanyprocedure',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='insuranceCompanyProcedure', to='prodHCM.level'),
        ),
    ]