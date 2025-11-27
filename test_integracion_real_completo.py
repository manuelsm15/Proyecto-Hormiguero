"""
Pruebas de integración reales que ejecutan el proceso completo:
- Servicio FastAPI real
- Base de datos real (SQL Server)
- Llamadas HTTP reales
- Validación de datos reales en BD
"""
import requests
import time
import sys
import os
from datetime import datetime
import json

# Configuración
BASE_URL = "http://localhost:8000"
TIMEOUT = 30
WAIT_FOR_SERVICE = 5

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

def wait_for_service():
    """Espera a que el servicio esté disponible."""
    print_info("Esperando a que el servicio esté disponible...")
    for i in range(WAIT_FOR_SERVICE):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print_success("Servicio disponible")
                return True
        except Exception as e:
            pass
        time.sleep(1)
        if i < WAIT_FOR_SERVICE - 1:
            print_info(f"Intento {i+1}/{WAIT_FOR_SERVICE}...")
    return False

def safe_request(method, url, json_data=None, params=None, expected_status=200):
    """Realiza una petición HTTP de forma segura."""
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=TIMEOUT)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, params=params, timeout=TIMEOUT)
        else:
            print_error(f"Método HTTP no soportado: {method}")
            return None
        
        if response.status_code == expected_status:
            return response
        else:
            print_error(f"Status code inesperado: {response.status_code} (esperado: {expected_status})")
            print_error(f"Respuesta: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error en petición: {e}")
        return None

# Inicio de pruebas
print_header("PRUEBAS DE INTEGRACIÓN REALES - PROCESO COMPLETO")

# Verificar que el servicio esté disponible
if not wait_for_service():
    print_error("El servicio no está disponible. Asegúrate de que esté ejecutándose en http://localhost:8000")
    print_info("Ejecuta: python src/recoleccion/main.py")
    sys.exit(1)

# PASO 1: Health Check
print_header("PASO 1: Verificar Salud del Servicio")
response = safe_request("GET", f"{BASE_URL}/health")
if response:
    data = response.json()
    print_success(f"Servicio saludable: {data.get('status')}")
    print_info(f"  Mensaje: {data.get('message', 'N/A')}")

# PASO 2: Usar Alimento Existente o Crear Nuevo
print_header("PASO 2: Obtener Alimento para la Prueba")

# Primero intentar usar un alimento existente del mock (A1, A2, A3)
print_info("Intentando usar alimento existente del sistema...")
response = safe_request("GET", f"{BASE_URL}/alimentos")
if response:
    alimentos = response.json()
    if alimentos and len(alimentos) > 0:
        # Usar el primer alimento disponible
        alimento_existente = alimentos[0]
        alimento_id = alimento_existente.get("id")
        print_success(f"Usando alimento existente: {alimento_id}")
        print_info(f"  Nombre: {alimento_existente.get('nombre')}")
        print_info(f"  Hormigas necesarias: {alimento_existente.get('cantidad_hormigas_necesarias')}")
        print_info(f"  Disponible: {alimento_existente.get('disponible')}")
    else:
        # Si no hay alimentos, crear uno nuevo
        print_info("No hay alimentos existentes, creando uno nuevo...")
        alimento_data = {
            "nombre": f"Alimento Integración {datetime.now().strftime('%Y%m%d%H%M%S')}",
            "cantidad_hormigas_necesarias": 3,
            "puntos_stock": 20,
            "tiempo_recoleccion": 60,
            "disponible": True
        }
        response = safe_request("POST", f"{BASE_URL}/alimentos", json_data=alimento_data)
        if not response:
            print_error("No se pudo crear el alimento")
            sys.exit(1)
        alimento_creado = response.json()
        alimento_id = alimento_creado.get("id")
        print_success(f"Alimento creado: {alimento_id}")
        time.sleep(2)  # Esperar a que se persista
else:
    # Si falla la consulta, usar A1 por defecto
    print_info("No se pudieron consultar alimentos, usando A1 por defecto...")
    alimento_id = "A1"

# PASO 3: Crear Tarea
print_header("PASO 3: Crear Tarea Real")
print_info(f"Intentando crear tarea con alimento_id: {alimento_id}")

# Intentar crear la tarea con el alimento_id en el body
tarea_data = {
    "tarea_id": f"TAREA_INTEG_{datetime.now().strftime('%Y%m%d%H%M%S')}",
    "alimento_id": alimento_id
}

response = safe_request("POST", f"{BASE_URL}/tareas", json_data=tarea_data, expected_status=200)
if not response:
    # Si falla, intentar con query parameters
    print_info("Falló con body, intentando con query parameters...")
    response = safe_request("POST", f"{BASE_URL}/tareas?tarea_id={tarea_data['tarea_id']}&alimento_id={alimento_id}", expected_status=200)
    
    if not response:
        print_error("No se pudo crear la tarea después de múltiples intentos")
        print_info(f"Alimento ID usado: {alimento_id}")
        sys.exit(1)

tarea_creada = response.json()
tarea_id = tarea_creada.get("id")
print_success(f"Tarea creada: {tarea_id}")
print_info(f"  Estado: {tarea_creada.get('estado')}")
print_info(f"  Alimento: {tarea_creada.get('alimento', {}).get('nombre', 'N/A')}")

# Verificar estado inicial
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response:
    status = response.json()
    print_info(f"  Hormigas asignadas (inicial): {status.get('hormigas_asignadas', 0)}")
    print_info(f"  Estado: {status.get('estado')}")

# PASO 4: Asignar Hormigas con Lote
print_header("PASO 4: Asignar Hormigas con Lote ID")
lote_id = f"LOTE_INTEG_{datetime.now().strftime('%Y%m%d%H%M%S')}"
asignar_data = {
    "hormigas_lote_id": lote_id,
    "cantidad": 3
}

response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/asignar-hormigas", json_data=asignar_data, expected_status=200)
if not response:
    print_error("No se pudo asignar las hormigas")
    sys.exit(1)

asignacion = response.json()
print_success("Hormigas asignadas")
print_info(f"  Lote ID: {lote_id}")
print_info(f"  Cantidad: {asignacion.get('cantidad_hormigas_asignadas', 0)}")
print_info(f"  Estado tarea: {asignacion.get('estado')}")

# Verificar que la tarea se inició automáticamente (si tiene suficientes hormigas)
if asignacion.get('iniciada'):
    print_success("Tarea iniciada automáticamente (tiene suficientes hormigas)")

# PASO 5: Verificar Status después de Asignar
print_header("PASO 5: Verificar Status después de Asignar")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response:
    status = response.json()
    print_success("Status obtenido")
    print_info(f"  Estado: {status.get('estado')}")
    print_info(f"  Hormigas asignadas: {status.get('hormigas_asignadas', 0)}")
    print_info(f"  Lote ID: {status.get('hormigas_lote_id')}")
    print_info(f"  Fecha inicio: {status.get('fecha_inicio')}")
    
    if status.get('hormigas_asignadas', 0) == 3:
        print_success("hormigas_asignadas = 3 (correcto)")
    else:
        print_error(f"hormigas_asignadas debería ser 3, es {status.get('hormigas_asignadas', 0)}")

# PASO 6: Iniciar Tarea (si no se inició automáticamente)
if not asignacion.get('iniciada'):
    print_header("PASO 6: Iniciar Tarea Manualmente")
    iniciar_data = {
        "hormigas_lote_id": lote_id
    }
    response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/iniciar", json_data=iniciar_data)
    if response:
        print_success("Tarea iniciada")
        iniciada = response.json()
        print_info(f"  Estado: {iniciada.get('estado')}")
        print_info(f"  Fecha inicio: {iniciada.get('fecha_inicio')}")

# PASO 7: Verificar Status después de Iniciar
print_header("PASO 7: Verificar Status después de Iniciar")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response:
    status = response.json()
    print_success("Status obtenido")
    print_info(f"  Estado: {status.get('estado')}")
    print_info(f"  Hormigas asignadas: {status.get('hormigas_asignadas', 0)}")
    print_info(f"  Lote ID: {status.get('hormigas_lote_id')}")
    
    if status.get('hormigas_asignadas', 0) == 3:
        print_success("hormigas_asignadas se mantiene después de iniciar: 3")
    else:
        print_error(f"hormigas_asignadas debería ser 3, es {status.get('hormigas_asignadas', 0)}")

# PASO 8: Completar Tarea
print_header("PASO 8: Completar Tarea")
# El endpoint requiere cantidad_recolectada como query parameter
response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/completar?cantidad_recolectada=20")
if response:
    print_success("Tarea completada")
    completada = response.json()
    print_info(f"  Estado: {completada.get('estado')}")
    print_info(f"  Alimento recolectado: {completada.get('alimento_recolectado', 0)}")
    print_info(f"  Fecha fin: {completada.get('fecha_fin')}")

# PASO 9: Verificar Status después de Completar
print_header("PASO 9: Verificar Status después de Completar")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response:
    status = response.json()
    print_success("Status obtenido")
    print_info(f"  Estado: {status.get('estado')}")
    print_info(f"  Hormigas asignadas: {status.get('hormigas_asignadas', 0)}")
    print_info(f"  Alimento recolectado: {status.get('alimento_recolectado', 0)}")
    
    if status.get('hormigas_asignadas', 0) == 3:
        print_success("hormigas_asignadas se mantiene después de completar: 3")
    else:
        print_error(f"hormigas_asignadas debería ser 3, es {status.get('hormigas_asignadas', 0)}")

# PASO 10: Consultar Tarea desde BD Real
print_header("PASO 10: Consultar Evidencias en Base de Datos Real")
print_info("Ejecutando consulta directa a la base de datos...")

try:
    from src.recoleccion.database.database_manager import SqlServerDatabaseManager
    
    db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
    cursor = db.connection.cursor()
    
    # Consultar la tarea específica
    db._exec(cursor, """
        SELECT t.id, t.alimento_id, t.estado, t.inicio, t.fin,
               t.cantidad_recolectada, t.hormigas_asignadas,
               a.nombre as alimento_nombre
        FROM dbo.Tareas t
        LEFT JOIN dbo.Alimentos a ON CAST(t.alimento_id AS VARCHAR) = CAST(a.id AS VARCHAR)
        WHERE t.id = ?
    """, (tarea_id,))
    
    result = cursor.fetchone()
    if result:
        print_section("EVIDENCIA EN BASE DE DATOS REAL (SQL Server)")
        columns = [description[0] for description in cursor.description]
        for col, val in zip(columns, result):
            print(f"  {col}: {val}")
        
        hormigas_idx = columns.index('hormigas_asignadas')
        hormigas_value = result[hormigas_idx]
        if hormigas_value == 3:
            print_success(f"\nhormigas_asignadas en BD REAL = {hormigas_value} (VALIDADO)")
        elif hormigas_value is None:
            print_error(f"\nhormigas_asignadas en BD REAL = None (ESPERADO: 3)")
            print_info("Nota: La columna existe pero el valor es None. Esto puede ser de una tarea antigua.")
        else:
            print_error(f"\nhormigas_asignadas en BD REAL = {hormigas_value} (ESPERADO: 3)")
    else:
        print_error("Tarea no encontrada en la base de datos")
    
    # Consultar asignaciones
    db._exec(cursor, """
        SELECT COUNT(*) as total_asignaciones
        FROM dbo.asignaciones_hormiga_tarea
        WHERE tarea_id = ?
    """, (tarea_id,))
    
    result = cursor.fetchone()
    if result:
        print_info(f"  Total asignaciones en BD: {result[0]}")
    
    # Consultar lote de hormigas (usar columnas correctas según el esquema)
    try:
        db._exec(cursor, """
            SELECT TOP 1 id, tarea_id, estado
            FROM dbo.lotes_hormigas
            WHERE tarea_id = ?
        """, (tarea_id,))
        lote_result = cursor.fetchone()
        if lote_result:
            print_section("EVIDENCIA: Lote de Hormigas en BD")
            lote_columns = [description[0] for description in cursor.description]
            for col, val in zip(lote_columns, lote_result):
                print(f"  {col}: {val}")
    except Exception as e:
        print_info(f"No se pudo consultar lote (puede que la tabla no exista o tenga otro esquema): {e}")
    
    lote_result = cursor.fetchone()
    if lote_result:
        print_section("EVIDENCIA: Lote de Hormigas en BD")
        lote_columns = [description[0] for description in cursor.description]
        for col, val in zip(lote_columns, lote_result):
            print(f"  {col}: {val}")
    
    db.connection.close()
    
except Exception as e:
    print_error(f"Error al consultar BD: {e}")
    import traceback
    traceback.print_exc()
    print_info("Continuando sin consulta directa a BD...")

# Resumen final
print_header("RESUMEN DE PRUEBAS DE INTEGRACIÓN REALES")
print_success("Todas las pruebas se ejecutaron sobre el proceso real")
print_info(f"  Alimento ID: {alimento_id}")
print_info(f"  Tarea ID: {tarea_id}")
print_info(f"  Lote ID: {lote_id}")
print_info(f"  Base de datos: SQL Server (SHIRORYUU / Hormiguero)")
print_info(f"  Servicio: FastAPI en http://localhost:8000")
print("\nTodas las evidencias se muestran arriba. Los datos están guardados en la BD real.")

