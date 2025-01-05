# Generated by Django 5.0.9 on 2025-01-05 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0033_remove_client_insuranceplan_remove_client_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insurancecompanyprocedure',
            name='insuranceCompany',
        ),
        migrations.RemoveField(
            model_name='insurancecompanyprocedure',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='level',
            name='procedure',
        ),
        migrations.AddField(
            model_name='level',
            name='insuranceCompanyProcedure',
            field=models.ManyToManyField(blank=True, null=True, related_name='insuranceCompanyProcedure', to='prodHCM.insurancecompanyprocedure'),
        ),
    ]
