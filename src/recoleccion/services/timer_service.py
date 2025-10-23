"""
Servicio de tiempo real para gestión de estados de tareas.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Optional
from ..models.tarea_recoleccion import TareaRecoleccion, EstadoTarea
from ..models.hormiga import EstadoHormiga
import logging

logger = logging.getLogger(__name__)


class TimerService:
    """
    Servicio para manejar el tiempo real de las tareas de recolección.
    """
    
    def __init__(self):
        """Inicializa el servicio de tiempo."""
        self.tareas_en_proceso: Dict[str, TareaRecoleccion] = {}
        self.timer_tasks: Dict[str, asyncio.Task] = {}
        self.callbacks: List[Callable] = []
        self._running = False
    
    def add_callback(self, callback: Callable):
        """Agrega un callback para notificar cambios de estado."""
        self.callbacks.append(callback)
    
    async def _notify_callbacks(self, tarea: TareaRecoleccion, evento: str):
        """Notifica a todos los callbacks registrados."""
        for callback in self.callbacks:
            try:
                await callback(tarea, evento)
            except Exception as e:
                logger.error(f"Error en callback: {e}")
    
    async def iniciar_tarea_timer(self, tarea: TareaRecoleccion) -> bool:
        """
        Inicia el timer para una tarea de recolección.
        
        Args:
            tarea: Tarea a procesar
            
        Returns:
            True si se inició correctamente, False si ya está en proceso
            
        Raises:
            ValueError: Si la tarea no tiene suficientes hormigas
        """
        if tarea.id in self.tareas_en_proceso:
            return False
        
        # Validar que la tarea tenga suficientes hormigas
        if not tarea.tiene_suficientes_hormigas():
            raise ValueError("No se puede iniciar la tarea sin suficientes hormigas")
        
        # Cambiar estado a EN_PROCESO
        tarea.estado = EstadoTarea.EN_PROCESO
        tarea.fecha_inicio = datetime.now()
        
        # Cambiar estado de hormigas a RECOLECTANDO
        for hormiga in tarea.hormigas_asignadas:
            hormiga.cambiar_estado(EstadoHormiga.RECOLECTANDO)
        
        # Registrar tarea
        self.tareas_en_proceso[tarea.id] = tarea
        
        # Crear timer task
        timer_task = asyncio.create_task(
            self._procesar_tarea_timer(tarea)
        )
        self.timer_tasks[tarea.id] = timer_task
        
        # Notificar inicio
        await self._notify_callbacks(tarea, "iniciada")
        
        logger.info(f"Timer iniciado para tarea {tarea.id} - Duración: {tarea.alimento.tiempo_recoleccion}s")
        return True
    
    async def _procesar_tarea_timer(self, tarea: TareaRecoleccion):
        """
        Procesa el timer de una tarea.
        
        Args:
            tarea: Tarea a procesar
        """
        try:
            # Esperar el tiempo de recolección
            await asyncio.sleep(tarea.alimento.tiempo_recoleccion)
            
            # Completar la tarea
            await self._completar_tarea(tarea)
            
        except asyncio.CancelledError:
            logger.info(f"Timer cancelado para tarea {tarea.id}")
        except Exception as e:
            logger.error(f"Error en timer de tarea {tarea.id}: {e}")
        finally:
            # Limpiar
            self.tareas_en_proceso.pop(tarea.id, None)
            self.timer_tasks.pop(tarea.id, None)
    
    async def _completar_tarea(self, tarea: TareaRecoleccion):
        """
        Completa una tarea automáticamente.
        
        Args:
            tarea: Tarea a completar
        """
        # Cambiar estado a COMPLETADA
        tarea.estado = EstadoTarea.COMPLETADA
        tarea.fecha_fin = datetime.now()
        tarea.alimento_recolectado = tarea.alimento.puntos_stock
        
        # Cambiar estado de hormigas a TRANSPORTANDO
        for hormiga in tarea.hormigas_asignadas:
            hormiga.cambiar_estado(EstadoHormiga.TRANSPORTANDO)
        
        # Notificar finalización
        await self._notify_callbacks(tarea, "completada")
        
        logger.info(f"Tarea {tarea.id} completada - Alimento recolectado: {tarea.alimento_recolectado}")
    
    async def cancelar_tarea(self, tarea_id: str) -> bool:
        """
        Cancela una tarea en proceso.
        
        Args:
            tarea_id: ID de la tarea a cancelar
            
        Returns:
            True si se canceló correctamente, False si no estaba en proceso
        """
        if tarea_id not in self.timer_tasks:
            return False
        
        # Cancelar timer
        timer_task = self.timer_tasks[tarea_id]
        timer_task.cancel()
        
        # Obtener tarea
        tarea = self.tareas_en_proceso.get(tarea_id)
        if tarea:
            # Cambiar estado a PAUSADA
            tarea.estado = EstadoTarea.PAUSADA
            
            # Cambiar estado de hormigas a DISPONIBLE
            for hormiga in tarea.hormigas_asignadas:
                hormiga.cambiar_estado(EstadoHormiga.DISPONIBLE)
            
            # Notificar cancelación
            await self._notify_callbacks(tarea, "cancelada")
        
        # Limpiar
        self.tareas_en_proceso.pop(tarea_id, None)
        self.timer_tasks.pop(tarea_id, None)
        
        logger.info(f"Tarea {tarea_id} cancelada")
        return True
    
    def get_tareas_en_proceso(self) -> List[TareaRecoleccion]:
        """Obtiene todas las tareas que están en proceso."""
        return list(self.tareas_en_proceso.values())
    
    def get_tiempo_restante(self, tarea_id: str) -> Optional[int]:
        """
        Obtiene el tiempo restante de una tarea en segundos.
        
        Args:
            tarea_id: ID de la tarea
            
        Returns:
            Tiempo restante en segundos, None si no está en proceso
        """
        tarea = self.tareas_en_proceso.get(tarea_id)
        if not tarea or not tarea.fecha_inicio:
            return None
        
        tiempo_transcurrido = (datetime.now() - tarea.fecha_inicio).total_seconds()
        tiempo_restante = tarea.alimento.tiempo_recoleccion - tiempo_transcurrido
        
        return max(0, int(tiempo_restante))
    
    def get_progreso(self, tarea_id: str) -> Optional[float]:
        """
        Obtiene el progreso de una tarea como porcentaje (0-100).
        
        Args:
            tarea_id: ID de la tarea
            
        Returns:
            Progreso como porcentaje, None si no está en proceso
        """
        tarea = self.tareas_en_proceso.get(tarea_id)
        if not tarea or not tarea.fecha_inicio:
            return None
        
        tiempo_transcurrido = (datetime.now() - tarea.fecha_inicio).total_seconds()
        progreso = (tiempo_transcurrido / tarea.alimento.tiempo_recoleccion) * 100
        
        return min(100.0, max(0.0, progreso))
    
    async def cleanup(self):
        """Limpia todos los timers activos."""
        for task in self.timer_tasks.values():
            task.cancel()
        
        self.tareas_en_proceso.clear()
        self.timer_tasks.clear()
        
        logger.info("Timer service cleanup completado")


# Instancia global del servicio de tiempo
timer_service = TimerService()
