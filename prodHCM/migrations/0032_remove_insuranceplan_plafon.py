# Generated by Django 5.0.9 on 2024-11-29 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0031_insuranceplan_plafon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insuranceplan',
            name='plafon',
        ),
    ]
