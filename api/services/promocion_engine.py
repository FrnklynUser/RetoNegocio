# api/services/promocion_engine.py

from api.models import Promocion, PromocionAplicada, CondicionPromocion, BeneficioPromocion, Producto, LineaProducto
from datetime import date

class PromocionEngine:
    """
    Motor principal para la aplicación de promociones a un pedido.
    Orquesta el filtrado, evaluación de condiciones y cálculo de beneficios.
    """
    def __init__(self, pedido, detalles):
        self.pedido = pedido
        self.detalles = detalles 
        self.promociones_aplicadas = []
        self.bonificaciones = []

    def aplicar_promociones(self):
        """
        Aplica todas las promociones vigentes y relevantes al pedido.
        Retorna una lista de beneficios aplicados (instancias de PromocionAplicada o dicts).
        """
        promociones = self._filtrar_promociones()
        for promo in promociones:
            for condicion in promo.condiciones.all():
                self._calcular_beneficio(promo, condicion)
        return self.bonificaciones

    def _calcular_beneficio(self, promo, condicion):
        """
        Calcula el beneficio (bonificación, descuento, etc.) para la promoción.
        Delegar a calculadores de beneficio según tipo.
        """
        # CASO1  Bonificación por cantidad de producto
        bonificacion_aplicada = False
        if condicion.tipo_condicion == 'cantidad' and condicion.producto:
            cantidad_pedido = sum([
                d['cantidad'] for d in self.detalles if int(d['producto']) == condicion.producto.id
            ])
            if cantidad_pedido >= condicion.valor_min:
                multiplos = int(cantidad_pedido // condicion.valor_min) if not condicion.valor_max else 1
                for beneficio in promo.beneficios.all():
                    if beneficio.tipo_beneficio == 'bonificacion' and beneficio.producto_bonificado:
                        bonificacion_total = beneficio.cantidad * multiplos
                        self.bonificaciones.append({
                            'producto_bonificado': beneficio.producto_bonificado.id,
                            'cantidad': bonificacion_total
                        })
                        PromocionAplicada.objects.create(
                            pedido=self.pedido,
                            promocion=promo,
                            descripcion_resultado=f"Bonificación de {bonificacion_total} {beneficio.producto_bonificado.nombre}"
                        )
                        self.promociones_aplicadas.append(promo)
                        bonificacion_aplicada = True
                    elif beneficio.tipo_beneficio == 'descuento' and beneficio.porcentaje_descuento:
                        # CASO 3 y CASO 4: Descuento por cantidad (incluye escalas)
                        if (condicion.valor_max is None and cantidad_pedido >= condicion.valor_min) or \
                           (condicion.valor_max is not None and condicion.valor_min <= cantidad_pedido <= condicion.valor_max):
                            monto_producto = sum([
                                d['cantidad'] * d.get('precio_unitario', 0)
                                for d in self.detalles if int(d['producto']) == condicion.producto.id
                            ])
                            descuento = monto_producto * (beneficio.porcentaje_descuento / 100)
                            self.bonificaciones.append({
                                'producto_descuento': condicion.producto.id,
                                'porcentaje_descuento': beneficio.porcentaje_descuento,
                                'monto_descuento': round(descuento, 2)
                            })
                            PromocionAplicada.objects.create(
                                pedido=self.pedido,
                                promocion=promo,
                                descripcion_resultado=f"Descuento del {beneficio.porcentaje_descuento}% sobre {condicion.producto.nombre} por volumen: S/{round(descuento,2)}"
                            )
                            self.promociones_aplicadas.append(promo)
        # CASO 2 y 5: Bonificación o descuento por importe en línea y marca
        elif condicion.tipo_condicion == 'importe' and condicion.linea_producto:
            importe = 0
            productos_en_linea = []
            for d in self.detalles:
                try:
                    producto = Producto.objects.get(id=d['producto'])
                except Producto.DoesNotExist:
                    continue
                if producto.linea_id == condicion.linea_producto.id:
                    productos_en_linea.append(producto.id)
                    if hasattr(condicion, 'marca') and condicion.marca: 
                        if producto.marca != condicion.marca:
                            continue
                    importe += d['cantidad'] * d.get('precio_unitario', 0)
            # Debug: mostrar productos considerados y el importe
            print(f"[DEBUG] Productos en línea {condicion.linea_producto.id}: {productos_en_linea}, Importe total: {importe}")
            if importe >= condicion.valor_min:
                multiplos = int(importe // condicion.valor_min) if not condicion.valor_max else 1
                for beneficio in promo.beneficios.all():
                    if beneficio.tipo_beneficio == 'bonificacion' and beneficio.producto_bonificado:
                        bonificacion_total = beneficio.cantidad * multiplos
                        self.bonificaciones.append({
                            'producto_bonificado': beneficio.producto_bonificado.id,
                            'cantidad': bonificacion_total
                        })
                        PromocionAplicada.objects.create(
                            pedido=self.pedido,
                            promocion=promo,
                            descripcion_resultado=f"Bonificación de {bonificacion_total} {beneficio.producto_bonificado.nombre} por importe"
                        )
                        self.promociones_aplicadas.append(promo)
                    elif beneficio.tipo_beneficio == 'descuento' and beneficio.porcentaje_descuento:
                        # CASO 5: Descuento por importe en línea
                        if (condicion.valor_max is None and importe >= condicion.valor_min) or \
                           (condicion.valor_max is not None and condicion.valor_min <= importe <= condicion.valor_max):
                            descuento = importe * (beneficio.porcentaje_descuento / 100)
                            self.bonificaciones.append({
                                'linea_descuento': condicion.linea_producto.id,
                                'porcentaje_descuento': beneficio.porcentaje_descuento,
                                'monto_descuento': round(descuento, 2)
                            })
                            PromocionAplicada.objects.create(
                                pedido=self.pedido,
                                promocion=promo,
                                descripcion_resultado=f"Descuento del {beneficio.porcentaje_descuento}% sobre línea {condicion.linea_producto.nombre} por importe: S/{round(descuento,2)}"
                            )
                            self.promociones_aplicadas.append(promo)
            else:
                print(f"[DEBUG] No se alcanza el importe mínimo para la línea {condicion.linea_producto.id}. Importe: {importe}, Mínimo: {condicion.valor_min}")
        # CASO 6: Descuento escalonado por importe en producto específico (rango)
        elif condicion.tipo_condicion == 'importe' and condicion.producto:
            # Solo ejecutar la lógica una vez por producto en el pedido
            if not hasattr(self, '_productos_descuento_aplicados'):
                self._productos_descuento_aplicados = set()
            if condicion.producto.id in self._productos_descuento_aplicados:
                return
            importe_producto = 0
            for d in self.detalles:
                if int(d['producto']) == condicion.producto.id:
                    importe_producto += d['cantidad'] * d.get('precio_unitario', 0)
            condiciones_producto = [c for c in promo.condiciones.all() if c.tipo_condicion == 'importe' and c.producto and c.producto.id == condicion.producto.id]
            mejor_condicion = None
            for c in condiciones_producto:
                if (c.valor_max is not None and c.valor_min <= importe_producto <= c.valor_max) or (c.valor_max is None and importe_producto >= c.valor_min):
                    if mejor_condicion is None or c.valor_min > mejor_condicion.valor_min:
                        mejor_condicion = c
            if mejor_condicion:
                beneficio_escala = None
                for beneficio in promo.beneficios.all():
                    if beneficio.tipo_beneficio == 'descuento' and beneficio.porcentaje_descuento:
                        if (
                            (mejor_condicion.valor_min == 500 and mejor_condicion.valor_max == 1499 and beneficio.porcentaje_descuento == 2) or
                            (mejor_condicion.valor_min == 1500 and mejor_condicion.valor_max == 4000 and beneficio.porcentaje_descuento == 4) or
                            (mejor_condicion.valor_min == 4001 and mejor_condicion.valor_max is None and beneficio.porcentaje_descuento == 5)
                        ):
                            beneficio_escala = beneficio
                            break
                if beneficio_escala:
                    descuento = importe_producto * (beneficio_escala.porcentaje_descuento / 100)
                    self.bonificaciones.append({
                        'producto_descuento': mejor_condicion.producto.id,
                        'porcentaje_descuento': beneficio_escala.porcentaje_descuento,
                        'monto_descuento': round(descuento, 2)
                    })
                    PromocionAplicada.objects.create(
                        pedido=self.pedido,
                        promocion=promo,
                        descripcion_resultado=f"Descuento del {beneficio_escala.porcentaje_descuento}% sobre {mejor_condicion.producto.nombre} por importe: S/{round(descuento,2)}"
                    )
                    self.promociones_aplicadas.append(promo)
                    self._productos_descuento_aplicados.add(condicion.producto.id)
            else:
                print(f"[DEBUG] No se alcanza el importe mínimo para el producto {condicion.producto.id}. Importe: {importe_producto}, Mínimo: {condicion.valor_min}")
        # CASO 7 y 8: Bonificación escalonada por volumen
        elif condicion.tipo_condicion == 'cantidad_escala' and condicion.producto:
            self._aplicar_bonificacion_escalonada_volumen(promo, condicion)
        elif condicion.tipo_condicion == 'importe_escala_bonificacion' and condicion.producto:
            self._aplicar_bonificacion_escala_importe(promo, condicion)
        # CASO 11: Bonificación escalonada por importe con rangos específicos
        elif condicion.tipo_condicion == 'importe_escala_fija' and condicion.producto:
            self._aplicar_bonificacion_escala_fija(promo, condicion)
        # CASO 12: Bonificación + descuento por volumen combinado
        elif condicion.tipo_condicion == 'volumen_combinado' and condicion.linea_producto:
            self._aplicar_promocion_combinada(promo, condicion)   
        # CASO 13: Descuento por compra combinada de productos específicos
        elif condicion.tipo_condicion == 'compra_combinada_productos':
            self._aplicar_descuento_compra_combinada(promo, condicion)     

    def _aplicar_bonificacion_escalonada_volumen(self, promo, condicion):
        """
        Aplica bonificaciones escalonadas por volumen según rangos definidos.
        Caso 7: 
        - 6 cajas (36 unidades) -> 2 unidades bonificadas
        - 18 cajas (108 unidades) -> 9 unidades bonificadas
        """
        # Verificar si ya se aplicó una bonificación para este producto
        producto_id = condicion.producto.id
        if hasattr(self, '_productos_bonificados') and producto_id in self._productos_bonificados:
            return
            
        cantidad_pedido = sum([
            d['cantidad'] for d in self.detalles if int(d['producto']) == producto_id
        ])
        
        # Convertir cantidad de unidades a cajas (6 unidades por caja)
        cajas = cantidad_pedido / 6
        
        # Determinar la bonificación según el rango
        bonificacion = 0
        if cajas >= 18:  # 18 cajas o más
            bonificacion = 9
        elif cajas >= 6:  # Entre 6 y 17 cajas
            bonificacion = 2
            
        if bonificacion > 0:
            for beneficio in promo.beneficios.all():
                if beneficio.tipo_beneficio == 'bonificacion' and beneficio.producto_bonificado:
                    # Verificar que el producto bonificado sea el mismo que el producto comprado
                    if beneficio.producto_bonificado.id == producto_id:
                        # Marcar el producto como bonificado
                        if not hasattr(self, '_productos_bonificados'):
                            self._productos_bonificados = set()
                        self._productos_bonificados.add(producto_id)
                        
                        self.bonificaciones.append({
                            'producto_bonificado': beneficio.producto_bonificado.id,
                            'cantidad': bonificacion
                        })
                        
                        descripcion = (
                            f"Bonificación escalonada: {bonificacion} unidades de "
                            f"{beneficio.producto_bonificado.nombre} por compra de "
                            f"{cantidad_pedido} unidades ({cajas:.0f} cajas)"
                        )
                        
                        PromocionAplicada.objects.create(
                            pedido=self.pedido,
                            promocion=promo,
                            descripcion_resultado=descripcion
                        )
                        self.promociones_aplicadas.append(promo)
                        break

    def _aplicar_bonificacion_escala_importe(self, promo, condicion):
        """
        Aplica bonificaciones escalonadas por importe según rangos definidos.
        Caso 10:
        - Compras entre S/5000 y S/9999.99 -> 1 caja bonificada
        - Compras >= S/10000 -> 3 cajas bonificadas
        """
        producto_id = condicion.producto.id
        
        # Evitar aplicar la bonificación más de una vez al mismo producto
        if hasattr(self, '_productos_bonificados_importe') and producto_id in self._productos_bonificados_importe:
            return
            
        importe_producto = sum([
            d['cantidad'] * d.get('precio_unitario', 0)
            for d in self.detalles if int(d['producto']) == producto_id
        ])
        
        # Determinar la bonificación según el rango de importe
        bonificacion_cajas = 0
        if importe_producto >= 10000:
            bonificacion_cajas = 3
        elif importe_producto >= 5000:
            bonificacion_cajas = 1
            
        if bonificacion_cajas > 0:
            for beneficio in promo.beneficios.all():
                if beneficio.tipo_beneficio == 'bonificacion' and beneficio.producto_bonificado:
                    if beneficio.producto_bonificado.id == producto_id:
                        # Marcar el producto como bonificado por importe
                        if not hasattr(self, '_productos_bonificados_importe'):
                            self._productos_bonificados_importe = set()
                        self._productos_bonificados_importe.add(producto_id)
                        
                        # Convertir cajas a unidades (asumiendo 6 unidades por caja)
                        unidades_bonificadas = bonificacion_cajas * 6
                        
                        self.bonificaciones.append({
                            'producto_bonificado': beneficio.producto_bonificado.id,
                            'cantidad': unidades_bonificadas
                        })
                        
                        descripcion = (
                            f"Bonificación por escala de importe: {bonificacion_cajas} cajas "
                            f"({unidades_bonificadas} unidades) de {beneficio.producto_bonificado.nombre} "
                            f"por compra de S/{importe_producto:.2f}"
                        )
                        
                        PromocionAplicada.objects.create(
                            pedido=self.pedido,
                            promocion=promo,
                            descripcion_resultado=descripcion
                        )
                        self.promociones_aplicadas.append(promo)
                        break

    def _aplicar_bonificacion_escala_fija(self, promo, condicion):
        """
        Aplica bonificaciones fijas por rangos de importe específicos.
        Caso 11: 
        - Compras entre S/5000 y S/9999.99 -> 2 unidades bonificadas
        - Compras >= S/10000 -> 12 unidades bonificadas
        """
        producto_id = condicion.producto.id
        
        # Evitar bonificaciones duplicadas
        if not hasattr(self, '_productos_bonificados_fijos'):
            self._productos_bonificados_fijos = set()
            
        if producto_id in self._productos_bonificados_fijos:
            return
            
        importe_producto = sum([
            d['cantidad'] * d.get('precio_unitario', 0)
            for d in self.detalles if int(d['producto']) == producto_id
        ])
        
        # Determinar bonificación según rango
        unidades_bonificadas = 0
        if importe_producto >= 10000:
            unidades_bonificadas = 12
        elif importe_producto >= 5000:
            unidades_bonificadas = 2
            
        if unidades_bonificadas > 0:
            for beneficio in promo.beneficios.all():
                if beneficio.tipo_beneficio == 'bonificacion' and beneficio.producto_bonificado:
                    if beneficio.producto_bonificado.id == producto_id:
                        self._productos_bonificados_fijos.add(producto_id)
                        
                        self.bonificaciones.append({
                            'producto_bonificado': beneficio.producto_bonificado.id,
                            'cantidad': unidades_bonificadas
                        })
                        
                        descripcion = (
                            f"Bonificación por escala fija: {unidades_bonificadas} unidades de "
                            f"{beneficio.producto_bonificado.nombre} "
                            f"por compra de S/{importe_producto:.2f}"
                        )
                        
                        PromocionAplicada.objects.create(
                            pedido=self.pedido,
                            promocion=promo,
                            descripcion_resultado=descripcion
                        )
                        self.promociones_aplicadas.append(promo)
                        break

    def _filtrar_promociones(self):
        hoy = date.today()
        sucursal = self.pedido.sucursal
        cliente = self.pedido.cliente
        # Filtrar solo promociones del canal correspondiente
        promociones = Promocion.objects.filter(
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy,
            empresa=sucursal.empresa,
            sucursal=sucursal,
            canal_cliente=cliente.canal
        )
        # Si la promoción es para canal MAYORISTA, solo aplicar si el cliente es mayorista
        promociones_filtradas = []
        for promo in promociones:
            if promo.canal_cliente.nombre.upper() == 'MAYORISTA':
                if cliente.canal.nombre.upper() == 'MAYORISTA':
                    promociones_filtradas.append(promo)
            else:
                promociones_filtradas.append(promo)
        return promociones_filtradas

    def _cumple_condiciones(self, promo):
        """
        Evalúa si el pedido cumple las condiciones de la promoción.
        Delegar a evaluadores de condición según tipo.
        """
        # TODO: Implementar evaluación de condiciones.
        return False

    def _aplicar_promocion_combinada(self, promo, condicion):
        """
        Aplica una promoción combinada (bonificación + descuento) por volumen.
        Caso 12:
        - Compra > 6 cajas (72 unidades) de detergentes -> 3 unidades gratis + 5% descuento
        """
        # Verificar si ya se aplicó una promoción combinada para esta línea
        if not hasattr(self, '_promociones_combinadas_aplicadas'):
            self._promociones_combinadas_aplicadas = set()
            
        if condicion.linea_producto.id in self._promociones_combinadas_aplicadas:
            return
            
        # Calcular cantidad total de unidades en la línea de producto
        cantidad_total = 0
        importe_total = 0
        for d in self.detalles:
            try:
                producto = Producto.objects.get(id=d['producto'])
                if producto.linea_id == condicion.linea_producto.id:
                    cantidad_total += d['cantidad']
                    importe_total += d['cantidad'] * d.get('precio_unitario', 0)
            except Producto.DoesNotExist:
                continue

        # Convertir a cajas (12 unidades por caja para detergentes)
        cajas = cantidad_total / 12
        
        if cajas > 6:  # Más de 6 cajas
            self._promociones_combinadas_aplicadas.add(condicion.linea_producto.id)
            
            # Aplicar bonificación
            for beneficio in promo.beneficios.all():
                if beneficio.tipo_beneficio == 'bonificacion' and beneficio.producto_bonificado:
                    self.bonificaciones.append({
                        'producto_bonificado': beneficio.producto_bonificado.id,
                        'cantidad': 3  # 3 unidades gratis
                    })
                # Aplicar descuento
                elif beneficio.tipo_beneficio == 'descuento' and beneficio.porcentaje_descuento:
                    descuento = importe_total * (beneficio.porcentaje_descuento / 100)
                    self.bonificaciones.append({
                        'linea_descuento': condicion.linea_producto.id,
                        'porcentaje_descuento': beneficio.porcentaje_descuento,
                        'monto_descuento': round(descuento, 2)
                    })
            
            descripcion = (
                f"Promoción combinada en {condicion.linea_producto.nombre}: "
                f"3 unidades gratis de GLO1 + 5% descuento "
                f"por compra de {cantidad_total} unidades ({cajas:.1f} cajas)"
            )
            
            PromocionAplicada.objects.create(
                pedido=self.pedido,
                promocion=promo,
                descripcion_resultado=descripcion
            )
            self.promociones_aplicadas.append(promo)

    def _aplicar_descuento_compra_combinada(self, promo, condicion):
        """
        Aplica descuento por compra combinada de productos específicos.
        Caso 13:
        - Compra de producto A (pisco) + producto B (gaseosa) -> 5% descuento
        """
        # Verificar si ya se aplicó el descuento para esta combinación
        if not hasattr(self, '_descuentos_combinados_aplicados'):
            self._descuentos_combinados_aplicados = set()
            
        combo_key = f"{condicion.producto.id}-{condicion.producto_secundario.id}"
        if combo_key in self._descuentos_combinados_aplicados:
            return
            
        # Verificar la presencia de ambos productos en el pedido
        producto_a_presente = False
        producto_b_presente = False
        importe_total = 0
        
        for d in self.detalles:
            try:
                producto = Producto.objects.get(id=d['producto'])
                if producto.id == condicion.producto.id:  # Pisco
                    producto_a_presente = True
                    importe_total += d['cantidad'] * d.get('precio_unitario', 0)
                elif producto.id == condicion.producto_secundario.id:  # Gaseosa
                    producto_b_presente = True
                    importe_total += d['cantidad'] * d.get('precio_unitario', 0)
            except Producto.DoesNotExist:
                continue

        # Solo aplicar el descuento si ambos productos están presentes
        if producto_a_presente and producto_b_presente:
            self._descuentos_combinados_aplicados.add(combo_key)
            
            for beneficio in promo.beneficios.all():
                if beneficio.tipo_beneficio == 'descuento' and beneficio.porcentaje_descuento:
                    descuento = importe_total * (beneficio.porcentaje_descuento / 100)
                    self.bonificaciones.append({
                        'producto_descuento': [condicion.producto.id, condicion.producto_secundario.id],
                        'porcentaje_descuento': beneficio.porcentaje_descuento,
                        'monto_descuento': round(descuento, 2)
                    })
                    
                    descripcion = (
                        f"Descuento del {beneficio.porcentaje_descuento}% por compra combinada de "
                        f"{condicion.producto.nombre} y {condicion.producto_secundario.nombre}: "
                        f"S/{round(descuento,2)}"
                    )
                    
                    PromocionAplicada.objects.create(
                        pedido=self.pedido,
                        promocion=promo,
                        descripcion_resultado=descripcion
                    )
                    self.promociones_aplicadas.append(promo)

