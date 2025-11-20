"""
Ejemplos simples de uso de las APIs del subsistema de recolección.
"""

import requests
import json
import time
from datetime import datetime

def test_health():
    """Probar health check."""
    print("=== HEALTH CHECK ===")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            data = response.json()
            print(f"OK - Servicio funcionando")
            print(f"  - Status: {data['status']}")
            print(f"  - Service: {data['service']}")
            print(f"  - Version: {data['version']}")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def test_alimentos():
    """Probar consulta de alimentos."""
    print("\n=== ALIMENTOS ===")
    try:
        response = requests.get("http://localhost:8000/alimentos")
        if response.status_code == 200:
            alimentos = response.json()
            print(f"OK - Alimentos obtenidos: {len(alimentos)}")
            for alimento in alimentos:
                print(f"  - {alimento['id']}: {alimento['nombre']} (Hormigas: {alimento['cantidad_hormigas_necesarias']})")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def test_tareas():
    """Probar consulta de tareas."""
    print("\n=== TAREAS ===")
    try:
        response = requests.get("http://localhost:8000/tareas")
        if response.status_code == 200:
            tareas = response.json()
            print(f"OK - Tareas obtenidas: {len(tareas)}")
            for tarea in tareas[:3]:  # Mostrar solo las primeras 3
                print(f"  - {tarea['id']}: {tarea['estado']} (Alimento: {tarea['alimento']['id']})")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def test_crear_tarea():
    """Probar crear tarea."""
    print("\n=== CREAR TAREA ===")
    try:
        tarea_id = f"ejemplo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        response = requests.post("http://localhost:8000/tareas", 
                               params={"tarea_id": tarea_id, "alimento_id": "A1"})
        if response.status_code == 200:
            tarea = response.json()
            print(f"OK - Tarea creada")
            print(f"  - ID: {tarea['id']}")
            print(f"  - Alimento: {tarea['alimento']['nombre']}")
            print(f"  - Estado: {tarea['estado']}")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def test_procesar():
    """Probar procesamiento."""
    print("\n=== PROCESAR RECOLECCION ===")
    try:
        response = requests.post("http://localhost:8000/procesar")
        if response.status_code == 200:
            resultado = response.json()
            print(f"OK - Procesamiento exitoso")
            print(f"  - Tareas procesadas: {resultado['tareas_procesadas']}")
            if 'tareas' in resultado and len(resultado['tareas']) > 0:
                for tarea in resultado['tareas'][:2]:  # Mostrar solo las primeras 2
                    print(f"  - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def test_estadisticas():
    """Probar estadísticas."""
    print("\n=== ESTADISTICAS ===")
    try:
        response = requests.get("http://localhost:8000/estadisticas")
        if response.status_code == 200:
            stats = response.json()
            print(f"OK - Estadísticas obtenidas")
            print(f"  - Tareas activas: {stats['tareas_activas']}")
            print(f"  - Tareas completadas: {stats['tareas_completadas']}")
            print(f"  - Total alimento recolectado: {stats['total_alimento_recolectado']}")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def test_tareas_completadas():
    """Probar tareas completadas."""
    print("\n=== TAREAS COMPLETADAS ===")
    try:
        response = requests.get("http://localhost:8000/tareas/completadas")
        if response.status_code == 200:
            tareas = response.json()
            print(f"OK - Tareas completadas: {len(tareas)}")
            for tarea in tareas[:2]:  # Mostrar solo las primeras 2
                print(f"  - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def test_tareas_en_proceso():
    """Probar tareas en proceso."""
    print("\n=== TAREAS EN PROCESO ===")
    try:
        response = requests.get("http://localhost:8000/tareas/en-proceso")
        if response.status_code == 200:
            tareas = response.json()
            print(f"OK - Tareas en proceso: {len(tareas)}")
            for tarea in tareas:
                print(f"  - {tarea['id']}: {tarea['estado']}")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def test_verificar_hormigas():
    """Probar verificación de hormigas."""
    print("\n=== VERIFICAR HORMIGAS ===")
    try:
        response = requests.post("http://localhost:8000/verificar-hormigas")
        if response.status_code == 200:
            resultado = response.json()
            print(f"OK - Verificación de hormigas exitosa")
            print(f"  - Resultado: {resultado}")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def test_documentacion():
    """Probar documentación."""
    print("\n=== DOCUMENTACION ===")
    try:
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print(f"OK - Documentación disponible")
            print(f"  - URL: http://localhost:8000/docs")
        else:
            print(f"ERROR: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    """Función principal."""
    print("EJEMPLOS DE APIs - SUBSISTEMA DE RECOLECCION")
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Esperar un poco para que el servicio se inicie
    print("Esperando 3 segundos...")
    time.sleep(3)
    
    # Ejecutar ejemplos
    test_health()
    test_alimentos()
    test_tareas()
    test_crear_tarea()
    test_procesar()
    test_estadisticas()
    test_tareas_completadas()
    test_tareas_en_proceso()
    test_verificar_hormigas()
    test_documentacion()
    
    print("\n=== EJEMPLOS COMPLETADOS ===")
    print("\nURLs disponibles:")
    print("  - API: http://localhost:8000")
    print("  - Health: http://localhost:8000/health")
    print("  - Docs: http://localhost:8000/docs")
    print("  - OpenAPI: http://localhost:8000/openapi.json")

if __name__ == "__main__":
    main()









