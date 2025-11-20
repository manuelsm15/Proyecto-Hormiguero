"""
Script para probar la persistencia de datos del subsistema.
"""

import requests
import time
import json
from datetime import datetime

def test_persistence():
    """Prueba la persistencia de datos."""
    print("=== PRUEBA DE PERSISTENCIA DE DATOS ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Verificar datos iniciales
        print("\n1. VERIFICANDO DATOS INICIALES:")
        stats_response = requests.get(f"{base_url}/estadisticas", timeout=5)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"  OK - Estadísticas iniciales obtenidas")
            print(f"    - Tareas activas: {stats.get('tareas_activas', 0)}")
            print(f"    - Tareas completadas: {stats.get('tareas_completadas', 0)}")
            print(f"    - Alimentos disponibles: {stats.get('alimentos_disponibles', 0)}")
        else:
            print(f"  ERROR - No se pudieron obtener estadísticas iniciales")
        
        # 2. Crear múltiples tareas
        print("\n2. CREANDO MULTIPLES TAREAS:")
        tareas_ids = []
        for i in range(5):
            tarea_id = f"tarea_persistencia_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            tarea_data = {
                "tarea_id": tarea_id,
                "alimento_id": f"A{(i % 3) + 1}"  # A1, A2, A3, A1, A2
            }
            
            tarea_response = requests.post(f"{base_url}/tareas", params=tarea_data, timeout=5)
            if tarea_response.status_code == 200:
                tarea = tarea_response.json()
                tareas_ids.append(tarea_id)
                print(f"  OK - Tarea {i+1} creada: {tarea['id']}")
            else:
                print(f"  ERROR - No se pudo crear tarea {i+1}")
        
        # 3. Verificar tareas creadas
        print("\n3. VERIFICANDO TAREAS CREADAS:")
        tareas_response = requests.get(f"{base_url}/tareas", timeout=5)
        if tareas_response.status_code == 200:
            tareas = tareas_response.json()
            print(f"  OK - {len(tareas)} tareas en total")
            for tarea in tareas:
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea['alimento']['id']})")
        else:
            print(f"  ERROR - No se pudieron obtener tareas")
        
        # 4. Procesar algunas tareas
        print("\n4. PROCESANDO ALGUNAS TAREAS:")
        procesar_response = requests.post(f"{base_url}/procesar", timeout=10)
        if procesar_response.status_code == 200:
            resultado = procesar_response.json()
            print(f"  OK - {len(resultado)} tareas procesadas")
            for tarea in resultado:
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        else:
            print(f"  ERROR - No se pudo procesar tareas")
        
        # 5. Verificar estado después del procesamiento
        print("\n5. VERIFICANDO ESTADO DESPUES DEL PROCESAMIENTO:")
        stats_response = requests.get(f"{base_url}/estadisticas", timeout=5)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"  OK - Estadísticas después del procesamiento")
            print(f"    - Tareas activas: {stats.get('tareas_activas', 0)}")
            print(f"    - Tareas completadas: {stats.get('tareas_completadas', 0)}")
            print(f"    - Alimentos disponibles: {stats.get('alimentos_disponibles', 0)}")
        else:
            print(f"  ERROR - No se pudieron obtener estadísticas después del procesamiento")
        
        # 6. Verificar tareas completadas
        print("\n6. VERIFICANDO TAREAS COMPLETADAS:")
        tareas_completadas_response = requests.get(f"{base_url}/tareas/completadas", timeout=5)
        if tareas_completadas_response.status_code == 200:
            tareas_completadas = tareas_completadas_response.json()
            print(f"  OK - {len(tareas_completadas)} tareas completadas")
            for tarea in tareas_completadas:
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        else:
            print(f"  ERROR - No se pudieron obtener tareas completadas")
        
        # 7. Verificar tareas activas
        print("\n7. VERIFICANDO TAREAS ACTIVAS:")
        tareas_activas_response = requests.get(f"{base_url}/tareas/activas", timeout=5)
        if tareas_activas_response.status_code == 200:
            tareas_activas = tareas_activas_response.json()
            print(f"  OK - {len(tareas_activas)} tareas activas")
            for tarea in tareas_activas:
                print(f"    - {tarea['id']}: {tarea['estado']}")
        else:
            print(f"  ERROR - No se pudieron obtener tareas activas")
        
        # 8. Probar persistencia de mensajes
        print("\n8. PROBANDO PERSISTENCIA DE MENSAJES:")
        mensajes_response = requests.get(f"{base_url}/mensajes", timeout=5)
        if mensajes_response.status_code == 200:
            mensajes = mensajes_response.json()
            print(f"  OK - {len(mensajes)} mensajes en el sistema")
            for mensaje in mensajes:
                print(f"    - {mensaje['id']}: {mensaje['tipo']} (Origen: {mensaje['subsistema_origen']})")
        else:
            print(f"  ERROR - No se pudieron obtener mensajes")
        
        # 9. Probar persistencia de eventos
        print("\n9. PROBANDO PERSISTENCIA DE EVENTOS:")
        eventos_response = requests.get(f"{base_url}/eventos", timeout=5)
        if eventos_response.status_code == 200:
            eventos = eventos_response.json()
            print(f"  OK - {len(eventos)} eventos en el sistema")
            for evento in eventos:
                print(f"    - {evento['id']}: {evento['tipo_evento']} - {evento['descripcion']}")
        else:
            print(f"  ERROR - No se pudieron obtener eventos")
        
        return True
        
    except Exception as e:
        print(f"ERROR GENERAL: {e}")
        return False

def test_data_consistency():
    """Prueba la consistencia de los datos."""
    print("\n=== PRUEBA DE CONSISTENCIA DE DATOS ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Verificar consistencia de tareas
        print("\n1. VERIFICANDO CONSISTENCIA DE TAREAS:")
        tareas_response = requests.get(f"{base_url}/tareas", timeout=5)
        if tareas_response.status_code == 200:
            tareas = tareas_response.json()
            print(f"  OK - {len(tareas)} tareas en total")
            
            # Verificar que cada tarea tenga un alimento válido
            for tarea in tareas:
                if 'alimento' in tarea and tarea['alimento']:
                    print(f"    - {tarea['id']}: Alimento válido ({tarea['alimento']['id']})")
                else:
                    print(f"    - {tarea['id']}: ERROR - Sin alimento")
        
        # 2. Verificar consistencia de estadísticas
        print("\n2. VERIFICANDO CONSISTENCIA DE ESTADISTICAS:")
        stats_response = requests.get(f"{base_url}/estadisticas", timeout=5)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"  OK - Estadísticas consistentes")
            print(f"    - Tareas activas: {stats.get('tareas_activas', 0)}")
            print(f"    - Tareas completadas: {stats.get('tareas_completadas', 0)}")
            print(f"    - Total esperado: {stats.get('tareas_activas', 0) + stats.get('tareas_completadas', 0)}")
        else:
            print(f"  ERROR - No se pudieron obtener estadísticas")
        
        # 3. Verificar consistencia de alimentos
        print("\n3. VERIFICANDO CONSISTENCIA DE ALIMENTOS:")
        alimentos_response = requests.get(f"{base_url}/alimentos", timeout=5)
        if alimentos_response.status_code == 200:
            alimentos = alimentos_response.json()
            print(f"  OK - {len(alimentos)} alimentos disponibles")
            for alimento in alimentos:
                print(f"    - {alimento['id']}: {alimento['nombre']} (Hormigas: {alimento['cantidad_hormigas_necesarias']})")
        else:
            print(f"  ERROR - No se pudieron obtener alimentos")
        
        return True
        
    except Exception as e:
        print(f"ERROR GENERAL: {e}")
        return False

def main():
    """Función principal."""
    print("PRUEBA DE PERSISTENCIA DE DATOS")
    
    # Esperar un poco para que el servicio se inicie
    print("Esperando 3 segundos...")
    time.sleep(3)
    
    # Probar persistencia
    if test_persistence():
        print("\nOK PERSISTENCIA EXITOSA!")
    else:
        print("\nERROR PERSISTENCIA FALLO!")
    
    # Probar consistencia de datos
    if test_data_consistency():
        print("\nOK CONSISTENCIA DE DATOS EXITOSA!")
    else:
        print("\nERROR CONSISTENCIA DE DATOS FALLO!")
    
    print("\n=== PRUEBA DE PERSISTENCIA FINALIZADA ===")

if __name__ == "__main__":
    main()









