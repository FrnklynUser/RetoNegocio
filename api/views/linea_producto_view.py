from rest_framework import viewsets
from api.models.linea_producto import LineaProducto
from api.serializers.linea_producto_serializer import LineaProductoSerializer

class LineaProductoViewSet(viewsets.ModelViewSet):
    queryset = LineaProducto.objects.all()
    serializer_class = LineaProductoSerializer 