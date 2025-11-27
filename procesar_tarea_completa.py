"""
Script para procesar completamente una tarea: iniciar y completar.
"""
import requests
import sys
import time

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

print_header(f"PROCESAR TAREA COMPLETA: {tarea_id}")

# 1. Verificar estado actual
print("\n1. Verificando estado actual...")
try:
    response = requests.get(f"{BASE_URL}/tareas/{tarea_id}/status", timeout=10)
    if response.status_code == 200:
        status = response.json()
        print_success("Estado obtenido")
        print_info(f"  Estado: {status.get('estado')}")
        print_info(f"  Hormigas asignadas: {status.get('hormigas_asignadas', 0)}")
        print_info(f"  Lote ID: {status.get('hormigas_lote_id')}")
        print_info(f"  Fecha inicio: {status.get('fecha_inicio')}")
        
        estado_actual = status.get('estado')
        
        # 2. Si está pendiente, iniciarla
        if estado_actual == 'pendiente':
            print_info("\n2. La tarea está pendiente. Iniciándola...")
            lote_id = status.get('hormigas_lote_id')
            if lote_id:
                iniciar_data = {"hormigas_lote_id": lote_id}
                response = requests.post(
                    f"{BASE_URL}/tareas/{tarea_id}/iniciar",
                    json=iniciar_data,
                    timeout=30
                )
                if response.status_code == 200:
                    print_success("Tarea iniciada")
                    time.sleep(2)  # Esperar a que se persista
                else:
                    print_error(f"No se pudo iniciar: {response.status_code} - {response.text}")
                    sys.exit(1)
            else:
                print_error("No hay lote_id asociado")
                sys.exit(1)
        
        # 3. Completar la tarea
        if estado_actual == 'en_proceso' or status.get('estado') == 'en_proceso':
            print_info("\n3. Completando la tarea...")
            cantidad_recolectada = 10  # Cantidad de ejemplo
            
            response = requests.post(
                f"{BASE_URL}/tareas/{tarea_id}/completar?cantidad_recolectada={cantidad_recolectada}",
                timeout=30
            )
            
            if response.status_code == 200:
                resultado = response.json()
                print_success("Tarea completada exitosamente")
                print_info(f"  Estado: {resultado.get('estado')}")
                print_info(f"  Alimento recolectado: {resultado.get('alimento_recolectado', 0)}")
                print_info(f"  Fecha fin: {resultado.get('fecha_fin')}")
                time.sleep(2)  # Esperar a que se persista
            else:
                print_error(f"No se pudo completar: {response.status_code}")
                print_error(f"Respuesta: {response.text}")
        elif estado_actual == 'completada':
            print_success("La tarea ya está completada")
        else:
            print_info(f"Estado actual: {estado_actual}")
        
        # 4. Verificar estado final
        print("\n4. Verificando estado final en BD...")
        time.sleep(1)
        
        try:
            from src.recoleccion.database.database_manager import SqlServerDatabaseManager
            
            db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
            cursor = db.connection.cursor()
            
            db._exec(cursor, """
                SELECT id, estado, inicio, fin, cantidad_recolectada, hormigas_asignadas
                FROM dbo.Tareas
                WHERE id = ?
            """, (tarea_id,))
            
            tarea_row = cursor.fetchone()
            if tarea_row:
                print_success("Estado en BD:")
                print_info(f"  ID: {tarea_row[0]}")
                print_info(f"  Estado: {tarea_row[1]}")
                print_info(f"  Inicio: {tarea_row[2]}")
                print_info(f"  Fin: {tarea_row[3]}")
                print_info(f"  Cantidad recolectada: {tarea_row[4]}")
                print_info(f"  Hormigas asignadas: {tarea_row[5]}")
                
                if tarea_row[1] == 'completada':
                    print_success("\nLa tarea fue procesada y completada correctamente")
                else:
                    print_info(f"\nLa tarea está en estado: {tarea_row[1]}")
            
            db.connection.close()
        except Exception as e:
            print_error(f"Error verificando BD: {e}")
    else:
        print_error(f"No se pudo obtener el estado: {response.status_code}")
        print_error(f"Respuesta: {response.text}")
except Exception as e:
    print_error(f"Error: {e}")
    import traceback
    traceback.print_exc()

print_header("PROCESO COMPLETADO")



