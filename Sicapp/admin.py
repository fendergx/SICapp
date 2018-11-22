from django.contrib import admin

# Register your models here.
from Sicapp.models import *
#Usuario admin:   user:admin    Password:barrons2018


class CompraAdmin(admin.ModelAdmin): list_display = ('idCompra','fecha','total')
class DetalleCompraAdmin(admin.ModelAdmin): list_display = ('idDetalleCompra','cantidad','concepto','precio','total')
class ProveedorAdmin(admin.ModelAdmin):list_display = ('idProveedor','razonSocial','estado')

admin.site.register(Compra,CompraAdmin)
admin.site.register(Detallecompra,DetalleCompraAdmin)
admin.site.register(Proveedor,ProveedorAdmin)
