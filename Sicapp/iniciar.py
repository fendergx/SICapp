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
    transaccion.terminoTransacion=compra.terminoVenta
    transaccion.save()

def agregarControlEfectivo(concepto,compra,periodo):
    if concepto=="Compra materia prima":
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
    else:
        control = ControlEfectivo()
        control.fecha = compra.fecha
        control.concepto = concepto
        control.tipoComprobante = "Factura"
        control.cuenta = Cuenta.objects.get(nombre="Caja general")
        control.saldoSalida = compra.total
        control.saldoEntrada = compra.total
        saldoAnterior = float(ControlEfectivo.objects.latest('idControl').saldoTotal)
        control.saldoTotal = saldoAnterior + control.saldoSalida
        control.periodo = periodo
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

def iniciarControl():
    periodo=PeriodoContable.objects.get(activo=True)
    ControlEfectivo.objects.create(fecha=date.today(),tipoComprobante="caja",concepto="inicio",saldoEntrada=0,saldoSalida=0,saldoTotal=10000,periodo=periodo)


def iniciarDetalleKardex():
    detalleKardex.objects.create(tipo="Materia Prima",nombre="Plastico PET",fecha=date.today())
    detalleKardex.objects.create(tipo="Materia Prima", nombre="Plastico PEHD", fecha=date.today())
    detalleKardex.objects.create(tipo="Materia Prima", nombre="Plastico PELD", fecha=date.today())
    detalleKardex.objects.create(tipo="Producto Terminado", nombre="Mesas para exterior", fecha=date.today())
    detalleKardex.objects.create(tipo="Producto Terminado", nombre="Bancas para exterior", fecha=date.today())
    detalleKardex.objects.create(tipo="Producto Terminado", nombre="Sillas de playa", fecha=date.today())
    detalleKardex.objects.create(tipo="Producto Terminado", nombre="Figuras", fecha=date.today())
    detalleKardex.objects.create(tipo="Producto Terminado", nombre="Losas plasticas", fecha=date.today())

def iniciarKardex():
    detalle1=detalleKardex.objects.get(nombre="Plastico PET")
    detalle2 = detalleKardex.objects.get(nombre="Plastico PEHD")
    detalle3 = detalleKardex.objects.get(nombre="Plastico PELD")
    detalle4 = detalleKardex.objects.get(nombre="Losas plasticas")
    detalle5 = detalleKardex.objects.get(nombre="Figuras")
    detalle6 = detalleKardex.objects.get(nombre="Sillas de playa")
    detalle7 = detalleKardex.objects.get(nombre="Bancas para exterior")
    detalle8 = detalleKardex.objects.get(nombre="Mesas para exterior")
    Kardex.objects.create(fecha=date.today(),cantEntrada = 0,precEntrada = 0,montoEntrada = 0,cantSalida = 0,precSalida = 0,
                          montoSalida = 0,cantExistencia = 160,precExistencia = 0.6,montoExistencia = 160 * 0.6,detalle=detalle1)

    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                          montoSalida=0, cantExistencia=160, precExistencia=0.6, montoExistencia=160 * 0.6,     detalle=detalle2)


    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                      montoSalida=0, cantExistencia=160, precExistencia=0.6, montoExistencia=160 * 0.6,  detalle=detalle3)
    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                          montoSalida=0, cantExistencia=6, precExistencia=3.5, montoExistencia=6 * 3.5,
                          detalle=detalle4)

    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                          montoSalida=0, cantExistencia=10, precExistencia=1, montoExistencia=10 * 1,
                          detalle=detalle5)
    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                          montoSalida=0, cantExistencia=2, precExistencia=18, montoExistencia=2 * 18,
                          detalle=detalle6)
    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                          montoSalida=0, cantExistencia=5, precExistencia=7, montoExistencia=5* 7,
                          detalle=detalle7)
    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                          montoSalida=0, cantExistencia=1, precExistencia=12, montoExistencia=1*12,
                          detalle=detalle8)


def agregarKardex(cantEntrada,precEntrada,cantSalida,precSalida,concepto):
    kardex=Kardex()
    detalle = detalleKardex.objects.get(nombre=concepto)

    print("detalle")
								 
							
							
							 
						   
						   
							
								 
								 
																		  
    print(detalle)
    print("Concepto")
    print(concepto)

    ultimo = Kardex.objects.filter(detalle=detalle).latest('idKardex')
    print("el ultimo")

    print(ultimo.idKardex)
    print(cantEntrada)
    if cantEntrada!=0:
        kardexGuardar=Kardex()
        kardexGuardar.fecha = date.today()
        kardexGuardar.cantEntrada = cantEntrada
        kardexGuardar.precEntrada = precEntrada
        kardexGuardar.montoEntrada = float(cantEntrada)*float(precEntrada)
        kardexGuardar.cantSalida =0
        kardexGuardar.precSalida = 0
        kardexGuardar.montoSalida = 0
        kardexGuardar.cantExistencia = float(ultimo.cantExistencia)+float(cantEntrada)
        kardexGuardar.montoExistencia = float(ultimo.montoExistencia)+float(kardexGuardar.montoEntrada)
        kardexGuardar.precExistencia =kardexGuardar.montoExistencia/kardexGuardar.cantExistencia
        kardexGuardar.detalle = detalle
        kardexGuardar.save()
    else:

        kardex.fecha = date.today()
        kardex.cantEntrada = 0
        kardex.precEntrada = 0
        kardex.montoEntrada = 0
        kardex.cantSalida = cantSalida
        kardex.precSalida = ultimo.precExistencia
        kardex.montoSalida = float(cantSalida)*float(ultimo.precExistencia)
        kardex.cantExistencia = float(ultimo.cantExistencia) - float(cantSalida)
        kardex.precExistencia = ultimo.precExistencia
        kardex.montoExistencia = float(kardex.cantExistencia)*float(ultimo.precExistencia)
        kardex.detalle = detalle
        print(kardex.idKardex)
        kardex.save()
		
def iniciarVenta():
    venta = Venta()
    venta.fecha = date.today()
    venta.iva = 0
    venta.total=0
    venta.terminoCompra="Venta Gravada"
    venta.tipoCompra="Contado"
    venta.periodoContable = 1
    venta.save()

    return venta.idVenta

def iniciarClientes():
    Cliente.objects.create(nrc="215",razonSocial="Mikkel SS",direccion="Urbanizacion Majuca, Cuscatanciongo, San Salvador")
    Cliente.objects.create(nrc="348", razonSocial="Jericho Barrons", direccion="Carretera a Agua Caliente, Kilometro 5 1/2, Soyapango, San Salvador")
    Cliente.objects.create(nrc="284", razonSocial="MacKayla Lane", direccion="Col La Rabida 4 Av. Nte No 1829, San Salvador")
    Cliente.objects.create(nrc="106", razonSocial="Danielle O'Maley", direccion="Km 24 1/2 carretera al puerto de La Libertad, Zaragoza")
    Cliente.objects.create(nrc="478", razonSocial="Ariana D", direccion="Km 17 Carretera a Quezaltepeque calle de Apopa a Nejapa San Salvador")