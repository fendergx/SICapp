from __future__ import unicode_literals

from django.db import models

class Proveedor(models.Model):
    idProveedor = models.AutoField(primary_key=True)
    nrc = models.CharField(max_length=100, null=False)
    razonSocial = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=200, null=False)
    estado = models.BooleanField(default=True)  # Activo o Inactivo

class Cliente(models.Model):
    idCliente = models.AutoField(primary_key=True)
    nrc = models.CharField(max_length=100, null=False)
    razonSocial = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=200, null=False)
    estado = models.BooleanField(default=True)  # Activo o Inactivo

class PeriodoContable(models.Model):
    idPeriodo=models.AutoField(primary_key=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    activo=models.BooleanField(default=True)
    anio = models.IntegerField()
    mes = models.IntegerField(null=True,default=1)
	
	
class Compra(models.Model):
    idCompra = models.AutoField(primary_key=True)
    fecha = models.DateField()
    terminoCompra = models.CharField(max_length=100, null=False,default="Compra Gravada")  # Exenta o gravada
    tipoCompra = models.CharField(max_length=100, null=False, default="Contado")  # Credito o Contado
    proveedor = models.CharField( max_length=5,null=True)
    plazo = models.CharField(max_length=100, null=True)
    iva = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.BooleanField(default=False)
    periodoCon=models.ForeignKey(PeriodoContable, on_delete=models.CASCADE,default=1)
    def __int__(self): return self.idCompra

class Detallecompra(models.Model):
    idDetalleCompra = models.AutoField(primary_key=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, default=1)
    cantidad = models.IntegerField()
    concepto = models.CharField(max_length=100, null=False)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)

class Venta(models.Model):
    idVenta = models.AutoField(primary_key=True)
    fecha = models.DateField()
    terminoVenta = models.CharField(max_length=100, null=False,default="Compra Gravada")  # Exenta o gravada
    tipoVenta = models.CharField(max_length=100, null=False, default="Contado")  # Credito o Contado
    cliente = models.CharField( max_length=5,null=True)
    plazo = models.CharField(max_length=100, null=True)
    iva = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.BooleanField(default=False)
    periodoCon=models.ForeignKey(PeriodoContable, on_delete=models.CASCADE,default=3)
    def __int__(self): return self.idVenta

class DetalleVenta(models.Model):
    idDetalleVenta = models.AutoField(primary_key=True)
    venta= models.ForeignKey(Venta, on_delete=models.CASCADE, default=1)
    cantidad = models.IntegerField()
    producto = models.CharField(max_length=100, null=False)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)

class Cuenta(models.Model):
    codCuenta = models.CharField(max_length=10, primary_key=True)
    codigoN = models.CharField(max_length=8) #Codigo segun NIIF
    nombre = models.CharField(max_length=50)
    tipoCuenta = models.CharField(max_length=25)
    padre = models.BooleanField(default=True)

class ControlEfectivo(models.Model):
    idControl = models.AutoField(primary_key=True)
    fecha = models.DateField()
    tipoComprobante = models.CharField(max_length=30)
    concepto = models.CharField(max_length=50)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE,default=1)
    saldoEntrada = models.DecimalField(max_digits=7, decimal_places=2,null=True)
    saldoSalida = models.DecimalField(max_digits=7, decimal_places=2,null=True)
    saldoTotal = models.DecimalField(max_digits=10, decimal_places=2,null=True, default=100000)
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE, default=1)

class TransaccionCV(models.Model):
    idTransaccion = models.AutoField(primary_key=True)
    fecha = models.DateField()
    concepto = models.CharField(max_length=50)
    comprobante = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50, null=True)
    abono = models.CharField(max_length=50, null=True)
    plazoCredito = models.CharField(max_length=50, null=True)
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE,default=1)
    saldo = models.DecimalField(max_digits=8, decimal_places=2)
    tipoTransaccion = models.CharField(max_length=6)  # Compra o venta
    terminoTransacion = models.CharField(max_length=6,default='Gravada' )  # Exenta o gravada
    # iva
    #Deberia llevar una tabla



class LibroMayor(models.Model):
    idLibroM = models.AutoField(primary_key=True)
    fecha = models.DateField()
    debe = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    haber = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    saldo = models.DecimalField(max_digits=7, decimal_places=2,null=True)
    estado = models.BooleanField(default=True)
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE, default=1)


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
    tipo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()

    def __str__(self): return self.nombre

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
    detalle = models.ForeignKey(detalleKardex, on_delete=models.CASCADE,default=1)




class LibroDiario(models.Model):
    idLibroD=models.AutoField(primary_key=True)
    fecha = models.DateField()
    libroM = models.ForeignKey(LibroMayor, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=300)
    cargo = models.CharField(max_length=80, null=True)
    abono = models.CharField(max_length=80,null=True)

class Planilla(models.Model):
    idPlanilla = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

class empleado(models.Model):
	nombreCompleto = models.CharField(max_length=60)
	cargo = models.CharField(max_length=100)
	sueldoBase = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	ingresoExtra = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	vacaciones = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	totalDevengado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	isss= models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	afp = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	renta = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	otrasDeducciones = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	sueldoLiquido = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

#---------------**********-----------------------*************----------------------

class CostoIndirecto(models.Model):
    idCif = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.DecimalField(max_digits=7, decimal_places=2)
    costoIF = models.TextField(null=True, blank=True)
    #="{% url 'costoIndirecto'   %}"    

class MateriaPrima(models.Model):
    idMp = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.DecimalField(max_digits=7, decimal_places=2)
    cantidadM = models.DecimalField(max_digits=7, decimal_places=2)
    valor = models.TextField(null=True, blank=True)
    

class ManoDeObraD(models.Model):    
    idMod = models.AutoField(primary_key=True)
    horasT = models.DecimalField(max_digits=7, decimal_places=2)
    costoMOD = models.TextField(null=True, blank=True)
     
class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombreP = models.CharField(max_length=50)

class DatoEntrada(models.Model):
    horas= models.DecimalField(decimal_places=2, max_digits=10)
    des= models.DecimalField(decimal_places=2, max_digits=10)
