from django.db import models
from .canal_cliente import CanalCliente

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    canal = models.ForeignKey(CanalCliente, on_delete=models.CASCADE, related_name='clientes')

    class Meta:
        db_table = 'cliente'
