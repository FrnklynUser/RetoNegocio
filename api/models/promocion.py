from django.db import models
from .empresa import Empresa
from .sucursal import Sucursal
from .canal_cliente import CanalCliente
from .producto import Producto

class Promocion(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_promocion = models.CharField(max_length=50)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='promociones')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='promociones')
    canal_cliente = models.ForeignKey(CanalCliente, on_delete=models.CASCADE, related_name='promociones')
    producto_adicional = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name='promociones_adicionales')

    class Meta:
        db_table = 'promocion'
