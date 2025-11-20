"""
Script para probar toda la funcionalidad del subsistema de recolección.
"""

import requests
import time
import json
from datetime import datetime

def test_full_functionality():
    """Prueba completa de toda la funcionalidad del subsistema."""
    print("=== PRUEBA COMPLETA DE FUNCIONALIDAD ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Verificar servicio
        print("\n1. VERIFICANDO SERVICIO:")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            print("  OK - Servicio funcionando")
        else:
            print("  ERROR - Servicio no disponible")
            return False
        
        # 2. Probar consulta de alimentos
        print("\n2. PROBANDO CONSULTA DE ALIMENTOS:")
        alimentos_response = requests.get(f"{base_url}/alimentos", timeout=5)
        if alimentos_response.status_code == 200:
            alimentos = alimentos_response.json()
            print(f"  OK - {len(alimentos)} alimentos disponibles")
            for alimento in alimentos:
                print(f"    - {alimento['id']}: {alimento['nombre']} (Hormigas: {alimento['cantidad_hormigas_necesarias']})")
        else:
            print(f"  ERROR - No se pudieron obtener alimentos")
        
        # 3. Crear una tarea de recolección
        print("\n3. CREANDO TAREA DE RECOLECCION:")
        tarea_id = f"tarea_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        tarea_response = requests.post(f"{base_url}/tareas", params={"tarea_id": tarea_id, "alimento_id": "A1"}, timeout=5)
        if tarea_response.status_code == 200:
            tarea = tarea_response.json()
            print(f"  OK - Tarea creada: {tarea['id']}")
            print(f"    - Alimento: {tarea['alimento']['nombre']}")
            print(f"    - Estado: {tarea['estado']}")
            print(f"    - Hormigas necesarias: {tarea['alimento']['cantidad_hormigas_necesarias']}")
        else:
            print(f"  ERROR - No se pudo crear tarea")
        
        # 4. Verificar tareas existentes
        print("\n4. VERIFICANDO TAREAS EXISTENTES:")
        tareas_response = requests.get(f"{base_url}/tareas", timeout=5)
        if tareas_response.status_code == 200:
            tareas = tareas_response.json()
            print(f"  OK - {len(tareas)} tareas en total")
            for tarea in tareas:
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea['alimento']['id']})")
        else:
            print(f"  ERROR - No se pudieron obtener tareas")
        
        # 5. Probar procesamiento de recolección
        print("\n5. PROBANDO PROCESAMIENTO DE RECOLECCION:")
        procesar_response = requests.post(f"{base_url}/procesar", timeout=10)
        if procesar_response.status_code == 200:
            resultado = procesar_response.json()
            print(f"  OK - Procesamiento exitoso")
            print(f"    - Tareas procesadas: {resultado.get('tareas_procesadas', 0)}")
            if 'tareas' in resultado:
                for tarea in resultado['tareas']:
                    print(f"      - {tarea['id']}: {tarea['estado']} (Alimento: {tarea.get('alimento_recolectado', 'N/A')})")
        else:
            print(f"  ERROR - No se pudo procesar recolección")
        
        # 6. Verificar tareas completadas
        print("\n6. VERIFICANDO TAREAS COMPLETADAS:")
        tareas_completadas_response = requests.get(f"{base_url}/tareas/completadas", timeout=5)
        if tareas_completadas_response.status_code == 200:
            tareas_completadas = tareas_completadas_response.json()
            print(f"  OK - {len(tareas_completadas)} tareas completadas")
            for tarea in tareas_completadas:
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea['alimento_recolectado']})")
        else:
            print(f"  ERROR - No se pudieron obtener tareas completadas")
        
        # 7. Verificar tareas en proceso
        print("\n7. VERIFICANDO TAREAS EN PROCESO:")
        tareas_proceso_response = requests.get(f"{base_url}/tareas/en-proceso", timeout=5)
        if tareas_proceso_response.status_code == 200:
            tareas_proceso = tareas_proceso_response.json()
            print(f"  OK - {len(tareas_proceso)} tareas en proceso")
            for tarea in tareas_proceso:
                print(f"    - {tarea['id']}: {tarea['estado']}")
        else:
            print(f"  ERROR - No se pudieron obtener tareas en proceso")
        
        # 8. Probar verificación de hormigas
        print("\n8. PROBANDO VERIFICACION DE HORMIGAS:")
        hormigas_response = requests.post(f"{base_url}/verificar-hormigas", timeout=5)
        if hormigas_response.status_code == 200:
            resultado_hormigas = hormigas_response.json()
            print(f"  OK - Verificación de hormigas exitosa")
        else:
            print(f"  ERROR - No se pudo verificar hormigas")
        
        # 9. Obtener estadísticas
        print("\n9. OBTENIENDO ESTADISTICAS:")
        stats_response = requests.get(f"{base_url}/estadisticas", timeout=5)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"  OK - Estadísticas obtenidas")
            print(f"    - Tareas activas: {stats.get('tareas_activas', 0)}")
            print(f"    - Tareas completadas: {stats.get('tareas_completadas', 0)}")
            print(f"    - Alimentos disponibles: {stats.get('alimentos_disponibles', 0)}")
            print(f"    - Mensajes procesados: {stats.get('mensajes_procesados', 0)}")
        else:
            print(f"  ERROR - No se pudieron obtener estadísticas")
        
        # 10. Probar documentación
        print("\n10. PROBANDO DOCUMENTACION:")
        docs_response = requests.get(f"{base_url}/docs", timeout=5)
        if docs_response.status_code == 200:
            print(f"  OK - Documentación disponible")
            print(f"    - URL: {base_url}/docs")
        else:
            print(f"  ERROR - Documentación no disponible")
        
        return True
        
    except Exception as e:
        print(f"ERROR GENERAL: {e}")
        return False

def test_api_endpoints():
    """Prueba todos los endpoints de la API."""
    print("\n=== PRUEBA DE ENDPOINTS DE API ===")
    
    base_url = "http://localhost:8000"
    endpoints = [
        ("/", "GET", "Endpoint raiz"),
        ("/health", "GET", "Healthcheck"),
        ("/alimentos", "GET", "Lista de alimentos"),
        ("/tareas", "GET", "Lista de tareas"),
        ("/tareas", "POST", "Crear tarea"),
        ("/tareas/en-proceso", "GET", "Tareas en proceso"),
        ("/tareas/completadas", "GET", "Tareas completadas"),
        ("/procesar", "POST", "Procesar recolección"),
        ("/verificar-hormigas", "POST", "Verificar hormigas"),
        ("/estadisticas", "GET", "Estadísticas"),
        ("/docs", "GET", "Documentación Swagger"),
        ("/openapi.json", "GET", "Especificación OpenAPI")
    ]
    
    results = []
    
    for endpoint, method, description in endpoints:
        print(f"\nProbando {description}...")
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            else:
                if endpoint == "/tareas":
                    response = requests.post(f"{base_url}{endpoint}", params={"tarea_id": "test_endpoint", "alimento_id": "A1"}, timeout=5)
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
    
    print(f"\n=== RESUMEN DE PRUEBAS DE API ===")
    print(f"Total de endpoints: {total}")
    print(f"Exitosos: {passed}")
    print(f"Fallidos: {failed}")
    print(f"Porcentaje de éxito: {(passed/total)*100:.1f}%")
    
    return passed == total

def main():
    """Función principal."""
    print("PRUEBA COMPLETA DE FUNCIONALIDAD DEL SUBSISTEMA DE RECOLECCION")
    
    # Esperar un poco para que el servicio se inicie
    print("Esperando 3 segundos...")
    time.sleep(3)
    
    # Probar funcionalidad completa
    if test_full_functionality():
        print("\nOK FUNCIONALIDAD COMPLETA EXITOSA!")
    else:
        print("\nERROR FUNCIONALIDAD COMPLETA FALLO!")
    
    # Probar endpoints de API
    if test_api_endpoints():
        print("\nOK TODOS LOS ENDPOINTS FUNCIONANDO!")
    else:
        print("\nERROR ALGUNOS ENDPOINTS FALLARON!")
    
    print("\n=== PRUEBA COMPLETA FINALIZADA ===")

if __name__ == "__main__":
    main()
