# Generated by Django 5.0.9 on 2025-01-05 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0044_alter_insuranceplan_insurancecompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuranceplan',
            name='hasPlafonewqeq',
            field=models.BooleanField(default=False),
        ),
    ]
