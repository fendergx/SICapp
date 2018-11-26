from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response


# Create your views here.
from Sicapp.iniciar import *
from Sicapp.models import *
from django.template import RequestContext
from django.db.models import Max
from .forms import EntradaForm


#def probando(request):return render(request, "index.html")

def probando(request):
    return render(request,"paginas/index.html",{'anios_esta':PeriodoContable.objects.raw('select * from Sicapp_PeriodoContable group by anio order by anio desc  ')})

def estadosFinancieros(request, id_estados):
    anios=PeriodoContable.objects.filter(anio=id_estados)
    anios_estados=PeriodoContable.objects.raw('select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    context ={
        'anios':anios,
        'anios_esta':anios_estados,
        'anio_select':id_estados
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

    if periodoC!=None:
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
                    subTotal = int(float(precio))*int(float(cantidad))
                    cantidadProd=cantidadProd+int(float(cantidad))
                    total=total+subTotal
                    detalle=Detallecompra(cantidad=cantidad,concepto=concepto,precio=precio,total=subTotal,compra=idCompra)
                    detalle.save()
                    cuenta=Cuenta.objects.get(nombre=concepto)
                    agregarDiario(cuenta,"compra",subTotal,0)
                    agregarKardex(cantidad,precio,0,0)
                    contador=contador+1


            if compraActualizar.terminoCompra=="Compra Gravada":
                compraActualizar.iva=total*0.13
                cuenta = Cuenta.objects.get(nombre="IVA")
                agregarDiario(cuenta, "compra", compraActualizar.iva, 0)
            compraActualizar.total=total+compraActualizar.iva

            if compraActualizar.total!=0:
                compraActualizar.estado=True
            compraActualizar.periodoContable=periodoC
            if compraActualizar.tipoCompra=="Credito":
                agregarTransaccionCV("Compra materia prima", total, compraActualizar, "compra", periodoC)
                cuenta = Cuenta.objects.get(nombre="Cuentas por pagar a proveedores")
                agregarDiario(cuenta, "compra", 0, compraActualizar.total)
            else:
                agregarControlEfectivo("Compra materia prima", compraActualizar,periodoC)
                cuenta = Cuenta.objects.get(nombre="Caja general")
                agregarDiario(cuenta, "compra", 0, compraActualizar.total)

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
    #c=iniciarCompra()

    context={
        'anios_esta':anios_estados,
        #'idCompra':c,
    }
    return render(request,"paginas/venta.html",context)

def periodoContable(request):
    anios_estados = PeriodoContable.objects.raw(
        'select * from Sicapp_PeriodoContable group by anio order by anio desc  ')


    try:
        periodo = PeriodoContable.objects.get(activo=True)
        periodoActualizar = PeriodoContable.objects.get(activo='True')
        libroMayor=LibroMayor.objects.get(estado=True)
        if request.GET:
            periodoActualizar.idPeriodo
            periodoActualizar.activo = False
            periodoActualizar.save()
            libroMayor.estado=False
            libroMayor.save()

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

   # def CostoIndirectoList(request):
    #model = CostoIndirecto
    #template_name = 'paginas/costoInditecto_list.html'

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
    inventario=Kardex.objects.all()
    detalleKardex.objects.get(tipo="Materia Prima")
    context = {
        'anios_esta': anios_estados,
        'inventario': inventario,
        'detalle'   : detalleKardex,

			 
								   
					  
    }
    return render(request, "paginas/inventarios.html", context)