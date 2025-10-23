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
    
    async def consultar_alimentos_disponibles(self) -> List[Alimento]:
        """
        Consulta los alimentos disponibles en el entorno.
        
        Returns:
            Lista de alimentos disponibles
            
        Raises:
            Exception: Si el servicio de entorno no está disponible
        """
        if not await self.entorno_service.is_disponible():
            raise Exception("Servicio de entorno no disponible")
        
        return await self.entorno_service.consultar_alimentos_disponibles()
    
    async def crear_tarea_recoleccion(self, tarea_id: str, alimento: Alimento) -> TareaRecoleccion:
        """
        Crea una nueva tarea de recolección.
        
        Args:
            tarea_id: Identificador único de la tarea
            alimento: Alimento a recolectar
            
        Returns:
            Tarea de recolección creada
        """
        tarea = TareaRecoleccion(id=tarea_id, alimento=alimento)
        self.tareas_activas.append(tarea)
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
    
    async def asignar_hormigas_a_tarea(self, tarea: TareaRecoleccion, hormigas: List[Hormiga]) -> None:
        """
        Asigna hormigas a una tarea de recolección.
        
        Args:
            tarea: Tarea a la que asignar las hormigas
            hormigas: Lista de hormigas a asignar
        """
        for hormiga in hormigas:
            tarea.agregar_hormiga(hormiga)
            hormiga.cambiar_estado(EstadoHormiga.DISPONIBLE)
    
    async def iniciar_tarea_recoleccion(self, tarea: TareaRecoleccion) -> None:
        """
        Inicia una tarea de recolección con timer en tiempo real.
        
        Args:
            tarea: Tarea a iniciar
            
        Raises:
            ValueError: Si la tarea no puede ser iniciada
        """
        if not tarea.tiene_suficientes_hormigas():
            raise ValueError("No se puede iniciar la tarea sin suficientes hormigas")
        
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
        
        # Mover tarea a completadas
        self.tareas_activas.remove(tarea)
        self.tareas_completadas.append(tarea)
    
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
            # 1. Consultar alimentos disponibles
            alimentos = await self.consultar_alimentos_disponibles()
            
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
                    continue
                
                # 4. Asignar hormigas a la tarea
                await self.asignar_hormigas_a_tarea(tarea, hormigas)
                
                # 5. Iniciar tarea
                await self.iniciar_tarea_recoleccion(tarea)
                
                # 6. Simular proceso de recolección
                await asyncio.sleep(0.1)  # Simulación de tiempo de recolección
                
                # 7. Completar tarea
                await self.completar_tarea_recoleccion(tarea, alimento.puntos_stock)
                
                # 8. Devolver hormigas
                await self.devolver_hormigas(hormigas, alimento.puntos_stock)
                
                # 9. Marcar alimento como recolectado en el entorno
                await self.entorno_service.marcar_alimento_como_recolectado(alimento.id)
                
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
