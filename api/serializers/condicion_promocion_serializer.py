from rest_framework import serializers
from api.models.condicion_promocion import CondicionPromocion

class CondicionPromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicionPromocion
        fields = ['id', 'promocion', 'tipo_condicion', 'valor_min', 'valor_max', 'producto', 'linea_producto', 'bonificacion_descuento'] 