"""
Script de prueba para validar que hormigas_asignadas se guarda correctamente en la BD.
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

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

def safe_request(method, url, json_data=None):
    """Hace una petición HTTP con manejo de errores."""
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, timeout=10)
        else:
            raise ValueError(f"Método no soportado: {method}")
        
        return response
    except Exception as e:
        print_error(f"Error en petición {method} {url}: {e}")
        return None

# Verificar que el servicio esté disponible
print_step(1, "Verificar que el servicio esté disponible")
response = safe_request("GET", f"{BASE_URL}/health")
if response and response.status_code == 200:
    print_success("Servicio disponible")
else:
    print_error("El servicio no está disponible. Inicia el servicio primero.")
    exit(1)

# Crear un alimento
print_step(2, "Crear un alimento")
alimento_id = f"ALIMENTO_TEST_{datetime.now().strftime('%Y%m%d%H%M%S')}"
alimento_data = {
    "id": alimento_id,
    "nombre": "Alimento de Prueba BD",
    "cantidad_hormigas_necesarias": 3,
    "puntos_stock": 20,
    "tiempo_recoleccion": 60
}
response = safe_request("POST", f"{BASE_URL}/alimentos", alimento_data)
if response and response.status_code == 200:
    print_success(f"Alimento creado: {alimento_id}")
    print(f"  Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
else:
    print_error(f"No se pudo crear el alimento. Status: {response.status_code if response else 'sin respuesta'}")
    if response:
        print(f"  Error: {response.text}")
    exit(1)

# Crear una tarea
print_step(3, "Crear una tarea")
tarea_id = f"TAREA_TEST_{datetime.now().strftime('%Y%m%d%H%M%S')}"
tarea_data = {
    "tarea_id": tarea_id,
    "alimento_id": alimento_id
}
response = safe_request("POST", f"{BASE_URL}/tareas", tarea_data)
if response and response.status_code == 200:
    print_success(f"Tarea creada: {tarea_id}")
    tarea_info = response.json()
    print(f"  Estado inicial: {tarea_info.get('estado')}")
    print(f"  Hormigas asignadas: {len(tarea_info.get('hormigas_asignadas', []))}")
else:
    print_error(f"No se pudo crear la tarea. Status: {response.status_code if response else 'sin respuesta'}")
    if response:
        print(f"  Error: {response.text}")
    exit(1)

# Verificar estado inicial en BD
print_step(4, "Verificar estado inicial en BD (sin hormigas asignadas)")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response and response.status_code == 200:
    status = response.json()
    print(f"  Estado: {status.get('estado')}")
    print(f"  Hormigas asignadas: {len(status.get('hormigas_asignadas', []))}")
    print_success("Estado inicial verificado")
else:
    print_error("No se pudo obtener el estado de la tarea")

# Asignar hormigas a la tarea
print_step(5, "Asignar hormigas a la tarea")
lote_id = f"LOTE_TEST_{datetime.now().strftime('%Y%m%d%H%M%S')}"
asignar_data = {
    "hormigas_lote_id": lote_id,
    "cantidad": 3
}
response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/asignar-hormigas", asignar_data)
if response and response.status_code == 200:
    print_success("Hormigas asignadas")
    asignacion_info = response.json()
    print(f"  Hormigas asignadas: {asignacion_info.get('hormigas_asignadas', 0)}")
    print(f"  Hormigas requeridas: {asignacion_info.get('hormigas_requeridas', 0)}")
    print(f"  Lote ID: {asignacion_info.get('hormigas_lote_id', 'N/A')}")
    print(f"  Iniciada: {asignacion_info.get('iniciada', False)}")
else:
    print_error(f"No se pudieron asignar hormigas. Status: {response.status_code if response else 'sin respuesta'}")
    if response:
        print(f"  Error: {response.text}")

# Verificar que las hormigas se guardaron en BD
print_step(6, "Verificar que las hormigas se guardaron en BD")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}")
if response and response.status_code == 200:
    tarea_info = response.json()
    hormigas_count = len(tarea_info.get('hormigas_asignadas', []))
    print(f"  Hormigas asignadas en respuesta: {hormigas_count}")
    if hormigas_count == 3:
        print_success(f"Se encontraron {hormigas_count} hormigas asignadas en la BD")
        for i, hormiga in enumerate(tarea_info.get('hormigas_asignadas', []), 1):
            print(f"    Hormiga {i}: {hormiga.get('id')} - Estado: {hormiga.get('estado')}")
    else:
        print_error(f"Se esperaban 3 hormigas, se encontraron {hormigas_count}")
else:
    print_error("No se pudo obtener la tarea de la BD")

# Verificar status después de asignación
print_step(7, "Verificar status después de asignación")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response and response.status_code == 200:
    status = response.json()
    print(f"  Estado: {status.get('estado')}")
    print(f"  Hormigas asignadas: {len(status.get('hormigas_asignadas', []))}")
    print(f"  Lote ID: {status.get('hormigas_lote_id', 'N/A')}")
    print_success("Status verificado")
else:
    print_error("No se pudo obtener el status")

# Iniciar la tarea si no está iniciada
print_step(8, "Iniciar la tarea")
if status.get('estado') != 'en_proceso':
    iniciar_data = {
        "hormigas_lote_id": lote_id
    }
    response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/iniciar", iniciar_data)
    if response and response.status_code == 200:
        print_success("Tarea iniciada")
        print(f"  Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print_error(f"No se pudo iniciar la tarea. Status: {response.status_code if response else 'sin respuesta'}")
        if response:
            print(f"  Error: {response.text}")
else:
    print_success("La tarea ya estaba iniciada")

# Verificar que hormigas_asignadas se mantiene después de iniciar
print_step(9, "Verificar que hormigas_asignadas se mantiene después de iniciar")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}")
if response and response.status_code == 200:
    tarea_info = response.json()
    hormigas_count = len(tarea_info.get('hormigas_asignadas', []))
    estado = tarea_info.get('estado')
    print(f"  Estado: {estado}")
    print(f"  Hormigas asignadas: {hormigas_count}")
    if hormigas_count == 3:
        print_success(f"hormigas_asignadas se mantiene correctamente: {hormigas_count}")
    else:
        print_error(f"hormigas_asignadas no se mantiene. Esperado: 3, Encontrado: {hormigas_count}")
else:
    print_error("No se pudo obtener la tarea después de iniciar")

# Consultar directamente desde el endpoint de debug de BD
print_step(10, "Consultar información de BD directamente")
response = safe_request("GET", f"{BASE_URL}/debug/db")
if response and response.status_code == 200:
    db_info = response.json()
    print(f"  Tareas en BD: {db_info.get('tareas_en_bd', 0)}")
    print(f"  Alimentos en BD: {db_info.get('alimentos_en_bd', 0)}")
    print_success("Información de BD obtenida")
else:
    print_error("No se pudo obtener información de BD")

# Verificar todas las tareas
print_step(11, "Verificar todas las tareas en BD")
response = safe_request("GET", f"{BASE_URL}/tareas")
if response and response.status_code == 200:
    tareas = response.json()
    tarea_encontrada = next((t for t in tareas if t.get('id') == tarea_id), None)
    if tarea_encontrada:
        hormigas_count = len(tarea_encontrada.get('hormigas_asignadas', []))
        print(f"  Tarea encontrada: {tarea_id}")
        print(f"  Estado: {tarea_encontrada.get('estado')}")
        print(f"  Hormigas asignadas: {hormigas_count}")
        if hormigas_count == 3:
            print_success(f"hormigas_asignadas se mantiene en lista de tareas: {hormigas_count}")
        else:
            print_error(f"hormigas_asignadas no se mantiene en lista. Esperado: 3, Encontrado: {hormigas_count}")
    else:
        print_error(f"Tarea {tarea_id} no encontrada en la lista")
else:
    print_error("No se pudo obtener la lista de tareas")

print(f"\n{'='*80}")
print("RESUMEN DE VALIDACIÓN")
print(f"{'='*80}")
print(f"Alimento ID: {alimento_id}")
print(f"Tarea ID: {tarea_id}")
print(f"Lote ID: {lote_id}")
print(f"\nTodas las validaciones se completaron. Revisa los resultados arriba.")



