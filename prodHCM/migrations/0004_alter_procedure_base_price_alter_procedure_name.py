# Generated by Django 5.0.9 on 2024-11-11 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0003_delete_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedure',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Preço Base'),
        ),
        migrations.AlterField(
            model_name='procedure',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Procedimento'),
        ),
    ]