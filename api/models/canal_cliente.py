from django.db import models

class CanalCliente(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'canal_cliente'
