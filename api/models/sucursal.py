from django.db import models
from .empresa import Empresa

class Sucursal(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='sucursales')
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'sucursal'
