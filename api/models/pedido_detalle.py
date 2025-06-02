from django.db import models
from .pedido import Pedido
from .producto import Producto

class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles')
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()

    class Meta:
        db_table = 'pedido_detalle'
