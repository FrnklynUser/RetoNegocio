from rest_framework import serializers
from core.models import Pedido, PedidoItem
from promociones.models import Promocion, ArticuloPromocion

class ArticuloPromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloPromocion
        fields = ['id', 'articulo', 'es_bonificacion', 'cantidad_bonificacion']

class PromocionSerializer(serializers.ModelSerializer):
    articulos = ArticuloPromocionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Promocion
        fields = [
            'id', 'codigo', 'nombre', 'empresa', 'sucursal', 'canal_cliente',
            'tipo_promocion', 'fecha_inicio', 'fecha_fin', 'estado',
            'cantidad_minima', 'cantidad_bonificacion', 'monto_minimo',
            'articulos'
        ]

class PedidoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoItem
        fields = ['articulo', 'cantidad', 'precio_unitario', 'subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    items = PedidoItemSerializer(many=True, source='pedidoitem_set')
    
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'fecha', 'monto_total', 'items'] 