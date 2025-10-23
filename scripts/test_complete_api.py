"""
Script para probar todas las APIs del subsistema de recoleccion.
"""

import requests
import time
import sys

def test_complete_api():
    """Prueba todas las APIs del subsistema."""
    print("=== PRUEBA COMPLETA DE APIs ===")
    
    base_url = "http://localhost:8000"
    
    # Lista de endpoints a probar
    endpoints = [
        ("/", "GET", "Endpoint raiz"),
        ("/health", "GET", "Healthcheck"),
        ("/alimentos", "GET", "Lista de alimentos"),
        ("/docs", "GET", "Documentacion Swagger"),
        ("/openapi.json", "GET", "Especificacion OpenAPI")
    ]
    
    results = []
    
    for endpoint, method, description in endpoints:
        print(f"\nProbando {description}...")
        print(f"  URL: {base_url}{endpoint}")
        
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:
                response = requests.post(f"{base_url}{endpoint}", timeout=10)
            
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
    print(f"\n=== RESUMEN ===")
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"Total de pruebas: {total}")
    print(f"Exitosas: {passed}")
    print(f"Fallidas: {failed}")
    print(f"Porcentaje de exito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("TODAS LAS PRUEBAS EXITOSAS!")
        return True
    else:
        print("ALGUNAS PRUEBAS FALLARON!")
        return False

if __name__ == "__main__":
    print("Iniciando prueba completa de APIs...")
    
    # Esperar un poco para que el servidor se inicie
    print("Esperando 2 segundos...")
    time.sleep(2)
    
    success = test_complete_api()
    
    if success:
        print("\nAPIs funcionando correctamente - Listo para deploy!")
        sys.exit(0)
    else:
        print("\nAPIs con problemas - Revisar antes del deploy!")
        sys.exit(1)

