"""
Modelo que representa un mensaje de comunicación entre subsistemas.
"""

from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Any, Optional

from .tipo_mensaje import TipoMensaje


@dataclass
class Mensaje:
    """
    Modelo que representa un mensaje de comunicación entre subsistemas.
    
    Attributes:
        id: Identificador único del mensaje
        tipo: Tipo de mensaje
        contenido: Contenido del mensaje
        subsistema_origen: Subsistema que envía el mensaje
        subsistema_destino: Subsistema destinatario
        fecha_creacion: Fecha y hora de creación del mensaje
        ttl: Time to live en segundos (por defecto 60)
        procesado: Si el mensaje ha sido procesado
    """
    
    id: str
    tipo: TipoMensaje
    contenido: Any
    subsistema_origen: str
    subsistema_destino: str
    fecha_creacion: datetime = field(default_factory=datetime.now)
    ttl: int = 60  # 1 minuto por defecto
    procesado: bool = False
    
    def __post_init__(self) -> None:
        """Validaciones post-inicialización."""
        if self.ttl <= 0:
            raise ValueError("El TTL debe ser mayor a 0")
    
    def is_expirado(self) -> bool:
        """
        Verifica si el mensaje ha expirado basándose en su TTL.
        
        Returns:
            True si el mensaje ha expirado, False en caso contrario
        """
        ahora = datetime.now()
        tiempo_expiracion = self.fecha_creacion + timedelta(seconds=self.ttl)
        return ahora > tiempo_expiracion
    
    def marcar_como_procesado(self) -> None:
        """Marca el mensaje como procesado."""
        self.procesado = True
    
    def __str__(self) -> str:
        return (
            f"Mensaje(id='{self.id}', tipo={self.tipo.value}, "
            f"origen='{self.subsistema_origen}', destino='{self.subsistema_destino}', "
            f"procesado={self.procesado}, expirado={self.is_expirado()})"
        )
    
    def __repr__(self) -> str:
        return self.__str__()

