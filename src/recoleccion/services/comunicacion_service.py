"""
Interfaz para la comunicación con el subsistema de Comunicación.
Permite enviar y recibir mensajes entre subsistemas.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.hormiga import Hormiga
from ..models.mensaje import Mensaje


class ComunicacionService(ABC):
    """
    Interfaz abstracta para la comunicación con el subsistema de Comunicación.
    """
    
    @abstractmethod
    async def enviar_mensaje(self, mensaje: Mensaje) -> str:
        """
        Envía un mensaje al subsistema de comunicación.
        
        Args:
            mensaje: Mensaje a enviar
            
        Returns:
            ID del mensaje enviado
        """
        pass
    
    @abstractmethod
    async def consultar_mensaje(self, mensaje_id: str) -> Optional[Mensaje]:
        """
        Consulta un mensaje por su ID.
        
        Args:
            mensaje_id: ID del mensaje a consultar
            
        Returns:
            Mensaje encontrado o None si no existe
        """
        pass
    
    @abstractmethod
    async def solicitar_hormigas(self, cantidad_hormigas: int, subsistema_destino: str) -> str:
        """
        Solicita hormigas para recolección al subsistema de Hormiga Reina.
        
        Args:
            cantidad_hormigas: Cantidad de hormigas solicitadas
            subsistema_destino: Subsistema que solicita las hormigas
            
        Returns:
            ID del mensaje de solicitud
        """
        pass
    
    @abstractmethod
    async def consultar_respuesta_hormigas(self, mensaje_id: str) -> List[Hormiga]:
        """
        Consulta la respuesta de una solicitud de hormigas.
        
        Args:
            mensaje_id: ID del mensaje de solicitud
            
        Returns:
            Lista de hormigas asignadas o lista vacía si no hay respuesta
        """
        pass
    
    @abstractmethod
    async def devolver_hormigas(self, hormigas: List[Hormiga], alimento_recolectado: int) -> str:
        """
        Devuelve hormigas al subsistema de Hormiga Reina con el alimento recolectado.
        
        Args:
            hormigas: Lista de hormigas a devolver
            alimento_recolectado: Cantidad de alimento recolectado
            
        Returns:
            ID del mensaje de devolución
        """
        pass
    
    @abstractmethod
    async def is_disponible(self) -> bool:
        """
        Verifica si el servicio de comunicación está disponible.
        
        Returns:
            True si está disponible, False en caso contrario
        """
        pass
