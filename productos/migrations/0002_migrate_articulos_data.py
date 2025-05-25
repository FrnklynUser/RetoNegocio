from django.db import migrations
from decimal import Decimal

def disable_foreign_key_checks(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute('SET CONSTRAINTS ALL DEFERRED')

def enable_foreign_key_checks(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute('SET CONSTRAINTS ALL IMMEDIATE')

def migrate_articulos_forward(apps, schema_editor):
    CoreArticulo = apps.get_model('core', 'Articulo')
    ProductosArticulo = apps.get_model('productos', 'Articulo')
    Empresa = apps.get_model('core', 'Empresa')
    SubLineaArticulo = apps.get_model('core', 'SubLineaArticulo')
    
    # Get default empresa and sublinea
    default_empresa = Empresa.objects.first()
    default_sublinea = SubLineaArticulo.objects.first()
    
    if not default_empresa or not default_sublinea:
        return  # Can't proceed without defaults
    
    # Get all articles from core app
    core_articulos = CoreArticulo.objects.all()
    
    # Create new articles in productos app
    for articulo in core_articulos:
        ProductosArticulo.objects.create(
            id=articulo.id,
            empresa=default_empresa,
            sub_linea=default_sublinea,
            codigo=articulo.codigo,
            codigo_barra=getattr(articulo, 'codigo_barra', None),
            nombre=articulo.nombre,
            descripcion=articulo.descripcion,
            unidad_medida=getattr(articulo, 'unidad_medida', 'UND'),
            peso=getattr(articulo, 'peso', Decimal('0.00')),
            precio=getattr(articulo, 'precio', Decimal('0.00')),
            stock_minimo=getattr(articulo, 'stock_minimo', 0),
            stock_maximo=getattr(articulo, 'stock_maximo', 0),
            estado=articulo.estado,
            fecha_creacion=articulo.fecha_creacion,
            fecha_actualizacion=articulo.fecha_actualizacion
        )

def migrate_articulos_backward(apps, schema_editor):
    ProductosArticulo = apps.get_model('productos', 'Articulo')
    ProductosArticulo.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('productos', '0001_initial'),
        ('core', '0002_alter_articulo_unique_together_and_more'),
    ]

    operations = [
        migrations.RunPython(disable_foreign_key_checks),
        migrations.RunPython(
            migrate_articulos_forward,
            migrate_articulos_backward
        ),
        migrations.RunPython(enable_foreign_key_checks),
    ] 