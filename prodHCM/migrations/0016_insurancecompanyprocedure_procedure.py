# Generated by Django 5.0.9 on 2024-11-14 21:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0015_alter_insurancecompanyprocedure_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurancecompanyprocedure',
            name='procedure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prodHCM.procedure'),
        ),
    ]
