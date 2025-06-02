from django.db import models
from .linea_producto import LineaProducto

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    linea = models.ForeignKey(LineaProducto, on_delete=models.CASCADE, related_name='productos')

    class Meta:
        db_table = 'producto'
