"""
Enum que define los posibles estados de una hormiga durante el proceso de recolección.
"""

from enum import Enum


class EstadoHormiga(Enum):
    """
    Estados posibles de una hormiga durante el proceso de recolección.
    """
    
    # Hormiga disponible para asignar a una tarea
    DISPONIBLE = "disponible"
    
    # Hormiga buscando alimento en el entorno
    BUSCANDO = "buscando"
    
    # Hormiga recolectando alimento específico
    RECOLECTANDO = "recolectando"
    
    # Hormiga transportando alimento al hormiguero
    TRANSPORTANDO = "transportando"
    
    # Hormiga muerta o inactiva
    MUERTA = "muerta"

