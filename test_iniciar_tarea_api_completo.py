"""
Test completo del endpoint de iniciar tarea para verificar que guarda correctamente.
"""
import requests
import time
import sys
import os
from datetime import datetime

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

print_header("TEST COMPLETO: Iniciar Tarea a través de API")

# 1. Obtener alimento
print("\n1. Obteniendo alimento...")
response = safe_request("GET", f"{BASE_URL}/alimentos")
if not response:
    sys.exit(1)

alimentos = response.json()
alimento = alimentos[0]
alimento_id = alimento.get("id")
print_success(f"Alimento: {alimento_id} ({alimento.get('nombre')})")

# 2. Crear tarea
print("\n2. Creando tarea...")
tarea_id = f"TEST_INICIAR_{os.getpid()}_{int(time.time())}"
tarea_data = {"tarea_id": tarea_id, "alimento_id": alimento_id}

response = safe_request("POST", f"{BASE_URL}/tareas", json_data=tarea_data)
if not response:
    sys.exit(1)

print_success(f"Tarea creada: {tarea_id}")
time.sleep(2)

# 3. Asignar hormigas con lote
print("\n3. Asignando hormigas con lote...")
lote_id = f"LOTE_INICIAR_{os.getpid()}_{int(time.time())}"
asignar_data = {"hormigas_lote_id": lote_id, "cantidad": 3}

response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/asignar-hormigas", json_data=asignar_data)
if not response:
    print_error("No se pudieron asignar las hormigas")
    sys.exit(1)

asignacion = response.json()
print_success("Hormigas asignadas")
print_info(f"  Lote ID: {lote_id}")
print_info(f"  Estado: {asignacion.get('estado')}")
print_info(f"  Iniciada automáticamente: {asignacion.get('iniciada', False)}")
time.sleep(2)

# 4. Verificar estado antes de iniciar
print("\n4. Verificando estado ANTES de iniciar manualmente...")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response:
    status_antes = response.json()
    print_info(f"  Estado: {status_antes.get('estado')}")
    print_info(f"  Hormigas asignadas: {status_antes.get('hormigas_asignadas', 0)}")
    print_info(f"  Fecha inicio: {status_antes.get('fecha_inicio')}")
    print_info(f"  Lote ID: {status_antes.get('hormigas_lote_id')}")

# 5. Iniciar la tarea manualmente usando el endpoint
print("\n5. Iniciando tarea manualmente usando POST /tareas/{id}/iniciar...")
iniciar_data = {"hormigas_lote_id": lote_id}

response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/iniciar", json_data=iniciar_data)
if not response:
    print_error("No se pudo iniciar la tarea")
    sys.exit(1)

resultado = response.json()
print_success("Tarea iniciada a través del API")
print_info(f"  Estado: {resultado.get('estado')}")
print_info(f"  Hormigas asignadas: {resultado.get('hormigas_asignadas', 0)}")
print_info(f"  Lote ID: {resultado.get('hormigas_lote_id')}")
time.sleep(2)  # Esperar a que se persista

# 6. Verificar estado DESPUÉS de iniciar
print("\n6. Verificando estado DESPUÉS de iniciar...")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response:
    status_despues = response.json()
    print_success("Status obtenido")
    print_info(f"  Estado: {status_despues.get('estado')}")
    print_info(f"  Hormigas asignadas: {status_despues.get('hormigas_asignadas', 0)}")
    print_info(f"  Fecha inicio: {status_despues.get('fecha_inicio')}")
    print_info(f"  Lote ID: {status_despues.get('hormigas_lote_id')}")
    
    if status_despues.get('estado') == 'en_proceso':
        print_success("Estado correcto: en_proceso")
    else:
        print_error(f"Estado incorrecto: {status_despues.get('estado')} (esperado: en_proceso)")
    
    if status_despues.get('fecha_inicio'):
        print_success("Fecha inicio establecida")
    else:
        print_error("Fecha inicio NO establecida")
    
    if status_despues.get('hormigas_asignadas', 0) > 0:
        print_success(f"Hormigas asignadas: {status_despues.get('hormigas_asignadas')}")
    else:
        print_error(f"Hormigas asignadas: {status_despues.get('hormigas_asignadas', 0)} (debería ser > 0)")

# 7. Verificar directamente en BD
print("\n7. Verificando directamente en BD...")
try:
    from src.recoleccion.database.database_manager import SqlServerDatabaseManager
    
    db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
    cursor = db.connection.cursor()
    
    db._exec(cursor, """
        SELECT id, estado, inicio, fin, hormigas_asignadas
        FROM dbo.Tareas
        WHERE id = ?
    """, (tarea_id,))
    
    tarea_row = cursor.fetchone()
    if tarea_row:
        print_success("Tarea encontrada en BD")
        print_info(f"  ID: {tarea_row[0]}")
        print_info(f"  Estado: {tarea_row[1]}")
        print_info(f"  Inicio: {tarea_row[2]}")
        print_info(f"  Fin: {tarea_row[3]}")
        print_info(f"  Hormigas asignadas: {tarea_row[4]}")
        
        if tarea_row[1] == 'en_proceso':
            print_success("Estado en BD: en_proceso (correcto)")
        else:
            print_error(f"Estado en BD: {tarea_row[1]} (esperado: en_proceso)")
        
        if tarea_row[2]:
            print_success("Fecha inicio en BD: establecida (correcto)")
        else:
            print_error("Fecha inicio en BD: NULL (incorrecto)")
        
        if tarea_row[4] and tarea_row[4] > 0:
            print_success(f"Hormigas asignadas en BD: {tarea_row[4]} (correcto)")
        else:
            print_error(f"Hormigas asignadas en BD: {tarea_row[4]} (debería ser > 0)")
    else:
        print_error("Tarea NO encontrada en BD")
    
    db.connection.close()
except Exception as e:
    print_error(f"Error verificando BD: {e}")
    import traceback
    traceback.print_exc()

print_header("TEST COMPLETADO")
print_info(f"Tarea ID: {tarea_id}")
print_info(f"Lote ID: {lote_id}")



