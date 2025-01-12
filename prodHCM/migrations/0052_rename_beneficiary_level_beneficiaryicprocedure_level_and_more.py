# Generated by Django 5.0.9 on 2025-01-09 14:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0051_beneficiarylevel_beneficiaryicprocedure_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beneficiaryicprocedure',
            old_name='beneficiary_level',
            new_name='level',
        ),
        migrations.RemoveField(
            model_name='beneficiaryicprocedure',
            name='plafon',
        ),
        migrations.RemoveField(
            model_name='beneficiarylevel',
            name='beneficiary_plan',
        ),
        migrations.RemoveField(
            model_name='beneficiarylevel',
            name='level',
        ),
        migrations.RemoveField(
            model_name='beneficiarylevel',
            name='plafon',
        ),
        migrations.RemoveField(
            model_name='beneficiaryplan',
            name='insurancePlan',
        ),
        migrations.RemoveField(
            model_name='insurancecompanyprocedure',
            name='insurancePlan',
        ),
        migrations.AddField(
            model_name='beneficiaryicprocedure',
            name='negotiated_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Preço Negociado'),
        ),
        migrations.AddField(
            model_name='beneficiarylevel',
            name='hasPlafon',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='beneficiarylevel',
            name='insurancePlan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='beneficiaryLevel', to='prodHCM.beneficiaryplan'),
        ),
        migrations.AddField(
            model_name='beneficiarylevel',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='beneficiarylevel',
            name='parent_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sublevels', to='prodHCM.beneficiarylevel'),
        ),
        migrations.AddField(
            model_name='beneficiarylevel',
            name='plafonPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Plafon do plano'),
        ),
        migrations.AlterField(
            model_name='beneficiaryicprocedure',
            name='procedure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='beneficiaryICProcedure', to='prodHCM.procedure'),
        ),
        migrations.AlterField(
            model_name='beneficiaryplan',
            name='beneficiary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiaryPlan', to='prodHCM.beneficiaries'),
        ),
        migrations.AlterField(
            model_name='client',
            name='insurancePlan',
            field=models.ManyToManyField(blank=True, related_name='client', to='prodHCM.insuranceplan'),
        ),
    ]
