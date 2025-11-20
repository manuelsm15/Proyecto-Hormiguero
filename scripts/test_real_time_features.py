"""
Script para probar las características de tiempo real del subsistema.
"""

import requests
import time
import json
from datetime import datetime

def test_real_time_features():
    """Prueba las características de tiempo real."""
    print("=== PRUEBA DE CARACTERISTICAS DE TIEMPO REAL ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Crear una tarea con tiempo de recolección corto
        print("\n1. CREANDO TAREA CON TIEMPO CORTO:")
        tarea_id = f"tarea_tiempo_real_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        tarea_data = {
            "tarea_id": tarea_id,
            "alimento_id": "A3"  # A3 tiene tiempo_recoleccion=120 segundos
        }
        
        tarea_response = requests.post(f"{base_url}/tareas", params=tarea_data, timeout=5)
        if tarea_response.status_code == 200:
            tarea = tarea_response.json()
            print(f"  OK - Tarea creada: {tarea['id']}")
            print(f"    - Alimento: {tarea['alimento']['nombre']}")
            print(f"    - Tiempo de recolección: {tarea['alimento']['tiempo_recoleccion']} segundos")
            print(f"    - Hormigas necesarias: {tarea['alimento']['cantidad_hormigas_necesarias']}")
        else:
            print(f"  ERROR - No se pudo crear tarea")
            return False
        
        # 2. Iniciar la tarea
        print("\n2. INICIANDO TAREA:")
        iniciar_response = requests.post(f"{base_url}/tareas/{tarea_id}/iniciar", timeout=5)
        if iniciar_response.status_code == 200:
            print(f"  OK - Tarea iniciada")
        else:
            print(f"  ERROR - No se pudo iniciar tarea")
            return False
        
        # 3. Monitorear progreso en tiempo real
        print("\n3. MONITOREANDO PROGRESO EN TIEMPO REAL:")
        for i in range(10):  # Monitorear por 10 iteraciones
            try:
                # Obtener tiempo restante
                tiempo_response = requests.get(f"{base_url}/tareas/{tarea_id}/tiempo-restante", timeout=5)
                if tiempo_response.status_code == 200:
                    tiempo_restante = tiempo_response.json()
                    print(f"  Iteración {i+1}: Tiempo restante: {tiempo_restante.get('tiempo_restante', 'N/A')} segundos")
                
                # Obtener progreso
                progreso_response = requests.get(f"{base_url}/tareas/{tarea_id}/progreso", timeout=5)
                if progreso_response.status_code == 200:
                    progreso = progreso_response.json()
                    print(f"  Iteración {i+1}: Progreso: {progreso.get('progreso', 'N/A')}%")
                
                # Verificar estado
                estado_response = requests.get(f"{base_url}/tareas/{tarea_id}", timeout=5)
                if estado_response.status_code == 200:
                    tarea = estado_response.json()
                    print(f"  Iteración {i+1}: Estado: {tarea.get('estado', 'N/A')}")
                    
                    # Si la tarea está completada, salir del bucle
                    if tarea.get('estado') == 'completada':
                        print(f"  OK - Tarea completada en iteración {i+1}")
                        break
                
                # Esperar antes de la siguiente iteración
                time.sleep(2)
                
            except Exception as e:
                print(f"  ERROR en iteración {i+1}: {e}")
                break
        
        # 4. Verificar tareas en proceso
        print("\n4. VERIFICANDO TAREAS EN PROCESO:")
        tareas_proceso_response = requests.get(f"{base_url}/tareas/en-proceso", timeout=5)
        if tareas_proceso_response.status_code == 200:
            tareas_proceso = tareas_proceso_response.json()
            print(f"  OK - {len(tareas_proceso)} tareas en proceso")
            for tarea in tareas_proceso:
                print(f"    - {tarea['id']}: {tarea['estado']}")
        else:
            print(f"  ERROR - No se pudieron obtener tareas en proceso")
        
        # 5. Verificar tareas completadas
        print("\n5. VERIFICANDO TAREAS COMPLETADAS:")
        tareas_completadas_response = requests.get(f"{base_url}/tareas/completadas", timeout=5)
        if tareas_completadas_response.status_code == 200:
            tareas_completadas = tareas_completadas_response.json()
            print(f"  OK - {len(tareas_completadas)} tareas completadas")
            for tarea in tareas_completadas:
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        else:
            print(f"  ERROR - No se pudieron obtener tareas completadas")
        
        return True
        
    except Exception as e:
        print(f"ERROR GENERAL: {e}")
        return False

def test_timer_service():
    """Prueba el servicio de timer."""
    print("\n=== PRUEBA DEL SERVICIO DE TIMER ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Crear múltiples tareas
        print("\n1. CREANDO MULTIPLES TAREAS:")
        tareas_ids = []
        for i in range(3):
            tarea_id = f"tarea_timer_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            tarea_data = {
                "tarea_id": tarea_id,
                "alimento_id": f"A{i+1}"  # A1, A2, A3
            }
            
            tarea_response = requests.post(f"{base_url}/tareas", params=tarea_data, timeout=5)
            if tarea_response.status_code == 200:
                tarea = tarea_response.json()
                tareas_ids.append(tarea_id)
                print(f"  OK - Tarea {i+1} creada: {tarea['id']}")
            else:
                print(f"  ERROR - No se pudo crear tarea {i+1}")
        
        # 2. Iniciar todas las tareas
        print("\n2. INICIANDO TODAS LAS TAREAS:")
        for tarea_id in tareas_ids:
            iniciar_response = requests.post(f"{base_url}/tareas/{tarea_id}/iniciar", timeout=5)
            if iniciar_response.status_code == 200:
                print(f"  OK - Tarea {tarea_id} iniciada")
            else:
                print(f"  ERROR - No se pudo iniciar tarea {tarea_id}")
        
        # 3. Monitorear todas las tareas
        print("\n3. MONITOREANDO TODAS LAS TAREAS:")
        for i in range(5):  # Monitorear por 5 iteraciones
            print(f"\n  Iteración {i+1}:")
            for tarea_id in tareas_ids:
                try:
                    # Tiempo restante
                    tiempo_response = requests.get(f"{base_url}/tareas/{tarea_id}/tiempo-restante", timeout=5)
                    if tiempo_response.status_code == 200:
                        tiempo_restante = tiempo_response.json()
                        print(f"    {tarea_id}: Tiempo restante: {tiempo_restante.get('tiempo_restante', 'N/A')}s")
                    
                    # Progreso
                    progreso_response = requests.get(f"{base_url}/tareas/{tarea_id}/progreso", timeout=5)
                    if progreso_response.status_code == 200:
                        progreso = progreso_response.json()
                        print(f"    {tarea_id}: Progreso: {progreso.get('progreso', 'N/A')}%")
                    
                    # Estado
                    estado_response = requests.get(f"{base_url}/tareas/{tarea_id}", timeout=5)
                    if estado_response.status_code == 200:
                        tarea = estado_response.json()
                        print(f"    {tarea_id}: Estado: {tarea.get('estado', 'N/A')}")
                
                except Exception as e:
                    print(f"    ERROR con {tarea_id}: {e}")
            
            # Esperar antes de la siguiente iteración
            time.sleep(3)
        
        # 4. Verificar estado final
        print("\n4. VERIFICANDO ESTADO FINAL:")
        tareas_proceso_response = requests.get(f"{base_url}/tareas/en-proceso", timeout=5)
        if tareas_proceso_response.status_code == 200:
            tareas_proceso = tareas_proceso_response.json()
            print(f"  Tareas en proceso: {len(tareas_proceso)}")
        
        tareas_completadas_response = requests.get(f"{base_url}/tareas/completadas", timeout=5)
        if tareas_completadas_response.status_code == 200:
            tareas_completadas = tareas_completadas_response.json()
            print(f"  Tareas completadas: {len(tareas_completadas)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR GENERAL: {e}")
        return False

def main():
    """Función principal."""
    print("PRUEBA DE CARACTERISTICAS DE TIEMPO REAL")
    
    # Esperar un poco para que el servicio se inicie
    print("Esperando 3 segundos...")
    time.sleep(3)
    
    # Probar características de tiempo real
    if test_real_time_features():
        print("\nOK CARACTERISTICAS DE TIEMPO REAL EXITOSAS!")
    else:
        print("\nERROR CARACTERISTICAS DE TIEMPO REAL FALLARON!")
    
    # Probar servicio de timer
    if test_timer_service():
        print("\nOK SERVICIO DE TIMER EXITOSO!")
    else:
        print("\nERROR SERVICIO DE TIMER FALLO!")
    
    print("\n=== PRUEBA DE TIEMPO REAL FINALIZADA ===")

if __name__ == "__main__":
    main()









