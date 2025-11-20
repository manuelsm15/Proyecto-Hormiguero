"""
Script para diagnosticar problemas en el subsistema.
"""

import requests
import json
from datetime import datetime

def diagnose_issues():
    """Diagnostica problemas en el subsistema."""
    print("=== DIAGNOSTICO DE PROBLEMAS ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Verificar servicio básico
        print("\n1. VERIFICANDO SERVICIO BASICO:")
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
        
        # 2. Verificar estructura de respuestas
        print("\n2. VERIFICANDO ESTRUCTURA DE RESPUESTAS:")
        
        # Probar endpoint raiz
        root_response = requests.get(f"{base_url}/", timeout=5)
        if root_response.status_code == 200:
            root_data = root_response.json()
            print(f"  OK - Endpoint raiz")
            print(f"    - Tipo de respuesta: {type(root_data)}")
            if isinstance(root_data, dict):
                print(f"    - Claves: {list(root_data.keys())}")
            else:
                print(f"    - Contenido: {root_data}")
        else:
            print(f"  ERROR - Endpoint raiz (Status: {root_response.status_code})")
        
        # 3. Verificar alimentos
        print("\n3. VERIFICANDO ALIMENTOS:")
        alimentos_response = requests.get(f"{base_url}/alimentos", timeout=5)
        if alimentos_response.status_code == 200:
            alimentos_data = alimentos_response.json()
            print(f"  OK - Alimentos obtenidos")
            print(f"    - Tipo: {type(alimentos_data)}")
            print(f"    - Cantidad: {len(alimentos_data) if isinstance(alimentos_data, list) else 'N/A'}")
            if isinstance(alimentos_data, list) and len(alimentos_data) > 0:
                print(f"    - Primer alimento: {alimentos_data[0]}")
        else:
            print(f"  ERROR - Alimentos (Status: {alimentos_response.status_code})")
        
        # 4. Verificar tareas
        print("\n4. VERIFICANDO TAREAS:")
        tareas_response = requests.get(f"{base_url}/tareas", timeout=5)
        if tareas_response.status_code == 200:
            tareas_data = tareas_response.json()
            print(f"  OK - Tareas obtenidas")
            print(f"    - Tipo: {type(tareas_data)}")
            print(f"    - Cantidad: {len(tareas_data) if isinstance(tareas_data, list) else 'N/A'}")
            if isinstance(tareas_data, list) and len(tareas_data) > 0:
                print(f"    - Primera tarea: {tareas_data[0]}")
                if 'alimento' in tareas_data[0]:
                    print(f"    - Alimento de primera tarea: {tareas_data[0]['alimento']}")
        else:
            print(f"  ERROR - Tareas (Status: {tareas_response.status_code})")
        
        # 5. Verificar procesamiento
        print("\n5. VERIFICANDO PROCESAMIENTO:")
        procesar_response = requests.post(f"{base_url}/procesar", timeout=10)
        if procesar_response.status_code == 200:
            procesar_data = procesar_response.json()
            print(f"  OK - Procesamiento exitoso")
            print(f"    - Tipo: {type(procesar_data)}")
            print(f"    - Cantidad: {len(procesar_data) if isinstance(procesar_data, list) else 'N/A'}")
            if isinstance(procesar_data, list) and len(procesar_data) > 0:
                print(f"    - Primera tarea procesada: {procesar_data[0]}")
                if isinstance(procesar_data[0], dict):
                    print(f"    - Claves de primera tarea: {list(procesar_data[0].keys())}")
        else:
            print(f"  ERROR - Procesamiento (Status: {procesar_response.status_code})")
        
        # 6. Verificar estadísticas
        print("\n6. VERIFICANDO ESTADISTICAS:")
        stats_response = requests.get(f"{base_url}/estadisticas", timeout=5)
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"  OK - Estadísticas obtenidas")
            print(f"    - Tipo: {type(stats_data)}")
            if isinstance(stats_data, dict):
                print(f"    - Claves: {list(stats_data.keys())}")
                for key, value in stats_data.items():
                    print(f"    - {key}: {value}")
        else:
            print(f"  ERROR - Estadísticas (Status: {stats_response.status_code})")
        
        # 7. Verificar tareas completadas
        print("\n7. VERIFICANDO TAREAS COMPLETADAS:")
        completadas_response = requests.get(f"{base_url}/tareas/completadas", timeout=5)
        if completadas_response.status_code == 200:
            completadas_data = completadas_response.json()
            print(f"  OK - Tareas completadas obtenidas")
            print(f"    - Tipo: {type(completadas_data)}")
            print(f"    - Cantidad: {len(completadas_data) if isinstance(completadas_data, list) else 'N/A'}")
            if isinstance(completadas_data, list) and len(completadas_data) > 0:
                print(f"    - Primera tarea completada: {completadas_data[0]}")
        else:
            print(f"  ERROR - Tareas completadas (Status: {completadas_response.status_code})")
        
        # 8. Verificar tareas en proceso
        print("\n8. VERIFICANDO TAREAS EN PROCESO:")
        proceso_response = requests.get(f"{base_url}/tareas/en-proceso", timeout=5)
        if proceso_response.status_code == 200:
            proceso_data = proceso_response.json()
            print(f"  OK - Tareas en proceso obtenidas")
            print(f"    - Tipo: {type(proceso_data)}")
            print(f"    - Cantidad: {len(proceso_data) if isinstance(proceso_data, list) else 'N/A'}")
        else:
            print(f"  ERROR - Tareas en proceso (Status: {proceso_response.status_code})")
        
        return True
        
    except Exception as e:
        print(f"ERROR GENERAL: {e}")
        return False

def main():
    """Función principal."""
    print("DIAGNOSTICO DE PROBLEMAS DEL SUBSISTEMA")
    
    if diagnose_issues():
        print("\nOK DIAGNOSTICO COMPLETADO!")
    else:
        print("\nERROR DIAGNOSTICO FALLO!")
    
    print("\n=== DIAGNOSTICO FINALIZADO ===")

if __name__ == "__main__":
    main()









