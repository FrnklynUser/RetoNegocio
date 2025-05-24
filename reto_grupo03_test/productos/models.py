from django.db import models
from django.core.validators import MinValueValidator
from core.models import Empresa, SubLineaArticulo

# Create your models here.

class CategoriaProducto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
        unique_together = ['empresa', 'codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class LineaProducto(models.Model):
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, related_name='lineas')
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Línea de Producto"
        verbose_name_plural = "Líneas de Productos"
        unique_together = ['categoria', 'codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Articulo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    sub_linea = models.ForeignKey(SubLineaArticulo, on_delete=models.CASCADE, related_name='articulos')
    codigo = models.CharField(max_length=20)
    codigo_barra = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=20)
    peso = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(validators=[MinValueValidator(0)])
    stock_maximo = models.IntegerField(validators=[MinValueValidator(0)])
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        unique_together = ['empresa', 'codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
