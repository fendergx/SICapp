from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Proveedor(models.Model):
    idProveedor= models.AutoField(primary_key=True)
    nrc=models.CharField(max_length=100,null=False)
    razonSocial=models.CharField(max_length=100,null=False)
    direccion=models.CharField(max_length=100,null=False)
    estado=models.BooleanField(default=True)                #Activo o Inactivo


class Compra(models.Model):
    idCompra = models.AutoField(primary_key=True)
    fecha=models.DateField()
    terminoCompra=models.CharField(max_length=100,null=False)       #Exenta o gravada
    tipoCompra=models.CharField(max_length=100,null=False)          #Credito o Contado
    proveedor=models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    plazo=models.CharField(max_length=100,null=False)
    iva=models.DecimalField(max_digits=8, decimal_places=2)
    total=models.DecimalField(max_digits=8, decimal_places=2)
    estado=models.BooleanField(default=False)

class Detallecompra(models.Model):
    idDetalleCompra=models.AutoField(primary_key=True)
    compra=models.ForeignKey(Compra, on_delete=models.CASCADE)
    cantidad=models.IntegerField()
    concepto=models.CharField(max_length=100,null=False)
    precio=models.DecimalField(max_digits=8, decimal_places=2)
    total=models.DecimalField(max_digits=8, decimal_places=2)



#---------------------------------------------------------------------------------------------------------------

class Cuenta(models.Model):
    codCuenta = models.CharField(max_length=10,primary_key=True)
    nombre = models.CharField(max_length=50)
    tipoCuenta = models.CharField(max_length=35)

class ControlEfectivo(models.Model):
    idControl = models.AutoField(primary_key=True)
    fecha = models.DateField()
    tipoComprobante = models.CharField(max_length=30)
    concepto = models.CharField(max_length=50)
    cuenta=models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    saldoEntrada = models.DecimalField(max_digits=7, decimal_places=2)
    SaldoSalida = models.DecimalField(max_digits=7, decimal_places=2)
    SaldoTotal = models.DecimalField(max_digits=7, decimal_places=2)


class TransaccionCV(models.Model):
    idTransaccion = models.AutoField(primary_key=True)
    fecha = models.DateField()
    concepto = models.CharField(max_length=50)
    comprobante = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    abono = models.CharField(max_length=50)
    plazoCredito = models.IntegerField()
    periodo = models.CharField(max_length=50)
    saldo = models.DecimalField(max_digits=8, decimal_places=2)
    tipoTransaccion = models.CharField(max_length=6)            #Compra o venta
    terminoTransacion = models.CharField(max_length=6)          #Exenta o gravada
    #iva                                                        Deberia llevar una tabla

class PeriodoContable(models.Model):
    idPeriodoConta = models.AutoField(primary_key=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    activo = models.BooleanField()
    anio = models.IntegerField()
    mes = models.IntegerField()


class libroMayor(models.Model):
    idLibroM = models.AutoField(primary_key=True)
    fecha = models.DateField()
    debe = models.CharField(max_length=100)
    haber = models.CharField(max_length=100)
    saldo = models.DecimalField(max_digits=7, decimal_places=2)
    estado = models.BooleanField()
    periodo = models.OneToOneField(PeriodoContable, on_delete=models.CASCADE)


class CostoAbsorcion(models.Model):
    idCostoAbs = models.AutoField(primary_key=True)
    producto = models.IntegerField()
    costoProduccion = models.DecimalField(max_digits=7, decimal_places=2)
    costoAdmon = models.DecimalField(max_digits=7, decimal_places=2)
    costoComercial = models.DecimalField(max_digits=7, decimal_places=2)
    costoFinanciero = models.DecimalField(max_digits=7, decimal_places=2)


class CostoUnitario(models.Model):
    idCostoUnit = models.AutoField(primary_key=True)
    periodo = models.OneToOneField(PeriodoContable, on_delete=models.CASCADE)
    produccionAnual = models.IntegerField()
    costoUnitario = models.DecimalField(max_digits=4, decimal_places=2)
    precioVenta = models.DecimalField(max_digits=4, decimal_places=2)

class detalleKardex(models.Model):
    idDetalle = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()


class Kardex(models.Model):
    idKardex = models.AutoField(primary_key=True)
    fecha = models.DateField()
    #entradas
    cantEntrada = models.IntegerField()
    precEntrada = models.DecimalField(max_digits=7, decimal_places=2)
    montoEntrada = models.DecimalField(max_digits=20, decimal_places=2)
    #Salidas
    cantSalida = models.IntegerField()
    precSalida = models.DecimalField(max_digits=7, decimal_places=2)
    montoSalida = models.DecimalField(max_digits=20, decimal_places=2)
    #Existencia
    cantExistencia = models.IntegerField()
    precExistencia = models.DecimalField(max_digits=7, decimal_places=2)
    montoExistencia = models.DecimalField(max_digits=20, decimal_places=2)
    detalle = models.ForeignKey(detalleKardex, on_delete=models.CASCADE)




class libroDiario(models.Model):
    idLibroD = models.AutoField(primary_key=True)
    fecha = models.DateField()
    libroM = models.OneToOneField(libroMayor, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=300)
    cargo = models.CharField(max_length=80)
    abono = models.CharField(max_length=80)

class Planilla(models.Model):
    idPlanilla = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)