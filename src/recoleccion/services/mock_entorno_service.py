"""
Implementación mock del servicio de entorno para pruebas.
"""

from typing import List, Optional
from ..models.alimento import Alimento
from .entorno_service import EntornoService


class MockEntornoService(EntornoService):
    """
    Implementación mock del servicio de entorno.
    """
    
    def __init__(self):
        """Inicializa el servicio mock."""
        self.alimentos = []
        self.disponible = True
        self._cargar_datos_iniciales()
    
    def _cargar_datos_iniciales(self):
        """Carga datos iniciales para las pruebas."""
        self.alimentos = [
            Alimento(
                id="A1",
                nombre="Fruta",
                cantidad_hormigas_necesarias=3,
                puntos_stock=10,
                tiempo_recoleccion=300,
                disponible=True
            ),
            Alimento(
                id="A2",
                nombre="Semilla",
                cantidad_hormigas_necesarias=2,
                puntos_stock=5,
                tiempo_recoleccion=180,
                disponible=True
            ),
            Alimento(
                id="A3",
                nombre="Hoja",
                cantidad_hormigas_necesarias=1,
                puntos_stock=3,
                tiempo_recoleccion=120,
                disponible=True
            )
        ]
    
    async def consultar_alimentos_disponibles(
        self, 
        zona_id: Optional[int] = None,
        estado: Optional[str] = None
    ) -> List[Alimento]:
        """
        Consulta todos los alimentos disponibles.
        
        Args:
            zona_id: ID de zona para filtrar (opcional, no implementado en mock)
            estado: Estado para filtrar (opcional: "disponible", "en_proceso", "recolectado")
        """
        alimentos_filtrados = self.alimentos
        
        # Filtrar por estado
        if estado == "disponible":
            alimentos_filtrados = [a for a in alimentos_filtrados if a.disponible]
        elif estado == "en_proceso" or estado == "recolectado":
            alimentos_filtrados = [a for a in alimentos_filtrados if not a.disponible]
        elif estado is None:
            # Por defecto, solo disponibles
            alimentos_filtrados = [a for a in alimentos_filtrados if a.disponible]
        
        # Nota: zona_id no se implementa en mock ya que Alimento no tiene zona_id
        return alimentos_filtrados
    
    async def consultar_alimento_por_id(self, alimento_id: str) -> Optional[Alimento]:
        """Consulta un alimento específico por ID."""
        return next((alimento for alimento in self.alimentos if alimento.id == alimento_id), None)
    
    async def marcar_alimento_como_recolectado(
        self, 
        alimento_id: str,
        cantidad_recolectada: Optional[int] = None
    ) -> bool:
        """
        Marca un alimento como recolectado.
        
        Args:
            alimento_id: ID del alimento recolectado
            cantidad_recolectada: Cantidad que se recolectó (opcional, no usado en mock)
        """
        alimento = await self.consultar_alimento_por_id(alimento_id)
        if alimento:
            alimento.marcar_como_recolectado()
            return True
        return False
    
    async def is_disponible(self) -> bool:
        """Verifica si el servicio está disponible."""
        return self.disponible
    
    def set_disponible(self, disponible: bool):
        """Establece la disponibilidad del servicio."""
        self.disponible = disponible
    
    def agregar_alimento(self, alimento: Alimento):
        """Agrega un alimento al entorno."""
        self.alimentos.append(alimento)
    
    def limpiar_alimentos(self):
        """Limpia todos los alimentos."""
        self.alimentos.clear()
        self._cargar_datos_iniciales()
