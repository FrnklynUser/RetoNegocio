from django.contrib import admin
from .models import (
    Empresa, Sucursal, TipoIdentificacion, CondicionVenta,
    GrupoProveedor, LineaArticulo, SubLineaArticulo,
    CanalCliente, Vendedor, Cliente, Pedido, PedidoItem
)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'ruc', 'estado')
    search_fields = ('codigo', 'nombre', 'ruc')
    list_filter = ('estado',)

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'codigo', 'nombre', 'estado')
    search_fields = ('codigo', 'nombre')
    list_filter = ('empresa', 'estado')

@admin.register(TipoIdentificacion)
class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'estado')
    search_fields = ('codigo', 'nombre')
    list_filter = ('estado',)

@admin.register(CondicionVenta)
class CondicionVentaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'dias_credito', 'estado')
    search_fields = ('codigo', 'nombre')
    list_filter = ('estado',)

@admin.register(GrupoProveedor)
class GrupoProveedorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'estado')
    search_fields = ('codigo', 'nombre')
    list_filter = ('estado',)

@admin.register(LineaArticulo)
class LineaArticuloAdmin(admin.ModelAdmin):
    list_display = ('grupo_proveedor', 'codigo', 'nombre', 'estado')
    search_fields = ('codigo', 'nombre')
    list_filter = ('grupo_proveedor', 'estado')

@admin.register(SubLineaArticulo)
class SubLineaArticuloAdmin(admin.ModelAdmin):
    list_display = ('linea_articulo', 'codigo', 'nombre', 'estado')
    search_fields = ('codigo', 'nombre')
    list_filter = ('linea_articulo', 'estado')

@admin.register(CanalCliente)
class CanalClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'estado')
    search_fields = ('codigo', 'nombre')
    list_filter = ('estado',)

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'tipo_identificacion', 'numero_identificacion', 'canal', 'estado')
    search_fields = ('nombres', 'apellidos', 'numero_identificacion')
    list_filter = ('tipo_identificacion', 'canal', 'estado')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercial', 'nombres', 'apellidos', 'tipo_identificacion', 'numero_identificacion', 'canal', 'estado')
    search_fields = ('nombre_comercial', 'nombres', 'apellidos', 'numero_identificacion')
    list_filter = ('tipo_identificacion', 'canal', 'estado')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'vendedor', 'fecha', 'monto_total', 'estado')
    search_fields = ('cliente__nombre_comercial', 'cliente__nombres', 'vendedor__nombres')
    list_filter = ('estado',)
    date_hierarchy = 'fecha'

@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'articulo', 'cantidad', 'precio_unitario', 'subtotal', 'estado')
    search_fields = ('pedido__id', 'articulo__nombre')
    list_filter = ('estado',)
