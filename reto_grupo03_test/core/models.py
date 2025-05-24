from django.db import models
from django.utils import timezone


# Master Catalog Models
class Empresa(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11, unique=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']

class Sucursal(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.empresa.nombre} - {self.nombre}"

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        unique_together = ['empresa', 'codigo']
        ordering = ['empresa', 'nombre']

class TipoIdentificacion(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de Identificación"
        verbose_name_plural = "Tipos de Identificación"

class CondicionVenta(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    dias_credito = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Condición de Venta"
        verbose_name_plural = "Condiciones de Venta"

class GrupoProveedor(models.Model):
    grupo_id = models.CharField(max_length=36, primary_key=True)  # UUID field
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)  # Link to Empresa
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.IntegerField(default=1)
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Grupo Proveedor"
        verbose_name_plural = "Grupos Proveedores"

class LineaArticulo(models.Model):
    grupo_proveedor = models.ForeignKey(GrupoProveedor, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.grupo_proveedor.nombre} - {self.nombre}"

    class Meta:
        verbose_name = "Línea de Artículo"
        verbose_name_plural = "Líneas de Artículos"
        unique_together = ['grupo_proveedor', 'codigo']

class SubLineaArticulo(models.Model):
    linea_articulo = models.ForeignKey(LineaArticulo, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.linea_articulo.nombre} - {self.nombre}"

    class Meta:
        verbose_name = "Sub Línea de Artículo"
        verbose_name_plural = "Sub Líneas de Artículos"
        unique_together = ['linea_articulo', 'codigo']

class CanalCliente(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Canal de Cliente"
        verbose_name_plural = "Canales de Cliente"

class Vendedor(models.Model):
    tipo_identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.CASCADE)
    numero_identificacion = models.CharField(max_length=20)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    canal = models.ForeignKey(CanalCliente, on_delete=models.CASCADE)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"
        unique_together = ['tipo_identificacion', 'numero_identificacion']

class Cliente(models.Model):
    tipo_identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.CASCADE)
    numero_identificacion = models.CharField(max_length=20)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nombre_comercial = models.CharField(max_length=200, blank=True, null=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    canal = models.ForeignKey(CanalCliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True)
    condicion_venta = models.ForeignKey(CondicionVenta, on_delete=models.CASCADE)
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        if self.nombre_comercial:
            return self.nombre_comercial
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        unique_together = ['tipo_identificacion', 'numero_identificacion']

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    articulo = models.ForeignKey('productos.Articulo', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pedido} - {self.articulo}"

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Items de Pedido"