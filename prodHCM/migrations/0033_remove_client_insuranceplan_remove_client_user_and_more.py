# Generated by Django 5.0.9 on 2025-01-02 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodHCM', '0032_remove_insuranceplan_plafon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='insurancePlan',
        ),
        migrations.RemoveField(
            model_name='client',
            name='user',
        ),
        migrations.RemoveField(
            model_name='insuranceplan',
            name='procedure',
        ),
        migrations.AddField(
            model_name='insuranceplan',
            name='hasPlafon',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='insuranceplan',
            name='plafonPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Plafon do plano'),
        ),
        migrations.AlterField(
            model_name='insuranceplan',
            name='status',
            field=models.CharField(choices=[('activo', 'Activo'), ('cancelado', 'Cancelado'), ('suspenso', 'Suspenso'), ('expirado', 'Expirado')], default='activo', max_length=20, verbose_name='Status do Plano'),
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome do Nível')),
                ('hasPlafon', models.BooleanField(blank=True, default=False, null=True)),
                ('plafonPrice', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Plafon do plano')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('parent_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sublevels', to='prodHCM.level', verbose_name='Nível Pai')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='prodHCM.insuranceplan', verbose_name='Plano')),
                ('procedure', models.ManyToManyField(blank=True, related_name='insurancePlan', to='prodHCM.procedure')),
            ],
        ),
    ]