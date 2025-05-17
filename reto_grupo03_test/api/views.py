from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from core.models import Pedido, PedidoItem
from promociones.models import Promocion
from .serializers import PromocionSerializer, PedidoSerializer
from core.views import procesar_promociones

class PromocionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing promotions
    """
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer

@api_view(['POST'])
def check_promotions(request):
    """
    API endpoint to check applicable promotions for an order
    Expected payload:
    {
        "cliente_id": 1,
        "items": [
            {
                "articulo_id": 1,
                "cantidad": 48,
                "precio_unitario": 100.00
            }
        ]
    }
    """
    try:
        # Create a temporary order object to process promotions
        cliente_id = request.data.get('cliente_id')
        items = request.data.get('items', [])
        
        if not cliente_id or not items:
            return Response(
                {'error': 'Cliente ID and items are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create temporary order
        pedido = Pedido.objects.create(
            cliente_id=cliente_id,
            fecha=timezone.now(),
            monto_total=0
        )
        
        # Create order items
        monto_total = 0
        for item in items:
            subtotal = item['cantidad'] * item['precio_unitario']
            monto_total += subtotal
            
            PedidoItem.objects.create(
                pedido=pedido,
                articulo_id=item['articulo_id'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario'],
                subtotal=subtotal
            )
        
        pedido.monto_total = monto_total
        pedido.save()
        
        # Process promotions
        bonificaciones = procesar_promociones(pedido)
        
        # Format response
        response_data = {
            'pedido_id': pedido.id,
            'monto_total': float(pedido.monto_total),
            'bonificaciones': [
                {
                    'articulo_id': b['articulo'].id,
                    'articulo_nombre': b['articulo'].nombre,
                    'cantidad': b['cantidad'],
                    'tipo': b['tipo']
                }
                for b in bonificaciones
            ]
        }
        
        # Delete temporary order
        pedido.delete()
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 