"""
Script para probar acceso externo al contenedor.
"""

import requests
import time
import sys

def test_external_access():
    """Prueba el acceso externo al contenedor."""
    print("=== PRUEBA DE ACCESO EXTERNO AL CONTENEDOR ===")
    
    # URLs para probar
    base_urls = [
        "http://localhost:8000",
        "http://192.168.18.3:8000",
        "http://127.0.0.1:8000"
    ]
    
    endpoints = [
        ("/health", "Healthcheck"),
        ("/", "Endpoint raiz"),
        ("/alimentos", "Lista de alimentos"),
        ("/docs", "Documentacion Swagger"),
        ("/tareas", "Lista de tareas"),
        ("/estadisticas", "Estadisticas")
    ]
    
    results = []
    
    for base_url in base_urls:
        print(f"\nProbando acceso desde: {base_url}")
        
        for endpoint, description in endpoints:
            url = f"{base_url}{endpoint}"
            print(f"  Probando {description}...")
            
            try:
                response = requests.get(url, timeout=10)
                print(f"    Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"    OK - {description}")
                    results.append(True)
                else:
                    print(f"    ERROR - {description} (Status: {response.status_code})")
                    results.append(False)
                    
            except Exception as e:
                print(f"    ERROR - {description}: {e}")
                results.append(False)
    
    # Resumen
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"\n=== RESUMEN DE PRUEBAS EXTERNAS ===")
    print(f"Total de pruebas: {total}")
    print(f"Exitosas: {passed}")
    print(f"Fallidas: {failed}")
    print(f"Porcentaje de exito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\nTODAS LAS PRUEBAS EXTERNAS EXITOSAS!")
        print("El contenedor es accesible desde:")
        print("  - localhost:8000")
        print("  - 192.168.18.3:8000")
        print("  - 127.0.0.1:8000")
        return True
    else:
        print("\nALGUNAS PRUEBAS EXTERNAS FALLARON!")
        return False

def main():
    """Funcion principal."""
    print("Iniciando prueba de acceso externo...")
    
    # Esperar un poco para que el servidor se inicie
    print("Esperando 3 segundos...")
    time.sleep(3)
    
    success = test_external_access()
    
    if success:
        print("\nCONTENEDOR LISTO PARA ACCESO EXTERNO!")
        print("Puedes acceder desde otros dispositivos usando:")
        print("  http://192.168.18.3:8000/docs")
    else:
        print("\nPROBLEMAS CON ACCESO EXTERNO!")
        sys.exit(1)

if __name__ == "__main__":
    main()

