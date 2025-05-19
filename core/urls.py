from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    # Authentication
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
    
    # Client 
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    
    # Order 
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),

    # Empresa 
    path('empresas/', views.lista_empresas, name='lista_empresas'),
    path('empresas/crear/', views.crear_empresa, name='crear_empresa'),
    path('empresas/editar/<int:empresa_id>/', views.editar_empresa, name='editar_empresa'),
    
    # Sucursal 
    path('sucursales/', views.lista_sucursales, name='lista_sucursales'),
    path('sucursales/crear/', views.crear_sucursal, name='crear_sucursal'),
    path('sucursales/editar/<int:sucursal_id>/', views.editar_sucursal, name='editar_sucursal'),
] 