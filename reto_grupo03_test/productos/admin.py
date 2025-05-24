from django.contrib import admin
from .models import Articulo

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'empresa', 'sub_linea', 'precio', 'estado')
    search_fields = ('codigo', 'nombre', 'codigo_barra')
    list_filter = ('empresa', 'sub_linea', 'estado')
    list_per_page = 20
