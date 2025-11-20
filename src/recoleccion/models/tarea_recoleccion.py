"""
Modelo que representa una tarea de recolección específica.
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional

from .alimento import Alimento
from .hormiga import Hormiga
from .estado_tarea import EstadoTarea


@dataclass
class TareaRecoleccion:
    """
    Modelo que representa una tarea de recolección específica.
    
    Attributes:
        id: Identificador único de la tarea
        alimento: Alimento a recolectar
        hormigas_asignadas: Lista de hormigas asignadas a la tarea
        hormigas_lote_id: ID del lote de hormigas que se usa para iniciar la tarea
        estado: Estado actual de la tarea
        fecha_inicio: Fecha y hora de inicio de la tarea
        fecha_fin: Fecha y hora de finalización de la tarea
        alimento_recolectado: Cantidad de alimento recolectado
    """
    
    id: str
    alimento: Alimento
    hormigas_asignadas: List[Hormiga] = field(default_factory=list)
    hormigas_lote_id: Optional[str] = None
    estado: EstadoTarea = EstadoTarea.PENDIENTE
    fecha_inicio: datetime = None
    fecha_fin: datetime = None
    alimento_recolectado: int = 0
    
    def __post_init__(self) -> None:
        """Validaciones post-inicialización."""
        if self.alimento_recolectado < 0:
            raise ValueError("El alimento recolectado no puede ser negativo")
    
    def agregar_hormiga(self, hormiga: Hormiga) -> None:
        """
        Agrega una hormiga a la tarea.
        
        Args:
            hormiga: Hormiga a agregar
        """
        if hormiga is not None:
            self.hormigas_asignadas.append(hormiga)
    
    def tiene_suficientes_hormigas(self) -> bool:
        """
        Verifica si la tarea tiene suficientes hormigas asignadas.
        
        Returns:
            True si tiene suficientes hormigas, False en caso contrario
        """
        return len(self.hormigas_asignadas) >= self.alimento.cantidad_hormigas_necesarias
    
    def todas_las_hormigas_vivas(self) -> bool:
        """
        Verifica si todas las hormigas asignadas están vivas.
        
        Returns:
            True si todas están vivas, False si alguna ha muerto
        """
        return all(hormiga.is_viva() for hormiga in self.hormigas_asignadas)
    
    def iniciar_tarea(self) -> None:
        """Inicia la tarea de recolección."""
        if self.estado != EstadoTarea.PENDIENTE:
            raise ValueError("Solo se pueden iniciar tareas en estado PENDIENTE")
        
        if not self.tiene_suficientes_hormigas():
            raise ValueError("No se puede iniciar la tarea sin suficientes hormigas")
        
        self.estado = EstadoTarea.EN_PROCESO
        self.fecha_inicio = datetime.now()
    
    def completar_tarea(self, cantidad_recolectada: int) -> None:
        """
        Completa la tarea de recolección.
        
        Args:
            cantidad_recolectada: Cantidad de alimento recolectado
        """
        if self.estado != EstadoTarea.EN_PROCESO:
            raise ValueError("Solo se pueden completar tareas en estado EN_PROCESO")
        
        self.alimento_recolectado = cantidad_recolectada
        self.estado = EstadoTarea.COMPLETADA
        self.fecha_fin = datetime.now()
    
    def pausar_tarea(self) -> None:
        """Pausa la tarea por falta de hormigas vivas."""
        if self.estado != EstadoTarea.EN_PROCESO:
            raise ValueError("Solo se pueden pausar tareas en estado EN_PROCESO")
        
        self.estado = EstadoTarea.PAUSADA
    
    def __str__(self) -> str:
        return (
            f"TareaRecoleccion(id='{self.id}', alimento='{self.alimento.nombre}', "
            f"hormigas={len(self.hormigas_asignadas)}, estado={self.estado.value}, "
            f"recolectado={self.alimento_recolectado})"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
