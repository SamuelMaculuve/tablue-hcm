# Generated by Django 5.0.9 on 2024-11-10 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0002_insurancecompany_insurancecompanytype_insuranceplan_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
