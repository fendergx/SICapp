# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-29 17:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sicapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoResultado',
            fields=[
                ('id_estadoResultado', models.AutoField(primary_key=True, serialize=False)),
                ('ingresosV', models.CharField(max_length=100)),
                ('costoV', models.CharField(max_length=100)),
                ('gastosA', models.CharField(max_length=100)),
                ('gastosC', models.CharField(max_length=100)),
                ('gastoF', models.CharField(max_length=100)),
                ('reserva', models.CharField(max_length=100)),
                ('impuestoR', models.CharField(max_length=100)),
                ('estadoF', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sicapp.EstadosF')),
            ],
        ),
    ]