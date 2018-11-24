from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Sicapp.iniciar import iniciarCompra
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