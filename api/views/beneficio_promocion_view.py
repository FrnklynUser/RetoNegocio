from rest_framework import viewsets
from api.models.beneficio_promocion import BeneficioPromocion
from api.serializers.beneficio_promocion_serializer import BeneficioPromocionSerializer

class BeneficioPromocionViewSet(viewsets.ModelViewSet):
    queryset = BeneficioPromocion.objects.all()
    serializer_class = BeneficioPromocionSerializer 