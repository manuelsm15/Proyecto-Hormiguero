"""
Implementación del servicio de comunicación que se conecta a la API REST
del Subsistema de Comunicación y Hormiga Reina.
"""

import httpx
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.hormiga import Hormiga
from ..models.mensaje import Mensaje
from ..models.tipo_mensaje import TipoMensaje
from ..models.estado_hormiga import EstadoHormiga
from .comunicacion_service import ComunicacionService


class ComunicacionAPIService(ComunicacionService):
    """
    Implementación del servicio de comunicación que se conecta a la API REST.
    
    Se conecta al Subsistema de Comunicación y Hormiga Reina usando los endpoints:
    - POST /messages: Crear/enviar mensajes
    - GET /messages/{id}: Consultar mensaje por ID
    - POST /ants/request: Solicitar hormigas
    - GET /ants/response/{message_id}: Consultar respuesta de hormigas
    - POST /ants/return: Devolver hormigas
    """
    
    def __init__(self, base_url: str = "http://localhost:8002", timeout: int = 30):
        """
        Inicializa el servicio de API de comunicación.
        
        Args:
            base_url: URL base del subsistema de comunicación/reina (por defecto localhost:8002)
            timeout: Timeout en segundos para las peticiones HTTP
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        self._disponible = True
        self.subsistema_id = "recoleccion"  # ID del subsistema de recolección
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[dict]:
        """
        Realiza una petición HTTP al subsistema de comunicación.
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint relativo (ej: /messages)
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
    
    def _mapear_hormiga_api_a_modelo(self, hormiga_data: dict) -> Hormiga:
        """
        Mapea los datos de una hormiga de la API al modelo Hormiga.
        
        Args:
            hormiga_data: Diccionario con los datos de la hormiga de la API
            
        Returns:
            Instancia de Hormiga
        """
        return Hormiga(
            id=str(hormiga_data.get("id", "")),
            capacidad_carga=hormiga_data.get("capacidad_carga", 5),
            estado=EstadoHormiga.DISPONIBLE,  # Por defecto disponible
            tiempo_vida=hormiga_data.get("tiempo_vida", 3600),
            subsistema_origen=hormiga_data.get("subsistema_origen", "hormiga_reina")
        )
    
    async def enviar_mensaje(self, mensaje: Mensaje) -> str:
        """
        Envía un mensaje al subsistema de comunicación.
        
        Args:
            mensaje: Mensaje a enviar
            
        Returns:
            ID del mensaje enviado
        """
        payload = {
            "tipo": mensaje.tipo.value,
            "contenido": mensaje.contenido,
            "subsistema_origen": mensaje.subsistema_origen,
            "subsistema_destino": mensaje.subsistema_destino,
            "ttl": mensaje.ttl
        }
        
        # Hacer petición POST /messages o equivalente
        response = await self._make_request(
            "POST",
            "/messages",
            json=payload
        )
        
        if response:
            mensaje_id = response.get("id") or response.get("message_id")
            if mensaje_id:
                mensaje.id = mensaje_id
                return mensaje_id
        
        # Si no hay respuesta válida, generar un ID local
        import time
        mensaje_id = f"msg_{int(time.time() * 1000)}"
        mensaje.id = mensaje_id
        return mensaje_id
    
    async def consultar_mensaje(self, mensaje_id: str) -> Optional[Mensaje]:
        """
        Consulta un mensaje por su ID.
        
        Args:
            mensaje_id: ID del mensaje a consultar
            
        Returns:
            Mensaje encontrado o None si no existe
        """
        # Hacer petición GET /messages/{id} o equivalente
        response = await self._make_request("GET", f"/messages/{mensaje_id}")
        
        if response is None:
            return None
        
        try:
            return Mensaje(
                id=response.get("id", mensaje_id),
                tipo=TipoMensaje(response.get("tipo", "confirmacion")),
                contenido=response.get("contenido", {}),
                subsistema_origen=response.get("subsistema_origen", ""),
                subsistema_destino=response.get("subsistema_destino", ""),
                fecha_creacion=datetime.fromisoformat(response.get("fecha_creacion", datetime.now().isoformat())),
                ttl=response.get("ttl", 60),
                procesado=response.get("procesado", False)
            )
        except Exception:
            return None
    
    async def solicitar_hormigas(self, cantidad_hormigas: int, subsistema_destino: str = "recoleccion") -> str:
        """
        Solicita hormigas para recolección al subsistema de Hormiga Reina.
        
        Args:
            cantidad_hormigas: Cantidad de hormigas solicitadas
            subsistema_destino: Subsistema que solicita las hormigas (por defecto "recoleccion")
            
        Returns:
            ID del mensaje de solicitud
        """
        # Crear mensaje de solicitud
        mensaje = Mensaje(
            id="",  # Se asignará en enviar_mensaje
            tipo=TipoMensaje.SOLICITAR_HORMIGAS_RECOLECCION,
            contenido={
                "cantidad": cantidad_hormigas,
                "subsistema": subsistema_destino
            },
            subsistema_origen=subsistema_destino,
            subsistema_destino="hormiga_reina"
        )
        
        # Intentar usar endpoint específico para solicitar hormigas
        payload = {
            "cantidad": cantidad_hormigas,
            "subsistema_destino": subsistema_destino,
            "subsistema_origen": subsistema_destino
        }
        
        response = await self._make_request(
            "POST",
            "/ants/request",  # O endpoint equivalente
            json=payload
        )
        
        if response:
            mensaje_id = response.get("id") or response.get("message_id") or response.get("mensaje_id")
            if mensaje_id:
                mensaje.id = mensaje_id
                return mensaje_id
        
        # Si no hay endpoint específico, usar enviar_mensaje
        return await self.enviar_mensaje(mensaje)
    
    async def consultar_respuesta_hormigas(self, mensaje_id: str) -> List[Hormiga]:
        """
        Consulta la respuesta de una solicitud de hormigas.
        
        Args:
            mensaje_id: ID del mensaje de solicitud
            
        Returns:
            Lista de hormigas asignadas o lista vacía si no hay respuesta
        """
        # Intentar consultar endpoint específico
        response = await self._make_request("GET", f"/ants/response/{mensaje_id}")
        
        if response is None:
            # Si no hay respuesta, consultar el mensaje directamente
            mensaje = await self.consultar_mensaje(mensaje_id)
            if mensaje and mensaje.procesado:
                # Extraer hormigas del contenido del mensaje
                hormigas_data = mensaje.contenido.get("hormigas", [])
                if isinstance(hormigas_data, list):
                    return [self._mapear_hormiga_api_a_modelo(h) for h in hormigas_data]
            return []
        
        # Procesar respuesta
        hormigas_data = response.get("hormigas", [])
        if isinstance(hormigas_data, list):
            return [self._mapear_hormiga_api_a_modelo(h) for h in hormigas_data]
        
        return []
    
    async def devolver_hormigas(self, hormigas: List[Hormiga], alimento_recolectado: int) -> str:
        """
        Devuelve hormigas al subsistema de Hormiga Reina con el alimento recolectado.
        
        Args:
            hormigas: Lista de hormigas a devolver
            alimento_recolectado: Cantidad de alimento recolectado
            
        Returns:
            ID del mensaje de devolución
        """
        # Crear mensaje de devolución
        mensaje = Mensaje(
            id="",  # Se asignará en enviar_mensaje
            tipo=TipoMensaje.DEVOLVER_HORMIGAS_RECOLECCION,
            contenido={
                "hormigas": [
                    {
                        "id": h.id,
                        "capacidad_carga": h.capacidad_carga,
                        "tiempo_vida": h.tiempo_vida,
                        "estado": h.estado.value
                    } for h in hormigas
                ],
                "alimento_recolectado": alimento_recolectado
            },
            subsistema_origen="recoleccion",
            subsistema_destino="hormiga_reina"
        )
        
        # Intentar usar endpoint específico para devolver hormigas
        payload = {
            "hormigas": [
                {
                    "id": h.id,
                    "capacidad_carga": h.capacidad_carga,
                    "tiempo_vida": h.tiempo_vida,
                    "estado": h.estado.value
                } for h in hormigas
            ],
            "alimento_recolectado": alimento_recolectado,
            "subsistema_origen": "recoleccion"
        }
        
        response = await self._make_request(
            "POST",
            "/ants/return",  # O endpoint equivalente
            json=payload
        )
        
        if response:
            mensaje_id = response.get("id") or response.get("message_id") or response.get("mensaje_id")
            if mensaje_id:
                mensaje.id = mensaje_id
                return mensaje_id
        
        # Si no hay endpoint específico, usar enviar_mensaje
        return await self.enviar_mensaje(mensaje)
    
    async def is_disponible(self) -> bool:
        """
        Verifica si el servicio de comunicación está disponible.
        
        Returns:
            True si está disponible, False en caso contrario
        """
        # Intentar hacer una petición simple para verificar disponibilidad
        try:
            # Usar endpoint de salud si está disponible
            response = await self._make_request("GET", "/health")
            if response is None:
                # Intentar con endpoint alternativo
                response = await self._make_request("GET", "/")
            return self._disponible and response is not None
        except Exception:
            return False
    
    async def __aenter__(self):
        """Context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cierra el cliente HTTP."""
        await self.client.aclose()



