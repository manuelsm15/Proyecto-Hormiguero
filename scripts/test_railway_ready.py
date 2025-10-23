"""
Script para verificar que el proyecto esta listo para Railway.
"""

import requests
import time
import sys

def test_railway_readiness():
    """Verifica que el proyecto esta listo para Railway."""
    print("=== VERIFICACION DE READINESS PARA RAILWAY ===")
    
    base_url = "http://localhost:8000"
    
    # Lista de endpoints criticos para Railway
    critical_endpoints = [
        ("/health", "GET", "Healthcheck - CRITICO para Railway"),
        ("/", "GET", "Endpoint raiz"),
        ("/alimentos", "GET", "Lista de alimentos"),
        ("/docs", "GET", "Documentacion Swagger"),
        ("/tareas", "GET", "Lista de tareas"),
        ("/tareas/en-proceso", "GET", "Tareas en proceso"),
        ("/estadisticas", "GET", "Estadisticas del servicio")
    ]
    
    results = []
    
    for endpoint, method, description in critical_endpoints:
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
    print(f"\n=== RESUMEN DE READINESS ===")
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"Total de pruebas: {total}")
    print(f"Exitosas: {passed}")
    print(f"Fallidas: {failed}")
    print(f"Porcentaje de exito: {(passed/total)*100:.1f}%")
    
    # Verificaciones especificas para Railway
    print(f"\n=== VERIFICACIONES ESPECIFICAS PARA RAILWAY ===")
    
    # 1. Healthcheck debe funcionar
    healthcheck_ok = results[0] if len(results) > 0 else False
    print(f"1. Healthcheck funcionando: {'SI' if healthcheck_ok else 'NO'}")
    
    # 2. Servidor debe responder en puerto correcto
    print(f"2. Servidor respondiendo en localhost:8000: {'SI' if passed > 0 else 'NO'}")
    
    # 3. Documentacion debe estar disponible
    docs_ok = results[3] if len(results) > 3 else False
    print(f"3. Documentacion Swagger disponible: {'SI' if docs_ok else 'NO'}")
    
    # 4. APIs principales funcionando
    apis_ok = results[1] and results[2] if len(results) > 2 else False
    print(f"4. APIs principales funcionando: {'SI' if apis_ok else 'NO'}")
    
    # Verificacion final
    railway_ready = healthcheck_ok and docs_ok and apis_ok
    
    print(f"\n=== RESULTADO FINAL ===")
    if railway_ready:
        print("OK PROYECTO LISTO PARA RAILWAY!")
        print("OK Healthcheck funcionando")
        print("OK APIs principales funcionando")
        print("OK Documentacion disponible")
        print("OK Servidor estable")
        return True
    else:
        print("ERROR PROYECTO NO LISTO PARA RAILWAY!")
        print("ERROR Revisar errores antes del deploy")
        return False

if __name__ == "__main__":
    print("Iniciando verificacion de readiness para Railway...")
    
    # Esperar un poco para que el servidor se inicie
    print("Esperando 2 segundos...")
    time.sleep(2)
    
    success = test_railway_readiness()
    
    if success:
        print("\nLISTO PARA DEPLOY EN RAILWAY!")
        sys.exit(0)
    else:
        print("\nNO LISTO PARA DEPLOY - REVISAR ERRORES!")
        sys.exit(1)
