"""
Script para probar las funcionalidades especificas del subsistema de recoleccion.
"""

import requests
import time
import sys

def test_recoleccion_features():
    """Prueba las funcionalidades especificas del subsistema."""
    print("=== PRUEBA DE FUNCIONALIDADES DE RECOLECCION ===")
    
    base_url = "http://localhost:8000"
    
    # 1. Probar consulta de alimentos
    print("\n1. Probando consulta de alimentos...")
    try:
        response = requests.get(f"{base_url}/alimentos", timeout=10)
        if response.status_code == 200:
            alimentos = response.json()
            print(f"  OK - Encontrados {len(alimentos)} alimentos")
            for alimento in alimentos:
                print(f"    - {alimento['id']}: {alimento['nombre']} (Hormigas: {alimento['cantidad_hormigas_necesarias']})")
        else:
            print(f"  ERROR - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False
    
    # 2. Probar consulta de alimento especifico
    print("\n2. Probando consulta de alimento especifico...")
    try:
        response = requests.get(f"{base_url}/alimentos/A1", timeout=10)
        if response.status_code == 200:
            alimento = response.json()
            print(f"  OK - Alimento A1: {alimento['nombre']}")
        else:
            print(f"  ERROR - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False
    
    # 3. Probar creacion de tarea
    print("\n3. Probando creacion de tarea...")
    try:
        tarea_data = {
            "id": "tarea_test_001",
            "alimento_id": "A1"
        }
        response = requests.post(f"{base_url}/tareas", json=tarea_data, timeout=10)
        if response.status_code == 200:
            tarea = response.json()
            print(f"  OK - Tarea creada: {tarea['id']}")
        else:
            print(f"  ERROR - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False
    
    # 4. Probar consulta de tareas
    print("\n4. Probando consulta de tareas...")
    try:
        response = requests.get(f"{base_url}/tareas", timeout=10)
        if response.status_code == 200:
            tareas = response.json()
            print(f"  OK - Encontradas {len(tareas)} tareas")
        else:
            print(f"  ERROR - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False
    
    # 5. Probar tareas en proceso
    print("\n5. Probando tareas en proceso...")
    try:
        response = requests.get(f"{base_url}/tareas/en-proceso", timeout=10)
        if response.status_code == 200:
            tareas = response.json()
            print(f"  OK - Tareas en proceso: {len(tareas)}")
        else:
            print(f"  ERROR - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False
    
    print("\n=== TODAS LAS FUNCIONALIDADES FUNCIONANDO ===")
    return True

if __name__ == "__main__":
    print("Iniciando prueba de funcionalidades de recoleccion...")
    
    # Esperar un poco para que el servidor se inicie
    print("Esperando 2 segundos...")
    time.sleep(2)
    
    success = test_recoleccion_features()
    
    if success:
        print("\nFUNCIONALIDADES DE RECOLECCION FUNCIONANDO CORRECTAMENTE!")
        sys.exit(0)
    else:
        print("\nFUNCIONALIDADES DE RECOLECCION CON PROBLEMAS!")
        sys.exit(1)

