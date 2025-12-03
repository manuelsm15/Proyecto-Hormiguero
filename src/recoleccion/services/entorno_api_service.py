"""
Implementación del servicio de entorno que se conecta a la API REST
del Subsistema de Generación de Entorno.
"""

import httpx
from typing import List, Optional
from enum import Enum

from ..models.alimento import Alimento
from .entorno_service import EntornoService


class EstadoRecurso(str, Enum):
    """Estados posibles de un recurso según la especificación del entorno."""
    DISPONIBLE = "disponible"
    EN_PROCESO = "en_proceso"
    RECOLECTADO = "recolectado"


class TipoRecurso(str, Enum):
    """Tipos de recursos según la especificación del entorno."""
    FRUTA = "fruta"
    SEMILLA = "semilla"
    HOJA = "hoja"
    NECTAR = "nectar"
    INSECTO = "insecto"
    OTRO = "otro"


class EntornoAPIService(EntornoService):
    """
    Implementación del servicio de entorno que se conecta a la API REST.
    
    Se conecta al Subsistema de Generación de Entorno usando los endpoints:
    - GET /resources: Listar recursos (con filtros opcionales)
    - GET /resources/{id}: Obtener recurso por ID
    - PUT /resources/{id}: Actualizar recurso
    """
    
    def __init__(self, base_url: str = "http://localhost:8001", timeout: int = 30):
        """
        Inicializa el servicio de API del entorno.
        
        Args:
            base_url: URL base del subsistema de entorno (por defecto localhost:8001)
            timeout: Timeout en segundos para las peticiones HTTP
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        self._disponible = True
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[dict]:
        """
        Realiza una petición HTTP al subsistema de entorno.
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint relativo (ej: /resources)
            **kwargs: Argumentos adicionales para httpx
            
        Returns:
            Respuesta JSON como diccionario o None si hay error
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = await self.client.request(method, url, **kwargs)
            
            # Verificar disponibilidad del servicio
            if response.status_code >= 500:
                self._disponible = False
                return None
            
            self._disponible = True
            
            if response.status_code == 404:
                return None
            
            if response.status_code in [200, 201]:
                return response.json()
            
            # Para otros códigos, retornar None
            return None
            
        except (httpx.TimeoutException, httpx.ConnectError, httpx.RequestError) as e:
            self._disponible = False
            return None
        except Exception as e:
            self._disponible = False
            return None
    
    def _mapear_recurso_a_alimento(self, recurso: dict) -> Alimento:
        """
        Mapea un recurso del entorno a un Alimento del subsistema de recolección.
        
        Según la especificación del entorno:
        - ID (Integer) -> id (str)
        - ID zona (Integer) -> (no se usa directamente)
        - Nombre -> nombre
        - Tipo (Enum) -> (se usa para validación)
        - Cantidad unitaria -> (no se mapea directamente, se usa para stock)
        - Peso -> (no se mapea directamente)
        - Duración recolección -> tiempo_recoleccion
        - Cantidad requerida de hormigas -> cantidad_hormigas_necesarias
        - Estado -> disponible (disponible=True si estado="disponible")
        
        Args:
            recurso: Diccionario con los datos del recurso del entorno
            
        Returns:
            Instancia de Alimento
        """
        # Mapear estado del recurso a disponible
        estado = recurso.get("estado", "disponible")
        disponible = estado == "disponible"
        
        # Mapear campos
        alimento = Alimento(
            id=str(recurso.get("id", "")),
            nombre=recurso.get("nombre", ""),
            cantidad_hormigas_necesarias=recurso.get("cantidad_requerida_hormigas", 1),
            puntos_stock=recurso.get("cantidad_unitaria", 0),
            tiempo_recoleccion=recurso.get("duracion_recoleccion", 0),
            disponible=disponible
        )
        
        return alimento
    
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
        # Construir parámetros de consulta
        params = {}
        if zona_id is not None:
            params["zona_id"] = zona_id
        if estado:
            params["estado"] = estado
        
        # Si no se especifica estado, filtrar solo disponibles
        if estado is None:
            params["estado"] = "disponible"
        
        # Intentar múltiples rutas posibles para compatibilidad
        endpoints_a_probar = ["/resources", "/api/resources", "/entorno/resources"]
        response = None
        
        for endpoint in endpoints_a_probar:
            response = await self._make_request("GET", endpoint, params=params)
            if response is not None:
                break
        
        if response is None:
            return []
        
        # Si la respuesta es una lista
        if isinstance(response, list):
            alimentos = []
            for recurso in response:
                try:
                    alimento = self._mapear_recurso_a_alimento(recurso)
                    alimentos.append(alimento)
                except Exception:
                    # Si hay error al mapear un recurso, continuar con el siguiente
                    continue
            return alimentos
        
        # Si es un diccionario, convertirlo a lista
        if isinstance(response, dict):
            try:
                alimento = self._mapear_recurso_a_alimento(response)
                return [alimento]
            except Exception:
                return []
        
        return []
    
    async def consultar_alimento_por_id(self, alimento_id: str) -> Optional[Alimento]:
        """
        Consulta un alimento específico por su ID.
        
        Args:
            alimento_id: ID del alimento a consultar
            
        Returns:
            Alimento encontrado o None si no existe
        """
        # Hacer petición GET /resources/{id}
        response = await self._make_request("GET", f"/resources/{alimento_id}")
        
        if response is None:
            return None
        
        try:
            return self._mapear_recurso_a_alimento(response)
        except Exception:
            return None
    
    async def marcar_alimento_como_recolectado(
        self, 
        alimento_id: str,
        cantidad_recolectada: Optional[int] = None
    ) -> bool:
        """
        Marca un alimento como recolectado y actualiza su estado en el entorno.
        
        Según la especificación:
        - Si cantidad llega a 0, estado = "recolectado"
        - Si cantidad > 0 pero < cantidad_unitaria, estado = "en_proceso"
        
        Args:
            alimento_id: ID del alimento recolectado
            cantidad_recolectada: Cantidad que se recolectó (opcional)
            
        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        # Primero obtener el recurso actual
        recurso_actual = await self._make_request("GET", f"/resources/{alimento_id}")
        if recurso_actual is None:
            return False
        
        # Calcular nueva cantidad
        cantidad_unitaria_actual = recurso_actual.get("cantidad_unitaria", 0)
        
        if cantidad_recolectada is None:
            # Si no se especifica, asumir que se recolectó todo
            nueva_cantidad = 0
        else:
            nueva_cantidad = max(0, cantidad_unitaria_actual - cantidad_recolectada)
        
        # Determinar nuevo estado
        if nueva_cantidad == 0:
            nuevo_estado = "recolectado"
        elif nueva_cantidad < cantidad_unitaria_actual:
            nuevo_estado = "en_proceso"
        else:
            nuevo_estado = "disponible"
        
        # Preparar payload para actualización
        payload = {
            "estado": nuevo_estado,
            "cantidad_unitaria": nueva_cantidad
        }
        
        # Hacer petición PUT /resources/{id}
        response = await self._make_request(
            "PUT", 
            f"/resources/{alimento_id}",
            json=payload
        )
        
        return response is not None
    
    async def is_disponible(self) -> bool:
        """
        Verifica si el servicio de entorno está disponible.
        
        Returns:
            True si está disponible, False en caso contrario
        """
        # Intentar hacer una petición simple para verificar disponibilidad
        try:
            # Usar endpoint de salud si está disponible, o listar recursos
            response = await self._make_request("GET", "/resources", params={"limit": 1})
            return self._disponible and response is not None
        except Exception:
            return False
    
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
    
    async def __aenter__(self):
        """Context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cierra el cliente HTTP."""
        await self.client.aclose()

