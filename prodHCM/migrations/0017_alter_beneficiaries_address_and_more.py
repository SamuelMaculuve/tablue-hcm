# Generated by Django 5.0.9 on 2024-11-15 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0016_beneficiaries_session_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiaries',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='beneficiaries',
            name='date_of_activity_start',
            field=models.DateField(blank=True, null=True, verbose_name='Início de actividade'),
        ),
        migrations.AlterField(
            model_name='beneficiaries',
            name='district',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Distrito'),
        ),
        migrations.AlterField(
            model_name='beneficiaries',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='beneficiaries',
            name='nuitNumber',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='NUIT'),
        ),
        migrations.AlterField(
            model_name='beneficiaries',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Número de celular'),
        ),
        migrations.AlterField(
            model_name='beneficiaries',
            name='province',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Provincia'),
        ),
    ]