"""
Implementación mock del servicio de comunicación para pruebas.
"""

from typing import List, Optional, Dict
from ..models.hormiga import Hormiga
from ..models.mensaje import Mensaje
from ..models.tipo_mensaje import TipoMensaje
from .comunicacion_service import ComunicacionService


class MockComunicacionService(ComunicacionService):
    """
    Implementación mock del servicio de comunicación.
    """
    
    def __init__(self):
        """Inicializa el servicio mock."""
        self.mensajes: Dict[str, Mensaje] = {}
        self.respuestas_hormigas: Dict[str, List[Hormiga]] = {}
        self.disponible = True
        self.contador_mensajes = 0
    
    async def enviar_mensaje(self, mensaje: Mensaje) -> str:
        """Envía un mensaje al subsistema de comunicación."""
        self.contador_mensajes += 1
        mensaje_id = f"mensaje_{self.contador_mensajes:03d}"
        mensaje.id = mensaje_id
        self.mensajes[mensaje_id] = mensaje
        return mensaje_id
    
    async def consultar_mensaje(self, mensaje_id: str) -> Optional[Mensaje]:
        """Consulta un mensaje por su ID."""
        return self.mensajes.get(mensaje_id)
    
    async def solicitar_hormigas(self, cantidad_hormigas: int, subsistema_destino: str) -> str:
        """Solicita hormigas para recolección."""
        mensaje = Mensaje(
            id="",  # Se asignará en enviar_mensaje
            tipo=TipoMensaje.SOLICITAR_HORMIGAS_RECOLECCION,
            contenido={"cantidad": cantidad_hormigas, "subsistema": subsistema_destino},
            subsistema_origen="recoleccion",
            subsistema_destino="hormiga_reina"
        )
        return await self.enviar_mensaje(mensaje)
    
    async def consultar_respuesta_hormigas(self, mensaje_id: str) -> List[Hormiga]:
        """Consulta la respuesta de una solicitud de hormigas."""
        if mensaje_id in self.respuestas_hormigas:
            return self.respuestas_hormigas[mensaje_id]
        
        # Generar hormigas mock si no hay respuesta predefinida
        mensaje = await self.consultar_mensaje(mensaje_id)
        if mensaje and mensaje.tipo == TipoMensaje.SOLICITAR_HORMIGAS_RECOLECCION:
            cantidad = mensaje.contenido.get("cantidad", 1)
            hormigas = self._generar_hormigas_mock(cantidad)
            self.respuestas_hormigas[mensaje_id] = hormigas
            return hormigas
        
        return []
    
    async def devolver_hormigas(self, hormigas: List[Hormiga], alimento_recolectado: int) -> str:
        """Devuelve hormigas al subsistema de Hormiga Reina."""
        mensaje = Mensaje(
            id="",  # Se asignará en enviar_mensaje
            tipo=TipoMensaje.DEVOLVER_HORMIGAS_RECOLECCION,
            contenido={
                "hormigas": [{"id": h.id, "capacidad_carga": h.capacidad_carga} for h in hormigas],
                "alimento_recolectado": alimento_recolectado
            },
            subsistema_origen="recoleccion",
            subsistema_destino="hormiga_reina"
        )
        return await self.enviar_mensaje(mensaje)
    
    async def is_disponible(self) -> bool:
        """Verifica si el servicio está disponible."""
        return self.disponible
    
    def set_disponible(self, disponible: bool):
        """Establece la disponibilidad del servicio."""
        self.disponible = disponible
    
    def _generar_hormigas_mock(self, cantidad: int) -> List[Hormiga]:
        """Genera hormigas mock para las pruebas."""
        hormigas = []
        for i in range(cantidad):
            hormiga = Hormiga(
                id=f"hormiga_mock_{i+1:03d}",
                capacidad_carga=5,
                tiempo_vida=3600,
                subsistema_origen="hormiga_reina"
            )
            hormigas.append(hormiga)
        return hormigas
    
    def configurar_respuesta_hormigas(self, mensaje_id: str, hormigas: List[Hormiga]):
        """Configura una respuesta específica para un mensaje."""
        self.respuestas_hormigas[mensaje_id] = hormigas
    
    def limpiar_mensajes(self):
        """Limpia todos los mensajes."""
        self.mensajes.clear()
        self.respuestas_hormigas.clear()
        self.contador_mensajes = 0
