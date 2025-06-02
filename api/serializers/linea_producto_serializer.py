from rest_framework import serializers
from api.models.linea_producto import LineaProducto

class LineaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaProducto
        fields = ['id', 'nombre', 'categoria'] 