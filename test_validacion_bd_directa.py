"""
Script de prueba para validar directamente en la BD que hormigas_asignadas se guarda correctamente.
"""
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.recoleccion.database.database_manager import DatabaseManager
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.estado_tarea import EstadoTarea
from src.recoleccion.models.estado_hormiga import EstadoHormiga

def print_step(step_num, description):
    """Imprime un paso de la prueba."""
    print(f"\n{'='*80}")
    print(f"PASO {step_num}: {description}")
    print(f"{'='*80}")

def print_success(message):
    """Imprime un mensaje de éxito."""
    print(f"[OK] {message}")

def print_error(message):
    """Imprime un mensaje de error."""
    print(f"[ERROR] {message}")

def print_info(message):
    """Imprime un mensaje informativo."""
    print(f"[INFO] {message}")

# Determinar qué base de datos usar
print("Inicializando base de datos...")
try:
    # Intentar usar SQL Server si está disponible
    db = DatabaseManager(server="SHIRORYUU", database="Hormiguero")
    db_type = "SQL Server"
    print_success(f"Conectado a {db_type}: SHIRORYUU / Hormiguero")
except Exception as e:
    # Fallback a SQLite
    db_path = "test_validacion_hormigas.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    db = DatabaseManager(db_path)
    db_type = "SQLite"
    print_success(f"Usando {db_type}: {db_path}")

# La base de datos se inicializa automáticamente en el constructor

# Crear un alimento
print_step(1, "Crear un alimento")
alimento_id = f"ALIMENTO_TEST_{datetime.now().strftime('%Y%m%d%H%M%S')}"
alimento = Alimento(
    id=alimento_id,
    nombre="Alimento de Prueba BD",
    cantidad_hormigas_necesarias=3,
    puntos_stock=20,
    tiempo_recoleccion=60
)
if db.guardar_alimento(alimento):
    print_success(f"Alimento creado: {alimento_id}")
else:
    print_error(f"No se pudo crear el alimento: {db.last_error}")
    exit(1)

# Crear una tarea sin hormigas
print_step(2, "Crear una tarea sin hormigas asignadas")
tarea_id = f"TAREA_TEST_{datetime.now().strftime('%Y%m%d%H%M%S')}"
tarea = TareaRecoleccion(id=tarea_id, alimento=alimento)
if db.guardar_tarea(tarea):
    print_success(f"Tarea creada: {tarea_id}")
    print_info(f"  Estado: {tarea.estado.value}")
    print_info(f"  Hormigas asignadas: {len(tarea.hormigas_asignadas)}")
else:
    print_error(f"No se pudo crear la tarea: {db.last_error}")
    exit(1)

# Verificar que hormigas_asignadas es 0 inicialmente
print_step(3, "Verificar que hormigas_asignadas es 0 inicialmente")
tareas = db.obtener_tareas()
tarea_bd = next((t for t in tareas if t.id == tarea_id), None)
if tarea_bd:
    hormigas_count = len(tarea_bd.hormigas_asignadas)
    print_info(f"  Hormigas asignadas en BD: {hormigas_count}")
    if hormigas_count == 0:
        print_success("hormigas_asignadas es 0 inicialmente (correcto)")
    else:
        print_error(f"Se esperaban 0 hormigas, se encontraron {hormigas_count}")
else:
    print_error("Tarea no encontrada en BD")

# Agregar hormigas a la tarea
print_step(4, "Agregar 3 hormigas a la tarea")
h1 = Hormiga(id="H1_TEST", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
h2 = Hormiga(id="H2_TEST", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
h3 = Hormiga(id="H3_TEST", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)

tarea.agregar_hormiga(h1)
tarea.agregar_hormiga(h2)
tarea.agregar_hormiga(h3)

print_info(f"  Hormigas agregadas en memoria: {len(tarea.hormigas_asignadas)}")
print_success("3 hormigas agregadas a la tarea en memoria")
print_info("  Nota: Las hormigas se guardarán automáticamente al guardar la tarea")

# Guardar la tarea con hormigas
print_step(5, "Guardar la tarea con hormigas asignadas")
if db.guardar_tarea(tarea):
    print_success("Tarea guardada con hormigas asignadas")
else:
    print_error(f"No se pudo guardar la tarea: {db.last_error}")
    exit(1)

# Verificar que hormigas_asignadas se guardó correctamente
print_step(6, "Verificar que hormigas_asignadas se guardó correctamente en BD")
tareas = db.obtener_tareas()
tarea_bd = next((t for t in tareas if t.id == tarea_id), None)
if tarea_bd:
    hormigas_count = len(tarea_bd.hormigas_asignadas)
    print_info(f"  Hormigas asignadas en BD: {hormigas_count}")
    if hormigas_count == 3:
        print_success(f"hormigas_asignadas se guardó correctamente: {hormigas_count}")
        for i, hormiga in enumerate(tarea_bd.hormigas_asignadas, 1):
            print_info(f"    Hormiga {i}: {hormiga.id} - Estado: {hormiga.estado.value}")
    else:
        print_error(f"Se esperaban 3 hormigas, se encontraron {hormigas_count}")
else:
    print_error("Tarea no encontrada en BD después de guardar")

# Consultar directamente la columna hormigas_asignadas en la tabla
print_step(7, "Consultar columna hormigas_asignadas directamente en la tabla")
try:
    if db_type == "SQLite":
        cursor = db.connection.cursor()
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", (tarea_id,))
        result = cursor.fetchone()
        if result:
            valor_columna = result[0]
            print_info(f"  Valor en columna hormigas_asignadas: {valor_columna}")
            if valor_columna == 3:
                print_success(f"Columna hormigas_asignadas tiene el valor correcto: {valor_columna}")
            else:
                print_error(f"Valor incorrecto. Esperado: 3, Encontrado: {valor_columna}")
        else:
            print_error("No se encontró la tarea en la tabla")
    else:
        # SQL Server
        cursor = db.connection.cursor()
        db._exec(cursor, "SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea_id,))
        result = cursor.fetchone()
        if result:
            valor_columna = result[0]
            print_info(f"  Valor en columna hormigas_asignadas: {valor_columna}")
            if valor_columna == 3:
                print_success(f"Columna hormigas_asignadas tiene el valor correcto: {valor_columna}")
            else:
                print_error(f"Valor incorrecto. Esperado: 3, Encontrado: {valor_columna}")
        else:
            print_error("No se encontró la tarea en la tabla")
except Exception as e:
    print_error(f"Error al consultar columna: {e}")

# Iniciar la tarea
print_step(8, "Iniciar la tarea")
tarea.iniciar_tarea()
if db.guardar_tarea(tarea):
    print_success("Tarea iniciada y guardada")
    print_info(f"  Estado: {tarea.estado.value}")
    print_info(f"  Fecha inicio: {tarea.fecha_inicio}")
else:
    print_error(f"No se pudo guardar la tarea iniciada: {db.last_error}")

# Verificar que hormigas_asignadas se mantiene después de iniciar
print_step(9, "Verificar que hormigas_asignadas se mantiene después de iniciar")
tareas = db.obtener_tareas()
tarea_bd = next((t for t in tareas if t.id == tarea_id), None)
if tarea_bd:
    hormigas_count = len(tarea_bd.hormigas_asignadas)
    print_info(f"  Estado: {tarea_bd.estado.value}")
    print_info(f"  Hormigas asignadas: {hormigas_count}")
    if hormigas_count == 3:
        print_success(f"hormigas_asignadas se mantiene después de iniciar: {hormigas_count}")
    else:
        print_error(f"hormigas_asignadas no se mantiene. Esperado: 3, Encontrado: {hormigas_count}")
    
    # Verificar columna directamente
    try:
        if db_type == "SQLite":
            cursor = db.connection.cursor()
            cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", (tarea_id,))
            result = cursor.fetchone()
            if result and result[0] == 3:
                print_success(f"Columna hormigas_asignadas se mantiene: {result[0]}")
            else:
                print_error(f"Columna no se mantiene. Valor: {result[0] if result else 'None'}")
        else:
            cursor = db.connection.cursor()
            db._exec(cursor, "SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea_id,))
            result = cursor.fetchone()
            if result and result[0] == 3:
                print_success(f"Columna hormigas_asignadas se mantiene: {result[0]}")
            else:
                print_error(f"Columna no se mantiene. Valor: {result[0] if result else 'None'}")
    except Exception as e:
        print_error(f"Error al verificar columna: {e}")
else:
    print_error("Tarea no encontrada después de iniciar")

# Completar la tarea
print_step(10, "Completar la tarea")
tarea.completar_tarea(20)
if db.guardar_tarea(tarea):
    print_success("Tarea completada y guardada")
    print_info(f"  Estado: {tarea.estado.value}")
    print_info(f"  Alimento recolectado: {tarea.alimento_recolectado}")
else:
    print_error(f"No se pudo guardar la tarea completada: {db.last_error}")

# Verificar que hormigas_asignadas se mantiene después de completar
print_step(11, "Verificar que hormigas_asignadas se mantiene después de completar")
tareas = db.obtener_tareas()
tarea_bd = next((t for t in tareas if t.id == tarea_id), None)
if tarea_bd:
    hormigas_count = len(tarea_bd.hormigas_asignadas)
    print_info(f"  Estado: {tarea_bd.estado.value}")
    print_info(f"  Hormigas asignadas: {hormigas_count}")
    if hormigas_count == 3:
        print_success(f"hormigas_asignadas se mantiene después de completar: {hormigas_count}")
    else:
        print_error(f"hormigas_asignadas no se mantiene. Esperado: 3, Encontrado: {hormigas_count}")
    
    # Verificar columna directamente
    try:
        if db_type == "SQLite":
            cursor = db.connection.cursor()
            cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", (tarea_id,))
            result = cursor.fetchone()
            if result and result[0] == 3:
                print_success(f"Columna hormigas_asignadas se mantiene después de completar: {result[0]}")
            else:
                print_error(f"Columna no se mantiene. Valor: {result[0] if result else 'None'}")
        else:
            cursor = db.connection.cursor()
            db._exec(cursor, "SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea_id,))
            result = cursor.fetchone()
            if result and result[0] == 3:
                print_success(f"Columna hormigas_asignadas se mantiene después de completar: {result[0]}")
            else:
                print_error(f"Columna no se mantiene. Valor: {result[0] if result else 'None'}")
    except Exception as e:
        print_error(f"Error al verificar columna: {e}")
else:
    print_error("Tarea no encontrada después de completar")

# Limpiar
if db_type == "SQLite" and os.path.exists(db_path):
    print(f"\n[INFO] Base de datos de prueba: {db_path}")
    print("[INFO] Puedes eliminar manualmente el archivo si lo deseas")

print(f"\n{'='*80}")
print("RESUMEN DE VALIDACIÓN")
print(f"{'='*80}")
print(f"Base de datos: {db_type}")
print(f"Alimento ID: {alimento_id}")
print(f"Tarea ID: {tarea_id}")
print(f"\nTodas las validaciones se completaron. Revisa los resultados arriba.")

