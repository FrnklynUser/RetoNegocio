from django.db import models

# Create your models here.

class PromocionCombinada(models.Model):
    """
    Modelo para promociones que combinan bonificación y descuento (Caso 9)
    """
    nombre = models.CharField(max_length=255)
    producto_principal = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Promoción combinada: {self.nombre}"
    
    def aplicar_promocion(self, producto, monto_total):
        """
        Aplica la promoción combinada según el producto y monto total
        """
        if producto != self.producto_principal:
            return {'bonificacion': None, 'descuento': 0}
        
        if producto == "Detergente A":
            if 1500 < monto_total < 3000:
                bonificacion = {"producto": "Producto B", "cantidad": 5}
                descuento = 0.02
                return {'bonificacion': bonificacion, 'descuento': descuento}
            elif monto_total >= 3000:
                bonificacion = {"producto": "Producto B", "cantidad": 8}
                descuento = 0.03
                return {'bonificacion': bonificacion, 'descuento': descuento}
        
        return {'bonificacion': None, 'descuento': 0}


class RangoPromocionCombinada(models.Model):
    """
    Rangos para las promociones combinadas
    """
    promocion = models.ForeignKey(PromocionCombinada, on_delete=models.CASCADE, related_name='rangos')
    minimo = models.DecimalField(max_digits=10, decimal_places=2)
    maximo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bonificacion_producto = models.CharField(max_length=100)
    bonificacion_cantidad = models.IntegerField()
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
