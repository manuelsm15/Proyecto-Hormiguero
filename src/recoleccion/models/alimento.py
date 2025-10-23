"""
Modelo que representa un alimento disponible en el entorno
para ser recolectado por las hormigas.
"""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Alimento:
    """
    Modelo que representa un alimento disponible en el entorno.
    
    Attributes:
        id: Identificador único del alimento
        nombre: Nombre descriptivo del alimento
        cantidad_hormigas_necesarias: Número de hormigas requeridas para recolectar
        puntos_stock: Puntos de stock que vale el alimento
        tiempo_recoleccion: Tiempo en segundos para recolectar
        disponible: Si el alimento está disponible para recolección
        fecha_creacion: Fecha y hora de creación del alimento
    """
    
    id: str
    nombre: str
    cantidad_hormigas_necesarias: int
    puntos_stock: int
    tiempo_recoleccion: int  # en segundos
    disponible: bool = True
    fecha_creacion: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """Validaciones post-inicialización."""
        if self.cantidad_hormigas_necesarias <= 0:
            raise ValueError("La cantidad de hormigas necesarias debe ser mayor a 0")
        if self.puntos_stock <= 0:
            raise ValueError("Los puntos de stock deben ser mayores a 0")
        if self.tiempo_recoleccion <= 0:
            raise ValueError("El tiempo de recolección debe ser mayor a 0")
    
    def marcar_como_recolectado(self) -> None:
        """Marca el alimento como recolectado."""
        self.disponible = False
    
    def __str__(self) -> str:
        return (
            f"Alimento(id='{self.id}', nombre='{self.nombre}', "
            f"hormigas_necesarias={self.cantidad_hormigas_necesarias}, "
            f"puntos_stock={self.puntos_stock}, disponible={self.disponible})"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
