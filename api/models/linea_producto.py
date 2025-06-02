from django.db import models

class LineaProducto(models.Model):
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)

    class Meta:
        db_table = 'linea_producto'
