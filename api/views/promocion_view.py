from rest_framework import viewsets
from api.models.promocion import Promocion
from api.serializers.promocion_serializer import PromocionSerializer

class PromocionViewSet(viewsets.ModelViewSet):
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer 