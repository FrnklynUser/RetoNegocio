from django.db import models
from .pedido import Pedido
from .promocion import Promocion

class PromocionAplicada(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='promociones_aplicadas')
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, related_name='aplicaciones')
    descripcion_resultado = models.TextField()

    class Meta:
        db_table = 'promocion_aplicada'
