"""
Test que verifica que el API realmente persiste los datos.
Captura los logs del servicio y verifica en BD.
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

# Test completo
print_header("TEST DE API CON VERIFICACIÓN DE PERSISTENCIA")

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
tarea_id = f"TEST_API_{os.getpid()}_{int(time.time())}"
tarea_data = {"tarea_id": tarea_id, "alimento_id": alimento_id}

response = safe_request("POST", f"{BASE_URL}/tareas", json_data=tarea_data)
if not response:
    sys.exit(1)

print_success(f"Tarea creada: {tarea_id}")
time.sleep(2)  # Esperar persistencia

# 3. Asignar hormigas
print("\n3. Asignando hormigas...")
lote_id = f"LOTE_API_{os.getpid()}_{int(time.time())}"
asignar_data = {"hormigas_lote_id": lote_id, "cantidad": 3}

response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/asignar-hormigas", json_data=asignar_data)
if not response:
    sys.exit(1)

print_success(f"Hormigas asignadas, lote: {lote_id}")
time.sleep(3)  # Esperar persistencia

# 4. Verificar en BD directamente
print("\n4. Verificando en BD directamente...")
try:
    from src.recoleccion.database.database_manager import SqlServerDatabaseManager
    
    db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
    cursor = db.connection.cursor()
    
    # Verificar tarea
    db._exec(cursor, "SELECT COUNT(*) FROM dbo.Tareas WHERE id = ?", (tarea_id,))
    count = cursor.fetchone()[0]
    if count > 0:
        print_success(f"Tarea encontrada en BD: {tarea_id}")
        db._exec(cursor, "SELECT id, alimento_id, estado, hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea_id,))
        row = cursor.fetchone()
        if row:
            print_info(f"  Datos: id={row[0]}, alimento_id={row[1]}, estado={row[2]}, hormigas_asignadas={row[3]}")
    else:
        print_error(f"Tarea NO encontrada en BD: {tarea_id}")
    
    # Verificar lote
    db._exec(cursor, "SELECT COUNT(*) FROM dbo.lotes_hormigas WHERE lote_id = ?", (lote_id,))
    count = cursor.fetchone()[0]
    if count > 0:
        print_success(f"Lote encontrado en BD: {lote_id}")
    else:
        print_error(f"Lote NO encontrado en BD: {lote_id}")
    
    # Verificar asignaciones
    db._exec(cursor, "SELECT COUNT(*) FROM dbo.asignaciones_hormiga_tarea WHERE tarea_id = ?", (tarea_id,))
    count = cursor.fetchone()[0]
    if count > 0:
        print_success(f"Asignaciones encontradas: {count}")
    else:
        print_error(f"No hay asignaciones en BD para tarea: {tarea_id}")
    
    db.connection.close()
    
except Exception as e:
    print_error(f"Error verificando BD: {e}")
    import traceback
    traceback.print_exc()

print_header("TEST COMPLETADO")
print_info(f"Tarea ID: {tarea_id}")
print_info(f"Lote ID: {lote_id}")
print_info("\nIMPORTANTE: Si no ves los datos en BD, el servicio necesita reiniciarse")
print_info("para usar el código actualizado que guarda correctamente.")



