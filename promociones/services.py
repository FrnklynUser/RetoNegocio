from decimal import Decimal
from typing import List, Dict, Tuple
from datetime import date
from .models import Promocion, ArticuloPromocion, TipoPromocion

class PromocionService:
    @staticmethod
    def calcular_bonificaciones(
        canal_cliente_id: int,
        items: List[Dict[str, any]]  # [{'articulo_id': int, 'cantidad': int, 'precio': Decimal}]
    ) -> List[Dict[str, any]]:  # returns [{'articulo_id': int, 'cantidad': int}]
        """
        Calcula las bonificaciones aplicables según las promociones vigentes.
        """
        # Obtener promociones activas para el canal
        promociones = Promocion.objects.filter(
            canal_cliente_id=canal_cliente_id,
            activo=True,
            fecha_inicio__lte=date.today(),
            fecha_fin__gte=date.today()
        ).prefetch_related('articulos')
        
        bonificaciones = []
        
        for promocion in promociones:
            if promocion.tipo_promocion.codigo == TipoPromocion.VOLUMEN:
                bonif = PromocionService._procesar_promocion_volumen(promocion, items)
                if bonif:
                    bonificaciones.extend(bonif)
            
            elif promocion.tipo_promocion.codigo == TipoPromocion.MONTO:
                bonif = PromocionService._procesar_promocion_monto(promocion, items)
                if bonif:
                    bonificaciones.extend(bonif)
        
        return PromocionService._consolidar_bonificaciones(bonificaciones)
    
    @staticmethod
    def _procesar_promocion_volumen(promocion: Promocion, items: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Procesa una promoción por volumen y retorna las bonificaciones aplicables.
        """
        bonificaciones = []
        
        # Obtener artículos principales y de bonificación de la promoción
        articulos_principales = list(promocion.articulos.filter(es_bonificacion=False).values_list('articulo_id', flat=True))
        articulos_bonificacion = list(promocion.articulos.filter(es_bonificacion=True))
        
        if not articulos_principales or not articulos_bonificacion:
            return []
        
        # Verificar si los items cumplen con la cantidad mínima
        cantidad_total = sum(
            item['cantidad'] 
            for item in items 
            if item['articulo_id'] in articulos_principales
        )
        
        if cantidad_total >= promocion.cantidad_minima:
            # Calcular cuántas veces se aplica la promoción
            veces_aplicable = cantidad_total // promocion.cantidad_minima
            
            # Aplicar bonificaciones
            for art_bonif in articulos_bonificacion:
                bonificaciones.append({
                    'articulo_id': art_bonif.articulo_id,
                    'cantidad': art_bonif.cantidad_bonificacion * veces_aplicable
                })
        
        return bonificaciones
    
    @staticmethod
    def _procesar_promocion_monto(promocion: Promocion, items: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Procesa una promoción por monto y retorna las bonificaciones aplicables.
        """
        bonificaciones = []
        
        # Obtener artículos principales y de bonificación de la promoción
        articulos_principales = list(promocion.articulos.filter(es_bonificacion=False).values_list('articulo_id', flat=True))
        articulos_bonificacion = list(promocion.articulos.filter(es_bonificacion=True))
        
        if not articulos_principales or not articulos_bonificacion:
            return []
        
        # Calcular monto total de los artículos principales
        monto_total = sum(
            Decimal(str(item['cantidad'])) * Decimal(str(item['precio']))
            for item in items
            if item['articulo_id'] in articulos_principales
        )
        
        if monto_total >= promocion.monto_minimo:
            # Calcular cuántas veces se aplica la promoción
            veces_aplicable = int(monto_total // promocion.monto_minimo)
            
            # Aplicar bonificaciones
            for art_bonif in articulos_bonificacion:
                bonificaciones.append({
                    'articulo_id': art_bonif.articulo_id,
                    'cantidad': art_bonif.cantidad_bonificacion * veces_aplicable
                })
        
        return bonificaciones
    
    @staticmethod
    def _consolidar_bonificaciones(bonificaciones: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Consolida las bonificaciones por artículo sumando las cantidades.
        """
        consolidado = {}
        for bonif in bonificaciones:
            art_id = bonif['articulo_id']
            if art_id in consolidado:
                consolidado[art_id]['cantidad'] += bonif['cantidad']
            else:
                consolidado[art_id] = bonif.copy()
        
        return list(consolidado.values()) 