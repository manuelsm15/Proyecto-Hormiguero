"""
Servicio principal de recolección de alimentos.
Implementa la lógica de negocio para la recolección siguiendo TDD.
"""

import asyncio
from typing import List, Optional
from datetime import datetime

from ..models.alimento import Alimento
from ..models.hormiga import Hormiga
from ..models.tarea_recoleccion import TareaRecoleccion
from ..models.estado_tarea import EstadoTarea
from ..models.estado_hormiga import EstadoHormiga
from ..models.mensaje import Mensaje
from ..models.tipo_mensaje import TipoMensaje
from .entorno_service import EntornoService
from .comunicacion_service import ComunicacionService
from .timer_service import timer_service


class RecoleccionService:
    """
    Servicio principal para la recolección de alimentos.
    
    Coordina la comunicación con los subsistemas de Entorno y Comunicación
    para gestionar el proceso completo de recolección.
    """
    
    def __init__(self, entorno_service: EntornoService, comunicacion_service: ComunicacionService):
        """
        Inicializa el servicio de recolección.
        
        Args:
            entorno_service: Servicio para comunicación con el entorno
            comunicacion_service: Servicio para comunicación entre subsistemas
        """
        self.entorno_service = entorno_service
        self.comunicacion_service = comunicacion_service
        self.tareas_activas: List[TareaRecoleccion] = []
        self.tareas_completadas: List[TareaRecoleccion] = []
        
        # Configurar callbacks del timer service
        timer_service.add_callback(self._on_tarea_completada)
    
    async def _on_tarea_completada(self, tarea: TareaRecoleccion, evento: str):
        """
        Callback para manejar eventos de tareas del timer service.
        
        Args:
            tarea: Tarea que cambió de estado
            evento: Tipo de evento (iniciada, completada, cancelada)
        """
        if evento == "completada":
            # Mover tarea de activas a completadas
            if tarea in self.tareas_activas:
                self.tareas_activas.remove(tarea)
            if tarea not in self.tareas_completadas:
                self.tareas_completadas.append(tarea)
            
            # Persistir tarea completada en BD
            try:
                from ..services.persistence_service import persistence_service
                await persistence_service.guardar_tarea(tarea)
                await persistence_service.actualizar_estado_tarea(tarea.id, tarea.estado)
                # Guardar evento de completado
                await persistence_service.guardar_evento(
                    "tarea_completada_automatica",
                    f"Tarea {tarea.id} completada automáticamente por timer",
                    {"tarea_id": tarea.id, "alimento_id": tarea.alimento.id, "cantidad": tarea.alimento_recolectado}
                )
            except Exception as e:
                print(f"Advertencia: No se pudo persistir tarea completada automáticamente en BD: {e}")
    
    async def consultar_alimentos_disponibles(
        self,
        zona_id: Optional[int] = None,
        estado: Optional[str] = None
    ) -> List[Alimento]:
        """
        Consulta los alimentos disponibles en el entorno.
        
        Args:
            zona_id: ID de zona para filtrar (opcional)
            estado: Estado para filtrar (opcional: "disponible", "en_proceso", "recolectado")
        
        Returns:
            Lista de alimentos disponibles
            
        Raises:
            Exception: Si el servicio de entorno no está disponible
        """
        if not await self.entorno_service.is_disponible():
            raise Exception("Servicio de entorno no disponible")
        
        return await self.entorno_service.consultar_alimentos_disponibles(
            zona_id=zona_id,
            estado=estado
        )
    
    async def crear_tarea_recoleccion(self, tarea_id: str, alimento: Alimento) -> TareaRecoleccion:
        """
        Crea una nueva tarea de recolección.
        
        Args:
            tarea_id: Identificador único de la tarea
            alimento: Alimento a recolectar
            
        Returns:
            Tarea de recolección creada
            
        Raises:
            ValueError: Si el alimento no está disponible
        """
        # Validar que el alimento esté disponible
        if not alimento.disponible:
            raise ValueError(f"El alimento '{alimento.nombre}' (ID: {alimento.id}) no está disponible. Estado: agotado")
        
        tarea = TareaRecoleccion(id=tarea_id, alimento=alimento)
        self.tareas_activas.append(tarea)
        
        # Persistir en base de datos
        try:
            from ..services.persistence_service import persistence_service
            await persistence_service.guardar_tarea(tarea)
        except Exception as e:
            # Si falla la persistencia, continuar sin ella
            print(f"Advertencia: No se pudo persistir la tarea: {e}")
        
        return tarea
    
    async def solicitar_hormigas(self, cantidad: int) -> List[Hormiga]:
        """
        Solicita hormigas al subsistema de Hormiga Reina.
        
        Args:
            cantidad: Cantidad de hormigas solicitadas
            
        Returns:
            Lista de hormigas asignadas
        """
        if not await self.comunicacion_service.is_disponible():
            raise Exception("Servicio de comunicación no disponible")
        
        # Solicitar hormigas
        mensaje_id = await self.comunicacion_service.solicitar_hormigas(
            cantidad, "recoleccion"
        )
        
        # Esperar respuesta (en un escenario real, esto sería asíncrono)
        await asyncio.sleep(0.1)  # Simulación de latencia
        
        # Consultar respuesta
        hormigas = await self.comunicacion_service.consultar_respuesta_hormigas(mensaje_id)
        return hormigas
    
    async def asignar_hormigas_a_tarea(
        self, 
        tarea: TareaRecoleccion, 
        hormigas: List[Hormiga], 
        lote_id: Optional[str] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Asigna hormigas a una tarea de recolección usando lotes.
        
        Args:
            tarea: Tarea a la que asignar las hormigas
            hormigas: Lista de hormigas a asignar
            lote_id: ID del lote (opcional, se genera si no se proporciona)
            
        Returns:
            Tupla (exitoso, mensaje_error)
        """
        from ..services.persistence_service import persistence_service
        
        cantidad_enviada = len(hormigas)
        cantidad_requerida = tarea.alimento.cantidad_hormigas_necesarias
        
        # Validar cantidad antes de crear el lote
        if cantidad_enviada < cantidad_requerida:
            error_msg = f"El lote tiene cantidad insuficiente de hormigas. Enviadas: {cantidad_enviada}, Requeridas: {cantidad_requerida}"
            return False, error_msg
        
        # Generar lote_id si no se proporciona
        if not lote_id:
            from datetime import datetime
            lote_id = f"LOTE_{datetime.now().strftime('%Y%m%d%H%M%S')}_{tarea.id}"
        
        # Verificar que el lote no esté en uso
        es_valido, error_msg = await persistence_service.verificar_lote_disponible(lote_id, cantidad_requerida)
        if not es_valido and error_msg and "no encontrado" not in error_msg:
            # Si el lote existe pero está en uso o tiene problemas, retornar error
            return False, error_msg
        
        # Crear el lote en la base de datos
        exito, error = await persistence_service.crear_lote_hormigas(
            lote_id, tarea.id, cantidad_enviada, cantidad_requerida
        )
        if not exito:
            return False, error or "Error desconocido al crear lote"
        
        # Aceptar el lote
        exito, error = await persistence_service.aceptar_lote_hormigas(lote_id)
        if not exito:
            return False, error or "Error desconocido al aceptar lote"
        
        # Asignar hormigas a la tarea en memoria
        for hormiga in hormigas:
            tarea.agregar_hormiga(hormiga)
            hormiga.cambiar_estado(EstadoHormiga.DISPONIBLE)
        
        # Guardar hormigas en el lote en la base de datos
        exito = await persistence_service.guardar_hormigas_en_lote(lote_id, hormigas)
        if not exito:
            return False, "Error al guardar hormigas en el lote"
        
        # Asignar lote_id a la tarea
        tarea.hormigas_lote_id = lote_id
        
        # Persistir tarea (sin hormigas_asignadas, se obtienen del lote)
        try:
            await persistence_service.guardar_tarea(tarea)
        except Exception as e:
            print(f"Advertencia: No se pudo persistir tarea: {e}")
        
        return True, None
    
    async def iniciar_tarea_recoleccion(self, tarea: TareaRecoleccion, hormigas_lote_id: Optional[str] = None) -> None:
        """
        Inicia una tarea de recolección con timer en tiempo real.
        
        Args:
            tarea: Tarea a iniciar
            hormigas_lote_id: ID opcional del lote de hormigas que se usa para iniciar la tarea.
            
        Raises:
            ValueError: Si la tarea no puede ser iniciada
        """
        from ..services.persistence_service import persistence_service
        
        if not tarea.tiene_suficientes_hormigas():
            raise ValueError("No se puede iniciar la tarea sin suficientes hormigas")
        
        # Si se proporciona un lote ID, guardarlo en la tarea
        if hormigas_lote_id is not None:
            tarea.hormigas_lote_id = hormigas_lote_id
        
        # Si hay un lote_id, validar que esté disponible y marcar como en uso
        if tarea.hormigas_lote_id:
            es_valido, error_msg = await persistence_service.verificar_lote_disponible(
                tarea.hormigas_lote_id, 
                tarea.alimento.cantidad_hormigas_necesarias
            )
            if not es_valido:
                raise ValueError(error_msg or "El lote de hormigas no está disponible")
            
            # Marcar el lote como en uso
            await persistence_service.marcar_lote_en_uso(tarea.hormigas_lote_id)
        
        # Usar timer service para manejo en tiempo real
        try:
            success = await timer_service.iniciar_tarea_timer(tarea)
            if not success:
                raise ValueError("La tarea ya está en proceso")
        except ValueError as e:
            # Re-lanzar el error del timer service
            raise e
        
        # Agregar a tareas activas si no está
        if tarea not in self.tareas_activas:
            self.tareas_activas.append(tarea)
        
        # Actualizar persistencia
        try:
            await persistence_service.guardar_tarea(tarea)
            await persistence_service.actualizar_estado_tarea(tarea.id, tarea.estado)
        except Exception as e:
            print(f"Advertencia: No se pudo actualizar la tarea en BD: {e}")
    
    async def verificar_y_completar_tarea_por_tiempo(self, tarea: TareaRecoleccion) -> bool:
        """
        Verifica si una tarea debe completarse automáticamente por tiempo transcurrido.
        
        Args:
            tarea: Tarea a verificar
            
        Returns:
            True si se completó la tarea, False si no era necesario
        """
        # Obtener estado como valor para comparar
        estado_valor = tarea.estado.value if hasattr(tarea.estado, 'value') else str(tarea.estado)
        
        # Solo verificar tareas en proceso
        if estado_valor != "en_proceso":
            return False
        
        # Debe tener fecha de inicio
        if not tarea.fecha_inicio:
            return False
        
        # Calcular tiempo transcurrido
        from datetime import datetime, timedelta
        ahora = datetime.now()
        tiempo_transcurrido = (ahora - tarea.fecha_inicio).total_seconds()
        tiempo_recoleccion = tarea.alimento.tiempo_recoleccion
        
        # Si el tiempo transcurrido es mayor o igual al tiempo de recolección, completar
        if tiempo_transcurrido >= tiempo_recoleccion:
            # Calcular fecha_fin como fecha_inicio + tiempo_recoleccion (momento exacto de finalización)
            fecha_fin_calculada = tarea.fecha_inicio + timedelta(seconds=tiempo_recoleccion)
            
            # Completar la tarea (esto establece fecha_fin = datetime.now() temporalmente)
            await self.completar_tarea_recoleccion(tarea, tarea.alimento.puntos_stock)
            
            # Sobrescribir fecha_fin con el tiempo exacto calculado (fecha_inicio + tiempo_recoleccion)
            tarea.fecha_fin = fecha_fin_calculada
            
            # Persistir nuevamente con la fecha_fin correcta
            try:
                from ..services.persistence_service import persistence_service
                await persistence_service.guardar_tarea(tarea)
            except Exception as e:
                print(f"Advertencia: No se pudo actualizar fecha_fin en BD: {e}")
            
            return True
        
        return False
    
    async def completar_tarea_recoleccion(self, tarea: TareaRecoleccion, cantidad_recolectada: int) -> None:
        """
        Completa una tarea de recolección.
        
        Args:
            tarea: Tarea a completar
            cantidad_recolectada: Cantidad de alimento recolectado
        """
        tarea.completar_tarea(cantidad_recolectada)
        
        # Cambiar estado de las hormigas a transportando
        for hormiga in tarea.hormigas_asignadas:
            hormiga.cambiar_estado(EstadoHormiga.TRANSPORTANDO)
        
        # Marcar el alimento como no disponible (agotado)
        tarea.alimento.marcar_como_recolectado()
        
        # Mover tarea a completadas
        if tarea in self.tareas_activas:
            self.tareas_activas.remove(tarea)
        if tarea not in self.tareas_completadas:
            self.tareas_completadas.append(tarea)
        
        # Persistir tarea completada y actualizar disponibilidad del alimento en BD
        try:
            from ..services.persistence_service import persistence_service
            await persistence_service.guardar_tarea(tarea)
            await persistence_service.actualizar_estado_tarea(tarea.id, tarea.estado)
            await persistence_service.actualizar_alimento_disponibilidad(tarea.alimento.id, False)
        except Exception as e:
            print(f"Advertencia: No se pudo persistir tarea completada o actualizar alimento en BD: {e}")
    
    async def devolver_hormigas(self, hormigas: List[Hormiga], alimento_recolectado: int) -> str:
        """
        Devuelve hormigas al subsistema de Hormiga Reina.
        
        Args:
            hormigas: Lista de hormigas a devolver
            alimento_recolectado: Cantidad de alimento recolectado
            
        Returns:
            ID del mensaje de devolución
        """
        if not await self.comunicacion_service.is_disponible():
            raise Exception("Servicio de comunicación no disponible")
        
        return await self.comunicacion_service.devolver_hormigas(hormigas, alimento_recolectado)
    
    async def procesar_recoleccion(self) -> List[TareaRecoleccion]:
        """
        Procesa el ciclo completo de recolección.
        
        Returns:
            Lista de tareas procesadas
        """
        tareas_procesadas = []
        
        try:
            # 1. Consultar alimentos desde BD primero; si falla o no hay, usar servicio de entorno
            alimentos = []
            try:
                from ..services.persistence_service import persistence_service
                alimentos = await persistence_service.obtener_alimentos()
            except Exception:
                alimentos = []
            if not alimentos:
                # Fallback a servicio de entorno (si estuviera configurado)
                try:
                    alimentos = await self.consultar_alimentos_disponibles()
                except Exception:
                    alimentos = []
            
            for alimento in alimentos:
                if not alimento.disponible:
                    continue
                
                # 2. Crear tarea de recolección
                tarea_id = f"tarea_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{alimento.id}"
                tarea = await self.crear_tarea_recoleccion(tarea_id, alimento)
                
                # 3. Solicitar hormigas necesarias
                hormigas = await self.solicitar_hormigas(alimento.cantidad_hormigas_necesarias)
                
                if not hormigas:
                    tarea.estado = EstadoTarea.CANCELADA
                    # Persistir estado cancelado
                    try:
                        from ..services.persistence_service import persistence_service
                        await persistence_service.actualizar_estado_tarea(tarea.id, tarea.estado)
                    except Exception:
                        pass
                    continue
                
                # 4. Asignar hormigas a la tarea (esto ya persiste en BD)
                await self.asignar_hormigas_a_tarea(tarea, hormigas)
                
                # 5. Iniciar tarea (esto ya persiste en BD)
                await self.iniciar_tarea_recoleccion(tarea)
                
                # 6. Simular proceso de recolección
                await asyncio.sleep(0.1)  # Simulación de tiempo de recolección
                
                # 7. Completar tarea (esto ya persiste en BD)
                await self.completar_tarea_recoleccion(tarea, alimento.puntos_stock)
                
                # 8. Devolver hormigas
                await self.devolver_hormigas(hormigas, alimento.puntos_stock)
                
                # 9. Intentar marcar alimento como recolectado en entorno (si disponible)
                try:
                    await self.entorno_service.marcar_alimento_como_recolectado(
                        alimento.id, 
                        cantidad_recolectada=alimento.puntos_stock
                    )
                except Exception:
                    pass
                
                # Guardar evento de procesamiento exitoso
                try:
                    from ..services.persistence_service import persistence_service
                    await persistence_service.guardar_evento(
                        "tarea_procesada",
                        f"Tarea {tarea.id} procesada exitosamente",
                        {"tarea_id": tarea.id, "alimento_id": alimento.id, "cantidad": alimento.puntos_stock}
                    )
                except Exception:
                    pass
                
                tareas_procesadas.append(tarea)
        
        except Exception as e:
            print(f"Error en el procesamiento de recolección: {e}")
        
        return tareas_procesadas
    
    async def verificar_hormigas_muertas(self) -> None:
        """
        Verifica si hay hormigas muertas en las tareas activas y las pausa si es necesario.
        """
        for tarea in self.tareas_activas:
            if tarea.estado == EstadoTarea.EN_PROCESO and not tarea.todas_las_hormigas_vivas():
                tarea.pausar_tarea()
                print(f"Tarea {tarea.id} pausada por hormigas muertas")
    
    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas del servicio de recolección.
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            "tareas_activas": len(self.tareas_activas),
            "tareas_completadas": len(self.tareas_completadas),
            "total_alimento_recolectado": sum(
                tarea.alimento_recolectado for tarea in self.tareas_completadas
            )
        }
