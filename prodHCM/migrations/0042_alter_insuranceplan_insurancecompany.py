# Generated by Django 5.0.9 on 2025-01-05 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0041_alter_insuranceplan_insurancecompany'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuranceplan',
            name='insuranceCompany',
            field=models.ManyToManyField(blank=True, default=1, null=True, related_name='insurancePlans', to='prodHCM.insurancecompany'),
        ),
    ]
