# Generated by Django 5.0.9 on 2024-11-12 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0007_remove_supplier_procedure_insurancecompany_supplier_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insuranceplan',
            name='procedure',
        ),
        migrations.CreateModel(
            name='InsuranceCompanyProcedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('negotiated_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço Negociado')),
                ('insuranceCompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prodHCM.insurancecompany')),
                ('procedure', models.ManyToManyField(blank=True, to='prodHCM.procedure')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prodHCM.supplier')),
            ],
        ),
        migrations.DeleteModel(
            name='NegotiatedPrice',
        ),
    ]