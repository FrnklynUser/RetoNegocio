from rest_framework import serializers
from api.models.beneficio_promocion import BeneficioPromocion

class BeneficioPromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficioPromocion
        fields = ['id', 'promocion', 'tipo_beneficio', 'producto_bonificado', 'cantidad', 'porcentaje_descuento'] 