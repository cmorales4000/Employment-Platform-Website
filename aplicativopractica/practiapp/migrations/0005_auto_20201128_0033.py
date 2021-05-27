# Generated by Django 3.1.2 on 2020-11-28 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practiapp', '0004_auto_20201127_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='is_empresa',
            field=models.BooleanField(default=False, verbose_name='Es Empleador? (Empresa)'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Nombre/Razón Legal'),
        ),
    ]
