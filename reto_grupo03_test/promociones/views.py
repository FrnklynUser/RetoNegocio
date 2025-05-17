from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .services import PromocionService
import json

# Create your views here.

class CalcularBonificacionesView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            # Validar datos requeridos
            if not all(key in data for key in ['canal_cliente_id', 'items']):
                return JsonResponse({
                    'error': 'Se requieren canal_cliente_id e items'
                }, status=400)
            
            # Validar estructura de items
            for item in data['items']:
                if not all(key in item for key in ['articulo_id', 'cantidad', 'precio']):
                    return JsonResponse({
                        'error': 'Cada item debe tener articulo_id, cantidad y precio'
                    }, status=400)
            
            # Calcular bonificaciones
            bonificaciones = PromocionService.calcular_bonificaciones(
                canal_cliente_id=data['canal_cliente_id'],
                items=data['items']
            )
            
            return JsonResponse({
                'bonificaciones': bonificaciones
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'JSON inválido'
            }, status=400)
            
        except ValidationError as e:
            return JsonResponse({
                'error': str(e)
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'error': 'Error interno del servidor'
            }, status=500)
