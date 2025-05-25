from django.core.management.base import BaseCommand
from core.models import Empresa, GrupoProveedor, LineaArticulo, CanalCliente, Vendedor
import pandas as pd

class Command(BaseCommand):
    help = 'Import data from Excel files'

    def handle(self, *args, **kwargs):
        # Import Empresas
        empresa, _ = Empresa.objects.get_or_create(
            codigo='EMP001',
            defaults={
                'nombre': 'Default Empresa',
                'ruc': '12345678901',
                'direccion': 'Default Address',
                'email': 'default@empresa.com',
                'telefono': '123456789',
                'estado': True
            }
        )

        # Import Grupos
        try:
            df_grupos = pd.read_excel('core/data/TemplateImportarGrupos.xlsx')  # Updated path
            for _, row in df_grupos.iterrows():
                GrupoProveedor.objects.get_or_create(
                    grupo_id=row['grupo_id'],
                    defaults={
                        'empresa': empresa,
                        'codigo': row['codigo'],
                        'nombre': row['nombre'],
                        'estado': row['estado']
                    }
                )
            self.stdout.write(self.style.SUCCESS('Grupos imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing Grupos: {e}'))

        # Import Lineas
        try:
            df_lineas = pd.read_excel('core/data/TemplateImportarLineas.xlsx')  # Updated path
            for _, row in df_lineas.iterrows():
                grupo = GrupoProveedor.objects.get(grupo_id=row['grupo_id'])
                LineaArticulo.objects.get_or_create(
                    linea_id=row['linea_id'],
                    empresa=empresa,
                    grupo=grupo,
                    codigo=row['codigo'],
                    nombre=row['nombre'],
                    estado=row['estado']
                )
            self.stdout.write(self.style.SUCCESS('Lineas imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing Lineas: {e}'))

        # Import Articulos
        try:
            df_articulos = pd.read_excel('core/data/template_articulos.xlsx')  # Updated path
            for _, row in df_articulos.iterrows():
                grupo = GrupoProveedor.objects.get(grupo_id=row['grupo_id'])
                linea = LineaArticulo.objects.get(linea_id=row['linea_id'])
                LineaArticulo.objects.get_or_create(
                    articulo_id=row['articulo_id'],
                    empresa=empresa,
                    codigo_articulo=row['codigo_articulo'],
                    codigo_barras=row.get('codigo_barras', None),
                    codigo_ean=row.get('codigo_ean', None),
                    descripcion=row['descripcion'],
                    grupo=grupo,
                    linea=linea,
                    unidad_medida=row['unidad_medida'],
                    unidad_compra=row['unidad_compra'],
                    unidad_reparto=row['unidad_reparto'],
                    unidad_bonificacion=row['unidad_bonificacion'],
                    factor_reparto=row['factor_reparto'],
                    factor_compra=row['factor_compra'],
                    factor_bonificacion=row['factor_bonificacion'],
                    tipo_afectacion=row['tipo_afectacion'],
                    peso=row['peso'],
                    tipo_producto=row['tipo_producto'],
                    afecto_retencion=row.get('afecto_retencion', False),
                    afecto_detraccion=row.get('afecto_detraccion', False),
                    precio=row.get('precio', 0.00)
                )
            self.stdout.write(self.style.SUCCESS('Articulos imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing Articulos: {e}'))

        # Import Vendedores
        try:
            df_vendedores = pd.read_excel('core/data/TemplateVendedores.xlsx')  # Updated path
            canal, _ = CanalCliente.objects.get_or_create(nombre='Default Canal')
            for _, row in df_vendedores.iterrows():
                Vendedor.objects.get_or_create(
                    tipo_identificacion=row['tipo_identificacion_id'],
                    nro_documento=row['nro_documento'],
                    nombres=row['nombres'],
                    direccion=row.get('direccion', None),
                    nro_movil=row.get('nro_movil', None),
                    canal=canal,
                    supervisor=row.get('supervisor', None),
                    correo_electronico=row.get('correo_electronico', None),
                    territorio=row.get('territorio', None),
                    rol=row['rol_id']
                )
            self.stdout.write(self.style.SUCCESS('Vendedores imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing Vendedores: {e}'))

        self.stdout.write(self.style.SUCCESS('All data imported successfully'))