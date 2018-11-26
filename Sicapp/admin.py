from django.contrib import admin

# Register your models here.
from Sicapp.models import *
#Usuario admin:   user:admin    Password:barrons2018

class CompraAdmin(admin.ModelAdmin): list_display = ('idCompra','fecha','total')
class DetalleCompraAdmin(admin.ModelAdmin): list_display = ('idDetalleCompra','cantidad','concepto','precio','total')
class ProveedorAdmin(admin.ModelAdmin):list_display = ('idProveedor','razonSocial','estado')
class PeriodoContableAdmin(admin.ModelAdmin): list_display = ('idPeriodo', 'fechaInicio','anio','mes')
class TransaccionAdmin(admin.ModelAdmin): list_display = ('idTransaccion', 'fecha','concepto','saldo')
class CuentaAdmin(admin.ModelAdmin): list_display = ('codCuenta', 'nombre','tipoCuenta')
class ControlEfectivoAdmin(admin.ModelAdmin): list_display = ('idControl', 'concepto','saldoTotal')
class LibroMayorAdmin(admin.ModelAdmin): list_display = ('idLibroM', 'fecha','saldo','estado')
class LibroDiarioAdmin(admin.ModelAdmin): list_display = ('idLibroD', 'fecha','descripcion')
class KardexAdmin(admin.ModelAdmin): list_display = ('idKardex', 'cantExistencia','precExistencia','montoExistencia')
class DetalleKardexAdmin(admin.ModelAdmin): list_display = ('idDetalle', 'tipo','nombre')

admin.site.register(Compra,CompraAdmin)
admin.site.register(Detallecompra,DetalleCompraAdmin)
admin.site.register(Proveedor,ProveedorAdmin)
admin.site.register(PeriodoContable, PeriodoContableAdmin)
admin.site.register(TransaccionCV, TransaccionAdmin)
admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(ControlEfectivo, ControlEfectivoAdmin)
admin.site.register(LibroMayor, LibroMayorAdmin)
admin.site.register(LibroDiario, LibroDiarioAdmin)
admin.site.register(Kardex, KardexAdmin)
admin.site.register(detalleKardex, DetalleKardexAdmin)
