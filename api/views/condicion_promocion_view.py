from rest_framework import viewsets
from api.models.condicion_promocion import CondicionPromocion
from api.serializers.condicion_promocion_serializer import CondicionPromocionSerializer

class CondicionPromocionViewSet(viewsets.ModelViewSet):
    queryset = CondicionPromocion.objects.all()
    serializer_class = CondicionPromocionSerializer 