"""
Enum que define los posibles estados de una tarea de recolección.
"""

from enum import Enum


class EstadoTarea(Enum):
    """
    Estados posibles de una tarea de recolección.
    """
    
    # Tarea creada pero no iniciada
    PENDIENTE = "pendiente"
    
    # Tarea en proceso de asignación de hormigas
    ASIGNANDO_HORMIGAS = "asignando_hormigas"
    
    # Tarea en ejecución con hormigas trabajando
    EN_PROCESO = "en_proceso"
    
    # Tarea completada exitosamente
    COMPLETADA = "completada"
    
    # Tarea cancelada o fallida
    CANCELADA = "cancelada"
    
    # Tarea pausada por falta de hormigas vivas
    PAUSADA = "pausada"

