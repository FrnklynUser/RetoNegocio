from django.db import models
from .promocion import Promocion
from .producto import Producto

class BeneficioPromocion(models.Model):
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, related_name='beneficios')
    tipo_beneficio = models.CharField(max_length=50)
    producto_bonificado = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name='beneficios')
    cantidad = models.IntegerField(null=True, blank=True)
    porcentaje_descuento = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'beneficio_promocion'
