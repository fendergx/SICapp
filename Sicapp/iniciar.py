#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    libroMayor.save()

def iniciarProveedor():
    Proveedor.objects.create(nrc="215",razonSocial="Ressourcerie",direccion="Urbanizacion Majuca, Cuscatanciongo, San Salvador")
    Proveedor.objects.create(nrc="348", razonSocial="Invena", direccion="Carretera a Agua Caliente, Kilometro 5 1/2, Soyapango, San Salvador")
    Proveedor.objects.create(nrc="284", razonSocial="ServiPlastic", direccion="Col La Rabida 4 Av. Nte No 1829, San Salvador")
    Proveedor.objects.create(nrc="106", razonSocial="IberPlastic", direccion="Km 24 1/2 carretera al puerto de La Libertad, Zaragoza")
    Proveedor.objects.create(nrc="478", razonSocial="Rabo Group", direccion="Km 17 Carretera a Quezaltepeque calle de Apopa a Nejapa San Salvador")

def agregarTransaccionCV(concepto,total,compra,tipo,periodo):
    if tipo=="Venta":
        tipoTransaccion=compra.terminoVenta
    else: tipoTransaccion=compra.terminoCompra
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
    transaccion.terminoTransacion=tipoTransaccion
    transaccion.save()

def agregarControlEfectivo(concepto,compra,periodo):
    if concepto=="Compra materia prima":
        control=ControlEfectivo()
        control.fecha=compra.fecha
        control.concepto=concepto
        control.tipoComprobante="Factura"
        control.cuenta=Cuenta.objects.get(nombre="Caja General")
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
        control.cuenta = Cuenta.objects.get(nombre="Caja General")
        control.saldoSalida = compra.total
        control.saldoEntrada = compra.total
        saldoAnterior = float(ControlEfectivo.objects.latest('idControl').saldoTotal)
        control.saldoTotal = saldoAnterior + control.saldoSalida
        control.periodo = periodo
        control.save()

def agregarDiario(cuenta,descripcion,cargo,abono):
    mayor=LibroMayor.objects.get(estado=True)

    try:
        lb=LibroDiario.objects.filter(libroM=mayor).get(cuenta=cuenta)

    except:
        LibroDiario.DoesNotExist
        lb=None

    if lb==None:
        libroDiario = LibroDiario()
        libroDiario.fecha = date.today()
        libroDiario.libroM = LibroMayor.objects.get(estado=True)
        libroDiario.cuenta = cuenta
        libroDiario.descripcion = descripcion
        libroDiario.cargo = cargo
        libroDiario.abono = abono
        libroDiario.save()
    else:
        lb.abono = float(lb.abono) + abono
        lb.cargo = float(lb.cargo) + cargo
        lb.save()

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
                          montoSalida=0, cantExistencia=6, precExistencia=5.85, montoExistencia=6 * 5.85,
                          detalle=detalle4)

    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                          montoSalida=0, cantExistencia=10, precExistencia=4.53, montoExistencia=10 *4.53,
                          detalle=detalle5)
    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                          montoSalida=0, cantExistencia=2, precExistencia=18, montoExistencia=2 * 18,
                          detalle=detalle6)
    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                          montoSalida=0, cantExistencia=5, precExistencia=8.94, montoExistencia=5* 8.94,
                          detalle=detalle7)
    Kardex.objects.create(fecha=date.today(), cantEntrada=0, precEntrada=0, montoEntrada=0, cantSalida=0, precSalida=0,
                          montoSalida=0, cantExistencia=6, precExistencia=12, montoExistencia=6*12,
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

def startEmpleado():
    empleado.objects.create(nombreCompleto="Acevedo Manriquez Maria",cargo="Gerente General",sueldoBase=812.60,ingresoExtra=0.0,vacaciones=43.41,totalDevengado=856.01,isss=25.68,afp=53.50,renta=56.07,otrasDeducciones=0.0,sueldoLiquido=720.76,tipo="Administracion")
    empleado.objects.create(nombreCompleto="Acevedo Mejia Enrique",cargo="Jefe Administrativo",sueldoBase=507.88,ingresoExtra=0.0,vacaciones=43.41,totalDevengado=535.01,isss=16.05,afp=33.44,renta=23.97,otrasDeducciones=0.0,sueldoLiquido=461.55,tipo="Administracion")
    empleado.objects.create(nombreCompleto="Acevedo Ruiz Carolina",cargo="Jefe de Produccion",sueldoBase=507.88,ingresoExtra=0.0,vacaciones=43.41,totalDevengado=535.01,isss=16.05,afp=33.44,renta=23.97,otrasDeducciones=0.0,sueldoLiquido=461.55,tipo="Administracion")
    empleado.objects.create(nombreCompleto="Acosta Gamez Celina",cargo="Jefe de Marketing",sueldoBase=507.88,ingresoExtra=0.0,vacaciones=43.41,totalDevengado=535.01,isss=16.05,afp=33.44,renta=23.97,otrasDeducciones=0.0,sueldoLiquido=461.55,tipo="Administracion")
    empleado.objects.create(nombreCompleto="Aguilar Dorantes Irma",cargo="Jefe de Bodega",sueldoBase=507.88,ingresoExtra=0.0,vacaciones=43.41,totalDevengado=535.01,isss=16.05,afp=33.44,renta=23.97,otrasDeducciones=0.0,sueldoLiquido=461.55,tipo="Administracion")
    empleado.objects.create(nombreCompleto="Alarcon Licona Salomon",cargo="Encargado de Contabilidad",sueldoBase=310.3,ingresoExtra=0.0,vacaciones=16.58,totalDevengado=326.88,isss=9.81,afp=20.43,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=296.64,tipo="Administracion")
    empleado.objects.create(nombreCompleto="Alatriste Perez Hipolito",cargo="Encargado de control de calidad",sueldoBase=310.3,ingresoExtra=0.0,vacaciones=16.58,totalDevengado=326.88,isss=9.81,afp=20.43,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=296.64,tipo="Administracion")
    empleado.objects.create(nombreCompleto="Aldrete Vargas Adolfo",cargo="Recepcionista",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Administracion")
    empleado.objects.create(nombreCompleto="Alderete Porras Jacinta",cargo="Secretaria",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Administracion")
    empleado.objects.create(nombreCompleto="Aleman Mundo Maria",cargo="Secretaria",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Administracion")
    empleado.objects.create(nombreCompleto="Almman Mundo Marcial",cargo="Motorista de carga",sueldoBase=310.3,ingresoExtra=0.0,vacaciones=16.58,totalDevengado=326.88,isss=9.81,afp=20.43,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=296.64,tipo="Mano de Obra I.")
    empleado.objects.create(nombreCompleto="Alonso Ibarra Pascual",cargo="Motorista de carga",sueldoBase=310.3,ingresoExtra=0.0,vacaciones=16.58,totalDevengado=326.88,isss=9.81,afp=20.43,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=296.64,tipo="Mano de Obra I.")
    empleado.objects.create(nombreCompleto="Alvarado Mendoza Oscar",cargo="Vigilante",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Mano de Obra I.")
    empleado.objects.create(nombreCompleto="Alvarez Martinez Veronica",cargo="Vigilante",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Mano de Obra I.")
    empleado.objects.create(nombreCompleto="Alvarez Medellin Felipe",cargo="Vigilante",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Mano de Obra I.")
    empleado.objects.create(nombreCompleto="Alvarez Villanueva Salvador ",cargo="Vigilante",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Mano de Obra I.")
    empleado.objects.create(nombreCompleto="Amaya Salvador Arturo",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Produccion")
    empleado.objects.create(nombreCompleto="Andrade Bujanda Rafael",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Produccion")
    empleado.objects.create(nombreCompleto="Angulo Garfias Raúl",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Produccion")
    empleado.objects.create(nombreCompleto="Ayala Quijano Mario Andrés",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción")
    empleado.objects.create(nombreCompleto="Bacab Pech Guillermo",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción")
    empleado.objects.create(nombreCompleto="Balderas Flores Luis",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción")
    empleado.objects.create(nombreCompleto="Bastidas Iribe Audel",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción")
    empleado.objects.create(nombreCompleto="Bautista Mejía Alejandro",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción")
    empleado.objects.create(nombreCompleto="Betanzos Torres Noel",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción")
    empleado.objects.create(nombreCompleto="Caballero Green Francisco",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción")
    empleado.objects.create(nombreCompleto="Gomez Evora Francisco",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción")
    empleado.objects.create(nombreCompleto="Hernández Monterrey Grace",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción")
    empleado.objects.create(nombreCompleto="Iraheta Herrera Carlos",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción")
    empleado.objects.create(nombreCompleto="Lenidas Ponce Carlos",cargo="Operario",sueldoBase=224.57,ingresoExtra=0.0,vacaciones=12,totalDevengado=236.57,isss=7.10,afp=14.79,renta=0.0,otrasDeducciones=0.0,sueldoLiquido=214.69,tipo="Producción") 
def iniciarClientes():
    Cliente.objects.create(nrc="215",razonSocial="Mikkel SS",direccion="Urbanizacion Majuca, Cuscatanciongo, San Salvador")
    Cliente.objects.create(nrc="348", razonSocial="Jericho Barrons", direccion="Carretera a Agua Caliente, Kilometro 5 1/2, Soyapango, San Salvador")
    Cliente.objects.create(nrc="284", razonSocial="MacKayla Lane", direccion="Col La Rabida 4 Av. Nte No 1829, San Salvador")
    Cliente.objects.create(nrc="106", razonSocial="Danielle O'Maley", direccion="Km 24 1/2 carretera al puerto de La Libertad, Zaragoza")
    Cliente.objects.create(nrc="478", razonSocial="Ariana D", direccion="Km 17 Carretera a Quezaltepeque calle de Apopa a Nejapa San Salvador")

def iniciarCatalogo():
    Cuenta.objects.create(codCuenta="AC001", codigoN="11", nombre="Activo Corriente", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC002", codigoN="111", nombre="Caja", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC003", codigoN="1111", nombre="Caja General", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC004", codigoN="1112", nombre="Caja Chica", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC005", codigoN="112", nombre="Bancos", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC006", codigoN="1121", nombre="Cuenta Corriente", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC007", codigoN="1122", nombre="Cuenta de Ahorros", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC008", codigoN="113", nombre="Cuentas por Cobrar", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC009", codigoN="1131", nombre="Clientes", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC010", codigoN="1132", nombre="Prestamos y Anticipios a Empleados", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC011", codigoN="1133", nombre="Deudores Varios", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC012", codigoN="114", nombre="Inventarios", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC013", codigoN="1141", nombre="Productos Terminados", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC014", codigoN="11411", nombre="Muebles para Exterior", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC015", codigoN="11412", nombre="Mesas para exterior", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC016", codigoN="11413", nombre="Sillas de playa", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC017", codigoN="11414", nombre="Losas plasticas", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC018", codigoN="11415", nombre="Figuras", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC019", codigoN="1142", nombre="Productos en Proceso", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC020", codigoN="1143", nombre="Materia Prima", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC021", codigoN="11431", nombre="Plastico PEHD", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC022", codigoN="11432", nombre="Plastico PET", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC023", codigoN="11433", nombre="Plastico PELD", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC024", codigoN="1144", nombre="Materiales Indirectos", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC025", codigoN="11441", nombre="Cajas de Carton Corrugado", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC026", codigoN="11442", nombre="Cajas Plegadizas", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC027", codigoN="11443", nombre="Empaque Primario", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC028", codigoN="11444", nombre="Cinta Adhesiva", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC029", codigoN="115", nombre="Gastos Pagados por Anticipado", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC030", codigoN="1151", nombre="Servicios Pagados por Anticiapdo", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC031", codigoN="11511", nombre="Servicios de Publicidad", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC032", codigoN="11512", nombre="Servicios de Construccion de Obra Civil", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC033", codigoN="11513", nombre="Servicios de Seguridad", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC034", codigoN="11514", nombre="Alquileres Pagados por Anticipado", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC035", codigoN="11515", nombre="Seguros Pagados por Anticipado", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC036", codigoN="1152", nombre="Otros Gastos Pagados por Anticipado", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC037", codigoN="116", nombre="Pago a Cuenta (ISR)", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC038", codigoN="117", nombre="Credito Fiscal (IVA)", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC039", codigoN="12", nombre="Activo No Corriente", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC040", codigoN="121", nombre="Propiedad, Planta y Equipo", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC041", codigoN="1211", nombre="Bienes No Despreciables", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC042", codigoN="12111", nombre="Terrenos", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC043", codigoN="1212", nombre="Bienes Despreciables", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC044", codigoN="12121", nombre="Edificios", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC045", codigoN="12122", nombre="Mobiliario y Equipo de Oficina", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC046", codigoN="121221", nombre="Mobiliario de Oficina", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC047", codigoN="1212211", nombre="Escritorios", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC048", codigoN="1212112", nombre="Archiveros", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC049", codigoN="1212113", nombre="Sillas de Oficina", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC050", codigoN="1212114", nombre="Sillas de Espera", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC051", codigoN="1212115", nombre="Mesas", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC052", codigoN="1212116", nombre="Muebles para Computadoras", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC053", codigoN="121222", nombre="Equipo de Oficina", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC054", codigoN="212221", nombre="Computadoras", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC055", codigoN="1212222", nombre="Impresores  ", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC056", codigoN="1212223", nombre="Telefonos", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC057", codigoN="1212224", nombre="Fotocopiadoras", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC058", codigoN="12123", nombre="Mobiliario, Equipo y Herramientas Industriales", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC059", codigoN="121231", nombre="Maquinaria Industrial", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC060", codigoN="1212311", nombre="Maquina Mezcladora", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC061", codigoN="1212312", nombre="Extrusora", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC062", codigoN="1212313", nombre="Maquinas HEATmx ", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC063", codigoN="1212314", nombre="Prensa de Reposo", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC064", codigoN="1212315", nombre="Sierra Circular", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC065", codigoN="1212316", nombre="Molino Triturador", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC066", codigoN="121232", nombre="Equipo Industrial", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC067", codigoN="1212321", nombre="Equipo de Higiene y Seguridad Industrial", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC068", codigoN="1212322", nombre="Equipo de Mantenimiento de las Instalaciones", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC069", codigoN="1212323", nombre="Equipo de Proteccion Personal", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC070", codigoN="1212324", nombre="Estantes", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC071", codigoN="1212325", nombre="Pallets", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC072", codigoN="1212326", nombre="Contenedores", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC073", codigoN="1212327", nombre="Otros", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC074", codigoN="1213", nombre="Depreciacion Acumulada", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC075", codigoN="12131", nombre="Edificios", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC076", codigoN="12132", nombre="Mobiliario de Oficina", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC077", codigoN="121321", nombre="Escritorios", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC078", codigoN="121322", nombre="Archiveros", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC079", codigoN="121323", nombre="Sillas de Oficina", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC080", codigoN="121324", nombre="Sillas de Espera", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC081", codigoN="121325", nombre="Mesas", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC082", codigoN="121326", nombre="Muebles para Computadoras", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC083", codigoN="12133 ", nombre="Equipo de Oficina", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC084", codigoN="121331", nombre="Computadoras", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC085", codigoN="121332", nombre="Impresores", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC086", codigoN="121333", nombre="Telefonos", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC087", codigoN="121334", nombre="Fotocopiadoras", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC088", codigoN="12134", nombre="Maquinaria Industrial ", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC089", codigoN="121341", nombre="Maquina Mezcladora", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC090", codigoN="121342", nombre="Extrusora", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC091", codigoN="121343", nombre="Maquinas HEATmx", tipoCuenta="Activo" )
    Cuenta.objects.create(codCuenta="AC092", codigoN="121344", nombre="Prensa de Reposo", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC093", codigoN="121345", nombre="Sierra Circular", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC094", codigoN="121346", nombre="Molino Triturador", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC095", codigoN="12135", nombre="Equipo industrial", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC096", codigoN="121351", nombre="Equipo de Higiene y Seguridad Industrial", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC097", codigoN="121352", nombre="Equipo de Mantenimiento de las Instalaciones", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC098", codigoN="121353", nombre="Equipo de Proteccion Personal", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC099", codigoN="121354", nombre="Estantes", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC100", codigoN="121355", nombre="Pallets", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC101", codigoN="121356", nombre="Contenedores", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC102", codigoN="121357", nombre="Otros", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC103", codigoN="1214", nombre="Activos intangibles", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC104", codigoN="12141", nombre="Software", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC105", codigoN="12142", nombre="Licencias de software ", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="AC106", codigoN="12143", nombre="Amortizacion  ", tipoCuenta="Activo")
    Cuenta.objects.create(codCuenta="PA001", codigoN="21", nombre="Pasivo Corriente", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA002", codigoN="211", nombre="Prestamos Bancarios", tipoCuenta="Pasivo" )
    Cuenta.objects.create(codCuenta="PA003", codigoN="212", nombre="Cuentas por Pagar", tipoCuenta="Pasivo" )
    Cuenta.objects.create(codCuenta="PA004", codigoN="2121", nombre="Intereses por Pagar", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA005", codigoN="2122", nombre="Impuestos por Pagar", tipoCuenta="Pasivo" )
    Cuenta.objects.create(codCuenta="PA006", codigoN="21221", nombre="Impuestos Municipales", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA007", codigoN="21222", nombre="Matriculas de Comercio", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA008", codigoN="21223", nombre="Seguro Social (ISSS)", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA009", codigoN="22124", nombre="Administradora de Fondos de Pensiones (AFP)", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA010", codigoN="22125", nombre="IVA por Pagar ", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA011", codigoN="22126", nombre="Impuesto Sobre la Renta por Pagar", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA012", codigoN="22127", nombre="Otros Impuestos y Contribuciones  ", tipoCuenta=" Pasivo")
    Cuenta.objects.create(codCuenta="PA013", codigoN="213", nombre="Cuentas por Pagar a Proveedores", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA014", codigoN="214", nombre="Sueldos por Pagar", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA015", codigoN="215", nombre="Impuesto Sobre la Renta (ISR)", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA016", codigoN="216", nombre="Debito Fiscal (IVA)", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA017", codigoN="217", nombre="Impuestos y Contribuciones Retenidas", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA018", codigoN="2171", nombre="Impuesto Sobre la Renta Empleados", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA019", codigoN="2172", nombre="Retenciones a Personas Naturales por Servicios 10%", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA020", codigoN="2173", nombre="Seguro Social (ISSS)", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA021", codigoN="2174", nombre="Administradora de Fondos de Pensiones (AFP)", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA022", codigoN="2175", nombre="Impuesto de Vialidad", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA023", codigoN="2176", nombre="INSAFORP", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA024", codigoN="2177", nombre="Otras Retenciones al Personal", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA025", codigoN="2178", nombre="IVA Retenido a Terceros", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA026", codigoN="2179", nombre="Otros Impuestos y Contribuciones Retenidos", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA027", codigoN="22", nombre="Pasivo No Corriente", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA028", codigoN="221", nombre="Documentos por Pagar", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA029", codigoN="2211", nombre="Bancos ", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA030", codigoN="2212", nombre="Otras Instituciones Financieras", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="PA031", codigoN="2213", nombre="Otros", tipoCuenta="Pasivo")
    Cuenta.objects.create(codCuenta="K001", codigoN="31", nombre="Capital Social", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="K002", codigoN="311", nombre="Aportaciones", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="K003", codigoN="312", nombre="Reserva Legal", tipoCuenta="Patrimonio   ")
    Cuenta.objects.create(codCuenta="K004", codigoN="313", nombre="Superavit por Revaluaciones", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="K005", codigoN="32", nombre="Resultados por Aplicar", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="K006", codigoN="321", nombre="Utilidad Acumulada", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="K007", codigoN="3211", nombre="Utilidades Distribuibles", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="K008", codigoN="3212", nombre="Utilidades no Distribuibles", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="K009", codigoN="3213", nombre="Perdida Acumulada", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="K010", codigoN="322", nombre="Utilidades del Ejercicio", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="K011", codigoN="3221", nombre="Utilidad del Ejercicio", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="K012", codigoN="3222", nombre="Perdida del Ejercicio", tipoCuenta="Patrimonio")
    Cuenta.objects.create(codCuenta="CRD001", codigoN="41", nombre="Gastos y Costos", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD002", codigoN="411", nombre="Gastos de Administracion", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD003", codigoN="4111", nombre="Sueldos", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD004", codigoN="4112", nombre="Servicios Profesionales y Tecnicos", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD005", codigoN="4113", nombre="Vigilancia", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD006", codigoN="4114", nombre="Energia Electrica y Agua", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD007", codigoN="4115", nombre="Depreciaciones", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD008", codigoN="4116", nombre="Impuestos y Municipalidades", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD009", codigoN="4117", nombre="Otros", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD010", codigoN="412", nombre="Gastos Financieros", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD011", codigoN="4121", nombre="Intereses", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD012", codigoN="4122", nombre="Otros", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD013", codigoN="413", nombre="Costos de Produccion", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD014", codigoN="4131", nombre="Materiales Directos", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD015", codigoN="4132", nombre="Mano de Obra Directa", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD016", codigoN="4133", nombre="Gastos de Fabricacion", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD017", codigoN="4134", nombre="Limpieza y Aseo de Maquinaria", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD018", codigoN="4135", nombre="Reparacion de Maquinaria", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRD019", codigoN="42", nombre="Costo de lo Vendido", tipoCuenta="Cuentas de Resultado Deudor")
    Cuenta.objects.create(codCuenta="CRA001", codigoN="51", nombre="Ingresos y Costos", tipoCuenta="Cuentas de Resultado Acreedor")
    Cuenta.objects.create(codCuenta="CRA002", codigoN="511", nombre="Ingreso por Ventas", tipoCuenta="Cuentas de Resultado Acreedor")
    Cuenta.objects.create(codCuenta="CRA003", codigoN="512", nombre="Ingreso por Servicios", tipoCuenta="Cuentas de Resultado Acreedor")   
    Cuenta.objects.create(codCuenta="CL01", codigoN="61", nombre="Cuenta Liquidadora", tipoCuenta="Cuenta de Cierre")
    Cuenta.objects.create(codCuenta="CL02", codigoN="611", nombre="Perdidas y Ganancias", tipoCuenta="Cuenta de Cierre")

def costosUnitarios(cantidad,producto,abono):
    detallePeld = detalleKardex.objects.get(nombre="Plastico PELD")
    detallePehd = detalleKardex.objects.get(nombre="Plastico PEHD")
    detallePet = detalleKardex.objects.get(nombre="Plastico PET")

    ultimoPet=Kardex.objects.filter(detalle=detallePet).latest('idKardex')
    ultimoPehd = Kardex.objects.filter(detalle=detallePehd).latest('idKardex')
    ultimoPeld = Kardex.objects.filter(detalle=detallePeld).latest('idKardex')

    mpdMesa=29963.1*float(ultimoPehd.precExistencia)
    mpdBancas=25129.6*float(ultimoPehd.precExistencia)
    mpdSillas=4667.2*float(ultimoPehd.precExistencia)
    mpdFiguras=7889.6*float(ultimoPehd.precExistencia)
    mpdLosas=5603.10*float(ultimoPet.precExistencia)

    costopMesa = mpdMesa+13394.152
    costopBanca = mpdBancas + 14831.24
    costopSillas = mpdSillas + 12438.73
    costopFiguras = mpdFiguras + 2310.19
    costopLosas = mpdLosas + 3905.22

    totalMesas=costopMesa+157789.55+16156.61+28784.15
    totalLosas = costopLosas + 20963.63+3021.29+5382.64
    totalBancas=costopBanca+149387.63+13550.3+24140.83
    totalSillas=costopSillas+49231.54+2516.63+4483.56
    totalFiguras=costopFiguras+17659.96+4254.2+7549.17

    cuMesas=totalMesas/29963.10
    cuLosas=totalLosas/5603.10
    cuBancas=totalBancas/25129.6
    cuSillas=totalSillas/4667.2
    cuFiguras=totalFiguras/7889.6

    if producto == "Mesas para exterior":
        agregarKardex(cantidad, cuMesas, 0, 0, producto)
        total=cantidad*cuMesas
    else:
        if producto == "Bancas para exterior":
            agregarKardex(cantidad, cuBancas, 0, 0, producto)
            total=cantidad*cuBancas
        else:
            if producto == "Sillas de playa":
                agregarKardex(cantidad, cuSillas, 0, 0, producto)
                total=float(cantidad)*cuSillas
            else:
                if producto == "Losas plasticas":
                    agregarKardex(cantidad, cuLosas, 0, 0, producto)
                    total=cantidad*cuLosas
                else:
                    agregarKardex(cantidad, cuFiguras, 0, 0, producto)
                    total=cantidad*cuFiguras


    cuentaP=Cuenta.objects.get(nombre="Productos en Proceso")  
    cuenta1=Cuenta.objects.get(nombre=producto)                     
    agregarDiario(cuentaP,"Orden",abono,0)
    agregarDiario(cuentaP,"Orden",0,total)
    agregarDiario(cuenta1,"Orden",total,0)

    print("mesas: ")
    print(cuMesas)
    print("Losas: ")
    print(cuLosas)
    print("Bancas: ")
    print(cuBancas)
    print("Sillas: ")
    print(cuSillas)
    print("Figuras: ")
    print(cuFiguras)
