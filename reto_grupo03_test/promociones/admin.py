from django.contrib import admin
from .models import TipoPromocion, Promocion, ArticuloPromocion

class ArticuloPromocionInline(admin.TabularInline):
    model = ArticuloPromocion
    extra = 1
    fields = ['articulo', 'es_bonificacion', 'cantidad_bonificacion']

@admin.register(TipoPromocion)
class TipoPromocionAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion']
    search_fields = ['codigo', 'descripcion']

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'empresa', 'sucursal', 'canal_cliente', 'tipo_promocion', 'fecha_inicio', 'fecha_fin', 'estado']
    search_fields = ['codigo', 'nombre']
    list_filter = ['empresa', 'sucursal', 'canal_cliente', 'tipo_promocion', 'estado']
    date_hierarchy = 'fecha_inicio'
    inlines = [ArticuloPromocionInline]
    
    fieldsets = [
        (None, {
            'fields': ['empresa', 'sucursal', 'canal_cliente', 'codigo', 'nombre', 'descripcion', 'tipo_promocion', 'estado']
        }),
        ('Fechas', {
            'fields': ['fecha_inicio', 'fecha_fin']
        }),
        ('Reglas de Promoción', {
            'fields': ['cantidad_minima', 'cantidad_bonificacion', 'monto_minimo'],
            'description': 'Complete los campos según el tipo de promoción'
        })
    ]
