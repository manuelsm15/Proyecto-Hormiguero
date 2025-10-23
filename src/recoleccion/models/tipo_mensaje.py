"""
Enum que define los tipos de mensajes que pueden intercambiarse entre subsistemas.
"""

from enum import Enum


class TipoMensaje(Enum):
    """
    Tipos de mensajes que pueden intercambiarse entre subsistemas.
    """
    
    # Solicitud de información de alimentos disponibles
    SOLICITAR_ALIMENTOS = "solicitar_alimentos"
    
    # Respuesta con lista de alimentos disponibles
    RESPUESTA_ALIMENTOS = "respuesta_alimentos"
    
    # Solicitud de hormigas para recolección
    SOLICITAR_HORMIGAS_RECOLECCION = "solicitar_hormigas_recoleccion"
    
    # Respuesta con hormigas asignadas
    RESPUESTA_HORMIGAS_RECOLECCION = "respuesta_hormigas_recoleccion"
    
    # Devolución de hormigas y alimento recolectado
    DEVOLVER_HORMIGAS_RECOLECCION = "devolver_hormigas_recoleccion"
    
    # Confirmación de recepción
    CONFIRMACION = "confirmacion"
    
    # Error en el procesamiento
    ERROR = "error"
