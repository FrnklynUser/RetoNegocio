from django.db import models
from .cliente import Cliente
from .sucursal import Sucursal

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='pedidos', null=True, blank=True)  # <--- CAMBIO AQUÍ
    fecha = models.DateTimeField(auto_now_add=True)
    total_monto = models.FloatField()
    class Meta:
        db_table = 'pedido'
