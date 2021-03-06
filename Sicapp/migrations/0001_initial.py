# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-28 07:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('idCliente', models.AutoField(primary_key=True, serialize=False)),
                ('nrc', models.CharField(max_length=100)),
                ('razonSocial', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('idCompra', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('terminoCompra', models.CharField(default='Compra Gravada', max_length=100)),
                ('tipoCompra', models.CharField(default='Contado', max_length=100)),
                ('proveedor', models.CharField(max_length=5, null=True)),
                ('plazo', models.CharField(max_length=100, null=True)),
                ('iva', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ControlEfectivo',
            fields=[
                ('idControl', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('tipoComprobante', models.CharField(max_length=30)),
                ('concepto', models.CharField(max_length=50)),
                ('saldoEntrada', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('saldoSalida', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('saldoTotal', models.DecimalField(decimal_places=2, default=100000, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CostoAbsorcion',
            fields=[
                ('idCostoAbs', models.AutoField(primary_key=True, serialize=False)),
                ('producto', models.IntegerField()),
                ('costoProduccion', models.DecimalField(decimal_places=2, max_digits=7)),
                ('costoAdmon', models.DecimalField(decimal_places=2, max_digits=7)),
                ('costoComercial', models.DecimalField(decimal_places=2, max_digits=7)),
                ('costoFinanciero', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='CostoIndirecto',
            fields=[
                ('idCif', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.DecimalField(decimal_places=2, max_digits=7)),
                ('costoIF', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CostoUnitario',
            fields=[
                ('idCostoUnit', models.AutoField(primary_key=True, serialize=False)),
                ('produccionAnual', models.IntegerField()),
                ('costoUnitario', models.DecimalField(decimal_places=2, max_digits=4)),
                ('precioVenta', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('codCuenta', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('codigoN', models.CharField(max_length=8)),
                ('nombre', models.CharField(max_length=50)),
                ('tipoCuenta', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='DatoEntrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horas', models.DecimalField(decimal_places=2, max_digits=10)),
                ('des', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Detallecompra',
            fields=[
                ('idDetalleCompra', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('concepto', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('compra', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sicapp.Compra')),
            ],
        ),
        migrations.CreateModel(
            name='detalleKardex',
            fields=[
                ('idDetalle', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('idDetalleVenta', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('producto', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Kardex',
            fields=[
                ('idKardex', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('cantEntrada', models.IntegerField()),
                ('precEntrada', models.DecimalField(decimal_places=2, max_digits=7)),
                ('montoEntrada', models.DecimalField(decimal_places=2, max_digits=20)),
                ('cantSalida', models.IntegerField()),
                ('precSalida', models.DecimalField(decimal_places=2, max_digits=7)),
                ('montoSalida', models.DecimalField(decimal_places=2, max_digits=20)),
                ('cantExistencia', models.IntegerField()),
                ('precExistencia', models.DecimalField(decimal_places=2, max_digits=7)),
                ('montoExistencia', models.DecimalField(decimal_places=2, max_digits=20)),
                ('detalle', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sicapp.detalleKardex')),
            ],
        ),
        migrations.CreateModel(
            name='LibroDiario',
            fields=[
                ('idLibroD', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('descripcion', models.CharField(max_length=300)),
                ('cargo', models.CharField(max_length=80, null=True)),
                ('abono', models.CharField(max_length=80, null=True)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sicapp.Cuenta')),
            ],
        ),
        migrations.CreateModel(
            name='LibroMayor',
            fields=[
                ('idLibroM', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('debe', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('haber', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ManoDeObraD',
            fields=[
                ('idMod', models.AutoField(primary_key=True, serialize=False)),
                ('horasT', models.DecimalField(decimal_places=2, max_digits=7)),
                ('costoMOD', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MateriaPrima',
            fields=[
                ('idMp', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.DecimalField(decimal_places=2, max_digits=7)),
                ('cantidadM', models.DecimalField(decimal_places=2, max_digits=7)),
                ('valor', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodoContable',
            fields=[
                ('idPeriodo', models.AutoField(primary_key=True, serialize=False)),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('activo', models.BooleanField(default=True)),
                ('anio', models.IntegerField()),
                ('mes', models.IntegerField(default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Planilla',
            fields=[
                ('idPlanilla', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idProducto', models.AutoField(primary_key=True, serialize=False)),
                ('nombreP', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('idProveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nrc', models.CharField(max_length=100)),
                ('razonSocial', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransaccionCV',
            fields=[
                ('idTransaccion', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('concepto', models.CharField(max_length=50)),
                ('comprobante', models.CharField(max_length=50)),
                ('cargo', models.CharField(max_length=50, null=True)),
                ('abono', models.CharField(max_length=50, null=True)),
                ('plazoCredito', models.CharField(max_length=50, null=True)),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tipoTransaccion', models.CharField(max_length=6)),
                ('terminoTransacion', models.CharField(default='Gravada', max_length=6)),
                ('periodo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sicapp.PeriodoContable')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('idVenta', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('terminoVenta', models.CharField(default='Compra Gravada', max_length=100)),
                ('tipoVenta', models.CharField(default='Contado', max_length=100)),
                ('cliente', models.CharField(max_length=5, null=True)),
                ('plazo', models.CharField(max_length=100, null=True)),
                ('iva', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estado', models.BooleanField(default=False)),
                ('periodoCon', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='Sicapp.PeriodoContable')),
            ],
        ),
        migrations.AddField(
            model_name='libromayor',
            name='periodo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sicapp.PeriodoContable'),
        ),
        migrations.AddField(
            model_name='librodiario',
            name='libroM',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sicapp.LibroMayor'),
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='venta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sicapp.Venta'),
        ),
        migrations.AddField(
            model_name='costounitario',
            name='periodo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Sicapp.PeriodoContable'),
        ),
        migrations.AddField(
            model_name='controlefectivo',
            name='cuenta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sicapp.Cuenta'),
        ),
        migrations.AddField(
            model_name='controlefectivo',
            name='periodo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sicapp.PeriodoContable'),
        ),
        migrations.AddField(
            model_name='compra',
            name='periodoCon',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sicapp.PeriodoContable'),
        ),
    ]
