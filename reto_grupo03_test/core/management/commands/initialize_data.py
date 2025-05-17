from django.core.management.base import BaseCommand
from core.models import TipoIdentificacion, CanalCliente, CondicionVenta, Empresa, GrupoProveedor, LineaArticulo, SubLineaArticulo
from promociones.models import TipoPromocion

class Command(BaseCommand):
    help = 'Initialize basic data for the application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Initializing basic data...')

        # Crear tipos de identificación
        self.stdout.write('Creating identification types...')
        TipoIdentificacion.objects.get_or_create(codigo='DNI', defaults={'descripcion': 'DNI'})
        TipoIdentificacion.objects.get_or_create(codigo='RUC', defaults={'descripcion': 'RUC'})

        # Crear canales de cliente
        self.stdout.write('Creating customer channels...')
        CanalCliente.objects.get_or_create(codigo='MAY', defaults={'descripcion': 'MAYORISTA'})
        CanalCliente.objects.get_or_create(codigo='MIN', defaults={'descripcion': 'MINORISTA'})

        # Crear condiciones de venta
        self.stdout.write('Creating sales conditions...')
        CondicionVenta.objects.get_or_create(codigo='CON', defaults={'descripcion': 'CONTADO'})
        CondicionVenta.objects.get_or_create(codigo='CRE', defaults={'descripcion': 'CRÉDITO'})

        # Crear empresa demo
        self.stdout.write('Creating demo company...')
        Empresa.objects.get_or_create(
            codigo='EMP001',
            defaults={
                'nombre': 'Empresa Demo S.A.',
                'ruc': '20123456789',
                'direccion': 'Av. Principal 123',
                'telefono': '01-234-5678',
                'email': 'contacto@empresademo.com'
            }
        )

        # Crear grupo de proveedor demo
        self.stdout.write('Creating provider groups...')
        grupo_prov, _ = GrupoProveedor.objects.get_or_create(
            codigo='GP001',
            defaults={'descripcion': 'Grupo Proveedor 1'}
        )

        # Crear línea de artículo demo
        self.stdout.write('Creating article lines...')
        linea_art, _ = LineaArticulo.objects.get_or_create(
            codigo='LA001',
            defaults={'descripcion': 'Línea Artículo 1'}
        )

        # Crear sublínea de artículo demo
        self.stdout.write('Creating article sub-lines...')
        SubLineaArticulo.objects.get_or_create(
            codigo='SLA001',
            defaults={
                'descripcion': 'Sublínea Artículo 1',
                'linea_articulo': linea_art
            }
        )

        # Crear tipos de promoción
        self.stdout.write('Creating promotion types...')
        TipoPromocion.objects.get_or_create(
            codigo=TipoPromocion.VOLUMEN,
            defaults={'descripcion': 'Promoción por Volumen'}
        )
        TipoPromocion.objects.get_or_create(
            codigo=TipoPromocion.MONTO,
            defaults={'descripcion': 'Promoción por Monto'}
        )

        self.stdout.write(self.style.SUCCESS('Successfully initialized basic data')) 