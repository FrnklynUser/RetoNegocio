from django.db import models
from .promocion import Promocion
from .producto import Producto
from .linea_producto import LineaProducto
from .canal_cliente import CanalCliente

class CondicionPromocion(models.Model):
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, related_name='condiciones')
    tipo_condicion = models.CharField(max_length=50)
    valor_min = models.FloatField()
    valor_max = models.FloatField(null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name='condiciones')
    linea_producto = models.ForeignKey(LineaProducto, on_delete=models.SET_NULL, null=True, blank=True, related_name='condiciones')
    canal_cliente = models.ForeignKey(CanalCliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='condiciones')
    bonificacion_descuento = models.BooleanField()

    class Meta:
        db_table = 'condicion_promocion'
