"""
Script para consultar y mostrar las evidencias reales guardadas en la base de datos.
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.recoleccion.database.database_manager import DatabaseManager

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

def print_info(message):
    print(f"[INFO] {message}")

# Conectar a la base de datos
print_header("CONSULTA DE EVIDENCIAS EN BASE DE DATOS")

# Intentar SQL Server primero
try:
    from src.recoleccion.database.database_manager import SqlServerDatabaseManager
    db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
    db_type = "sqlserver"
    print_success("Conectado a SQL Server: SHIRORYUU / Hormiguero")
    cursor = db.connection.cursor()
except Exception as e:
    # Fallback a SQLite
    print_info(f"No se pudo conectar a SQL Server: {e}")
    print_info("Usando SQLite...")
    db_path = "recoleccion.db"
    if os.path.exists(db_path):
        # Agregar columna si no existe
        db_temp = DatabaseManager(db_path)
        cursor_temp = db_temp.connection.cursor()
        try:
            cursor_temp.execute("ALTER TABLE tareas ADD COLUMN hormigas_asignadas INTEGER DEFAULT 0")
            db_temp.connection.commit()
            print_info("Columna hormigas_asignadas agregada a la tabla existente")
        except Exception:
            # La columna ya existe
            pass
        db_temp.cerrar()
    
    db = DatabaseManager(db_path)
    db_type = "sqlite"
    print_success(f"Usando SQLite: {db_path}")
    cursor = db.connection.cursor()

# Consultar todas las tareas con hormigas_asignadas
print_header("EVIDENCIAS: Todas las Tareas con hormigas_asignadas")

if db_type == "sqlite":
    cursor.execute("""
        SELECT t.id, t.alimento_id, t.estado, t.fecha_inicio, t.fecha_fin,
               t.alimento_recolectado, t.hormigas_asignadas,
               a.nombre as alimento_nombre
        FROM tareas t
        LEFT JOIN alimentos a ON t.alimento_id = a.id
        ORDER BY t.fecha_creacion DESC
        LIMIT 20
    """)
else:
    # SQL Server
    db._exec(cursor, """
        SELECT TOP 20
            t.id, t.alimento_id, t.estado, t.inicio, t.fin,
            t.cantidad_recolectada, t.hormigas_asignadas,
            a.nombre as alimento_nombre
        FROM dbo.Tareas t
        LEFT JOIN dbo.Alimentos a ON CAST(t.alimento_id AS VARCHAR) = CAST(a.id AS VARCHAR)
        ORDER BY t.id DESC
    """)

rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

if rows:
    print(f"\nTotal de tareas encontradas: {len(rows)}")
    print(f"\nColumnas: {', '.join(columns)}")
    print_section("Registros de Tareas")
    
    for i, row in enumerate(rows, 1):
        print(f"\n  Tarea {i}:")
        for col, val in zip(columns, row):
            if col == 'hormigas_asignadas':
                status = "OK" if val is not None and val > 0 else "SIN HORMIGAS"
                print(f"    {col}: {val} ({status})")
            else:
                print(f"    {col}: {val}")
else:
    print_info("No se encontraron tareas en la base de datos")

# Consultar estadísticas
print_header("ESTADÍSTICAS DE hormigas_asignadas")

if db_type == "sqlite":
    cursor.execute("""
        SELECT 
            COUNT(*) as total_tareas,
            SUM(CASE WHEN hormigas_asignadas = 0 THEN 1 ELSE 0 END) as sin_hormigas,
            SUM(CASE WHEN hormigas_asignadas > 0 THEN 1 ELSE 0 END) as con_hormigas,
            AVG(hormigas_asignadas) as promedio_hormigas,
            MAX(hormigas_asignadas) as max_hormigas,
            MIN(hormigas_asignadas) as min_hormigas
        FROM tareas
    """)
else:
    db._exec(cursor, """
        SELECT 
            COUNT(*) as total_tareas,
            SUM(CASE WHEN hormigas_asignadas = 0 THEN 1 ELSE 0 END) as sin_hormigas,
            SUM(CASE WHEN hormigas_asignadas > 0 THEN 1 ELSE 0 END) as con_hormigas,
            AVG(CAST(hormigas_asignadas AS FLOAT)) as promedio_hormigas,
            MAX(hormigas_asignadas) as max_hormigas,
            MIN(hormigas_asignadas) as min_hormigas
        FROM dbo.Tareas
    """)

stats = cursor.fetchone()
if stats:
    stats_cols = [description[0] for description in cursor.description]
    print_section("Estadísticas Generales")
    for col, val in zip(stats_cols, stats):
        if val is not None:
            if col == 'promedio_hormigas':
                print(f"  {col}: {float(val):.2f}")
            else:
                print(f"  {col}: {int(val)}")

# Consultar tareas por estado
print_header("TAREAS POR ESTADO CON hormigas_asignadas")

if db_type == "sqlite":
    cursor.execute("""
        SELECT estado, 
               COUNT(*) as cantidad,
               AVG(hormigas_asignadas) as promedio_hormigas,
               SUM(hormigas_asignadas) as total_hormigas
        FROM tareas
        GROUP BY estado
        ORDER BY cantidad DESC
    """)
else:
    db._exec(cursor, """
        SELECT estado, 
               COUNT(*) as cantidad,
               AVG(CAST(hormigas_asignadas AS FLOAT)) as promedio_hormigas,
               SUM(hormigas_asignadas) as total_hormigas
        FROM dbo.Tareas
        GROUP BY estado
        ORDER BY cantidad DESC
    """)

rows = cursor.fetchall()
if rows:
    print_section("Distribución por Estado")
    cols = [description[0] for description in cursor.description]
    for row in rows:
        print(f"\n  Estado: {row[0]}")
        for col, val in zip(cols[1:], row[1:]):
            if val is not None:
                if 'promedio' in col:
                    print(f"    {col}: {float(val):.2f}")
                else:
                    print(f"    {col}: {int(val)}")

# Consultar últimas tareas modificadas
print_header("ÚLTIMAS 10 TAREAS MODIFICADAS")

if db_type == "sqlite":
    cursor.execute("""
        SELECT id, estado, hormigas_asignadas, fecha_inicio, fecha_fin
        FROM tareas
        ORDER BY fecha_creacion DESC
        LIMIT 10
    """)
else:
    db._exec(cursor, """
        SELECT TOP 10 id, estado, hormigas_asignadas, inicio, fin
        FROM dbo.Tareas
        ORDER BY id DESC
    """)

rows = cursor.fetchall()
if rows:
    print_section("Últimas Tareas")
    cols = [description[0] for description in cursor.description]
    for i, row in enumerate(rows, 1):
        print(f"\n  Tarea {i}:")
        for col, val in zip(cols, row):
            print(f"    {col}: {val}")

print_header("CONSULTA COMPLETADA")
print(f"Base de datos: {db_type}")
print(f"Fecha de consulta: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

