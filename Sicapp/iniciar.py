from datetime import  date

from Sicapp.models import *


def iniciarCompra():
    compra = Compra()
    compra.fecha = date.today()
    compra.iva = 0
    compra.total=0
    compra.terminoCompra="Compra Gravada"
    compra.tipoCompra="Credito"
    compra.periodoContable = 1
    compra.save()

    return compra.idCompra

def iniciarPeriodo(): #Inicializar un periodo contable en caso de que no haya uno activo
    periodoC=PeriodoContable()
    periodoC.fechaInicio= date.today()
    mes=date.today().month
    anio=date.today().year
    if mes==2:
        dia=28
    else:
        if mes==4 or mes==6 or mes==9 or mes==11:
            dia=30
        else: dia=31
    periodoC.fechaFin= date(anio,mes,dia)
    periodoC.anio=anio
    periodoC.mes=mes
    periodoC.save()

def iniciarLibroMayor(periodo):
    libroMayor=LibroMayor()
    libroMayor.fecha=date.today()
    libroMayor.debe=0
    libroMayor.haber=0
    libroMayor.saldo=0
    libroMayor.estado=True
    libroMayor.periodo=periodo

def iniciarProveedor():
    Proveedor.objects.create(nrc="215",razonSocial="Ressourcerie",direccion="Urbanizacion Majuca, Cuscatanciongo, San Salvador")
    Proveedor.objects.create(nrc="348", razonSocial="Invena", direccion="Carretera a Agua Caliente, Kilometro 5 1/2, Soyapango, San Salvador")
    Proveedor.objects.create(nrc="284", razonSocial="ServiPlastic", direccion="Col La Rabida 4 Av. Nte No 1829, San Salvador")
    Proveedor.objects.create(nrc="106", razonSocial="IberPlastic", direccion="Km 24 1/2 carretera al puerto de La Libertad, Zaragoza")
    Proveedor.objects.create(nrc="478", razonSocial="Rabo Group", direccion="Km 17 Carretera a Quezaltepeque calle de Apopa a Nejapa San Salvador")

def agregarTransaccionCV(concepto,total,compra,tipo,periodo):
    transaccion=TransaccionCV()
    transaccion.fecha=compra.fecha
    transaccion.concepto=concepto
    transaccion.comprobante="Factura"
    transaccion.cargo=total
    transaccion.abono=0
    transaccion.plazoCredito=compra.plazo
    transaccion.periodo=periodo
    transaccion.saldo=total
    transaccion.tipoTransaccion=tipo
    transaccion.terminoTransacion=compra.terminoCompra
    transaccion.save()

def agregarControlEfectivo(concepto,compra,periodo):
    control=ControlEfectivo()
    control.fecha=compra.fecha
    control.concepto=concepto
    control.tipoComprobante="Factura"
    control.cuenta=Cuenta.objects.get(nombre="Caja general")
    control.saldoSalida=compra.total
    control.saldoEntrada=0
    saldoAnterior=float(ControlEfectivo.objects.latest('idControl').saldoTotal)
    control.saldoTotal=saldoAnterior-control.saldoSalida
    control.periodo=periodo
    control.save()

def agregarDiario(cuenta,descripcion,cargo,abono):
    libroDiario=LibroDiario()
    libroDiario.fecha=date.today()
    libroDiario.libroM=LibroMayor.objects.get(estado=True)
    libroDiario.cuenta=cuenta
    libroDiario.descripcion=descripcion
    libroDiario.cargo=cargo
    libroDiario.abono=abono
    libroDiario.save()

def iniciarDetalleKardex():
    detalleKardex.objects.create(tipo="Materia Prima",nombre="Plastico PET",fecha=date.today())



def agregarKardex(cantEntrada,precEntrada,cantSalida,precSalida):
    kardex=Kardex()
    kardexAnterior = Kardex.objects.all()

    if len(kardexAnterior)==0:
        kardex.fecha=date.today()
        kardex.cantEntrada=0
        kardex.precEntrada=0
        kardex.montoEntrada=0
        kardex.cantSalida=0
        kardex.precSalida=0
        kardex.montoSalida=0
        kardex.cantExistencia=160
        kardex.precExistencia=0.6
        kardex.montoExistencia=kardex.cantExistencia*kardex.precExistencia
        detalle=detalleKardex.objects.filter(tipo="Materia Prima")
        if len(detalle)==0:
            iniciarDetalleKardex()
            detalle = detalleKardex.objects.get(tipo="Materia Prima")
        Kardex.detalle=detalle
        kardex.save()
    if cantEntrada!=0:
        kardex.fecha = date.today()
        kardexAnterior = Kardex.objects.latest('idKardex')
        kardex.cantEntrada = cantEntrada
        kardex.precEntrada = precEntrada
        kardex.montoEntrada = float(cantEntrada)*float(precEntrada)
        kardex.cantSalida =0
        kardex.precSalida = 0
        kardex.montoSalida = 0
        kardex.cantExistencia = float(kardexAnterior.cantExistencia)+float(cantEntrada)
        kardex.montoExistencia = float(kardexAnterior.montoExistencia)+float(kardex.montoEntrada)
        kardex.precExistencia =kardex.montoExistencia/kardex.cantExistencia
    else:
        kardex.fecha = date.today()
        kardex.cantEntrada = 0
        kardex.precEntrada = 0
        kardex.montoEntrada = 0
        kardex.cantSalida = cantSalida
        kardex.precSalida = precSalida
        kardex.montoSalida = float(cantSalida)*float(precSalida)
        kardex.cantExistencia = float(kardexAnterior.cantExistencia) - float(cantSalida)
        kardex.precExistencia = precSalida
        kardex.montoExistencia = float(kardex.cantExistencia)*float(precSalida)
    detalle = detalleKardex.objects.filter(tipo="Materia Prima")
    if len(detalle) == 0:
        iniciarDetalleKardex()
        detalle = detalleKardex.objects.get(tipo="Materia Prima")
    Kardex.detalle = detalle
    kardex.save()







