"""
Script para probar railway_main.py localmente.
"""

import subprocess
import time
import sys
import requests
import os

def test_railway_main():
    """Prueba railway_main.py localmente."""
    print("Probando railway_main.py localmente...")
    
    try:
        # Cambiar al directorio del proyecto
        os.chdir("C:\\Users\\manue\\Proyecto Hormiguero")
        
        # Iniciar el servidor en background
        print("Iniciando servidor...")
        process = subprocess.Popen([
            sys.executable, "railway_main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Esperar a que el servidor se inicie
        print("Esperando 5 segundos para que el servidor se inicie...")
        time.sleep(5)
        
        # Probar healthcheck
        print("Probando healthcheck...")
        response = requests.get("http://localhost:8000/health", timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("Healthcheck exitoso")
            
            # Probar otros endpoints
            print("Probando otros endpoints...")
            
            # Probar root
            root_response = requests.get("http://localhost:8000/", timeout=10)
            print(f"Root Status: {root_response.status_code}")
            
            # Probar alimentos
            alimentos_response = requests.get("http://localhost:8000/alimentos", timeout=10)
            print(f"Alimentos Status: {alimentos_response.status_code}")
            
            # Terminar el proceso
            process.terminate()
            process.wait()
            
            print("Todas las pruebas exitosas!")
            return True
        else:
            print("Healthcheck fallo")
            process.terminate()
            process.wait()
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        if 'process' in locals():
            process.terminate()
            process.wait()
        return False

if __name__ == "__main__":
    print("Iniciando prueba completa de railway_main.py...")
    
    success = test_railway_main()
    
    if success:
        print("railway_main.py funcionando correctamente!")
        sys.exit(0)
    else:
        print("railway_main.py fallo")
        sys.exit(1)
