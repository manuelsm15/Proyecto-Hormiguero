"""
Interfaz para la comunicación con el subsistema de Entorno.
Permite consultar alimentos disponibles y actualizar su estado.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.alimento import Alimento


class EntornoService(ABC):
    """
    Interfaz abstracta para la comunicación con el subsistema de Entorno.
    """
    
    @abstractmethod
    async def consultar_alimentos_disponibles(self) -> List[Alimento]:
        """
        Consulta todos los alimentos disponibles en el entorno.
        
        Returns:
            Lista de alimentos disponibles
        """
        pass
    
    @abstractmethod
    async def consultar_alimento_por_id(self, alimento_id: str) -> Optional[Alimento]:
        """
        Consulta un alimento específico por su ID.
        
        Args:
            alimento_id: ID del alimento a consultar
            
        Returns:
            Alimento encontrado o None si no existe
        """
        pass
    
    @abstractmethod
    async def marcar_alimento_como_recolectado(self, alimento_id: str) -> bool:
        """
        Marca un alimento como recolectado y actualiza su estado en el entorno.
        
        Args:
            alimento_id: ID del alimento recolectado
            
        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    async def is_disponible(self) -> bool:
        """
        Verifica si el servicio de entorno está disponible.
        
        Returns:
            True si está disponible, False en caso contrario
        """
        pass
