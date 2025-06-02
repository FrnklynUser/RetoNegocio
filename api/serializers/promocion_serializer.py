from rest_framework import serializers
from api.models.promocion import Promocion

class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'tipo_promocion', 
                 'empresa', 'sucursal', 'canal_cliente', 'producto_adicional']