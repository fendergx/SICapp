# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-27 09:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sicapp', '0018_auto_20181127_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librodiario',
            name='libroM',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sicapp.LibroMayor'),
        ),
    ]