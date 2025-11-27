"""
Gestor de base de datos para persistencia de datos del subsistema de recolección.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from ..models.alimento import Alimento
from ..models.hormiga import Hormiga
from ..models.tarea_recoleccion import TareaRecoleccion
from ..models.mensaje import Mensaje
from ..models.estado_tarea import EstadoTarea
from ..models.estado_hormiga import EstadoHormiga


class DatabaseManager:
    """
    Gestor de base de datos para persistencia de datos.
    """
    
    def __init__(self, db_path: str = "recoleccion.db"):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta del archivo de base de datos
        """
        self.db_path = db_path
        self.connection = None
        self.last_error = None
        self._init_database()
    
    def _init_database(self):
        """Inicializa la base de datos y crea las tablas."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self._create_tables()
            print(f"Base de datos inicializada: {self.db_path}")
        except Exception as e:
            self.last_error = str(e)
            print(f"Error inicializando base de datos: {e}")
            raise
    
    def _create_tables(self):
        """Crea las tablas necesarias."""
        cursor = self.connection.cursor()
        
        # Tabla de alimentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alimentos (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad_hormigas_necesarias INTEGER NOT NULL,
                puntos_stock INTEGER NOT NULL,
                tiempo_recoleccion INTEGER NOT NULL,
                disponible BOOLEAN DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de tareas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id TEXT PRIMARY KEY,
                alimento_id TEXT NOT NULL,
                estado TEXT NOT NULL,
                fecha_inicio TIMESTAMP,
                fecha_fin TIMESTAMP,
                alimento_recolectado INTEGER DEFAULT 0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (alimento_id) REFERENCES alimentos (id)
            )
        """)
        
        # Tabla de hormigas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hormigas (
                id TEXT PRIMARY KEY,
                capacidad_carga INTEGER DEFAULT 5,
                estado TEXT DEFAULT 'disponible',
                tiempo_vida INTEGER DEFAULT 3600,
                subsistema_origen TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de lotes de hormigas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lotes_hormigas (
                lote_id TEXT PRIMARY KEY,
                tarea_id TEXT NOT NULL,
                cantidad_hormigas_enviadas INTEGER NOT NULL,
                cantidad_hormigas_requeridas INTEGER NOT NULL,
                estado TEXT NOT NULL DEFAULT 'pendiente',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_aceptacion TIMESTAMP,
                FOREIGN KEY (tarea_id) REFERENCES tareas (id)
            )
        """)
        
        # Tabla de asignaciones hormiga-tarea (modificada para incluir lote_id)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asignaciones_hormiga_tarea (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarea_id TEXT NOT NULL,
                hormiga_id TEXT NOT NULL,
                lote_id TEXT,
                fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tarea_id) REFERENCES tareas (id),
                FOREIGN KEY (hormiga_id) REFERENCES hormigas (id),
                FOREIGN KEY (lote_id) REFERENCES lotes_hormigas (lote_id)
            )
        """)
        
        # Tabla de mensajes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id TEXT PRIMARY KEY,
                tipo TEXT NOT NULL,
                contenido TEXT NOT NULL,
                subsistema_origen TEXT NOT NULL,
                subsistema_destino TEXT NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ttl INTEGER DEFAULT 60,
                procesado BOOLEAN DEFAULT 0
            )
        """)
        
        # Tabla de eventos (logs de actividades)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_evento TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                datos_adicionales TEXT,
                fecha_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
        print("Tablas de base de datos creadas exitosamente")
    
    def guardar_alimento(self, alimento: Alimento) -> bool:
        """Guarda un alimento en la base de datos."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO alimentos 
                (id, nombre, cantidad_hormigas_necesarias, puntos_stock, tiempo_recoleccion, disponible)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                alimento.id,
                alimento.nombre,
                alimento.cantidad_hormigas_necesarias,
                alimento.puntos_stock,
                alimento.tiempo_recoleccion,
                alimento.disponible
            ))
            self.connection.commit()
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error guardando alimento: {e}")
            return False
    
    def obtener_alimentos(self) -> List[Alimento]:
        """Obtiene todos los alimentos de la base de datos."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM alimentos")
            rows = cursor.fetchall()
            
            alimentos = []
            for row in rows:
                alimento = Alimento(
                    id=row['id'],
                    nombre=row['nombre'],
                    cantidad_hormigas_necesarias=row['cantidad_hormigas_necesarias'],
                    puntos_stock=row['puntos_stock'],
                    tiempo_recoleccion=row['tiempo_recoleccion'],
                    disponible=bool(row['disponible'])
                )
                alimentos.append(alimento)
            
            return alimentos
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo alimentos: {e}")
            return []

    def actualizar_alimento_disponibilidad(self, alimento_id: str, disponible: bool) -> bool:
        """Actualiza la disponibilidad de un alimento."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE alimentos 
                SET disponible = ?
                WHERE id = ?
            """, (disponible, alimento_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.last_error = str(e)
            print(f"Error actualizando disponibilidad de alimento: {e}")
            return False

    def obtener_alimento_por_id(self, alimento_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un alimento por ID (como dict crudo)."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM alimentos WHERE id = ?", (alimento_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error obteniendo alimento por id: {e}")
            return None
    
    def guardar_tarea(self, tarea: TareaRecoleccion) -> bool:
        """Guarda una tarea en la base de datos."""
        try:
            cursor = self.connection.cursor()
            
            # Agregar columna hormigas_asignadas si no existe
            try:
                cursor.execute("ALTER TABLE tareas ADD COLUMN hormigas_asignadas INTEGER DEFAULT 0")
                self.connection.commit()
            except Exception:
                # La columna ya existe, continuar
                pass
            
            # Calcular cantidad de hormigas asignadas
            cantidad_hormigas = len(tarea.hormigas_asignadas) if tarea.hormigas_asignadas else 0
            
            cursor.execute("""
                INSERT OR REPLACE INTO tareas 
                (id, alimento_id, estado, fecha_inicio, fecha_fin, alimento_recolectado, hormigas_asignadas)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                tarea.id,
                tarea.alimento.id,
                tarea.estado.value,
                tarea.fecha_inicio.isoformat() if tarea.fecha_inicio else None,
                tarea.fecha_fin.isoformat() if tarea.fecha_fin else None,
                tarea.alimento_recolectado,
                cantidad_hormigas
            ))
            
            # Guardar asignaciones de hormigas
            # Primero eliminar asignaciones antiguas (si existen)
            cursor.execute("""
                DELETE FROM asignaciones_hormiga_tarea 
                WHERE tarea_id = ? AND (lote_id IS NULL OR lote_id = '')
            """, (tarea.id,))
            
            # Luego insertar las nuevas asignaciones
            for hormiga in tarea.hormigas_asignadas:
                cursor.execute("""
                    INSERT OR REPLACE INTO asignaciones_hormiga_tarea 
                    (tarea_id, hormiga_id, lote_id)
                    VALUES (?, ?, ?)
                """, (tarea.id, hormiga.id, tarea.hormigas_lote_id))
            
            self.connection.commit()
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error guardando tarea: {e}")
            return False
    
    def obtener_tareas(self) -> List[TareaRecoleccion]:
        """Obtiene todas las tareas de la base de datos."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT t.*, a.nombre, a.cantidad_hormigas_necesarias, 
                       a.puntos_stock, a.tiempo_recoleccion, a.disponible
                FROM tareas t
                JOIN alimentos a ON t.alimento_id = a.id
            """)
            rows = cursor.fetchall()
            
            tareas = []
            for row in rows:
                # Crear alimento
                alimento = Alimento(
                    id=row['alimento_id'],
                    nombre=row['nombre'],
                    cantidad_hormigas_necesarias=row['cantidad_hormigas_necesarias'],
                    puntos_stock=row['puntos_stock'],
                    tiempo_recoleccion=row['tiempo_recoleccion'],
                    disponible=bool(row['disponible'])
                )
                
                # Crear tarea
                tarea = TareaRecoleccion(
                    id=row['id'],
                    alimento=alimento,
                    estado=EstadoTarea(row['estado']),
                    fecha_inicio=datetime.fromisoformat(row['fecha_inicio']) if row['fecha_inicio'] else None,
                    fecha_fin=datetime.fromisoformat(row['fecha_fin']) if row['fecha_fin'] else None,
                    alimento_recolectado=row['alimento_recolectado']
                )
                
                # Obtener lote_id de la tarea (si existe en la tabla de tareas)
                # Primero intentar obtener desde lotes_hormigas
                cursor.execute("""
                    SELECT lote_id FROM lotes_hormigas WHERE tarea_id = ? LIMIT 1
                """, (tarea.id,))
                lote_row = cursor.fetchone()
                
                if lote_row:
                    lote_id = lote_row[0]
                    tarea.hormigas_lote_id = lote_id
                    # Obtener hormigas desde el lote
                    cursor.execute("""
                        SELECT h.* FROM hormigas h
                        JOIN asignaciones_hormiga_tarea aht ON h.id = aht.hormiga_id
                        WHERE aht.lote_id = ?
                    """, (lote_id,))
                else:
                    # Fallback: obtener hormigas directamente por tarea_id (compatibilidad)
                    cursor.execute("""
                        SELECT h.* FROM hormigas h
                        JOIN asignaciones_hormiga_tarea aht ON h.id = aht.hormiga_id
                        WHERE aht.tarea_id = ? AND aht.lote_id IS NULL
                    """, (tarea.id,))
                
                hormiga_rows = cursor.fetchall()
                
                for hormiga_row in hormiga_rows:
                    hormiga = Hormiga(
                        id=hormiga_row['id'],
                        capacidad_carga=hormiga_row['capacidad_carga'],
                        estado=EstadoHormiga(hormiga_row['estado']),
                        tiempo_vida=hormiga_row['tiempo_vida'],
                        subsistema_origen=hormiga_row['subsistema_origen']
                    )
                    tarea.agregar_hormiga(hormiga)
                
                tareas.append(tarea)
            
            return tareas
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo tareas: {e}")
            return []
    
    def guardar_evento(self, tipo_evento: str, descripcion: str, datos_adicionales: Dict[str, Any] = None):
        """Guarda un evento en la base de datos."""
        try:
            cursor = self.connection.cursor()
            datos_json = json.dumps(datos_adicionales) if datos_adicionales else None
            
            cursor.execute("""
                INSERT INTO eventos (tipo_evento, descripcion, datos_adicionales)
                VALUES (?, ?, ?)
            """, (tipo_evento, descripcion, datos_json))
            
            self.connection.commit()
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error guardando evento: {e}")
            return False
    
    def obtener_eventos(self, limite: int = 100) -> List[Dict[str, Any]]:
        """Obtiene los eventos más recientes."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM eventos 
                ORDER BY fecha_evento DESC 
                LIMIT ?
            """, (limite,))
            
            eventos = []
            for row in cursor.fetchall():
                evento = {
                    'id': row['id'],
                    'tipo_evento': row['tipo_evento'],
                    'descripcion': row['descripcion'],
                    'fecha_evento': row['fecha_evento'],
                    'datos_adicionales': json.loads(row['datos_adicionales']) if row['datos_adicionales'] else None
                }
                eventos.append(evento)
            
            return eventos
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo eventos: {e}")
            return []
    
    def cerrar(self):
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            print("Conexión a base de datos cerrada")

    # Nuevos helpers para unificar uso desde PersistenceService
    def actualizar_estado_tarea(self, tarea_id: str, nuevo_estado: str) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                UPDATE tareas 
                SET estado = ? 
                WHERE id = ?
                """,
                (nuevo_estado, tarea_id),
            )
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.last_error = str(e)
            print(f"Error actualizando estado de tarea (SQLite): {e}")
            return False

    def guardar_mensaje(self, mensaje: Mensaje) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO mensajes 
                (id, tipo, contenido, subsistema_origen, subsistema_destino, ttl, procesado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    mensaje.id,
                    mensaje.tipo.value,
                    json.dumps(mensaje.contenido),
                    mensaje.subsistema_origen,
                    mensaje.subsistema_destino,
                    mensaje.ttl,
                    mensaje.procesado,
                ),
            )
            self.connection.commit()
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error guardando mensaje (SQLite): {e}")
            return False

    def obtener_mensajes(self, subsistema_origen: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            if subsistema_origen:
                cursor.execute(
                    """
                    SELECT * FROM mensajes 
                    WHERE subsistema_origen = ? 
                    ORDER BY fecha_creacion DESC
                    """,
                    (subsistema_origen,),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM mensajes 
                    ORDER BY fecha_creacion DESC
                    """
                )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo mensajes (SQLite): {e}")
            return []

    def crear_lote_hormigas(
        self, 
        lote_id: str, 
        tarea_id: str, 
        cantidad_enviada: int, 
        cantidad_requerida: int
    ) -> bool:
        """
        Crea un lote de hormigas con validación de cantidad.
        
        Args:
            lote_id: ID único del lote
            tarea_id: ID de la tarea asociada
            cantidad_enviada: Cantidad de hormigas enviadas
            cantidad_requerida: Cantidad de hormigas requeridas
            
        Returns:
            True si se creó exitosamente, False si la cantidad es insuficiente
        """
        try:
            # Validar que cantidad_enviada >= cantidad_requerida
            if cantidad_enviada < cantidad_requerida:
                self.last_error = f"Cantidad insuficiente de hormigas. Enviadas: {cantidad_enviada}, Requeridas: {cantidad_requerida}"
                return False
            
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO lotes_hormigas 
                (lote_id, tarea_id, cantidad_hormigas_enviadas, cantidad_hormigas_requeridas, estado)
                VALUES (?, ?, ?, ?, 'pendiente')
            """, (lote_id, tarea_id, cantidad_enviada, cantidad_requerida))
            self.connection.commit()
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error creando lote de hormigas: {e}")
            return False
    
    def aceptar_lote_hormigas(self, lote_id: str) -> bool:
        """
        Acepta un lote de hormigas y lo marca como aceptado.
        
        Args:
            lote_id: ID del lote a aceptar
            
        Returns:
            True si se aceptó exitosamente, False si el lote está en uso o no existe
        """
        try:
            cursor = self.connection.cursor()
            # Verificar que el lote existe y no está en uso
            cursor.execute("""
                SELECT estado FROM lotes_hormigas WHERE lote_id = ?
            """, (lote_id,))
            row = cursor.fetchone()
            
            if not row:
                self.last_error = f"Lote {lote_id} no encontrado"
                return False
            
            estado_actual = row[0]
            if estado_actual == 'en_uso':
                self.last_error = f"Lote {lote_id} ya está en uso"
                return False
            
            # Marcar como aceptado
            cursor.execute("""
                UPDATE lotes_hormigas 
                SET estado = 'aceptado', fecha_aceptacion = CURRENT_TIMESTAMP
                WHERE lote_id = ?
            """, (lote_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.last_error = str(e)
            print(f"Error aceptando lote de hormigas: {e}")
            return False
    
    def marcar_lote_en_uso(self, lote_id: str) -> bool:
        """
        Marca un lote como en uso.
        
        Args:
            lote_id: ID del lote
            
        Returns:
            True si se marcó exitosamente
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE lotes_hormigas 
                SET estado = 'en_uso'
                WHERE lote_id = ?
            """, (lote_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.last_error = str(e)
            print(f"Error marcando lote en uso: {e}")
            return False
    
    def verificar_lote_disponible(self, lote_id: str, cantidad_requerida: int) -> tuple[bool, Optional[str]]:
        """
        Verifica que un lote esté disponible y tenga cantidad suficiente.
        
        Args:
            lote_id: ID del lote a verificar
            cantidad_requerida: Cantidad de hormigas requeridas
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT estado, cantidad_hormigas_enviadas 
                FROM lotes_hormigas 
                WHERE lote_id = ?
            """, (lote_id,))
            row = cursor.fetchone()
            
            if not row:
                return False, f"Lote {lote_id} no encontrado"
            
            estado, cantidad_enviada = row[0], row[1]
            
            if estado == 'en_uso':
                return False, f"Lote {lote_id} ya está en uso"
            
            if cantidad_enviada < cantidad_requerida:
                return False, f"Lote {lote_id} tiene cantidad insuficiente. Tiene: {cantidad_enviada}, Requiere: {cantidad_requerida}"
            
            return True, None
        except Exception as e:
            return False, f"Error verificando lote: {str(e)}"
    
    def guardar_hormigas_en_lote(self, lote_id: str, hormigas: List[Hormiga]) -> bool:
        """
        Guarda las hormigas asignadas en un lote.
        
        Args:
            lote_id: ID del lote
            hormigas: Lista de hormigas a guardar
            
        Returns:
            True si se guardaron exitosamente
        """
        try:
            cursor = self.connection.cursor()
            # Obtener tarea_id del lote
            cursor.execute("SELECT tarea_id FROM lotes_hormigas WHERE lote_id = ?", (lote_id,))
            row = cursor.fetchone()
            if not row:
                self.last_error = f"Lote {lote_id} no encontrado"
                return False
            
            tarea_id = row[0]
            
            # Guardar cada hormiga en asignaciones con el lote_id
            for hormiga in hormigas:
                # Guardar hormiga si no existe
                cursor.execute("""
                    INSERT OR IGNORE INTO hormigas 
                    (id, capacidad_carga, estado, tiempo_vida, subsistema_origen)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    hormiga.id,
                    hormiga.capacidad_carga,
                    hormiga.estado.value if hasattr(hormiga.estado, 'value') else str(hormiga.estado),
                    hormiga.tiempo_vida,
                    hormiga.subsistema_origen
                ))
                
                # Guardar asignación con lote_id
                cursor.execute("""
                    INSERT OR REPLACE INTO asignaciones_hormiga_tarea 
                    (tarea_id, hormiga_id, lote_id)
                    VALUES (?, ?, ?)
                """, (tarea_id, hormiga.id, lote_id))
            
            self.connection.commit()
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error guardando hormigas en lote: {e}")
            return False
    
    def obtener_hormigas_por_lote(self, lote_id: str) -> List[Hormiga]:
        """
        Obtiene las hormigas asignadas a un lote.
        
        Args:
            lote_id: ID del lote
            
        Returns:
            Lista de hormigas
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT h.* FROM hormigas h
                JOIN asignaciones_hormiga_tarea aht ON h.id = aht.hormiga_id
                WHERE aht.lote_id = ?
            """, (lote_id,))
            rows = cursor.fetchall()
            
            hormigas = []
            for row in rows:
                hormigas.append(Hormiga(
                    id=row['id'],
                    capacidad_carga=row['capacidad_carga'],
                    estado=EstadoHormiga(row['estado']),
                    tiempo_vida=row['tiempo_vida'],
                    subsistema_origen=row['subsistema_origen']
                ))
            return hormigas
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo hormigas por lote: {e}")
            return []

    def obtener_estadisticas(self) -> Dict[str, Any]:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM tareas")
            total_tareas = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) as activas FROM tareas WHERE estado IN ('pendiente', 'en_proceso')")
            tareas_activas = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) as completadas FROM tareas WHERE estado = 'completada'")
            tareas_completadas = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) as total FROM alimentos")
            total_alimentos = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) as disponibles FROM alimentos WHERE disponible = 1")
            alimentos_disponibles = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) as total FROM mensajes")
            total_mensajes = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) as total FROM eventos")
            total_eventos = cursor.fetchone()[0]
            return {
                "tareas": {"total": total_tareas, "activas": tareas_activas, "completadas": tareas_completadas},
                "alimentos": {"total": total_alimentos, "disponibles": alimentos_disponibles},
                "mensajes": {"total": total_mensajes},
                "eventos": {"total": total_eventos},
                "fecha_consulta": datetime.now().isoformat(),
            }
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo estadísticas (SQLite): {e}")
            return {}


class SqlServerDatabaseManager:
    """
    Gestor de base de datos para Microsoft SQL Server (autenticación de Windows).
    Requiere el controlador ODBC adecuado instalado (p. ej., ODBC Driver 18 for SQL Server).
    """

    def __init__(self, server: str, database: str):
        import pyodbc  # importación tardía para evitar dependencia si no se usa
        self.pyodbc = pyodbc
        self.last_error = None
        # Trusted Connection con autenticación de Windows
        driver = os.getenv("SQLSERVER_ODBC_DRIVER", "ODBC Driver 18 for SQL Server")
        encrypt = os.getenv("SQLSERVER_ENCRYPT", "no")  # "yes" si tu política lo requiere
        trust_server_cert = os.getenv("SQLSERVER_TRUST_SERVER_CERT", "yes")
        conn_str = (
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
            f"Trusted_Connection=yes;Encrypt={encrypt};TrustServerCertificate={trust_server_cert}"
        )
        self.connection = self.pyodbc.connect(conn_str)
        self.connection.autocommit = True
        self._detect_schema()
        print(f"Base de datos SQL Server inicializada: {server} / {database}")

    def _exec(self, cursor, sql: str, params: tuple = ()):
        cursor.execute(sql, params) if params else cursor.execute(sql)

    def _fetchall_dicts(self, cursor) -> List[Dict[str, Any]]:
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def _detect_schema(self):
        cursor = self.connection.cursor()
        # Detectar columnas de dbo.Alimentos
        self._exec(cursor, "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME='Alimentos'")
        cols = {row[0].lower() for row in cursor.fetchall()}
        # Dos variantes soportadas:
        # - esquema 'nuevo': cantidad_hormigas_necesarias, puntos_stock, tiempo_recoleccion, disponible
        # - esquema 'script': cantidad_unitaria, duracion_recoleccion, hormigas_requeridas, estado, peso, tipo, zona_id
        if {"cantidad_hormigas_necesarias","puntos_stock","tiempo_recoleccion"}.issubset(cols):
            self.schema_type = "nuevo"
        else:
            self.schema_type = "script"

    # API similar a DatabaseManager
    def guardar_alimento(self, alimento: Alimento) -> bool:
        try:
            cursor = self.connection.cursor()
            if self.schema_type == "nuevo":
                # UPSERT manual con columnas del modelo
                self._exec(cursor, """
                    UPDATE dbo.Alimentos SET
                        nombre = ?,
                        cantidad_hormigas_necesarias = ?,
                        puntos_stock = ?,
                        tiempo_recoleccion = ?,
                        disponible = ?
                    WHERE id = ?
                """, (
                    alimento.nombre,
                    alimento.cantidad_hormigas_necesarias,
                    alimento.puntos_stock,
                    alimento.tiempo_recoleccion,
                    1 if alimento.disponible else 0,
                    alimento.id,
                ))
                if cursor.rowcount == 0:
                    self._exec(cursor, """
                        INSERT INTO dbo.Alimentos (id, nombre, cantidad_hormigas_necesarias, puntos_stock, tiempo_recoleccion, disponible)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        alimento.id,
                        alimento.nombre,
                        alimento.cantidad_hormigas_necesarias,
                        alimento.puntos_stock,
                        alimento.tiempo_recoleccion,
                        1 if alimento.disponible else 0,
                    ))
            else:
                # Esquema del script: id es IDENTITY (int). Ignorar alimento.id si viene.
                # Mapear campos al esquema existente
                tipo = "GEN"
                zona_id = None
                cantidad_unitaria = alimento.puntos_stock
                peso = 1
                duracion_recoleccion = alimento.tiempo_recoleccion
                hormigas_requeridas = alimento.cantidad_hormigas_necesarias
                estado = "disponible" if alimento.disponible else "recolectado"
                self._exec(cursor, """
                    INSERT INTO dbo.Alimentos (nombre, tipo, zona_id, cantidad_unitaria, peso, duracion_recoleccion, hormigas_requeridas, estado, disponible)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    alimento.nombre,
                    tipo,
                    zona_id,
                    cantidad_unitaria,
                    peso,
                    duracion_recoleccion,
                    hormigas_requeridas,
                    estado,
                    1 if alimento.disponible else 0,
                ))
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error guardando alimento (SQL Server): {e}")
            return False

    def obtener_alimentos(self) -> List[Alimento]:
        try:
            cursor = self.connection.cursor()
            if self.schema_type == "nuevo":
                self._exec(cursor, "SELECT id, nombre, cantidad_hormigas_necesarias, puntos_stock, tiempo_recoleccion, disponible FROM dbo.Alimentos")
                rows = self._fetchall_dicts(cursor)
                alimentos: List[Alimento] = []
                for row in rows:
                    alimentos.append(Alimento(
                        id=str(row['id']),
                        nombre=row['nombre'],
                        cantidad_hormigas_necesarias=row['cantidad_hormigas_necesarias'],
                        puntos_stock=row['puntos_stock'],
                        tiempo_recoleccion=row['tiempo_recoleccion'],
                        disponible=bool(row['disponible'])
                    ))
            else:
                self._exec(cursor, "SELECT id, nombre, cantidad_unitaria, duracion_recoleccion, hormigas_requeridas, disponible FROM dbo.Alimentos")
                rows = self._fetchall_dicts(cursor)
                alimentos = []
                for row in rows:
                    alimentos.append(Alimento(
                        id=str(row['id']),
                        nombre=row['nombre'],
                        cantidad_hormigas_necesarias=row['hormigas_requeridas'],
                        puntos_stock=row['cantidad_unitaria'],
                        tiempo_recoleccion=row['duracion_recoleccion'],
                        disponible=bool(row['disponible'])
                    ))
            return alimentos
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo alimentos (SQL Server): {e}")
            return []

    def obtener_alimento_por_id(self, alimento_id: str) -> Optional[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            if self.schema_type == "nuevo":
                self._exec(cursor, "SELECT id, nombre, cantidad_hormigas_necesarias, puntos_stock, tiempo_recoleccion, disponible FROM dbo.Alimentos WHERE id = ?", (alimento_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            else:
                # En esquema script, id es INT; intentar convertir
                try:
                    aid = int(alimento_id)
                except:
                    return None
                self._exec(cursor, "SELECT id, nombre, cantidad_unitaria AS puntos_stock, duracion_recoleccion AS tiempo_recoleccion, hormigas_requeridas AS cantidad_hormigas_necesarias, disponible FROM dbo.Alimentos WHERE id = ?", (aid,))
                row = cursor.fetchone()
                if not row:
                    return None
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
        except Exception as e:
            print(f"Error obteniendo alimento por id (SQL Server): {e}")
            return None

    def actualizar_alimento_disponibilidad(self, alimento_id: str, disponible: bool) -> bool:
        """Actualiza la disponibilidad de un alimento."""
        try:
            cursor = self.connection.cursor()
            if self.schema_type == "nuevo":
                # Esquema nuevo: id es texto
                self._exec(cursor, """
                    UPDATE dbo.Alimentos 
                    SET disponible = ?
                    WHERE id = ?
                """, (1 if disponible else 0, alimento_id))
            else:
                # Esquema script: id es INT
                try:
                    aid = int(alimento_id)
                    self._exec(cursor, """
                        UPDATE dbo.Alimentos 
                        SET disponible = ?, estado = ?
                        WHERE id = ?
                    """, (1 if disponible else 0, "disponible" if disponible else "recolectado", aid))
                except ValueError:
                    print(f"Error: alimento_id '{alimento_id}' no es un número válido para el esquema script")
                    return False
            cursor.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.last_error = str(e)
            print(f"Error actualizando disponibilidad de alimento (SQL Server): {e}")
            return False

    def guardar_tarea(self, tarea: TareaRecoleccion) -> bool:
        try:
            cursor = self.connection.cursor()
            
            # Agregar columna hormigas_asignadas si no existe
            try:
                self._exec(cursor, """
                    IF NOT EXISTS (
                        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_NAME = 'Tareas' AND COLUMN_NAME = 'hormigas_asignadas'
                    )
                    ALTER TABLE dbo.Tareas ADD hormigas_asignadas INT DEFAULT 0
                """)
            except Exception:
                # La columna ya existe o error al agregar, continuar
                pass
            
            # Calcular cantidad de hormigas asignadas
            cantidad_hormigas = len(tarea.hormigas_asignadas) if tarea.hormigas_asignadas else 0
            
            # Convertir alimento_id según el esquema
            alimento_id_valor = tarea.alimento.id
            if self.schema_type == "script":
                # En esquema script, alimento_id es INT, necesitamos buscar el ID numérico
                try:
                    # Intentar convertir directamente si es numérico
                    alimento_id_valor = int(tarea.alimento.id)
                except (ValueError, TypeError):
                    # Si no es numérico, buscar el alimento en BD para obtener su ID numérico
                    alimento_bd = self.obtener_alimento_por_id(tarea.alimento.id)
                    if alimento_bd and 'id' in alimento_bd:
                        # El ID en BD puede ser numérico
                        alimento_id_valor = alimento_bd['id']
                    else:
                        # Si no se encuentra, intentar usar el ID como está (puede fallar)
                        print(f"Advertencia: No se pudo convertir alimento_id '{tarea.alimento.id}' a INT para esquema script")
                        alimento_id_valor = tarea.alimento.id
            
            # UPSERT manual - usar nombres de columnas correctos de SQL Server
            # Columnas: id, alimento_id, estado, inicio, fin, cantidad_recolectada, hormigas_asignadas
            self._exec(cursor, """
                UPDATE dbo.Tareas SET
                    alimento_id = ?,
                    estado = ?,
                    inicio = ?,
                    fin = ?,
                    cantidad_recolectada = ?,
                    hormigas_asignadas = ?
                WHERE id = ?
            """, (
                alimento_id_valor,
                tarea.estado.value,
                tarea.fecha_inicio.isoformat() if tarea.fecha_inicio else None,
                tarea.fecha_fin.isoformat() if tarea.fecha_fin else None,
                tarea.alimento_recolectado,
                cantidad_hormigas,
                tarea.id,
            ))
            if cursor.rowcount == 0:
                self._exec(cursor, """
                    INSERT INTO dbo.Tareas (id, alimento_id, estado, inicio, fin, cantidad_recolectada, hormigas_asignadas)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    tarea.id,
                    alimento_id_valor,
                    tarea.estado.value,
                    tarea.fecha_inicio.isoformat() if tarea.fecha_inicio else None,
                    tarea.fecha_fin.isoformat() if tarea.fecha_fin else None,
                    tarea.alimento_recolectado,
                    cantidad_hormigas
                ))

            # Asignaciones de hormigas
            # Primero eliminar asignaciones antiguas sin lote_id (para mantener compatibilidad con lotes)
            self._exec(cursor, """
                DELETE FROM dbo.asignaciones_hormiga_tarea 
                WHERE tarea_id = ? AND (lote_id IS NULL OR lote_id = '')
            """, (tarea.id,))
            
            # Luego insertar las nuevas asignaciones
            for hormiga in tarea.hormigas_asignadas:
                self._exec(cursor, """
                    IF NOT EXISTS (
                        SELECT 1 FROM dbo.asignaciones_hormiga_tarea 
                        WHERE tarea_id = ? AND hormiga_id = ? AND (lote_id = ? OR (lote_id IS NULL AND ? IS NULL))
                    )
                    INSERT INTO dbo.asignaciones_hormiga_tarea (tarea_id, hormiga_id, lote_id) 
                    VALUES (?, ?, ?)
                """, (
                    tarea.id, hormiga.id, tarea.hormigas_lote_id, tarea.hormigas_lote_id,
                    tarea.id, hormiga.id, tarea.hormigas_lote_id
                ))
            
            # Hacer commit de todos los cambios
            cursor.commit()
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error guardando tarea (SQL Server): {e}")
            return False

    def obtener_tareas(self) -> List[TareaRecoleccion]:
        try:
            cursor = self.connection.cursor()
            # Primero intentar obtener todas las tareas sin JOIN para verificar que existen
            self._exec(cursor, "SELECT COUNT(*) as total FROM dbo.Tareas")
            count_row = cursor.fetchone()
            total_tareas = count_row[0] if count_row else 0
            print(f"[DEBUG] Total de tareas en SQL Server: {total_tareas}")
            
            # Consulta adaptada según el esquema detectado - usar LEFT JOIN para no perder tareas
            if self.schema_type == "nuevo":
                self._exec(cursor, """
                    SELECT t.id AS tarea_id, t.alimento_id, t.estado, t.inicio, t.fin, t.cantidad_recolectada,
                           a.nombre, a.cantidad_hormigas_necesarias, a.puntos_stock, a.tiempo_recoleccion, a.disponible
                    FROM dbo.Tareas t
                    LEFT JOIN dbo.Alimentos a ON CAST(t.alimento_id AS VARCHAR) = CAST(a.id AS VARCHAR)
                """)
            else:
                # Esquema script: usar alias para mapear columnas - LEFT JOIN para no perder tareas
                self._exec(cursor, """
                    SELECT t.id AS tarea_id, t.alimento_id, t.estado, t.inicio, t.fin, t.cantidad_recolectada,
                           a.nombre, 
                           a.hormigas_requeridas AS cantidad_hormigas_necesarias,
                           a.cantidad_unitaria AS puntos_stock,
                           a.duracion_recoleccion AS tiempo_recoleccion,
                           a.disponible
                    FROM dbo.Tareas t
                    LEFT JOIN dbo.Alimentos a ON CAST(t.alimento_id AS VARCHAR) = CAST(a.id AS VARCHAR)
                """)
            rows = self._fetchall_dicts(cursor)
            print(f"[DEBUG] Filas obtenidas del JOIN: {len(rows)}")

            tareas: List[TareaRecoleccion] = []
            for row in rows:
                # Debug: mostrar primera fila para diagnóstico
                if len(tareas) == 0:
                    print(f"[DEBUG] Primera fila de tarea: {row}")
                
                # Obtener alimento_id - puede ser INT o NVARCHAR
                alimento_id_raw = row.get('alimento_id')
                alimento_id_str = str(alimento_id_raw) if alimento_id_raw is not None else None
                
                # Mapear columnas según esquema - si no hay alimento en el JOIN, usar valores por defecto
                if self.schema_type == "nuevo":
                    cantidad_hormigas = row.get('cantidad_hormigas_necesarias', 0)
                    puntos = row.get('puntos_stock', 0)
                    tiempo = row.get('tiempo_recoleccion', 0)
                else:
                    cantidad_hormigas = row.get('cantidad_hormigas_necesarias', row.get('hormigas_requeridas', 0))
                    puntos = row.get('puntos_stock', row.get('cantidad_unitaria', 0))
                    tiempo = row.get('tiempo_recoleccion', row.get('duracion_recoleccion', 0))
                
                # Si no hay alimento en el JOIN (LEFT JOIN), crear uno con valores por defecto
                nombre_alimento = row.get('nombre')
                if not nombre_alimento:
                    # No hay alimento asociado, crear uno genérico
                    alimento = Alimento(
                        id=alimento_id_str or "UNKNOWN",
                        nombre="Alimento no encontrado",
                        cantidad_hormigas_necesarias=0,
                        puntos_stock=0,
                        tiempo_recoleccion=0,
                        disponible=False
                    )
                else:
                    alimento = Alimento(
                        id=alimento_id_str or "UNKNOWN",
                        nombre=nombre_alimento,
                        cantidad_hormigas_necesarias=int(cantidad_hormigas) if cantidad_hormigas else 0,
                        puntos_stock=int(puntos) if puntos else 0,
                        tiempo_recoleccion=int(tiempo) if tiempo else 0,
                        disponible=bool(row.get('disponible', False))
                    )
                
                # Manejar fechas de forma segura - usar nombres de columnas correctos de SQL Server
                fecha_inicio = None
                fecha_fin = None
                try:
                    # La columna en SQL Server se llama 'inicio', no 'fecha_inicio'
                    if row.get('inicio'):
                        inicio_val = row['inicio']
                        # Si es un objeto datetime de pyodbc, usarlo directamente
                        if isinstance(inicio_val, datetime):
                            fecha_inicio = inicio_val
                        else:
                            # Si es string, parsear
                            fecha_inicio_str = str(inicio_val)
                            if 'T' in fecha_inicio_str or '-' in fecha_inicio_str:
                                fecha_inicio = datetime.fromisoformat(fecha_inicio_str.replace('Z', '+00:00'))
                except Exception as e:
                    print(f"[DEBUG] Error parseando fecha_inicio: {e}, valor: {row.get('inicio')}")
                    pass
                try:
                    # La columna en SQL Server se llama 'fin', no 'fecha_fin'
                    if row.get('fin'):
                        fin_val = row['fin']
                        # Si es un objeto datetime de pyodbc, usarlo directamente
                        if isinstance(fin_val, datetime):
                            fecha_fin = fin_val
                        else:
                            # Si es string, parsear
                            fecha_fin_str = str(fin_val)
                            if 'T' in fecha_fin_str or '-' in fecha_fin_str:
                                fecha_fin = datetime.fromisoformat(fecha_fin_str.replace('Z', '+00:00'))
                except Exception as e:
                    print(f"[DEBUG] Error parseando fecha_fin: {e}, valor: {row.get('fin')}")
                    pass
                
                # Obtener ID de tarea - usar 'tarea_id' del alias o 'id' como fallback
                tarea_id = str(row.get('tarea_id', row.get('id', ''))).strip()
                if not tarea_id:
                    print(f"Advertencia: Tarea sin ID válido. Row: {row}")
                    continue
                
                # La columna en SQL Server se llama 'cantidad_recolectada', no 'alimento_recolectado'
                cantidad_recolectada = int(row.get('cantidad_recolectada', 0))
                
                tarea = TareaRecoleccion(
                    id=tarea_id,
                    alimento=alimento,
                    estado=EstadoTarea(row.get('estado', 'pendiente')),
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    alimento_recolectado=cantidad_recolectada
                )
                
                # Obtener hormigas_asignadas directamente de la columna
                try:
                    self._exec(cursor, "SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea.id,))
                    hormigas_row = cursor.fetchone()
                    if hormigas_row and hormigas_row[0] is not None:
                        cantidad_hormigas_bd = int(hormigas_row[0])
                        # Si hay hormigas asignadas en BD pero no en memoria, crear hormigas genéricas
                        if cantidad_hormigas_bd > 0 and len(tarea.hormigas_asignadas) == 0:
                            # Cargar asignaciones para obtener los IDs de hormigas
                            self._exec(cursor, """
                                SELECT hormiga_id FROM dbo.asignaciones_hormiga_tarea 
                                WHERE tarea_id = ?
                            """, (tarea.id,))
                            asignaciones = cursor.fetchall()
                            for asign in asignaciones:
                                hormiga_id = asign[0]
                                # Crear hormiga genérica (sin necesidad de que esté en tabla hormigas)
                                from ..models.hormiga import Hormiga
                                from ..models.estado_hormiga import EstadoHormiga
                                hormiga = Hormiga(
                                    id=str(hormiga_id),
                                    estado=EstadoHormiga.DISPONIBLE,
                                    capacidad_carga=5
                                )
                                tarea.agregar_hormiga(hormiga)
                except Exception as e:
                    print(f"[DEBUG] Error cargando hormigas_asignadas: {e}")
                
                # Obtener lote_id de la tarea
                try:
                    self._exec(cursor, """
                        SELECT TOP 1 lote_id FROM dbo.lotes_hormigas WHERE tarea_id = ?
                    """, (tarea.id,))
                    lote_row = cursor.fetchone()
                    
                    if lote_row:
                        lote_id = lote_row[0]
                        tarea.hormigas_lote_id = lote_id
                        # Si aún no hay hormigas cargadas, intentar cargarlas desde el lote
                        if len(tarea.hormigas_asignadas) == 0:
                            # Obtener hormigas desde el lote (si existen en tabla hormigas)
                            self._exec(cursor, """
                                SELECT h.* FROM dbo.hormigas h
                                JOIN dbo.asignaciones_hormiga_tarea aht ON h.id = aht.hormiga_id
                                WHERE aht.lote_id = ?
                            """, (lote_id,))
                    else:
                        # Fallback: obtener hormigas directamente por tarea_id
                        self._exec(cursor, """
                            SELECT h.* FROM dbo.hormigas h
                            JOIN dbo.asignaciones_hormiga_tarea aht ON h.id = aht.hormiga_id
                            WHERE aht.tarea_id = ? AND (aht.lote_id IS NULL OR aht.lote_id = '')
                        """, (tarea.id,))
                    
                    hrows = self._fetchall_dicts(cursor)
                    for hrow in hrows:
                        tarea.agregar_hormiga(Hormiga(
                            id=str(hrow.get('id', '')),
                            capacidad_carga=int(hrow.get('capacidad_carga', 5)),
                            estado=EstadoHormiga(hrow.get('estado', 'disponible')),
                            tiempo_vida=int(hrow.get('tiempo_vida', 3600)),
                            subsistema_origen=hrow.get('subsistema_origen')
                        ))
                except Exception as hormigas_error:
                    # Si no hay tabla de hormigas o asignaciones, continuar sin hormigas
                    print(f"Advertencia: No se pudieron cargar hormigas para tarea {tarea.id}: {hormigas_error}")
                
                tareas.append(tarea)
            
            print(f"[DEBUG] Total de tareas procesadas: {len(tareas)}")
            if len(tareas) > 0:
                print(f"[DEBUG] Primera tarea ID: {tareas[0].id}")
            return tareas
        except Exception as e:
            self.last_error = str(e)
            print(f"[ERROR] Error obteniendo tareas (SQL Server): {e}")
            import traceback
            traceback.print_exc()
            return []

    def guardar_evento(self, tipo_evento: str, descripcion: str, datos_adicionales: Dict[str, Any] = None):
        try:
            cursor = self.connection.cursor()
            datos_json = json.dumps(datos_adicionales) if datos_adicionales else None
            self._exec(cursor, """
                INSERT INTO dbo.Eventos (tipo_evento, descripcion, datos_adicionales)
                VALUES (?, ?, ?)
            """, (tipo_evento, descripcion, datos_json))
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error guardando evento (SQL Server): {e}")
            return False

    def obtener_eventos(self, limite: int = 100) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            self._exec(cursor, """
                SELECT TOP (?) * FROM dbo.Eventos ORDER BY fecha_evento DESC
            """, (limite,))
            rows = self._fetchall_dicts(cursor)
            eventos: List[Dict[str, Any]] = []
            for row in rows:
                eventos.append({
                    'id': row['id'],
                    'tipo_evento': row['tipo_evento'],
                    'descripcion': row['descripcion'],
                    'fecha_evento': row['fecha_evento'],
                    'datos_adicionales': json.loads(row['datos_adicionales']) if row.get('datos_adicionales') else None
                })
            return eventos
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo eventos (SQL Server): {e}")
            return []

    def cerrar(self):
        if self.connection:
            self.connection.close()
            print("Conexión a SQL Server cerrada")

    # Helpers unificados
    def actualizar_estado_tarea(self, tarea_id: str, nuevo_estado: str) -> bool:
        try:
            cursor = self.connection.cursor()
            self._exec(
                cursor,
                "UPDATE dbo.Tareas SET estado = ? WHERE id = ?",
                (nuevo_estado, tarea_id),
            )
            return cursor.rowcount > 0
        except Exception as e:
            self.last_error = str(e)
            print(f"Error actualizando estado de tarea (SQL Server): {e}")
            return False

    def guardar_mensaje(self, mensaje: Mensaje) -> bool:
        try:
            cursor = self.connection.cursor()
            # UPSERT manual
            self._exec(
                cursor,
                """
                UPDATE dbo.Mensajes SET
                    tipo = ?,
                    contenido = ?,
                    subsistema_origen = ?,
                    subsistema_destino = ?,
                    ttl = ?,
                    procesado = ?
                WHERE id = ?
                """,
                (
                    mensaje.tipo.value,
                    json.dumps(mensaje.contenido),
                    mensaje.subsistema_origen,
                    mensaje.subsistema_destino,
                    mensaje.ttl,
                    1 if mensaje.procesado else 0,
                    mensaje.id,
                ),
            )
            if cursor.rowcount == 0:
                self._exec(
                    cursor,
                    """
                    INSERT INTO dbo.Mensajes (id, tipo, contenido, subsistema_origen, subsistema_destino, ttl, procesado)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        mensaje.id,
                        mensaje.tipo.value,
                        json.dumps(mensaje.contenido),
                        mensaje.subsistema_origen,
                        mensaje.subsistema_destino,
                        mensaje.ttl,
                        1 if mensaje.procesado else 0,
                    ),
                )
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error guardando mensaje (SQL Server): {e}")
            return False

    def obtener_mensajes(self, subsistema_origen: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            if subsistema_origen:
                self._exec(
                    cursor,
                    "SELECT * FROM dbo.Mensajes WHERE subsistema_origen = ? ORDER BY fecha_creacion DESC",
                    (subsistema_origen,),
                )
            else:
                self._exec(cursor, "SELECT * FROM dbo.Mensajes ORDER BY fecha_creacion DESC")
            return self._fetchall_dicts(cursor)
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo mensajes (SQL Server): {e}")
            return []

    def crear_lote_hormigas(
        self, 
        lote_id: str, 
        tarea_id: str, 
        cantidad_enviada: int, 
        cantidad_requerida: int
    ) -> bool:
        """Crea un lote de hormigas con validación de cantidad (SQL Server)."""
        try:
            if cantidad_enviada < cantidad_requerida:
                self.last_error = f"Cantidad insuficiente de hormigas. Enviadas: {cantidad_enviada}, Requeridas: {cantidad_requerida}"
                return False
            
            cursor = self.connection.cursor()
            # Verificar si el lote ya existe
            self._exec(cursor, "SELECT COUNT(*) FROM dbo.lotes_hormigas WHERE lote_id = ?", (lote_id,))
            existe = cursor.fetchone()[0] > 0
            
            if existe:
                self.last_error = f"Lote {lote_id} ya existe"
                print(f"Lote {lote_id} ya existe en BD")
                return False
            
            # Insertar el lote
            self._exec(cursor, """
                INSERT INTO dbo.lotes_hormigas 
                (lote_id, tarea_id, cantidad_hormigas_enviadas, cantidad_hormigas_requeridas, estado)
                VALUES (?, ?, ?, ?, 'pendiente')
            """, (lote_id, tarea_id, cantidad_enviada, cantidad_requerida))
            
            print(f"Lote {lote_id} creado exitosamente en BD para tarea {tarea_id}")
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error creando lote de hormigas (SQL Server): {e}")
            return False
    
    def aceptar_lote_hormigas(self, lote_id: str) -> bool:
        """Acepta un lote de hormigas (SQL Server)."""
        try:
            cursor = self.connection.cursor()
            self._exec(cursor, """
                SELECT estado FROM dbo.lotes_hormigas WHERE lote_id = ?
            """, (lote_id,))
            row = cursor.fetchone()
            
            if not row:
                self.last_error = f"Lote {lote_id} no encontrado"
                return False
            
            if row[0] == 'en_uso':
                self.last_error = f"Lote {lote_id} ya está en uso"
                return False
            
            self._exec(cursor, """
                UPDATE dbo.lotes_hormigas 
                SET estado = 'aceptado', fecha_aceptacion = GETDATE()
                WHERE lote_id = ?
            """, (lote_id,))
            return cursor.rowcount > 0
        except Exception as e:
            self.last_error = str(e)
            print(f"Error aceptando lote (SQL Server): {e}")
            return False
    
    def marcar_lote_en_uso(self, lote_id: str) -> bool:
        """Marca un lote como en uso (SQL Server)."""
        try:
            cursor = self.connection.cursor()
            self._exec(cursor, """
                UPDATE dbo.lotes_hormigas 
                SET estado = 'en_uso'
                WHERE lote_id = ?
            """, (lote_id,))
            return cursor.rowcount > 0
        except Exception as e:
            self.last_error = str(e)
            print(f"Error marcando lote en uso (SQL Server): {e}")
            return False
    
    def verificar_lote_disponible(self, lote_id: str, cantidad_requerida: int) -> tuple[bool, Optional[str]]:
        """Verifica que un lote esté disponible (SQL Server)."""
        try:
            cursor = self.connection.cursor()
            self._exec(cursor, """
                SELECT estado, cantidad_hormigas_enviadas 
                FROM dbo.lotes_hormigas 
                WHERE lote_id = ?
            """, (lote_id,))
            row = cursor.fetchone()
            
            if not row:
                return False, f"Lote {lote_id} no encontrado"
            
            estado, cantidad_enviada = row[0], row[1]
            
            if estado == 'en_uso':
                return False, f"Lote {lote_id} ya está en uso"
            
            if cantidad_enviada < cantidad_requerida:
                return False, f"Lote {lote_id} tiene cantidad insuficiente. Tiene: {cantidad_enviada}, Requiere: {cantidad_requerida}"
            
            return True, None
        except Exception as e:
            return False, f"Error verificando lote: {str(e)}"
    
    def guardar_hormigas_en_lote(self, lote_id: str, hormigas: List[Hormiga]) -> bool:
        """Guarda las hormigas en un lote (SQL Server)."""
        try:
            cursor = self.connection.cursor()
            self._exec(cursor, "SELECT tarea_id FROM dbo.lotes_hormigas WHERE lote_id = ?", (lote_id,))
            row = cursor.fetchone()
            if not row:
                self.last_error = f"Lote {lote_id} no encontrado"
                return False
            
            tarea_id = row[0]
            
            for hormiga in hormigas:
                self._exec(cursor, """
                    IF NOT EXISTS (SELECT 1 FROM dbo.hormigas WHERE id = ?)
                    INSERT INTO dbo.hormigas (id, capacidad_carga, estado, tiempo_vida, subsistema_origen)
                    VALUES (?, ?, ?, ?, ?)
                """, (hormiga.id, hormiga.id, hormiga.capacidad_carga, 
                      hormiga.estado.value if hasattr(hormiga.estado, 'value') else str(hormiga.estado),
                      hormiga.tiempo_vida, hormiga.subsistema_origen))
                
                self._exec(cursor, """
                    IF NOT EXISTS (SELECT 1 FROM dbo.asignaciones_hormiga_tarea WHERE tarea_id = ? AND hormiga_id = ?)
                    INSERT INTO dbo.asignaciones_hormiga_tarea (tarea_id, hormiga_id, lote_id)
                    VALUES (?, ?, ?)
                """, (tarea_id, hormiga.id, tarea_id, hormiga.id, lote_id))
            
            return True
        except Exception as e:
            self.last_error = str(e)
            print(f"Error guardando hormigas en lote (SQL Server): {e}")
            return False
    
    def obtener_hormigas_por_lote(self, lote_id: str) -> List[Hormiga]:
        """Obtiene las hormigas de un lote (SQL Server)."""
        try:
            cursor = self.connection.cursor()
            self._exec(cursor, """
                SELECT h.* FROM dbo.hormigas h
                JOIN dbo.asignaciones_hormiga_tarea aht ON h.id = aht.hormiga_id
                WHERE aht.lote_id = ?
            """, (lote_id,))
            rows = self._fetchall_dicts(cursor)
            
            hormigas = []
            for row in rows:
                hormigas.append(Hormiga(
                    id=str(row.get('id', '')),
                    capacidad_carga=int(row.get('capacidad_carga', 5)),
                    estado=EstadoHormiga(row.get('estado', 'disponible')),
                    tiempo_vida=int(row.get('tiempo_vida', 3600)),
                    subsistema_origen=row.get('subsistema_origen')
                ))
            return hormigas
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo hormigas por lote (SQL Server): {e}")
            return []

    def obtener_estadisticas(self) -> Dict[str, Any]:
        try:
            cursor = self.connection.cursor()
            for name, sql in [
                ("total_tareas", "SELECT COUNT(*) AS c FROM dbo.Tareas"),
                ("tareas_activas", "SELECT COUNT(*) AS c FROM dbo.Tareas WHERE estado IN ('pendiente','en_proceso')"),
                ("tareas_completadas", "SELECT COUNT(*) AS c FROM dbo.Tareas WHERE estado = 'completada'"),
                ("total_alimentos", "SELECT COUNT(*) AS c FROM dbo.Alimentos"),
                ("alimentos_disponibles", "SELECT COUNT(*) AS c FROM dbo.Alimentos WHERE disponible = 1"),
                ("total_mensajes", "SELECT COUNT(*) AS c FROM dbo.Mensajes"),
                ("total_eventos", "SELECT COUNT(*) AS c FROM dbo.Eventos"),
            ]:
                self._exec(cursor, sql)
                locals()[name] = cursor.fetchone()[0]

            return {
                "tareas": {
                    "total": locals()["total_tareas"],
                    "activas": locals()["tareas_activas"],
                    "completadas": locals()["tareas_completadas"],
                },
                "alimentos": {
                    "total": locals()["total_alimentos"],
                    "disponibles": locals()["alimentos_disponibles"],
                },
                "mensajes": {"total": locals()["total_mensajes"]},
                "eventos": {"total": locals()["total_eventos"]},
                "fecha_consulta": datetime.now().isoformat(),
            }
        except Exception as e:
            self.last_error = str(e)
            print(f"Error obteniendo estadísticas (SQL Server): {e}")
            return {}


# Instancia global del gestor de base de datos, configurable por variable de entorno
DB_ENGINE = (os.getenv("DB_ENGINE") or "").lower()

def _try_sqlserver_autodetect() -> Optional[SqlServerDatabaseManager]:
    server = os.getenv("SQLSERVER_SERVER", "SHIRORYUU")
    database = os.getenv("SQLSERVER_DATABASE", "Hormiguero")
    # Preferir Driver 17 (común en tu equipo), luego 18
    driver = os.getenv("SQLSERVER_ODBC_DRIVER") or "ODBC Driver 17 for SQL Server"
    os.environ.setdefault("SQLSERVER_ODBC_DRIVER", driver)
    os.environ.setdefault("SQLSERVER_ENCRYPT", os.getenv("SQLSERVER_ENCRYPT", "no"))
    os.environ.setdefault("SQLSERVER_TRUST_SERVER_CERT", os.getenv("SQLSERVER_TRUST_SERVER_CERT", "yes"))
    try:
        return SqlServerDatabaseManager(server=server, database=database)
    except Exception as e:
        print(f"Autodetección SQL Server falló: {e}")
        return None

db_manager = None
if DB_ENGINE == "sqlserver":
    db_manager = _try_sqlserver_autodetect() or DatabaseManager()
elif DB_ENGINE == "sqlite":
    db_manager = DatabaseManager()
else:
    # Sin DB_ENGINE: intentar SQL Server primero, si falla caer a SQLite
    db_manager = _try_sqlserver_autodetect() or DatabaseManager()

