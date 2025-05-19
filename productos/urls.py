from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('articulos/', views.lista_articulos, name='lista_articulos'),
    path('articulos/crear/', views.crear_articulo, name='crear_articulo'),
    path('articulos/editar/<int:articulo_id>/', views.editar_articulo, name='editar_articulo'),
] 