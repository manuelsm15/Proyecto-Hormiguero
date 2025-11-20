"""
Servicio de persistencia para el subsistema de recolección.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.alimento import Alimento
from ..models.hormiga import Hormiga
from ..models.tarea_recoleccion import TareaRecoleccion
from ..models.mensaje import Mensaje
from ..models.tipo_mensaje import TipoMensaje
from ..models.estado_tarea import EstadoTarea
from ..models.estado_hormiga import EstadoHormiga
from ..database.database_manager import db_manager
import json


class PersistenceService:
    """
    Servicio de persistencia para datos del subsistema de recolección.
    """
    
    def __init__(self):
        """Inicializa el servicio de persistencia."""
        self.db = db_manager
    
    async def guardar_alimento(self, alimento: Alimento) -> bool:
        """Guarda un alimento en la base de datos."""
        success = self.db.guardar_alimento(alimento)
        if success:
            await self._registrar_evento(
                "alimento_guardado",
                f"Alimento {alimento.id} guardado en base de datos",
                {"alimento_id": alimento.id, "nombre": alimento.nombre}
            )
        return success
    
    async def obtener_alimentos(self) -> List[Alimento]:
        """Obtiene todos los alimentos de la base de datos."""
        return self.db.obtener_alimentos()
    
    async def obtener_alimento_por_id(self, alimento_id: str) -> Optional[Alimento]:
        """Obtiene un alimento por su ID desde la base de datos."""
        try:
            row = self.db.obtener_alimento_por_id(alimento_id)
            if not row:
                return None
            return Alimento(
                id=str(row['id']),
                nombre=row['nombre'],
                cantidad_hormigas_necesarias=row['cantidad_hormigas_necesarias'],
                puntos_stock=row['puntos_stock'],
                tiempo_recoleccion=row['tiempo_recoleccion'],
                disponible=bool(row['disponible'])
            )
        except Exception as e:
            print(f"Error obteniendo alimento por id: {e}")
            return None
    
    async def actualizar_alimento_disponibilidad(self, alimento_id: str, disponible: bool) -> bool:
        """Actualiza la disponibilidad de un alimento en la base de datos."""
        try:
            success = self.db.actualizar_alimento_disponibilidad(alimento_id, disponible)
            if success:
                await self._registrar_evento(
                    "alimento_actualizado",
                    f"Alimento {alimento_id} actualizado: disponible={disponible}",
                    {"alimento_id": alimento_id, "disponible": disponible}
                )
            return success
        except Exception as e:
            print(f"Error actualizando disponibilidad de alimento: {e}")
            return False
    
    async def guardar_tarea(self, tarea: TareaRecoleccion) -> bool:
        """Guarda una tarea en la base de datos."""
        success = self.db.guardar_tarea(tarea)
        if success:
            await self._registrar_evento(
                "tarea_guardada",
                f"Tarea {tarea.id} guardada en base de datos",
                {
                    "tarea_id": tarea.id,
                    "alimento_id": tarea.alimento.id,
                    "estado": tarea.estado.value,
                    "hormigas_asignadas": len(tarea.hormigas_asignadas)
                }
            )
        return success
    
    async def obtener_tareas(self) -> List[TareaRecoleccion]:
        """Obtiene todas las tareas de la base de datos."""
        return self.db.obtener_tareas()
    
    async def obtener_tareas_activas(self) -> List[TareaRecoleccion]:
        """Obtiene solo las tareas activas."""
        todas_las_tareas = await self.obtener_tareas()
        return [t for t in todas_las_tareas if t.estado in [EstadoTarea.PENDIENTE, EstadoTarea.EN_PROCESO]]
    
    async def obtener_tareas_completadas(self) -> List[TareaRecoleccion]:
        """Obtiene solo las tareas completadas."""
        todas_las_tareas = await self.obtener_tareas()
        return [t for t in todas_las_tareas if t.estado == EstadoTarea.COMPLETADA]
    
    async def actualizar_estado_tarea(self, tarea_id: str, nuevo_estado: EstadoTarea) -> bool:
        """Actualiza el estado de una tarea."""
        try:
            success = self.db.actualizar_estado_tarea(tarea_id, nuevo_estado.value)
            if success:
                await self._registrar_evento(
                    "tarea_actualizada",
                    f"Estado de tarea {tarea_id} actualizado a {nuevo_estado.value}",
                    {"tarea_id": tarea_id, "nuevo_estado": nuevo_estado.value}
                )
            return success
        except Exception as e:
            print(f"Error actualizando estado de tarea: {e}")
            return False
    
    async def guardar_mensaje(self, mensaje: Mensaje) -> bool:
        """Guarda un mensaje en la base de datos."""
        try:
            success = self.db.guardar_mensaje(mensaje)
            if success:
                await self._registrar_evento(
                    "mensaje_guardado",
                    f"Mensaje {mensaje.id} guardado en base de datos",
                    {
                        "mensaje_id": mensaje.id,
                        "tipo": mensaje.tipo.value,
                        "origen": mensaje.subsistema_origen,
                        "destino": mensaje.subsistema_destino
                    }
                )
            return success
        except Exception as e:
            print(f"Error guardando mensaje: {e}")
            return False
    
    async def obtener_mensajes(self, subsistema_origen: str = None) -> List[Mensaje]:
        """Obtiene mensajes de la base de datos."""
        try:
            rows = self.db.obtener_mensajes(subsistema_origen=subsistema_origen)
            mensajes: List[Mensaje] = []
            for row in rows:
                mensajes.append(Mensaje(
                    id=row['id'],
                    tipo=TipoMensaje(row['tipo']),
                    contenido=json.loads(row['contenido']),
                    subsistema_origen=row['subsistema_origen'],
                    subsistema_destino=row['subsistema_destino'],
                    fecha_creacion=datetime.fromisoformat(str(row['fecha_creacion'])) if row.get('fecha_creacion') else datetime.now(),
                    ttl=row.get('ttl', 60),
                    procesado=bool(row.get('procesado', 0))
                ))
            return mensajes
        except Exception as e:
            print(f"Error obteniendo mensajes: {e}")
            return []
    
    async def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas del subsistema."""
        try:
            return self.db.obtener_estadisticas()
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}
    
    async def obtener_eventos_recientes(self, limite: int = 50) -> List[Dict[str, Any]]:
        """Obtiene los eventos más recientes."""
        return self.db.obtener_eventos(limite)
    
    async def guardar_evento(self, tipo_evento: str, descripcion: str, datos_adicionales: Dict[str, Any] = None) -> bool:
        """Guarda un evento en la base de datos."""
        try:
            return self.db.guardar_evento(tipo_evento, descripcion, datos_adicionales)
        except Exception as e:
            print(f"Error guardando evento: {e}")
            return False
    
    async def obtener_info_bd(self) -> Dict[str, Any]:
        """Devuelve información sobre el motor y destino de BD actual."""
        try:
            db_impl = type(self.db).__name__
            engine = "sqlserver" if "SqlServer" in db_impl else "sqlite"
            info: Dict[str, Any] = {"engine": engine, "implementation": db_impl}
            if engine == "sqlserver":
                import os
                info.update({
                    "server": os.getenv("SQLSERVER_SERVER", "unknown"),
                    "database": os.getenv("SQLSERVER_DATABASE", "unknown"),
                    "odbc_driver": os.getenv("SQLSERVER_ODBC_DRIVER", "unknown")
                })
            # Adjuntar último error de BD si existe (para depurar)
            last_error = getattr(self.db, 'last_error', None)
            if last_error:
                info["last_error"] = last_error
            return info
        except Exception as e:
            return {"engine": "unknown", "error": str(e)}

    def obtener_ultimo_error(self) -> Optional[str]:
        return getattr(self.db, 'last_error', None)
    
    async def _registrar_evento(self, tipo_evento: str, descripcion: str, datos_adicionales: Dict[str, Any] = None):
        """Registra un evento en la base de datos."""
        self.db.guardar_evento(tipo_evento, descripcion, datos_adicionales)
    
    async def crear_lote_hormigas(
        self, 
        lote_id: str, 
        tarea_id: str, 
        cantidad_enviada: int, 
        cantidad_requerida: int
    ) -> tuple[bool, Optional[str]]:
        """
        Crea un lote de hormigas con validación de cantidad.
        
        Returns:
            Tupla (exitoso, mensaje_error)
        """
        try:
            success = self.db.crear_lote_hormigas(lote_id, tarea_id, cantidad_enviada, cantidad_requerida)
            if success:
                await self._registrar_evento(
                    "lote_creado",
                    f"Lote {lote_id} creado para tarea {tarea_id}",
                    {
                        "lote_id": lote_id,
                        "tarea_id": tarea_id,
                        "cantidad_enviada": cantidad_enviada,
                        "cantidad_requerida": cantidad_requerida
                    }
                )
                return True, None
            else:
                error_msg = self.db.last_error or "Error desconocido al crear lote"
                return False, error_msg
        except Exception as e:
            return False, str(e)
    
    async def aceptar_lote_hormigas(self, lote_id: str) -> tuple[bool, Optional[str]]:
        """Acepta un lote de hormigas."""
        try:
            success = self.db.aceptar_lote_hormigas(lote_id)
            if success:
                await self._registrar_evento(
                    "lote_aceptado",
                    f"Lote {lote_id} aceptado",
                    {"lote_id": lote_id}
                )
                return True, None
            else:
                error_msg = self.db.last_error or "Error desconocido al aceptar lote"
                return False, error_msg
        except Exception as e:
            return False, str(e)
    
    async def marcar_lote_en_uso(self, lote_id: str) -> bool:
        """Marca un lote como en uso."""
        try:
            success = self.db.marcar_lote_en_uso(lote_id)
            if success:
                await self._registrar_evento(
                    "lote_en_uso",
                    f"Lote {lote_id} marcado como en uso",
                    {"lote_id": lote_id}
                )
            return success
        except Exception as e:
            print(f"Error marcando lote en uso: {e}")
            return False
    
    async def verificar_lote_disponible(self, lote_id: str, cantidad_requerida: int) -> tuple[bool, Optional[str]]:
        """Verifica que un lote esté disponible y tenga cantidad suficiente."""
        return self.db.verificar_lote_disponible(lote_id, cantidad_requerida)
    
    async def guardar_hormigas_en_lote(self, lote_id: str, hormigas: List[Hormiga]) -> bool:
        """Guarda las hormigas asignadas en un lote."""
        try:
            success = self.db.guardar_hormigas_en_lote(lote_id, hormigas)
            if success:
                await self._registrar_evento(
                    "hormigas_guardadas_en_lote",
                    f"{len(hormigas)} hormigas guardadas en lote {lote_id}",
                    {"lote_id": lote_id, "cantidad_hormigas": len(hormigas)}
                )
            return success
        except Exception as e:
            print(f"Error guardando hormigas en lote: {e}")
            return False
    
    async def obtener_hormigas_por_lote(self, lote_id: str) -> List[Hormiga]:
        """Obtiene las hormigas asignadas a un lote."""
        return self.db.obtener_hormigas_por_lote(lote_id)

    def cerrar(self):
        """Cierra la conexión a la base de datos."""
        self.db.cerrar()


# Instancia global del servicio de persistencia
persistence_service = PersistenceService()

