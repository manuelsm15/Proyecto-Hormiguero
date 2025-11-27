"""
Script para iniciar una tarea existente usando el endpoint de la API.
"""
import requests
import sys
import os

BASE_URL = "http://localhost:8000"

def print_header(text):
    print(f"\n{'='*80}")
    print(f"{text}")
    print(f"{'='*80}")

def print_success(message):
    print(f"[OK] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_info(message):
    print(f"[INFO] {message}")

def print_warning(message):
    print(f"[ADVERTENCIA] {message}")

def safe_request(method, url, json_data=None, params=None, expected_status=200):
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, params=params, timeout=30)
        else:
            return None
        
        if response.status_code == expected_status:
            return response
        else:
            print_error(f"Status: {response.status_code}, Respuesta: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

# Tarea específica a iniciar
tarea_id = "TEST_DIRECT_18292"

print_header(f"INICIAR TAREA EXISTENTE: {tarea_id}")

# 1. Verificar estado actual
print("\n1. Verificando estado actual de la tarea...")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if not response:
    print_error(f"No se pudo obtener el estado de la tarea {tarea_id}")
    print_info("Verificando si el servicio está corriendo...")
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        if health.status_code == 200:
            print_info("El servicio está corriendo")
        else:
            print_error("El servicio no responde correctamente")
    except:
        print_error("El servicio no está disponible. Inícialo con: python main.py")
    sys.exit(1)

status = response.json()
print_success("Estado obtenido")
print_info(f"  Estado: {status.get('estado')}")
print_info(f"  Hormigas asignadas: {status.get('hormigas_asignadas', 0)}")
print_info(f"  Lote ID: {status.get('hormigas_lote_id')}")
print_info(f"  Fecha inicio: {status.get('fecha_inicio')}")

estado_actual = status.get('estado')
lote_id = status.get('hormigas_lote_id')

# 2. Verificar si puede iniciarse
if estado_actual == 'completada':
    print_success("La tarea ya está completada")
    sys.exit(0)
elif estado_actual == 'en_proceso':
    print_info("La tarea ya está en proceso")
    if not status.get('fecha_inicio'):
        print_warning("Pero no tiene fecha_inicio. Intentando guardar estado...")
        # Aunque esté en proceso, si no tiene fecha_inicio, algo está mal
        # Podemos intentar iniciarla de nuevo
        print_info("Intentando iniciar de nuevo para establecer fecha_inicio...")
    else:
        print_success("La tarea está correctamente iniciada")
        sys.exit(0)

# 3. Verificar que tenga hormigas
if status.get('hormigas_asignadas', 0) == 0:
    print_warning("La tarea no tiene hormigas asignadas en el status")
    print_info("Verificando en BD directamente...")
    
    # Verificar en BD
    try:
        from src.recoleccion.database.database_manager import SqlServerDatabaseManager
        db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
        cursor = db.connection.cursor()
        
        db._exec(cursor, """
            SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?
        """, (tarea_id,))
        
        hormigas_row = cursor.fetchone()
        if hormigas_row and hormigas_row[0] and hormigas_row[0] > 0:
            print_success(f"En BD tiene {hormigas_row[0]} hormigas asignadas")
            print_info("El problema es que el status no las está cargando correctamente")
        else:
            print_error("La tarea no tiene hormigas asignadas en BD")
            print_info("Necesitas asignar hormigas primero usando: POST /tareas/{id}/asignar-hormigas")
        
        db.connection.close()
    except Exception as e:
        print_error(f"Error verificando BD: {e}")

# 4. Iniciar la tarea
if estado_actual == 'pendiente':
    print("\n2. Iniciando la tarea...")
    
    iniciar_data = None
    if lote_id:
        iniciar_data = {"hormigas_lote_id": lote_id}
        print_info(f"Iniciando con lote_id: {lote_id}")
    else:
        print_info("Iniciando sin lote_id (se buscará automáticamente)")
    
    response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/iniciar", json_data=iniciar_data)
    
    if not response:
        print_error("No se pudo iniciar la tarea")
        print_info("Posibles causas:")
        print_info("  1. La tarea no tiene suficientes hormigas asignadas")
        print_info("  2. El servicio no tiene el código actualizado (reinicia el servicio)")
        print_info("  3. Error en la persistencia")
        sys.exit(1)
    
    resultado = response.json()
    print_success("Tarea iniciada exitosamente")
    print_info(f"  Estado: {resultado.get('estado')}")
    print_info(f"  Hormigas asignadas: {resultado.get('hormigas_asignadas', 0)}")
    print_info(f"  Fecha inicio: {resultado.get('fecha_inicio')}")
    print_info(f"  Lote ID: {resultado.get('hormigas_lote_id')}")
    
    import time
    time.sleep(2)  # Esperar a que se persista
    
    # 5. Verificar estado final
    print("\n3. Verificando estado final...")
    response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
    if response:
        status_final = response.json()
        print_success("Status final obtenido")
        print_info(f"  Estado: {status_final.get('estado')}")
        print_info(f"  Hormigas asignadas: {status_final.get('hormigas_asignadas', 0)}")
        print_info(f"  Fecha inicio: {status_final.get('fecha_inicio')}")
        print_info(f"  Lote ID: {status_final.get('hormigas_lote_id')}")
        
        if status_final.get('estado') == 'en_proceso':
            print_success("Estado correcto: en_proceso")
        else:
            print_error(f"Estado incorrecto: {status_final.get('estado')} (esperado: en_proceso)")
        
        if status_final.get('fecha_inicio'):
            print_success("Fecha inicio establecida correctamente")
        else:
            print_error("Fecha inicio NO establecida - el servicio necesita reiniciarse")
        
        if status_final.get('hormigas_asignadas', 0) > 0:
            print_success(f"Hormigas asignadas: {status_final.get('hormigas_asignadas')}")
        else:
            print_warning(f"Hormigas asignadas: {status_final.get('hormigas_asignadas', 0)} (puede ser un problema de carga desde BD)")
    
    # 6. Verificar en BD directamente
    print("\n4. Verificando en BD directamente...")
    try:
        from src.recoleccion.database.database_manager import SqlServerDatabaseManager
        db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
        cursor = db.connection.cursor()
        
        db._exec(cursor, """
            SELECT id, estado, inicio, hormigas_asignadas
            FROM dbo.Tareas
            WHERE id = ?
        """, (tarea_id,))
        
        tarea_row = cursor.fetchone()
        if tarea_row:
            print_success("Tarea encontrada en BD")
            print_info(f"  Estado: {tarea_row[1]}")
            print_info(f"  Inicio: {tarea_row[2]}")
            print_info(f"  Hormigas asignadas: {tarea_row[3]}")
            
            if tarea_row[1] == 'en_proceso':
                print_success("Estado en BD: en_proceso (correcto)")
            else:
                print_error(f"Estado en BD: {tarea_row[1]} (esperado: en_proceso)")
            
            if tarea_row[2]:
                print_success("Fecha inicio en BD: establecida (correcto)")
            else:
                print_error("Fecha inicio en BD: NULL (el servicio necesita reiniciarse)")
            
            if tarea_row[3] and tarea_row[3] > 0:
                print_success(f"Hormigas asignadas en BD: {tarea_row[3]} (correcto)")
            else:
                print_error(f"Hormigas asignadas en BD: {tarea_row[3]} (debería ser > 0)")
        else:
            print_error("Tarea NO encontrada en BD")
            print_info("El servicio necesita reiniciarse para guardar correctamente")
        
        db.connection.close()
    except Exception as e:
        print_error(f"Error verificando BD: {e}")
        import traceback
        traceback.print_exc()

print_header("PROCESO COMPLETADO")
print_info(f"Tarea ID: {tarea_id}")

