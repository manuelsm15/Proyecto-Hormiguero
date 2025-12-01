"""
Script para iniciar manualmente una tarea que tiene lote y hormigas asignadas.
"""
import requests
import sys

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

tarea_id = "TEST_DIRECT_13372"

print_header(f"INICIAR TAREA: {tarea_id}")

# 1. Verificar estado actual
print("\n1. Verificando estado actual de la tarea...")
try:
    response = requests.get(f"{BASE_URL}/tareas/{tarea_id}/status", timeout=10)
    if response.status_code == 200:
        status = response.json()
        print_success("Estado obtenido")
        print_info(f"  Estado: {status.get('estado')}")
        print_info(f"  Hormigas asignadas: {status.get('hormigas_asignadas', 0)}")
        print_info(f"  Lote ID: {status.get('hormigas_lote_id')}")
        print_info(f"  Fecha inicio: {status.get('fecha_inicio')}")
        
        lote_id = status.get('hormigas_lote_id')
        
        if status.get('estado') == 'pendiente':
            print_info("\nLa tarea está pendiente. Intentando iniciarla...")
            
            # 2. Iniciar la tarea
            if lote_id:
                print(f"\n2. Iniciando tarea con lote_id: {lote_id}")
                iniciar_data = {"hormigas_lote_id": lote_id}
                response = requests.post(
                    f"{BASE_URL}/tareas/{tarea_id}/iniciar",
                    json=iniciar_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    resultado = response.json()
                    print_success("Tarea iniciada exitosamente")
                    print_info(f"  Estado: {resultado.get('estado')}")
                    print_info(f"  Fecha inicio: {resultado.get('fecha_inicio')}")
                else:
                    print_error(f"No se pudo iniciar la tarea: {response.status_code}")
                    print_error(f"Respuesta: {response.text}")
            else:
                print_error("La tarea no tiene lote_id asociado")
                print_info("Intentando iniciar sin lote_id...")
                response = requests.post(
                    f"{BASE_URL}/tareas/{tarea_id}/iniciar",
                    timeout=30
                )
                
                if response.status_code == 200:
                    print_success("Tarea iniciada")
                else:
                    print_error(f"Error: {response.status_code} - {response.text}")
        elif status.get('estado') == 'en_proceso':
            print_success("La tarea ya está en proceso")
        elif status.get('estado') == 'completada':
            print_success("La tarea ya está completada")
        else:
            print_info(f"Estado actual: {status.get('estado')}")
    else:
        print_error(f"No se pudo obtener el estado: {response.status_code}")
        print_error(f"Respuesta: {response.text}")
except Exception as e:
    print_error(f"Error: {e}")
    import traceback
    traceback.print_exc()

# 3. Verificar estado final
print("\n3. Verificando estado final...")
try:
    response = requests.get(f"{BASE_URL}/tareas/{tarea_id}/status", timeout=10)
    if response.status_code == 200:
        status = response.json()
        print_success("Estado final:")
        print_info(f"  Estado: {status.get('estado')}")
        print_info(f"  Hormigas asignadas: {status.get('hormigas_asignadas', 0)}")
        print_info(f"  Lote ID: {status.get('hormigas_lote_id')}")
        print_info(f"  Fecha inicio: {status.get('fecha_inicio')}")
        print_info(f"  Fecha fin: {status.get('fecha_fin')}")
        print_info(f"  Alimento recolectado: {status.get('alimento_recolectado', 0)}")
        
        if status.get('estado') == 'en_proceso':
            print_success("\nLa tarea está en proceso y debería procesarse automáticamente")
            print_info("Puedes esperar o ejecutar: POST /tareas/{tarea_id}/completar?cantidad_recolectada=X")
except Exception as e:
    print_error(f"Error verificando estado final: {e}")

print_header("PROCESO COMPLETADO")



