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
    async def consultar_alimentos_disponibles(
        self, 
        zona_id: Optional[int] = None,
        estado: Optional[str] = None
    ) -> List[Alimento]:
        """
        Consulta todos los alimentos disponibles en el entorno.
        
        Args:
            zona_id: ID de zona para filtrar (opcional)
            estado: Estado para filtrar (opcional: "disponible", "en_proceso", "recolectado")
        
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
    async def marcar_alimento_como_recolectado(
        self, 
        alimento_id: str,
        cantidad_recolectada: Optional[int] = None
    ) -> bool:
        """
        Marca un alimento como recolectado y actualiza su estado en el entorno.
        
        Args:
            alimento_id: ID del alimento recolectado
            cantidad_recolectada: Cantidad que se recolectó (opcional)
            
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
    
    async def consultar_recursos_por_zona(self, zona_id: int) -> List[Alimento]:
        """
        Consulta todos los recursos de una zona específica.
        
        Args:
            zona_id: ID de la zona
            
        Returns:
            Lista de alimentos en esa zona
        """
        return await self.consultar_alimentos_disponibles(zona_id=zona_id)
    
    async def consultar_recursos_por_estado(self, estado: str) -> List[Alimento]:
        """
        Consulta recursos filtrados por estado.
        
        Args:
            estado: Estado del recurso ("disponible", "en_proceso", "recolectado")
            
        Returns:
            Lista de alimentos con ese estado
        """
        return await self.consultar_alimentos_disponibles(estado=estado)

