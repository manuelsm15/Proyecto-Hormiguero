"""
Modelo que representa una hormiga asignada para tareas de recolección.
"""

from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional

from .estado_hormiga import EstadoHormiga


@dataclass
class Hormiga:
    """
    Modelo que representa una hormiga asignada para tareas de recolección.
    
    Attributes:
        id: Identificador único de la hormiga
        capacidad_carga: Capacidad máxima de carga (por defecto 5 unidades)
        estado: Estado actual de la hormiga
        tiempo_vida: Tiempo de vida en segundos
        fecha_creacion: Fecha y hora de creación de la hormiga
        subsistema_origen: Subsistema que creó la hormiga
    """
    
    id: str
    capacidad_carga: int = 5  # máximo 5 unidades por defecto
    estado: EstadoHormiga = EstadoHormiga.DISPONIBLE
    tiempo_vida: int = 3600  # 1 hora por defecto
    fecha_creacion: datetime = field(default_factory=datetime.now)
    subsistema_origen: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validaciones post-inicialización."""
        if self.capacidad_carga <= 0:
            raise ValueError("La capacidad de carga debe ser mayor a 0")
        if self.tiempo_vida <= 0:
            raise ValueError("El tiempo de vida debe ser mayor a 0")
    
    def is_viva(self) -> bool:
        """
        Verifica si la hormiga está viva basándose en su tiempo de vida.
        
        Returns:
            True si la hormiga está viva, False si ha muerto
        """
        ahora = datetime.now()
        tiempo_muerte = self.fecha_creacion + timedelta(seconds=self.tiempo_vida)
        return ahora < tiempo_muerte
    
    def cambiar_estado(self, nuevo_estado: EstadoHormiga) -> None:
        """
        Cambia el estado de la hormiga.
        
        Args:
            nuevo_estado: Nuevo estado a asignar
        """
        self.estado = nuevo_estado
    
    def __str__(self) -> str:
        return (
            f"Hormiga(id='{self.id}', estado={self.estado.value}, "
            f"capacidad_carga={self.capacidad_carga}, viva={self.is_viva()})"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
