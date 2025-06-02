from rest_framework import viewsets
from api.models.sucursal import Sucursal
from api.serializers.sucursal_serializer import SucursalSerializer
 
class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer 