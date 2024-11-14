# Generated by Django 5.0.9 on 2024-11-14 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0012_alter_insuranceplan_insurancecompany'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='contractFile',
            field=models.FileField(upload_to='static/img/clients/'),
        ),
        migrations.AlterField(
            model_name='client',
            name='nuitFile',
            field=models.FileField(upload_to='static/img/clients/'),
        ),
        migrations.AlterField(
            model_name='insurancecompany',
            name='contractFile',
            field=models.FileField(upload_to='static/img/insuranceCompanyContracts/'),
        ),
        migrations.AlterField(
            model_name='insurancecompany',
            name='nuitFile',
            field=models.FileField(upload_to='static/img/insuranceCompanyNuits/'),
        ),
        migrations.AlterField(
            model_name='insurancecompany',
            name='supplier',
            field=models.ManyToManyField(blank=True, related_name='insuranceCompany', to='prodHCM.supplier'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='contractFile',
            field=models.FileField(upload_to='static/img/supplierContracts/'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='nuitFile',
            field=models.FileField(upload_to='static/img/supplierNuits/'),
        ),
    ]
