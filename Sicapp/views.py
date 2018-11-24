from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Sicapp.iniciar import *
from Sicapp.models import *


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
    anios_estados = PeriodoContable.objects.raw('select * from Sicapp_PeriodoContable group by anio order by anio desc  ')
    #c=iniciarCompra()

    context={
        'anios_esta':anios_estados,
        #'idCompra':c,
    }
    return render(request,"paginas/compra.html",context)

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
        if request.GET:
            periodoActualizar.idPeriodo
            periodoActualizar.activo = False
            periodoActualizar.save()

            try: periodo = PeriodoContable.objects.get(activo=True)
            except PeriodoContable.DoesNotExist:
                periodo = None


    except PeriodoContable.DoesNotExist:
        periodo = None


    if request.POST:
        fechaInicio = request.POST.get('fechaInicio')
        fechaFin = request.POST.get('fechaFin')
        anio = request.POST.get('id_anio')
        mes = request.POST.get('id_mes')
        newPeriodo = PeriodoContable(fechaInicio=fechaInicio, fechaFin=fechaFin, anio=anio, mes=mes)
        newPeriodo.save()
        try:
            periodo = PeriodoContable.objects.get(activo=True)
        except PeriodoContable.DoesNotExist:
            periodo = None

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