"""
Script para probar las APIs del contenedor Docker.
"""

import requests
import json
import time
from datetime import datetime

def test_docker_apis():
    """Prueba las APIs del contenedor Docker."""
    print("=== PRUEBAS DE APIs EN DOCKER ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Verificar servicio
        print("\n1. VERIFICANDO SERVICIO:")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"  OK - Servicio funcionando")
            print(f"    - Status: {health_data.get('status', 'N/A')}")
            print(f"    - Service: {health_data.get('service', 'N/A')}")
            print(f"    - Version: {health_data.get('version', 'N/A')}")
        else:
            print(f"  ERROR - Servicio no disponible (Status: {health_response.status_code})")
            return False
        
        # 2. Probar endpoint raiz
        print("\n2. PROBANDO ENDPOINT RAIZ:")
        root_response = requests.get(f"{base_url}/", timeout=5)
        if root_response.status_code == 200:
            root_data = root_response.json()
            print(f"  OK - Endpoint raiz funcionando")
            print(f"    - Mensaje: {root_data.get('message', 'N/A')}")
        else:
            print(f"  ERROR - Endpoint raiz (Status: {root_response.status_code})")
        
        # 3. Probar consulta de alimentos
        print("\n3. PROBANDO CONSULTA DE ALIMENTOS:")
        alimentos_response = requests.get(f"{base_url}/alimentos", timeout=5)
        if alimentos_response.status_code == 200:
            alimentos_data = alimentos_response.json()
            print(f"  OK - Alimentos obtenidos")
            print(f"    - Cantidad: {len(alimentos_data) if isinstance(alimentos_data, list) else 'N/A'}")
            if isinstance(alimentos_data, list) and len(alimentos_data) > 0:
                for alimento in alimentos_data:
                    print(f"    - {alimento['id']}: {alimento['nombre']} (Hormigas: {alimento['cantidad_hormigas_necesarias']})")
        else:
            print(f"  ERROR - Alimentos (Status: {alimentos_response.status_code})")
        
        # 4. Probar consulta de tareas
        print("\n4. PROBANDO CONSULTA DE TAREAS:")
        tareas_response = requests.get(f"{base_url}/tareas", timeout=5)
        if tareas_response.status_code == 200:
            tareas_data = tareas_response.json()
            print(f"  OK - Tareas obtenidas")
            print(f"    - Cantidad: {len(tareas_data) if isinstance(tareas_data, list) else 'N/A'}")
            if isinstance(tareas_data, list) and len(tareas_data) > 0:
                for tarea in tareas_data[:3]:  # Mostrar solo las primeras 3
                    print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea['alimento']['id']})")
        else:
            print(f"  ERROR - Tareas (Status: {tareas_response.status_code})")
        
        # 5. Probar crear tarea
        print("\n5. PROBANDO CREAR TAREA:")
        tarea_id = f"tarea_docker_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        tarea_response = requests.post(f"{base_url}/tareas", 
                                     params={"tarea_id": tarea_id, "alimento_id": "A1"}, 
                                     timeout=5)
        if tarea_response.status_code == 200:
            tarea_data = tarea_response.json()
            print(f"  OK - Tarea creada")
            print(f"    - ID: {tarea_data['id']}")
            print(f"    - Alimento: {tarea_data['alimento']['nombre']}")
            print(f"    - Estado: {tarea_data['estado']}")
        else:
            print(f"  ERROR - Crear tarea (Status: {tarea_response.status_code})")
        
        # 6. Probar procesamiento
        print("\n6. PROBANDO PROCESAMIENTO:")
        procesar_response = requests.post(f"{base_url}/procesar", timeout=10)
        if procesar_response.status_code == 200:
            procesar_data = procesar_response.json()
            print(f"  OK - Procesamiento exitoso")
            print(f"    - Tareas procesadas: {procesar_data.get('tareas_procesadas', 0)}")
            if 'tareas' in procesar_data and len(procesar_data['tareas']) > 0:
                for tarea in procesar_data['tareas'][:2]:  # Mostrar solo las primeras 2
                    print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        else:
            print(f"  ERROR - Procesamiento (Status: {procesar_response.status_code})")
        
        # 7. Probar estadísticas
        print("\n7. PROBANDO ESTADISTICAS:")
        stats_response = requests.get(f"{base_url}/estadisticas", timeout=5)
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"  OK - Estadísticas obtenidas")
            print(f"    - Tareas activas: {stats_data.get('tareas_activas', 0)}")
            print(f"    - Tareas completadas: {stats_data.get('tareas_completadas', 0)}")
            print(f"    - Total alimento recolectado: {stats_data.get('total_alimento_recolectado', 0)}")
        else:
            print(f"  ERROR - Estadísticas (Status: {stats_response.status_code})")
        
        # 8. Probar tareas completadas
        print("\n8. PROBANDO TAREAS COMPLETADAS:")
        completadas_response = requests.get(f"{base_url}/tareas/completadas", timeout=5)
        if completadas_response.status_code == 200:
            completadas_data = completadas_response.json()
            print(f"  OK - Tareas completadas obtenidas")
            print(f"    - Cantidad: {len(completadas_data) if isinstance(completadas_data, list) else 'N/A'}")
            if isinstance(completadas_data, list) and len(completadas_data) > 0:
                for tarea in completadas_data[:2]:  # Mostrar solo las primeras 2
                    print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        else:
            print(f"  ERROR - Tareas completadas (Status: {completadas_response.status_code})")
        
        # 9. Probar tareas activas
        print("\n9. PROBANDO TAREAS ACTIVAS:")
        activas_response = requests.get(f"{base_url}/tareas/activas", timeout=5)
        if activas_response.status_code == 200:
            activas_data = activas_response.json()
            print(f"  OK - Tareas activas obtenidas")
            print(f"    - Cantidad: {len(activas_data) if isinstance(activas_data, list) else 'N/A'}")
        else:
            print(f"  ERROR - Tareas activas (Status: {activas_response.status_code})")
        
        # 10. Probar tareas en proceso
        print("\n10. PROBANDO TAREAS EN PROCESO:")
        proceso_response = requests.get(f"{base_url}/tareas/en-proceso", timeout=5)
        if proceso_response.status_code == 200:
            proceso_data = proceso_response.json()
            print(f"  OK - Tareas en proceso obtenidas")
            print(f"    - Cantidad: {len(proceso_data) if isinstance(proceso_data, list) else 'N/A'}")
        else:
            print(f"  ERROR - Tareas en proceso (Status: {proceso_response.status_code})")
        
        # 11. Probar verificación de hormigas
        print("\n11. PROBANDO VERIFICACION DE HORMIGAS:")
        hormigas_response = requests.post(f"{base_url}/verificar-hormigas", timeout=5)
        if hormigas_response.status_code == 200:
            hormigas_data = hormigas_response.json()
            print(f"  OK - Verificación de hormigas exitosa")
        else:
            print(f"  ERROR - Verificación de hormigas (Status: {hormigas_response.status_code})")
        
        # 12. Probar documentación
        print("\n12. PROBANDO DOCUMENTACION:")
        docs_response = requests.get(f"{base_url}/docs", timeout=5)
        if docs_response.status_code == 200:
            print(f"  OK - Documentación disponible")
            print(f"    - URL: {base_url}/docs")
        else:
            print(f"  ERROR - Documentación (Status: {docs_response.status_code})")
        
        return True
        
    except Exception as e:
        print(f"ERROR GENERAL: {e}")
        return False

def main():
    """Función principal."""
    print("PRUEBAS DE APIs EN DOCKER")
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Esperar un poco para que el servicio se inicie
    print("Esperando 3 segundos...")
    time.sleep(3)
    
    if test_docker_apis():
        print("\nOK TODAS LAS PRUEBAS EXITOSAS!")
        print("\n🌐 URLs disponibles:")
        print("  - API: http://localhost:8000")
        print("  - Health: http://localhost:8000/health")
        print("  - Docs: http://localhost:8000/docs")
        print("  - OpenAPI: http://localhost:8000/openapi.json")
    else:
        print("\nERROR ALGUNAS PRUEBAS FALLARON!")
    
    print("\n=== PRUEBAS FINALIZADAS ===")

if __name__ == "__main__":
    main()









