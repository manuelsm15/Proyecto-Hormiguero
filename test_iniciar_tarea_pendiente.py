"""
Test para iniciar una tarea que está en estado pendiente (no iniciada automáticamente).
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

print_header("TEST: Iniciar Tarea Pendiente a través de API")

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
tarea_id = f"TEST_PENDIENTE_{os.getpid()}_{int(time.time())}"
tarea_data = {"tarea_id": tarea_id, "alimento_id": alimento_id}

response = safe_request("POST", f"{BASE_URL}/tareas", json_data=tarea_data)
if not response:
    sys.exit(1)

print_success(f"Tarea creada: {tarea_id}")
time.sleep(2)

# 3. Asignar hormigas SIN lote_id (para que NO se inicie automáticamente)
print("\n3. Asignando hormigas SIN lote_id (para mantener pendiente)...")
asignar_data = {"cantidad": 3}  # Sin lote_id

response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/asignar-hormigas", json_data=asignar_data)
if not response:
    print_error("No se pudieron asignar las hormigas")
    sys.exit(1)

asignacion = response.json()
print_success("Hormigas asignadas")
print_info(f"  Estado: {asignacion.get('estado')}")
print_info(f"  Iniciada automáticamente: {asignacion.get('iniciada', False)}")
time.sleep(2)

# 4. Verificar estado (debe estar pendiente)
print("\n4. Verificando estado (debe estar pendiente)...")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response:
    status = response.json()
    print_info(f"  Estado: {status.get('estado')}")
    print_info(f"  Hormigas asignadas: {status.get('hormigas_asignadas', 0)}")
    
    if status.get('estado') == 'pendiente':
        print_success("Tarea está en estado pendiente (correcto)")
    else:
        print_error(f"Tarea está en estado {status.get('estado')} (esperado: pendiente)")

# 5. Iniciar la tarea manualmente
print("\n5. Iniciando tarea manualmente usando POST /tareas/{id}/iniciar...")
# Primero obtener el lote_id si existe
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
lote_id = None
if response:
    status = response.json()
    lote_id = status.get('hormigas_lote_id')

if lote_id:
    iniciar_data = {"hormigas_lote_id": lote_id}
    print_info(f"Iniciando con lote_id: {lote_id}")
else:
    iniciar_data = None
    print_info("Iniciando sin lote_id")

response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/iniciar", json_data=iniciar_data)
if not response:
    print_error("No se pudo iniciar la tarea")
    sys.exit(1)

resultado = response.json()
print_success("Tarea iniciada a través del API")
print_info(f"  Estado: {resultado.get('estado')}")
print_info(f"  Hormigas asignadas: {resultado.get('hormigas_asignadas', 0)}")
print_info(f"  Fecha inicio: {resultado.get('fecha_inicio')}")
time.sleep(2)

# 6. Verificar estado final
print("\n6. Verificando estado final...")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response:
    status = response.json()
    print_success("Status obtenido")
    print_info(f"  Estado: {status.get('estado')}")
    print_info(f"  Hormigas asignadas: {status.get('hormigas_asignadas', 0)}")
    print_info(f"  Fecha inicio: {status.get('fecha_inicio')}")
    print_info(f"  Lote ID: {status.get('hormigas_lote_id')}")
    
    if status.get('estado') == 'en_proceso':
        print_success("Estado correcto: en_proceso")
    else:
        print_error(f"Estado incorrecto: {status.get('estado')} (esperado: en_proceso)")
    
    if status.get('fecha_inicio'):
        print_success("Fecha inicio establecida")
    else:
        print_error("Fecha inicio NO establecida")
    
    if status.get('hormigas_asignadas', 0) > 0:
        print_success(f"Hormigas asignadas: {status.get('hormigas_asignadas')}")
    else:
        print_error(f"Hormigas asignadas: {status.get('hormigas_asignadas', 0)} (debería ser > 0)")

# 7. Verificar en BD
print("\n7. Verificando en BD directamente...")
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
            print_error("Fecha inicio en BD: NULL (incorrecto)")
        
        if tarea_row[3] and tarea_row[3] > 0:
            print_success(f"Hormigas asignadas en BD: {tarea_row[3]} (correcto)")
        else:
            print_error(f"Hormigas asignadas en BD: {tarea_row[3]} (debería ser > 0)")
    else:
        print_error("Tarea NO encontrada en BD")
    
    db.connection.close()
except Exception as e:
    print_error(f"Error verificando BD: {e}")

print_header("TEST COMPLETADO")
print_info(f"Tarea ID: {tarea_id}")



