from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response


# Create your views here.
from Sicapp.iniciar import *
from Sicapp.models import *
from django.template import RequestContext
from django.db.models import Max
from .forms import EntradaForm
from decimal import Decimal


#def probando(request):return render(request, "index.html")

def probando(request):
    periodo=PeriodoContable.objects.all()
    if len(periodo)==0:
        iniciarPeriodo()
    proveedor=Proveedor.objects.all()
    if len(proveedor)==0:
        iniciarProveedor()
    clientes=Cliente.objects.all()
    if len(clientes)==0:
        iniciarClientes()
    detalle=detalleKardex.objects.all()
    if len(detalle)==0:
        iniciarDetalleKardex()
    kardex=Kardex.objects.all()
    if len(kardex)==0:
        iniciarKardex()
    controlEfectivo=ControlEfectivo.objects.all()
    if len(controlEfectivo)==0:
        iniciarControl()
    cuentas=Cuenta.objects.all()
    if len(cuentas)==0:
        iniciarCatalogo()
    libro=LibroMayor.objects.all()
    if len(libro)==0:
        iniciarLibroMayor
    return render(request,"paginas/index.html",{'anios_esta':PeriodoContable.objects.raw('select * from Sicapp_PeriodoContable group by anio order by anio desc  ')})

def estadosFinancieros(request, id_estados):
    anios=PeriodoContable.objects.filter(anio=id_estados)
    anios_estados=PeriodoContable.objects.raw('select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    librosDiarios = LibroDiario.objects.all().order_by('cuenta')
    listadoa = []
    listadob = []
    listadoc = []
    lisaux = []
    caracu = 0.0
    aboacu = 0.0
    activoa = 0.0
    pasivoa = 0.0
    capitaa = 0.0
    ingrven = 0.0
    costven = 0.0
    gastoop = 0.0
    financi = 0.0
    aportac = 0.0
    totalactivo = 0.00
    totalpasivo = 0.00
####### Metodo de ordenamiento de cuentas
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 11:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 12:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 13:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 19:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 21:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 22:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 23:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 24:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 31:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 32:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 33:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 41:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 42:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 51:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 52:
            lisaux.append(libros)


    for libros in lisaux:
        carg = float(libros.cargo)
        abon = float(libros.abono)
        cab = carg - abon
        if cab < 0:
            abon = float(-cab)
            carg = 0
        else:
            carg = cab
            abon = 0
        caracu = float(caracu + carg)
        aboacu = float(aboacu + abon)
        a = [libros.cuenta.codigoN,libros.cuenta.nombre,carg,abon,libros.cuenta.tipoCuenta]
        if a[4]=='Activo':
            listadoa.append(a)
            activoa = activoa + a[3]
            totalactivo = totalactivo + carg
        else:
            if a[4]=='Pasivo':
                listadob.append(a)
                pasivoa = pasivoa + a[3]
                totalpasivo = totalpasivo + abon
            else:
                listadoc.append(a)
                capitaa = capitaa + a[3]
        


    for libros in librosDiarios:
        if libros.cuenta.tipoCuenta == "Cuentas de Resultado Acreedor" or libros.cuenta.tipoCuenta == "Cuentas de Resultado Acre":
            carg = float(libros.cargo)
            abon = float(libros.abono)
            cab = carg - abon
            print (cab)
            if cab < 0.0:
                cab = -cab
            else:
                carg = cab
                abon = 0
            print ("paso por aqui")
            print (libros.cuenta.nombre)
            
            ingrven = ingrven + cab
    
    for libros in librosDiarios:
        if libros.cuenta.codigoN == "42":
            carg = float(libros.cargo)
            abon = float(libros.abono)
            cab = carg - abon
            if cab < 0:
                cab = -cab
            costven = costven + cab
    for libros in librosDiarios:
        if libros.cuenta.tipoCuenta == "Cuentas de Resultado Deud" or libros.cuenta.tipoCuenta == "Cuentas de Resultado Deudor":
            carg = float(libros.cargo)
            abon = float(libros.abono)
            cab = carg - abon
            if cab < 0:
                cab = -cab
            else:
                carg = cab
                abon = 0
            gastoop = gastoop + cab

    bruta = ingrven - costven
    gastoop = gastoop - costven
    neta = bruta - gastoop
    if neta <= 250000:
        ren = neta*0.25
    else:
        ren = neta*0.30
    newne = neta - ren
    reuti = newne*0.70
    reten = newne*0.30
    

    for libros in librosDiarios:
        if libros.cuenta.codigoN == "311":
            carg = float(libros.cargo)
            abon = float(libros.abono)
            cab = carg - abon
            if cab < 0:
                cab = -cab
            aportac = aportac + cab
    
    capso = aportac + reuti
    patri = capso + reten
    toral = totalpasivo + patri
    context ={
        'anios':anios,
        'anios_esta':anios_estados,
        'anio_select':id_estados,
        'librodia': listadoa,
        'librodib': listadob,
        'librodic': listadoc,
        'totaca': caracu,
        'totaab': aboacu,
        'ingreo': ingrven,
        'costov': costven,
        'bruta': bruta,
        'gastoop': gastoop,
        'neta': neta,
        'capso': capso,
        'aportac': aportac,
        'reuti': reuti,
        'totalactivo': totalactivo,
        'totalpasivo': totalpasivo,
        'reten': reten,
        'patri':patri,
        'toral': toral,

    }
    return render(request,"paginas/estados_financieros.html",context)

def compras(request):
    anios_estados = PeriodoContable.objects.raw(
        'select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    c=iniciarCompra()
    proveedores = Proveedor.objects.all()

    if len(proveedores)==0:
        iniciarProveedor()
        proveedores = Proveedor.objects.all()

    try:
        periodoC = PeriodoContable.objects.get(activo=True)
    except PeriodoContable.DoesNotExist:
        periodoC = None

    if periodoC==None:
        iniciarPeriodo()
        periodoC = PeriodoContable.objects.get(activo=True)

    if request.POST:
        compraActualizar=Compra.objects.get(idCompra=c)
        compraActualizar.terminoCompra=request.POST.get("termino")
        compraActualizar.tipoCompra=request.POST.get("tipoCompra")
        if compraActualizar.tipoCompra=="Credito":
            compraActualizar.proveedor=request.POST.get("proveedor")
            compraActualizar.plazo=request.POST.get("plazo")

        contador=0
        total = 0
        cantidadProd=0
        for i in range(1,12):

            cantidad = request.POST.get("cantidad"+str(i))

            idCompra=Compra.objects.get(idCompra=c)

            if cantidad!="0" and cantidad!= None:
                concepto=request.POST.get("concepto"+str(i))
                precio=request.POST.get("precio"+str(i))
                subTotal = (float(precio)*int(float(cantidad)))
                cantidadProd=cantidadProd+int(float(cantidad))
                total=total+subTotal
                detalle=Detallecompra(cantidad=cantidad,concepto=concepto,precio=precio,total=subTotal,compra=idCompra)
                detalle.save()
                cuenta=Cuenta.objects.get(nombre=concepto)
                agregarDiario(cuenta,"compra",subTotal,0)
                agregarKardex(cantidad,precio,0,0,concepto)
                contador=contador+1



        if compraActualizar.terminoCompra=="Compra Gravada":
            compraActualizar.iva=total*0.13
            cuenta = Cuenta.objects.get(nombre="Credito Fiscal (IVA)")
            agregarDiario(cuenta, "compra", compraActualizar.iva, 0)
            compraActualizar.total=total+compraActualizar.iva
        else:
            compraActualizar.total=total

        print("total")
        print(compraActualizar.total)

        if compraActualizar.total!=0:
            compraActualizar.estado=True
        compraActualizar.periodoContable=periodoC
        if compraActualizar.tipoCompra=="Credito":
            agregarTransaccionCV("Compra materia prima", total, compraActualizar, "compra", periodoC)
            cuenta = Cuenta.objects.get(nombre="Cuentas por Pagar a Proveedores")
            agregarDiario(cuenta, "compra", 0, compraActualizar.total)
        else:
            agregarControlEfectivo("Compra materia prima", compraActualizar,periodoC)
            cuenta = Cuenta.objects.get(nombre="Caja General")
            agregarDiario(cuenta, "compra", 0, compraActualizar.total)
        print(compraActualizar.total)
        compraActualizar.save()
        Compra.objects.filter(estado=False).delete()





    context = {
        'anios_esta': anios_estados,
        'idCompra':c,
        'proveedores': proveedores
    }
    return render(request, "paginas/compra.html", context)

def ventas(request):
    anios_estados = PeriodoContable.objects.raw('select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    c=iniciarVenta()
    clientes = Cliente.objects.all()
    det=detalleKardex.objects.get(nombre="Losas plasticas")
    precioL=Kardex.objects.filter(detalle=det).latest('idKardex')
    det = detalleKardex.objects.get(nombre="Figuras")
    precioF = Kardex.objects.filter(detalle=det).latest('idKardex')
    det = detalleKardex.objects.get(nombre="Sillas de playa")
    precioS = Kardex.objects.filter(detalle=det).latest('idKardex')
    det = detalleKardex.objects.get(nombre="Bancas para exterior")
    precioB = Kardex.objects.filter(detalle=det).latest('idKardex')
    det = detalleKardex.objects.get(nombre="Mesas para exterior")
    precioM = Kardex.objects.filter(detalle=det).latest('idKardex')


    if len(clientes) == 0:
        iniciarClientes()
        clientes = Cliente.objects.all()

    try:
        periodoC = PeriodoContable.objects.get(activo=True)
    except PeriodoContable.DoesNotExist:
        periodoC = None

    if periodoC == None:
        iniciarPeriodo()
        periodoC = PeriodoContable.objects.get(activo=True)

    if periodoC != None and request.POST:
        ventaActualizar = Venta.objects.get(idVenta=c)
        ventaActualizar.terminoVenta = request.POST.get("termino")
        ventaActualizar.tipoVenta = request.POST.get("tipoVenta")
        if ventaActualizar.tipoVenta == "Credito":
            ventaActualizar.cliente = request.POST.get("idCliente")
            ventaActualizar.plazo = request.POST.get("plazo")

        contador = 0
        total = 0
        cantidadProd = 0
        for i in range(1, 12):

            cantidad = request.POST.get("cantidad" + str(i))

            idVenta = Venta.objects.get(idVenta=c)

            if cantidad != "0" and cantidad != None:
                concepto = request.POST.get("concepto" + str(i))
                precio = request.POST.get("precio" + str(i))
                det = detalleKardex.objects.get(nombre=concepto)
                prec = Kardex.objects.filter(detalle=det).latest('idKardex')
                subTotalI = int(float(prec.precExistencia)) * int(float(cantidad))
                if concepto=="Losas" or concepto=="Figuras":
                    subTotal = subTotalI *1.35
                else: subTotal=subTotalI*1.5
                cantidadProd = cantidadProd + int(float(cantidad))
                total = total + subTotal
                detalle = DetalleVenta(cantidad=cantidad, producto=concepto, precio=prec.precExistencia, total=subTotal,
                                        venta=idVenta)
                detalle.save()
                cuenta = Cuenta.objects.get(nombre=concepto)
                cuenta1 = Cuenta.objects.get(nombre="Costo de lo Vendido")
                agregarDiario(cuenta, "Venta", 0, subTotalI)
                agregarDiario(cuenta1,"Venta",subTotalI,0)
                agregarKardex( 0, 0,cantidad, prec.precExistencia, concepto)
                contador = contador + 1
        cuenta1 = Cuenta.objects.get(nombre="Ingreso por Ventas")
        agregarDiario(cuenta1, "Venta", 0, total)
        if ventaActualizar.terminoVenta == "Venta Gravada":
            ventaActualizar.iva = total * 0.13
            cuenta = Cuenta.objects.get(nombre="Debito Fiscal (IVA)")
            agregarDiario(cuenta, "Venta", 0, ventaActualizar.iva)
            ventaActualizar.total = total + ventaActualizar.iva
        else: ventaActualizar.total=total

        if ventaActualizar.total != 0:
            ventaActualizar.estado = True
            ventaActualizar.periodoContable = periodoC
        if ventaActualizar.tipoVenta == "Credito":
            agregarTransaccionCV("Venta de producto", total, ventaActualizar, "Venta", periodoC)
            cuenta = Cuenta.objects.get(nombre="Clientes")
            agregarDiario(cuenta, "Venta",  ventaActualizar.total,0)
        else:
            agregarControlEfectivo("Venta Productos", ventaActualizar, periodoC)
            cuenta = Cuenta.objects.get(nombre="Caja General")
            agregarDiario(cuenta, "compra",  ventaActualizar.total,0)

        ventaActualizar.save()
        Venta.objects.filter(estado=False).delete()


    context={
        'anios_esta':anios_estados,
        'idVenta':c,
        'clientes':clientes,
        'precioL':precioL,
        'precioS': precioS,
        'precioM': precioM,
        'precioF': precioF,
        'precioB': precioB,
    }
    return render(request,"paginas/venta.html",context)

def periodoContable(request):
    anios_estados = PeriodoContable.objects.raw(
        'select * from Sicapp_PeriodoContable group by anio order by anio desc  ')


    try:
        periodo = PeriodoContable.objects.get(activo=True)
        periodoActualizar = PeriodoContable.objects.get(activo='True')

        if request.GET:
            periodoActualizar.idPeriodo
            periodoActualizar.activo = False
            periodoActualizar.save()
            try:
                libroMayor = LibroMayor.objects.get(estado=True)
                libroMayor.estado = False
                libroMayor.save()
            except: LibroMayor.DoesNotExist



            try:
                periodo = PeriodoContable.objects.get(activo=True)
            except PeriodoContable.DoesNotExist:
                periodo = None

    except PeriodoContable.DoesNotExist:
        periodo = None

    if request.POST:
        fechaInicio = request.POST.get('fechaInicio')
        fechaFin = request.POST.get('fechaFin')
        anio = request.POST.get('id_anio')
        mes = request.POST.get('id_mes')
        if fechaInicio==None:
            iniciarPeriodo()
        else:
            newPeriodo = PeriodoContable(fechaInicio=fechaInicio, fechaFin=fechaFin, anio=anio, mes=mes)
            newPeriodo.save()
        try:
            periodo = PeriodoContable.objects.get(activo=True)
        except PeriodoContable.DoesNotExist:
            periodo = None
        iniciarLibroMayor(periodo)

    context = {
        'anios_esta': anios_estados,
        'periodo_actual': periodo,
       }

    return render(request, "paginas/periodo_contable.html", context)
def costoIndirecto(request):
    anios_estados = PeriodoContable.objects.raw('select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    #c=iniciarCompra()

    context={
        'anios_esta':anios_estados,
        #'idCompra':c,
    }
    return render(request,"paginas/costo_indirecto.html",context)
    
def materiaPrima(request):
    anios_estados = PeriodoContable.objects.raw('select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    #c=iniciarCompra()

    context={
        'anios_esta':anios_estados,
        #'idCompra':c,
    }
    return render(request,"paginas/materia_prima.html",context)

def manoDeObraD(request):
    anios_estados = PeriodoContable.objects.raw('select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    #c=iniciarCompra()

    context={
        'anios_esta':anios_estados,
        #'idCompra':c,
    }
    return render(request,"paginas/mano_de_obra.html",context)

def producto(request):
    return render(request,"paginas/producto.html")


def Entradas(request):
    if request.method == 'POST':

        
                form1 = EntradaForm(request.POST)
                if form1.is_valid():
                    horas=request.POST.get('horas')
                    des=request.POST.get('des')
                    

                    totalmod=float(horas)
                    total1=12
                    
                    form1.save()
#return render_to_response('paginas/costo_indirecto.html', {'horas':horas, 'des':des, 'totalmod':totalmod, 'total1':total1,  'form1':form1})
                return render_to_response('paginas/costo_indirecto.html', {'form1':form1})

    else:
        form1=EntradaForm()

    #contexto ={
    #'entradas':form1,'salidas':suma
    #}
        return render(request,'paginas/entradas.html', {'form1':form1})

def inventario(request):
    anios_estados = PeriodoContable.objects.raw(
        'select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    detallePeld=detalleKardex.objects.get(nombre="Plastico PELD" )
    detallePehd = detalleKardex.objects.get(nombre="Plastico PEHD")
    detallePet = detalleKardex.objects.get(nombre="Plastico PET")

    inventario = Kardex.objects.all()
    if request.POST:
        producto = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        if producto == "Mesas para exterior":
            cant = float(cantidad) * 9.3
            precio=12 #Estos precio deberan de ser calculados con una funcion, ejemplo precio=calcularPrecio(cant)
        else:
            if producto == "Bancas para exterior":
                cant = float(cantidad) * 5.9
                concepto = "Plastico PEHD"
                precio =7

            else:
                if producto == "Sillas de playa":
                    cant = float(cantidad) * 8.9
                    concepto = "Plastico PEHD"
                    precio=18
                else:
                    if producto == "Losas plasticas":
                        cant = float(cantidad) * 1.7
                        concepto = "Plastico PELD"
                        precio=3.5
                    else:
                        cant = float(cantidad) * 1.3
                        concepto = "Plastico PET"
                        precio=1
        
        agregarKardex(0, 0, cant, 0, concepto)
        cuenta=Cuenta.objects.get(nombre=concepto)   
           
        detalle = detalleKardex.objects.get(nombre=concepto)
        ultimo = Kardex.objects.filter(detalle=detalle).latest('idKardex')
        abono=(float(ultimo.precExistencia)*float(cant))
        costosUnitarios(cantidad,producto,abono)    
        agregarDiario(cuenta,"Orden",0,abono)
		
        inventario = Kardex.objects.all()
        context = {
            'anios_esta': anios_estados,
            'inventario': inventario,
            'detallePeld': detallePeld,
            'detallePehd': detallePehd,
            'detallePet': detallePet,

        }
        return render(request, "paginas/inventarios.html", context)

    context = {
        'anios_esta': anios_estados,
        'inventario': inventario,
        'detallePeld'   : detallePeld,
        'detallePehd':detallePehd,
        'detallePet':detallePet,    }
    return render(request, "paginas/inventarios.html", context)

def inventarioProducto(request):
    anios_estados = PeriodoContable.objects.raw(
        'select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    detalleLosas = detalleKardex.objects.get(nombre="Losas plasticas")
    detalleFiguras = detalleKardex.objects.get(nombre="Figuras")
    detalleSillas = detalleKardex.objects.get(nombre="Sillas de playa")
    detalleBancas = detalleKardex.objects.get(nombre="Bancas para exterior")
    detalleMesas = detalleKardex.objects.get(nombre="Mesas para exterior")

    inventario = Kardex.objects.all()

    context = {
        'anios_esta': anios_estados,
        'inventario': inventario,
        'detalleFiguras': detalleFiguras,
        'detalleLosas': detalleLosas,
        'detalleSillas': detalleSillas,
        'detalleBancas':detalleBancas,
        'detalleMesas':detalleMesas,

    }
    return render(request, "paginas/inventario_producto.html", context)

def catalogo(request):
    cuentas = Cuenta.objects.all()
    if len(cuentas)==0:
        iniciarCatalogo()
    cuenta = Cuenta.objects.all()
    contexto = {'cuentas':cuenta}
    return render(request, "paginas/catalogo.html", contexto)

##############################################################
def transcuenta(request):

    anios_estados = PeriodoContable.objects.raw(
        'select * from Sicapp_PeriodoContable group by anio order by anio desc  ') 
    cuentas = Cuenta.objects.all()
    exito = ' '

    if request.POST:
        cuendebe = request.POST.get("idcue1")
        cuenhabe = request.POST.get("idcue2")
        monto = float(request.POST.get("monto"))
        cuentadedebe = Cuenta.objects.get(codCuenta = cuendebe)
        cuentadehaber = Cuenta.objects.get(codCuenta = cuenhabe)
        agregarDiario(cuentadedebe,"carga",monto,0)
        agregarDiario(cuentadehaber,"abono",0,monto)
        exito = "Se hizo una transaccion"
        context = {
            'anios_esta': anios_estados,
            'cuenta': cuentas,
            'cuende': cuentadedebe,
            'cuenha': cuentadehaber,
            'monto': monto,
            'exito': exito,
        }
        return render(request, "paginas/transa_cuentas.html", context)

    context ={
        'anios_esta': anios_estados,
        'cuenta': cuentas,
        'exito': exito,
    }
    return render(request, "paginas/transa_cuentas.html", context)

def inventario1(request):
    anios_estados = PeriodoContable.objects.raw(
        'select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
   # detallePeld=detalleKardex.objects.get(nombre="Plastico PELD" )
    #detallePehd = detalleKardex.objects.get(nombre="Plastico PEHD")
    #detallePet = detalleKardex.objects.get(nombre="Plastico PET")

    inventario = Kardex.objects.all()
    if request.POST:
        producto = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        if producto == "Mesas para exterior":
            plast == "PEHD"
            req = 29963.10
            costo0 = float(cantidad) *  float(req)  
        else:
            if producto == "Bancas para exterior":
                plast == "PEHD"
                req = 25129.60
                costo1 = float(cantidad) * float(req)
            else:
                if producto == "Sillas de playa":
                    plast == "PEHD"
                    req = 4667.20
                    costo2 = float(cantidad) * float(req)
                else:
                    if producto == "Losas plasticas":
                        plast == "PET"
                        req = 5603.10
                        costo3 = float(cantidad) * float(req)
                    else:
                        plast == "Figuras"
                        req = 7889.60
                        costo4 = float(cantidad) * float(req)

       # concepto = "Plastico PEHD"
        #agregarKardex(0, 0, cant, 0, concepto)
        
        #agregarKardex(cantidad,precio,0,0,producto)
        
        inventario1 = Kardex.objects.all()
        
        return render(request, "paginas/costo_indirecto.html")

    #context = {
     #   'anios_esta': anios_estados,
      #  'inventario': inventario,
       # 'detallePeld'   : detallePeld,
        #'detallePehd':detallePehd,
        #'detallePet':detallePet,    }
    #return render(request, "paginas/costo_indirecto.html", context)


    def inventario2(request):
        anios_estados = PeriodoContable.objects.raw(
        'select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
   # detallePeld=detalleKardex.objects.get(nombre="Plastico PELD" )
    #detallePehd = detalleKardex.objects.get(nombre="Plastico PEHD")
    #detallePet = detalleKardex.objects.get(nombre="Plastico PET")
        canti= Kardex.objects.get(cantExistencia)

        inventario = Kardex.objects.all()
        if request.POST:
            producto = request.POST.get("producto")
            cantidad = request.POST.get("cantidad")
            if producto == "Mesas para exterior":
                costop = 3417.89
                cif = 0
                costoad = 3021.29
                costoc = 5382.54
                t = float(costop) + float(cif) + float(costoad) + float(costoc) 
                ubpp = 5603.10
                cu= float(float(t) / int(canti))
            else:
                if producto == "Bancas para exterior":
                    costop = 3417.89
                    cif = 0
                    costoad = 3021.29
                    costoc = 5382.54
                    t = float(costop) + float(cif) + float(costoad) + float(costoc) 
                    ubpp = 5603.10
                    cu= float(float(t) / int(canti))
                else:
                    if producto == "Sillas de playa":
                        costop = 3417.89
                        cif = 0
                        costoad = 3021.29
                        costoc = 5382.54
                        t = float(costop) + float(cif) + float(costoad) + float(costoc) 
                        ubpp = 5603.10
                        cu= float(float(t) / int(canti))
                    else:
                        if producto == "Losas plasticas":
                            costop = 3417.89
                            cif = 0
                            costoad = 3021.29
                            costoc = 5382.54
                            t = float(costop) + float(cif) + float(costoad) + float(costoc) 
                            ubpp = 5603.10
                            cu= float(float(t) / int(canti))
                        else:
                            plast == "Figuras"
                            costop = 3417.89
                            cif = 0
                            costoad = 3021.29
                            costoc = 5382.54
                            t = float(costop) + float(cif) + float(costoad) + float(costoc) 
                            ubpp = 5603.10
                            cu= float(float(t) / int(canti))
           # concepto = "Plastico PEHD"
            #agregarKardex(0, 0, cant, 0, concepto)
            
            #agregarKardex(cantidad,precio,0,0,producto)
            
            inventario1 = Kardex.objects.all()
            
            return render(request, "paginas/costo_indirecto.html")

def comprobacion(request):
    librosDiarios = LibroDiario.objects.all().order_by('cuenta')
    listado = []
    lisaux = []
    caracu = 0.0
    aboacu = 0.0

####### Metodo de ordenamiento de cuentas
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 11:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 12:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 13:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 21:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 22:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 23:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 24:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 31:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 32:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 33:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 41:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 42:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 51:
            lisaux.append(libros)
    for libros in librosDiarios:
        if int(libros.cuenta.codigoN[0:2]) == 52:
            lisaux.append(libros)


    for libros in lisaux:
        carg = float(libros.cargo)
        abon = float(libros.abono)
        cab = carg - abon
        if cab < 0:
            abon = -cab
            carg = 0
        else:
            carg = cab
            abon = 0
        a = [libros.cuenta.codigoN,libros.cuenta.nombre,carg,abon]
        listado.append(a)
        caracu = caracu + carg
        aboacu = aboacu + abon

    context = {
        'librodia': listado,
        'totaca': caracu,
        'totaab': aboacu,
    }
    return render(request, "paginas/comprobacion.html", context)
def libroCompra(request):
    anios_estados = PeriodoContable.objects.raw(
        'select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    periodo=PeriodoContable.objects.filter(activo=False).latest('idPeriodo')
    compra=Compra.objects.filter(periodoCon=periodo)
    context={
        'anios_esta': anios_estados,
        'compra':compra,
    }
    return render(request,"paginas/libro_compras.html", context)

def libroVenta(request):
    anios_estados = PeriodoContable.objects.raw(
        'select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    periodo=PeriodoContable.objects.filter(activo=False).latest('idPeriodo')
    venta=Venta.objects.filter(periodoCon=periodo)
    context={
        'anios_esta': anios_estados,
        'venta':venta,
    }
    return render(request,"paginas/libro_ventas.html", context)

def empleados(request):
    empleado2 = empleado.objects.all()
    contexto = {'empleados':empleado2}
    return render(request, "paginas/empleados.html", contexto)