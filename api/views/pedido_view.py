from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Pedido, PedidoDetalle, Cliente, Producto, Sucursal
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from api.services.promocion_engine import PromocionEngine

class PedidoViewSet(viewsets.ViewSet):
    @transaction.atomic
    def create(self, request):
        try:
            cliente_id = request.data.get('cliente')
            sucursal_id = request.data.get('sucursal')
            detalles = request.data.get('detalles', [])
            cliente = Cliente.objects.get(id=cliente_id)
            sucursal = Sucursal.objects.get(id=sucursal_id)
        except ObjectDoesNotExist:
            return Response({'error': 'El cliente o la sucursal no existe.'}, status=400)
        pedido = Pedido.objects.create(cliente=cliente, sucursal=sucursal, total_monto=0)
        total_monto = 0
        for d in detalles:
            producto = Producto.objects.get(id=d['producto'])
            cantidad = d['cantidad']
            precio_unitario = d['precio_unitario']
            PedidoDetalle.objects.create(pedido=pedido, producto=producto, cantidad=cantidad, precio_unitario=precio_unitario)
            total_monto += cantidad * precio_unitario
        pedido.total_monto = total_monto
        pedido.save()

        # Usar el motor de promociones
        engine = PromocionEngine(pedido, detalles)
        bonificaciones = engine.aplicar_promociones()

        return Response({
            'pedido_id': pedido.id,
            'bonificaciones': bonificaciones
        }, status=status.HTTP_201_CREATED)