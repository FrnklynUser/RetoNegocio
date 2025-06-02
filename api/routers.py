from rest_framework.routers import DefaultRouter
from api.views.empresa_view import EmpresaViewSet
from api.views.sucursal_view import SucursalViewSet
from api.views.pedido_view import PedidoViewSet
from api.views.canal_cliente_view import CanalClienteViewSet
from api.views.cliente_view import ClienteViewSet
from api.views.linea_producto_view import LineaProductoViewSet
from api.views.producto_view import ProductoViewSet
from api.views.promocion_view import PromocionViewSet
from api.views.condicion_promocion_view import CondicionPromocionViewSet
from api.views.beneficio_promocion_view import BeneficioPromocionViewSet

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'sucursales', SucursalViewSet)
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'canales', CanalClienteViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'lineas', LineaProductoViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'promociones', PromocionViewSet)
router.register(r'condiciones', CondicionPromocionViewSet)
router.register(r'beneficios', BeneficioPromocionViewSet)


urlpatterns = router.urls