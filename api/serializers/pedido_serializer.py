from rest_framework import serializers
from api.models import Pedido, PedidoDetalle

class PedidoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoDetalle
        fields = ['producto', 'cantidad', 'precio_unitario']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = PedidoDetalleSerializer(many=True)
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'sucursal', 'fecha', 'total_monto', 'detalles'] 