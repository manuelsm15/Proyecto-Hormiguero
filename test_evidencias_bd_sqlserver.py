"""
Script de pruebas automáticas para validar evidencias en SQL Server.
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.recoleccion.database.database_manager import DatabaseManager
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.estado_tarea import EstadoTarea
from src.recoleccion.models.estado_hormiga import EstadoHormiga

def print_header(text):
    print(f"\n{'='*80}")
    print(f"{text}")
    print(f"{'='*80}")

def print_section(text):
    print(f"\n{'-'*80}")
    print(f"{text}")
    print(f"{'-'*80}")

def print_success(message):
    print(f"[OK] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_info(message):
    print(f"[INFO] {message}")

# Intentar conectar a SQL Server
print_header("PRUEBAS AUTOMÁTICAS EN SQL SERVER")
try:
    db = DatabaseManager(server="SHIRORYUU", database="Hormiguero")
    db_type = "sqlserver"
    print_success("Conectado a SQL Server: SHIRORYUU / Hormiguero")
except Exception as e:
    print_error(f"No se pudo conectar a SQL Server: {e}")
    print_info("Usando SQLite como alternativa...")
    db_path = "test_evidencias_sqlserver.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    db = DatabaseManager(db_path)
    db_type = "sqlite"
    print_success(f"Usando SQLite: {db_path}")

cursor = db.connection.cursor()

# Crear alimento
print_header("PASO 1: Crear Alimento")
alimento_id = f"ALIMENTO_SQL_{datetime.now().strftime('%Y%m%d%H%M%S')}"
alimento = Alimento(
    id=alimento_id,
    nombre="Alimento SQL Server",
    cantidad_hormigas_necesarias=4,
    puntos_stock=30,
    tiempo_recoleccion=180
)

if db.guardar_alimento(alimento):
    print_success(f"Alimento creado: {alimento_id}")
else:
    print_error(f"No se pudo crear el alimento: {db.last_error}")
    exit(1)

# Crear tarea
print_header("PASO 2: Crear Tarea")
tarea_id = f"TAREA_SQL_{datetime.now().strftime('%Y%m%d%H%M%S')}"
tarea = TareaRecoleccion(id=tarea_id, alimento=alimento)

if db.guardar_tarea(tarea):
    print_success(f"Tarea creada: {tarea_id}")
    print_info(f"  Estado inicial: {tarea.estado.value}")
    print_info(f"  Hormigas asignadas: {len(tarea.hormigas_asignadas)}")
    
    # Verificar hormigas_asignadas
    if db_type == "sqlite":
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", (tarea_id,))
    else:
        db._exec(cursor, "SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    result = cursor.fetchone()
    if result:
        print_info(f"  hormigas_asignadas en BD: {result[0]}")
        if result[0] == 0:
            print_success("hormigas_asignadas = 0 (correcto)")
else:
    print_error(f"No se pudo crear la tarea: {db.last_error}")
    exit(1)

# Agregar hormigas
print_header("PASO 3: Agregar Hormigas")
h1 = Hormiga(id="H1_SQL", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
h2 = Hormiga(id="H2_SQL", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
h3 = Hormiga(id="H3_SQL", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
h4 = Hormiga(id="H4_SQL", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)

tarea.agregar_hormiga(h1)
tarea.agregar_hormiga(h2)
tarea.agregar_hormiga(h3)
tarea.agregar_hormiga(h4)

print_info(f"Hormigas agregadas: {len(tarea.hormigas_asignadas)}")

if db.guardar_tarea(tarea):
    print_success("Tarea guardada con 4 hormigas")
    
    # Verificar hormigas_asignadas
    if db_type == "sqlite":
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", (tarea_id,))
    else:
        db._exec(cursor, "SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    result = cursor.fetchone()
    if result:
        print_info(f"  hormigas_asignadas en BD: {result[0]}")
        if result[0] == 4:
            print_success("hormigas_asignadas = 4 (correcto)")
        else:
            print_error(f"Esperado: 4, Encontrado: {result[0]}")

# Iniciar tarea
print_header("PASO 4: Iniciar Tarea")
tarea.iniciar_tarea()
if db.guardar_tarea(tarea):
    print_success("Tarea iniciada")
    
    # Verificar que se mantiene
    if db_type == "sqlite":
        cursor.execute("SELECT hormigas_asignadas, estado FROM tareas WHERE id = ?", (tarea_id,))
    else:
        db._exec(cursor, "SELECT hormigas_asignadas, estado FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    result = cursor.fetchone()
    if result:
        print_info(f"  Estado: {result[1]}")
        print_info(f"  hormigas_asignadas: {result[0]}")
        if result[0] == 4:
            print_success("hormigas_asignadas se mantiene: 4")

# Completar tarea
print_header("PASO 5: Completar Tarea")
tarea.completar_tarea(30)
if db.guardar_tarea(tarea):
    print_success("Tarea completada")
    
    # Verificar que se mantiene
    if db_type == "sqlite":
        cursor.execute("SELECT hormigas_asignadas, estado FROM tareas WHERE id = ?", (tarea_id,))
    else:
        db._exec(cursor, "SELECT hormigas_asignadas, estado FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    result = cursor.fetchone()
    if result:
        print_info(f"  Estado: {result[1]}")
        print_info(f"  hormigas_asignadas: {result[0]}")
        if result[0] == 4:
            print_success("hormigas_asignadas se mantiene después de completar: 4")

# Mostrar evidencia final
print_header("EVIDENCIA FINAL EN BASE DE DATOS")
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
    print_section("Datos Completos de la Tarea")
    columns = [description[0] for description in cursor.description]
    for col, val in zip(columns, result):
        print(f"  {col}: {val}")
    
    hormigas_idx = columns.index('hormigas_asignadas')
    if result[hormigas_idx] == 4:
        print_success(f"\nhormigas_asignadas = {result[hormigas_idx]} (VALIDADO)")
    else:
        print_error(f"\nhormigas_asignadas = {result[hormigas_idx]} (ESPERADO: 4)")

print_header("PRUEBAS COMPLETADAS")
print(f"Base de datos: {db_type}")
print(f"Alimento ID: {alimento_id}")
print(f"Tarea ID: {tarea_id}")



