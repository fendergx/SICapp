"""Sic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from Sicapp import views
from Sicapp.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.probando, name='prueba'),
    url(r'^estados/(?P<id_estados>\d+)/$',views.estadosFinancieros, name='estados'),
    url(r'^navbar/$', views.probando, name='navbar'),
    url(r'compras/$', views.compras, name='compras'),
    url(r'ventas/$', views.ventas, name='ventas'),
    url(r'periodoContable/$', views.periodoContable, name='periodoContable'),
    url(r'costoIndirecto/$', views.costoIndirecto, name='costoIndirecto'),
    url(r'materiaPrima/$', views.materiaPrima, name='materiaPrima'),
    url(r'manoDeObraD/$', views.manoDeObraD, name='manoDeObraD'),
    url(r'producto/', views.producto, name='producto'),
    url(r'Entradas/', views.Entradas,name="Entradas"),
	url(r'inventarios/$', views.inventario, name='inventarios'),
	url(r'inventarioProducto/$', views.inventarioProducto, name='inventarioProducto'),
    url(r'catalogo/$',views.catalogo,name='catalogo'),
    url(r'libroCompra/$',views.libroCompra,name='libroCompra'),
    url(r'libroVenta/$',views.libroVenta,name='libroVenta'),
    #Transacciones y Estados Financieros
    url(r'transcuenta/$', views.transcuenta, name='transcuenta'),
    url(r'comprobacion/$', views.comprobacion, name='comprobacion'),
       
]
