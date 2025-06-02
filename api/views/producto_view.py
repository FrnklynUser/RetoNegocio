from rest_framework import viewsets
from api.models.producto import Producto
from api.serializers.producto_serializer import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer 