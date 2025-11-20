"""
Ejemplos de uso de las APIs del subsistema de recolección.
"""

import requests
import json
import time
from datetime import datetime

def example_health_check():
    """Ejemplo: Verificar salud del servicio."""
    print("=== EJEMPLO: HEALTH CHECK ===")
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

def example_get_alimentos():
    """Ejemplo: Obtener lista de alimentos."""
    print("\n=== EJEMPLO: OBTENER ALIMENTOS ===")
    try:
        response = requests.get("http://localhost:8000/alimentos")
        if response.status_code == 200:
            alimentos = response.json()
            print(f"✅ Alimentos obtenidos: {len(alimentos)}")
            for alimento in alimentos:
                print(f"  - {alimento['id']}: {alimento['nombre']} (Hormigas: {alimento['cantidad_hormigas_necesarias']})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_get_tareas():
    """Ejemplo: Obtener lista de tareas."""
    print("\n=== EJEMPLO: OBTENER TAREAS ===")
    try:
        response = requests.get("http://localhost:8000/tareas")
        if response.status_code == 200:
            tareas = response.json()
            print(f"✅ Tareas obtenidas: {len(tareas)}")
            for tarea in tareas[:3]:  # Mostrar solo las primeras 3
                print(f"  - {tarea['id']}: {tarea['estado']} (Alimento: {tarea['alimento']['id']})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_create_tarea():
    """Ejemplo: Crear una nueva tarea."""
    print("\n=== EJEMPLO: CREAR TAREA ===")
    try:
        tarea_id = f"ejemplo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        response = requests.post("http://localhost:8000/tareas", 
                               params={"tarea_id": tarea_id, "alimento_id": "A1"})
        if response.status_code == 200:
            tarea = response.json()
            print(f"✅ Tarea creada")
            print(f"  - ID: {tarea['id']}")
            print(f"  - Alimento: {tarea['alimento']['nombre']}")
            print(f"  - Estado: {tarea['estado']}")
            print(f"  - Hormigas necesarias: {tarea['alimento']['cantidad_hormigas_necesarias']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_process_recoleccion():
    """Ejemplo: Procesar recolección."""
    print("\n=== EJEMPLO: PROCESAR RECOLECCION ===")
    try:
        response = requests.post("http://localhost:8000/procesar")
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ Procesamiento exitoso")
            print(f"  - Tareas procesadas: {resultado['tareas_procesadas']}")
            if 'tareas' in resultado and len(resultado['tareas']) > 0:
                for tarea in resultado['tareas'][:2]:  # Mostrar solo las primeras 2
                    print(f"  - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_get_estadisticas():
    """Ejemplo: Obtener estadísticas."""
    print("\n=== EJEMPLO: OBTENER ESTADISTICAS ===")
    try:
        response = requests.get("http://localhost:8000/estadisticas")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estadísticas obtenidas")
            print(f"  - Tareas activas: {stats['tareas_activas']}")
            print(f"  - Tareas completadas: {stats['tareas_completadas']}")
            print(f"  - Total alimento recolectado: {stats['total_alimento_recolectado']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_get_tareas_completadas():
    """Ejemplo: Obtener tareas completadas."""
    print("\n=== EJEMPLO: OBTENER TAREAS COMPLETADAS ===")
    try:
        response = requests.get("http://localhost:8000/tareas/completadas")
        if response.status_code == 200:
            tareas = response.json()
            print(f"✅ Tareas completadas: {len(tareas)}")
            for tarea in tareas[:2]:  # Mostrar solo las primeras 2
                print(f"  - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_get_tareas_activas():
    """Ejemplo: Obtener tareas activas."""
    print("\n=== EJEMPLO: OBTENER TAREAS ACTIVAS ===")
    try:
        response = requests.get("http://localhost:8000/tareas/activas")
        if response.status_code == 200:
            tareas = response.json()
            print(f"✅ Tareas activas: {len(tareas)}")
            for tarea in tareas[:3]:  # Mostrar solo las primeras 3
                print(f"  - {tarea['id']}: {tarea['estado']} (Alimento: {tarea['alimento']['id']})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_get_tareas_en_proceso():
    """Ejemplo: Obtener tareas en proceso."""
    print("\n=== EJEMPLO: OBTENER TAREAS EN PROCESO ===")
    try:
        response = requests.get("http://localhost:8000/tareas/en-proceso")
        if response.status_code == 200:
            tareas = response.json()
            print(f"✅ Tareas en proceso: {len(tareas)}")
            for tarea in tareas:
                print(f"  - {tarea['id']}: {tarea['estado']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_verificar_hormigas():
    """Ejemplo: Verificar hormigas."""
    print("\n=== EJEMPLO: VERIFICAR HORMIGAS ===")
    try:
        response = requests.post("http://localhost:8000/verificar-hormigas")
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ Verificación de hormigas exitosa")
            print(f"  - Resultado: {resultado}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_iniciar_tarea():
    """Ejemplo: Iniciar una tarea específica."""
    print("\n=== EJEMPLO: INICIAR TAREA ===")
    try:
        # Primero obtener una tarea
        response = requests.get("http://localhost:8000/tareas")
        if response.status_code == 200:
            tareas = response.json()
            if tareas:
                tarea_id = tareas[0]['id']
                print(f"  - Iniciando tarea: {tarea_id}")
                
                # Iniciar la tarea
                response = requests.post(f"http://localhost:8000/tareas/{tarea_id}/iniciar")
                if response.status_code == 200:
                    resultado = response.json()
                    print(f"✅ Tarea iniciada")
                    print(f"  - Mensaje: {resultado['message']}")
                else:
                    print(f"❌ Error iniciando tarea: {response.status_code}")
            else:
                print("❌ No hay tareas disponibles")
        else:
            print(f"❌ Error obteniendo tareas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_completar_tarea():
    """Ejemplo: Completar una tarea específica."""
    print("\n=== EJEMPLO: COMPLETAR TAREA ===")
    try:
        # Primero obtener una tarea
        response = requests.get("http://localhost:8000/tareas")
        if response.status_code == 200:
            tareas = response.json()
            if tareas:
                tarea_id = tareas[0]['id']
                print(f"  - Completando tarea: {tarea_id}")
                
                # Completar la tarea
                response = requests.post(f"http://localhost:8000/tareas/{tarea_id}/completar", 
                                       params={"cantidad_recolectada": 10})
                if response.status_code == 200:
                    resultado = response.json()
                    print(f"✅ Tarea completada")
                    print(f"  - Mensaje: {resultado['message']}")
                else:
                    print(f"❌ Error completando tarea: {response.status_code}")
            else:
                print("❌ No hay tareas disponibles")
        else:
            print(f"❌ Error obteniendo tareas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal."""
    print("EJEMPLOS DE USO DE APIs - SUBSISTEMA DE RECOLECCION")
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Esperar un poco para que el servicio se inicie
    print("Esperando 3 segundos...")
    time.sleep(3)
    
    # Ejecutar ejemplos
    example_health_check()
    example_get_alimentos()
    example_get_tareas()
    example_create_tarea()
    example_process_recoleccion()
    example_get_estadisticas()
    example_get_tareas_completadas()
    example_get_tareas_activas()
    example_get_tareas_en_proceso()
    example_verificar_hormigas()
    example_iniciar_tarea()
    example_completar_tarea()
    
    print("\n=== EJEMPLOS COMPLETADOS ===")
    print("\n🌐 URLs disponibles:")
    print("  - API: http://localhost:8000")
    print("  - Health: http://localhost:8000/health")
    print("  - Docs: http://localhost:8000/docs")
    print("  - OpenAPI: http://localhost:8000/openapi.json")

if __name__ == "__main__":
    main()
