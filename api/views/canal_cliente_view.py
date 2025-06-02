from rest_framework import viewsets
from api.models.canal_cliente import CanalCliente
from api.serializers.canal_cliente_serializer import CanalClienteSerializer

class CanalClienteViewSet(viewsets.ModelViewSet):
    queryset = CanalCliente.objects.all()
    serializer_class = CanalClienteSerializer