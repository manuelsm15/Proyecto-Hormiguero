"""
Script para simular el entorno Docker y probar las APIs.
"""

import subprocess
import sys
import time
import requests
import os
from datetime import datetime

def simulate_docker_environment():
    """Simula el entorno Docker ejecutando el servicio directamente."""
    print("=== SIMULANDO ENTORNO DOCKER ===")
    
    try:
        # Verificar si el servicio ya está ejecutándose
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ Servicio ya está ejecutándose")
                return True
        except:
            pass
        
        # Ejecutar el servicio en segundo plano
        print("Iniciando servicio...")
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Esperar a que el servicio se inicie
        print("Esperando servicio...")
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("OK - Servicio iniciado exitosamente")
                    return True
            except:
                pass
            
            attempt += 1
            print(f"  Intento {attempt}/{max_attempts}...")
            time.sleep(2)
        
        print("ERROR - Servicio no se pudo iniciar")
        return False
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_api_endpoints():
    """Prueba todos los endpoints de la API."""
    print("\n=== PROBANDO ENDPOINTS DE API ===")
    
    base_url = "http://localhost:8000"
    endpoints = [
        ("/", "GET", "Endpoint raiz"),
        ("/health", "GET", "Healthcheck"),
        ("/alimentos", "GET", "Lista de alimentos"),
        ("/tareas", "GET", "Lista de tareas"),
        ("/tareas", "POST", "Crear tarea"),
        ("/tareas/activas", "GET", "Tareas activas"),
        ("/tareas/completadas", "GET", "Tareas completadas"),
        ("/tareas/en-proceso", "GET", "Tareas en proceso"),
        ("/procesar", "POST", "Procesar recolección"),
        ("/verificar-hormigas", "POST", "Verificar hormigas"),
        ("/estadisticas", "GET", "Estadísticas"),
        ("/docs", "GET", "Documentación Swagger")
    ]
    
    results = []
    
    for endpoint, method, description in endpoints:
        print(f"\nProbando {description}...")
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            else:
                if endpoint == "/tareas":
                    response = requests.post(f"{base_url}{endpoint}", 
                                           params={"tarea_id": "test_simulacion", "alimento_id": "A1"}, 
                                           timeout=5)
                else:
                    response = requests.post(f"{base_url}{endpoint}", timeout=5)
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  OK - {description}")
                results.append(True)
            else:
                print(f"  ERROR - {description} (Status: {response.status_code})")
                results.append(False)
                
        except Exception as e:
            print(f"  ERROR - {description}: {e}")
            results.append(False)
    
    # Resumen
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"\n=== RESUMEN DE PRUEBAS ===")
    print(f"Total de endpoints: {total}")
    print(f"Exitosos: {passed}")
    print(f"Fallidos: {failed}")
    print(f"Porcentaje de éxito: {(passed/total)*100:.1f}%")
    
    return passed == total

def show_api_examples():
    """Muestra ejemplos de uso de las APIs."""
    print("\n=== EJEMPLOS DE USO DE APIs ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Health check
        print("\n1. HEALTH CHECK:")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"  OK - Servicio funcionando")
            print(f"    - Status: {data['status']}")
            print(f"    - Service: {data['service']}")
            print(f"    - Version: {data['version']}")
        
        # 2. Obtener alimentos
        print("\n2. OBTENER ALIMENTOS:")
        response = requests.get(f"{base_url}/alimentos")
        if response.status_code == 200:
            alimentos = response.json()
            print(f"  OK - Alimentos obtenidos: {len(alimentos)}")
            for alimento in alimentos:
                print(f"    - {alimento['id']}: {alimento['nombre']} (Hormigas: {alimento['cantidad_hormigas_necesarias']})")
        
        # 3. Obtener tareas
        print("\n3. OBTENER TAREAS:")
        response = requests.get(f"{base_url}/tareas")
        if response.status_code == 200:
            tareas = response.json()
            print(f"  OK - Tareas obtenidas: {len(tareas)}")
            for tarea in tareas[:3]:  # Mostrar solo las primeras 3
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea['alimento']['id']})")
        
        # 4. Crear tarea
        print("\n4. CREAR TAREA:")
        tarea_id = f"ejemplo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        response = requests.post(f"{base_url}/tareas", 
                               params={"tarea_id": tarea_id, "alimento_id": "A1"})
        if response.status_code == 200:
            tarea = response.json()
            print(f"  OK - Tarea creada")
            print(f"    - ID: {tarea['id']}")
            print(f"    - Alimento: {tarea['alimento']['nombre']}")
            print(f"    - Estado: {tarea['estado']}")
        
        # 5. Procesar recolección
        print("\n5. PROCESAR RECOLECCION:")
        response = requests.post(f"{base_url}/procesar")
        if response.status_code == 200:
            resultado = response.json()
            print(f"  OK - Procesamiento exitoso")
            print(f"    - Tareas procesadas: {resultado['tareas_procesadas']}")
            if 'tareas' in resultado and len(resultado['tareas']) > 0:
                for tarea in resultado['tareas'][:2]:  # Mostrar solo las primeras 2
                    print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        
        # 6. Obtener estadísticas
        print("\n6. OBTENER ESTADISTICAS:")
        response = requests.get(f"{base_url}/estadisticas")
        if response.status_code == 200:
            stats = response.json()
            print(f"  OK - Estadísticas obtenidas")
            print(f"    - Tareas activas: {stats['tareas_activas']}")
            print(f"    - Tareas completadas: {stats['tareas_completadas']}")
            print(f"    - Total alimento recolectado: {stats['total_alimento_recolectado']}")
        
        # 7. Obtener tareas completadas
        print("\n7. OBTENER TAREAS COMPLETADAS:")
        response = requests.get(f"{base_url}/tareas/completadas")
        if response.status_code == 200:
            tareas = response.json()
            print(f"  OK - Tareas completadas: {len(tareas)}")
            for tarea in tareas[:2]:  # Mostrar solo las primeras 2
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        
        # 8. Obtener tareas activas
        print("\n8. OBTENER TAREAS ACTIVAS:")
        response = requests.get(f"{base_url}/tareas/activas")
        if response.status_code == 200:
            tareas = response.json()
            print(f"  OK - Tareas activas: {len(tareas)}")
            for tarea in tareas[:3]:  # Mostrar solo las primeras 3
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea['alimento']['id']})")
        
        # 9. Obtener tareas en proceso
        print("\n9. OBTENER TAREAS EN PROCESO:")
        response = requests.get(f"{base_url}/tareas/en-proceso")
        if response.status_code == 200:
            tareas = response.json()
            print(f"  OK - Tareas en proceso: {len(tareas)}")
            for tarea in tareas:
                print(f"    - {tarea['id']}: {tarea['estado']}")
        
        # 10. Verificar hormigas
        print("\n10. VERIFICAR HORMIGAS:")
        response = requests.post(f"{base_url}/verificar-hormigas")
        if response.status_code == 200:
            resultado = response.json()
            print(f"  OK - Verificación de hormigas exitosa")
            print(f"    - Resultado: {resultado}")
        
        return True
        
    except Exception as e:
        print(f"ERROR en ejemplos: {e}")
        return False

def main():
    """Función principal."""
    print("SIMULACION DE ENTORNO DOCKER - SUBSISTEMA DE RECOLECCION")
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Simular entorno Docker
    if not simulate_docker_environment():
        print("ERROR - No se pudo simular el entorno Docker")
        return 1
    
    # 2. Probar endpoints
    if not test_api_endpoints():
        print("ERROR - Algunos endpoints fallaron")
        return 1
    
    # 3. Mostrar ejemplos
    if not show_api_examples():
        print("ERROR - Error en ejemplos")
        return 1
    
    print("\n=== SIMULACION COMPLETADA ===")
    print("OK - Entorno Docker simulado")
    print("OK - Servicio ejecutándose")
    print("OK - APIs funcionando")
    print("\nURLs disponibles:")
    print("  - API: http://localhost:8000")
    print("  - Health: http://localhost:8000/health")
    print("  - Docs: http://localhost:8000/docs")
    print("  - OpenAPI: http://localhost:8000/openapi.json")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
