from rest_framework import viewsets
from api.models.cliente import Cliente
from api.serializers.cliente_serializer import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer 