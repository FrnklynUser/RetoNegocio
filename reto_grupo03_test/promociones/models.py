from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from core.models import Empresa, Sucursal, CanalCliente
from productos.models import Articulo

class TipoPromocion(models.Model):
    VOLUMEN = 'VOL'
    MONTO = 'MON'
    
    TIPO_CHOICES = [
        (VOLUMEN, 'Volumen'),
        (MONTO, 'Monto'),
    ]
    
    codigo = models.CharField(max_length=3, primary_key=True, choices=TIPO_CHOICES)
    descripcion = models.CharField(max_length=50)
    
    def __str__(self):
        return self.descripcion

class Promocion(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    canal_cliente = models.ForeignKey(CanalCliente, on_delete=models.CASCADE, related_name='promociones')
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    tipo_promocion = models.ForeignKey(TipoPromocion, on_delete=models.PROTECT)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    
    # Para promociones por volumen
    cantidad_minima = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    cantidad_bonificacion = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    
    # Para promociones por monto
    monto_minimo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')
        
        if self.tipo_promocion.codigo == TipoPromocion.VOLUMEN:
            if not self.cantidad_minima or not self.cantidad_bonificacion:
                raise ValidationError('Para promociones por volumen, debe especificar cantidad mínima y bonificación')
            if self.monto_minimo:
                raise ValidationError('Las promociones por volumen no deben tener monto mínimo')
                
        if self.tipo_promocion.codigo == TipoPromocion.MONTO:
            if not self.monto_minimo:
                raise ValidationError('Para promociones por monto, debe especificar el monto mínimo')
            if self.cantidad_minima or self.cantidad_bonificacion:
                raise ValidationError('Las promociones por monto no deben tener cantidades especificadas')

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
        unique_together = ['empresa', 'codigo']

class ArticuloPromocion(models.Model):
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, related_name='articulos')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='promociones')
    es_bonificacion = models.BooleanField(default=False)
    cantidad_bonificacion = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    
    class Meta:
        verbose_name = "Artículo en Promoción"
        verbose_name_plural = "Artículos en Promoción"
        unique_together = [['promocion', 'articulo', 'es_bonificacion']]
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.es_bonificacion and not self.cantidad_bonificacion:
            raise ValidationError('Debe especificar la cantidad de bonificación para artículos de bonificación')
        if not self.es_bonificacion and self.cantidad_bonificacion:
            raise ValidationError('No debe especificar cantidad de bonificación para artículos que no son de bonificación')
    
    def __str__(self):
        tipo = "Bonificación" if self.es_bonificacion else "Principal"
        return f"{self.articulo} - {tipo}"
