from django import forms
from .models import Cliente, TipoIdentificacion, CanalCliente, CondicionVenta, Empresa, SubLineaArticulo
from productos.models import Articulo

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_identificacion',
            'numero_identificacion',
            'nombres',
            'apellidos',
            'nombre_comercial',
            'direccion',
            'telefono',
            'email',
            'canal',
            'condicion_venta',
            'limite_credito'
        ]
        widgets = {
            'tipo_identificacion': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'numero_identificacion': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'nombre_comercial': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'canal': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'condicion_venta': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'limite_credito': forms.NumberInput(attrs={
                'class': 'block w-full px-4 py-3 text-base rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-right',
                'step': '0.01'
            }),
        }

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = [
            'empresa',
            'sub_linea',
            'codigo',
            'codigo_barra',
            'nombre',
            'descripcion',
            'unidad_medida',
            'peso',
            'precio',
            'stock_minimo',
            'stock_maximo'
        ]
        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-select'}),
            'sub_linea': forms.Select(attrs={'class': 'form-select'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barra': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_maximo': forms.NumberInput(attrs={'class': 'form-control'}),
        } 