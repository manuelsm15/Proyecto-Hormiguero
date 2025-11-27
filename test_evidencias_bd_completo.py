"""
Script completo de pruebas automáticas que valida los datos guardados en la BD
y muestra las evidencias de lo que se guardó.
"""
import sys
import os
from datetime import datetime
import json

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.recoleccion.database.database_manager import DatabaseManager
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.estado_tarea import EstadoTarea
from src.recoleccion.models.estado_hormiga import EstadoHormiga

def print_header(text):
    """Imprime un encabezado."""
    print(f"\n{'='*80}")
    print(f"{text}")
    print(f"{'='*80}")

def print_section(text):
    """Imprime una sección."""
    print(f"\n{'-'*80}")
    print(f"{text}")
    print(f"{'-'*80}")

def print_success(message):
    """Imprime un mensaje de éxito."""
    print(f"[OK] {message}")

def print_error(message):
    """Imprime un mensaje de error."""
    print(f"[ERROR] {message}")

def print_info(message):
    """Imprime un mensaje informativo."""
    print(f"[INFO] {message}")

def mostrar_evidencia_tabla(cursor, tabla, descripcion, db_type="sqlite"):
    """Muestra el contenido de una tabla como evidencia."""
    print_section(f"EVIDENCIA: {descripcion}")
    try:
        if db_type == "sqlite":
            cursor.execute(f"SELECT * FROM {tabla}")
        else:
            # SQL Server
            cursor.execute(f"SELECT * FROM dbo.{tabla}")
        
        rows = cursor.fetchall()
        if rows:
            # Obtener nombres de columnas
            columns = [description[0] for description in cursor.description]
            print(f"Total de registros: {len(rows)}")
            print(f"Columnas: {', '.join(columns)}")
            print("\nRegistros:")
            for i, row in enumerate(rows, 1):
                print(f"\n  Registro {i}:")
                for col, val in zip(columns, row):
                    print(f"    {col}: {val}")
        else:
            print("  No hay registros en la tabla")
    except Exception as e:
        print_error(f"Error al consultar tabla {tabla}: {e}")

# Determinar qué base de datos usar
print_header("INICIALIZACIÓN DE PRUEBAS AUTOMÁTICAS COMPLETAS")
print("Determinando base de datos a usar...")

try:
    # Intentar usar SQL Server si está disponible
    db = DatabaseManager(server="SHIRORYUU", database="Hormiguero")
    db_type = "sqlserver"
    print_success(f"Conectado a SQL Server: SHIRORYUU / Hormiguero")
except Exception as e:
    # Fallback a SQLite
    db_path = "test_evidencias_bd.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    db = DatabaseManager(db_path)
    db_type = "sqlite"
    print_success(f"Usando SQLite: {db_path}")

cursor = db.connection.cursor()

# PASO 1: Crear alimento
print_header("PASO 1: Crear Alimento")
alimento_id = f"ALIMENTO_EVID_{datetime.now().strftime('%Y%m%d%H%M%S')}"
alimento = Alimento(
    id=alimento_id,
    nombre="Alimento de Evidencia",
    cantidad_hormigas_necesarias=3,
    puntos_stock=25,
    tiempo_recoleccion=120
)

if db.guardar_alimento(alimento):
    print_success(f"Alimento creado: {alimento_id}")
    print_info(f"  Nombre: {alimento.nombre}")
    print_info(f"  Hormigas necesarias: {alimento.cantidad_hormigas_necesarias}")
    print_info(f"  Puntos stock: {alimento.puntos_stock}")
    
    # Mostrar evidencia
    mostrar_evidencia_tabla(cursor, "alimentos", "Tabla Alimentos después de crear", db_type)
else:
    print_error(f"No se pudo crear el alimento: {db.last_error}")
    exit(1)

# PASO 2: Crear tarea sin hormigas
print_header("PASO 2: Crear Tarea sin Hormigas")
tarea_id = f"TAREA_EVID_{datetime.now().strftime('%Y%m%d%H%M%S')}"
tarea = TareaRecoleccion(id=tarea_id, alimento=alimento)

if db.guardar_tarea(tarea):
    print_success(f"Tarea creada: {tarea_id}")
    print_info(f"  Estado: {tarea.estado.value}")
    print_info(f"  Hormigas asignadas: {len(tarea.hormigas_asignadas)}")
    
    # Mostrar evidencia
    mostrar_evidencia_tabla(cursor, "tareas", "Tabla Tareas después de crear (sin hormigas)", db_type)
    
    # Verificar columna hormigas_asignadas
    if db_type == "sqlite":
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", (tarea_id,))
    else:
        db._exec(cursor, "SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    result = cursor.fetchone()
    if result:
        print_info(f"  Columna hormigas_asignadas en BD: {result[0]}")
        if result[0] == 0:
            print_success("hormigas_asignadas = 0 (correcto)")
        else:
            print_error(f"hormigas_asignadas debería ser 0, es {result[0]}")
else:
    print_error(f"No se pudo crear la tarea: {db.last_error}")
    exit(1)

# PASO 3: Agregar hormigas y guardar
print_header("PASO 3: Agregar Hormigas y Guardar")
h1 = Hormiga(id="H1_EVID", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
h2 = Hormiga(id="H2_EVID", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
h3 = Hormiga(id="H3_EVID", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)

tarea.agregar_hormiga(h1)
tarea.agregar_hormiga(h2)
tarea.agregar_hormiga(h3)

print_info(f"Hormigas agregadas en memoria: {len(tarea.hormigas_asignadas)}")

if db.guardar_tarea(tarea):
    print_success("Tarea guardada con 3 hormigas asignadas")
    
    # Mostrar evidencia
    mostrar_evidencia_tabla(cursor, "tareas", "Tabla Tareas después de agregar hormigas", db_type)
    
    # Verificar columna hormigas_asignadas
    if db_type == "sqlite":
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", (tarea_id,))
    else:
        db._exec(cursor, "SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    result = cursor.fetchone()
    if result:
        print_info(f"  Columna hormigas_asignadas en BD: {result[0]}")
        if result[0] == 3:
            print_success("hormigas_asignadas = 3 (correcto)")
        else:
            print_error(f"hormigas_asignadas debería ser 3, es {result[0]}")
    
    # Mostrar evidencia de asignaciones
    mostrar_evidencia_tabla(cursor, "asignaciones_hormiga_tarea", "Tabla Asignaciones después de agregar hormigas", db_type)
else:
    print_error(f"No se pudo guardar la tarea: {db.last_error}")

# PASO 4: Iniciar tarea
print_header("PASO 4: Iniciar Tarea")
tarea.iniciar_tarea()
print_info(f"Estado cambiado a: {tarea.estado.value}")
print_info(f"Fecha inicio: {tarea.fecha_inicio}")

if db.guardar_tarea(tarea):
    print_success("Tarea iniciada y guardada")
    
    # Mostrar evidencia
    mostrar_evidencia_tabla(cursor, "tareas", "Tabla Tareas después de iniciar", db_type)
    
    # Verificar que hormigas_asignadas se mantiene
    if db_type == "sqlite":
        cursor.execute("SELECT hormigas_asignadas, estado FROM tareas WHERE id = ?", (tarea_id,))
    else:
        db._exec(cursor, "SELECT hormigas_asignadas, estado FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    result = cursor.fetchone()
    if result:
        print_info(f"  Estado en BD: {result[1]}")
        print_info(f"  hormigas_asignadas en BD: {result[0]}")
        if result[0] == 3:
            print_success("hormigas_asignadas se mantiene después de iniciar: 3")
        else:
            print_error(f"hormigas_asignadas debería ser 3, es {result[0]}")
else:
    print_error(f"No se pudo guardar la tarea iniciada: {db.last_error}")

# PASO 5: Completar tarea
print_header("PASO 5: Completar Tarea")
tarea.completar_tarea(25)
print_info(f"Estado cambiado a: {tarea.estado.value}")
print_info(f"Fecha fin: {tarea.fecha_fin}")
print_info(f"Alimento recolectado: {tarea.alimento_recolectado}")

if db.guardar_tarea(tarea):
    print_success("Tarea completada y guardada")
    
    # Mostrar evidencia
    mostrar_evidencia_tabla(cursor, "tareas", "Tabla Tareas después de completar", db_type)
    
    # Verificar que hormigas_asignadas se mantiene
    if db_type == "sqlite":
        cursor.execute("SELECT hormigas_asignadas, estado, alimento_recolectado FROM tareas WHERE id = ?", (tarea_id,))
    else:
        db._exec(cursor, "SELECT hormigas_asignadas, estado, cantidad_recolectada FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    result = cursor.fetchone()
    if result:
        print_info(f"  Estado en BD: {result[1]}")
        print_info(f"  Alimento recolectado en BD: {result[2]}")
        print_info(f"  hormigas_asignadas en BD: {result[0]}")
        if result[0] == 3:
            print_success("hormigas_asignadas se mantiene después de completar: 3")
        else:
            print_error(f"hormigas_asignadas debería ser 3, es {result[0]}")
else:
    print_error(f"No se pudo guardar la tarea completada: {db.last_error}")

# PASO 6: Actualizar estado (sin afectar hormigas_asignadas)
print_header("PASO 6: Actualizar Estado (Validar que no afecta hormigas_asignadas)")
if db.actualizar_estado_tarea(tarea_id, EstadoTarea.COMPLETADA.value):
    print_success("Estado actualizado usando actualizar_estado_tarea")
    
    # Verificar que hormigas_asignadas NO se eliminó
    if db_type == "sqlite":
        cursor.execute("SELECT hormigas_asignadas, estado FROM tareas WHERE id = ?", (tarea_id,))
    else:
        db._exec(cursor, "SELECT hormigas_asignadas, estado FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    result = cursor.fetchone()
    if result:
        print_info(f"  Estado en BD: {result[1]}")
        print_info(f"  hormigas_asignadas en BD: {result[0]}")
        if result[0] == 3:
            print_success("hormigas_asignadas NO se eliminó al actualizar estado: 3")
        else:
            print_error(f"hormigas_asignadas debería ser 3, es {result[0]}")
else:
    print_error(f"No se pudo actualizar el estado: {db.last_error}")

# PASO 7: Consultar tarea desde BD
print_header("PASO 7: Consultar Tarea desde BD (Validar carga completa)")
tareas_bd = db.obtener_tareas()
tarea_cargada = next((t for t in tareas_bd if t.id == tarea_id), None)

if tarea_cargada:
    print_success("Tarea encontrada en BD")
    print_info(f"  ID: {tarea_cargada.id}")
    print_info(f"  Estado: {tarea_cargada.estado.value}")
    print_info(f"  Alimento: {tarea_cargada.alimento.nombre}")
    print_info(f"  Hormigas asignadas (cargadas): {len(tarea_cargada.hormigas_asignadas)}")
    print_info(f"  Fecha inicio: {tarea_cargada.fecha_inicio}")
    print_info(f"  Fecha fin: {tarea_cargada.fecha_fin}")
    print_info(f"  Alimento recolectado: {tarea_cargada.alimento_recolectado}")
    
    # Verificar columna directamente
    if db_type == "sqlite":
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", (tarea_id,))
    else:
        db._exec(cursor, "SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    result = cursor.fetchone()
    if result:
        print_info(f"  hormigas_asignadas (columna BD): {result[0]}")
        if result[0] == 3:
            print_success("Columna hormigas_asignadas tiene el valor correcto: 3")
        else:
            print_error(f"Columna debería ser 3, es {result[0]}")
else:
    print_error("Tarea no encontrada al cargar desde BD")

# PASO 8: Resumen final de evidencias
print_header("RESUMEN FINAL DE EVIDENCIAS EN BASE DE DATOS")

# Mostrar todas las tablas relevantes
print_section("EVIDENCIA COMPLETA: Tabla Alimentos")
mostrar_evidencia_tabla(cursor, "alimentos", "Todos los alimentos", db_type)

print_section("EVIDENCIA COMPLETA: Tabla Tareas")
mostrar_evidencia_tabla(cursor, "tareas", "Todas las tareas", db_type)

print_section("EVIDENCIA COMPLETA: Tabla Asignaciones")
mostrar_evidencia_tabla(cursor, "asignaciones_hormiga_tarea", "Todas las asignaciones", db_type)

# Consulta específica de la tarea de prueba
print_section("EVIDENCIA ESPECÍFICA: Tarea de Prueba")
if db_type == "sqlite":
    cursor.execute("""
        SELECT t.id, t.alimento_id, t.estado, t.fecha_inicio, t.fecha_fin, 
               t.alimento_recolectado, t.hormigas_asignadas,
               a.nombre as alimento_nombre
        FROM tareas t
        JOIN alimentos a ON t.alimento_id = a.id
        WHERE t.id = ?
    """, (tarea_id,))
else:
    db._exec(cursor, """
        SELECT t.id, t.alimento_id, t.estado, t.inicio, t.fin, 
               t.cantidad_recolectada, t.hormigas_asignadas,
               a.nombre as alimento_nombre
        FROM dbo.Tareas t
        JOIN dbo.Alimentos a ON CAST(t.alimento_id AS VARCHAR) = CAST(a.id AS VARCHAR)
        WHERE t.id = ?
    """, (tarea_id,))

result = cursor.fetchone()
if result:
    print("\nDatos completos de la tarea en BD:")
    columns = [description[0] for description in cursor.description]
    for col, val in zip(columns, result):
        print(f"  {col}: {val}")
    
    # Validar hormigas_asignadas
    hormigas_idx = columns.index('hormigas_asignadas')
    if result[hormigas_idx] == 3:
        print_success(f"\nhormigas_asignadas = {result[hormigas_idx]} (VALIDADO)")
    else:
        print_error(f"\nhormigas_asignadas = {result[hormigas_idx]} (ESPERADO: 3)")

# Cerrar conexión
if db_type == "sqlite":
    db.cerrar()
    print(f"\n[INFO] Base de datos de prueba: {db_path}")
    print("[INFO] Puedes eliminar manualmente el archivo si lo deseas")
else:
    print(f"\n[INFO] Datos guardados en SQL Server: SHIRORYUU / Hormiguero")

print_header("PRUEBAS AUTOMÁTICAS COMPLETADAS")
print(f"Alimento ID: {alimento_id}")
print(f"Tarea ID: {tarea_id}")
print(f"\nTodas las evidencias se muestran arriba. Revisa los resultados.")

