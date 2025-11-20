"""
Script para iniciar el contenedor con hostname para pruebas externas.
"""

import subprocess
import time
import requests
import sys
import os

def start_container_with_hostname():
    """Inicia el contenedor con hostname para pruebas externas."""
    print("=== INICIANDO CONTENEDOR CON HOSTNAME ===")
    
    try:
        # Cambiar al directorio del proyecto
        os.chdir("C:\\Users\\manue\\Proyecto Hormiguero")
        
        print("Iniciando servidor con hostname...")
        print("Hostname: 192.168.18.3")
        print("Puerto: 8000")
        print("URL: http://192.168.18.3:8000/docs")
        
        # Iniciar el servidor con hostname específico
        process = subprocess.Popen([
            sys.executable, "railway_main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("Servidor iniciado exitosamente")
        print("Esperando 5 segundos para que se inicie...")
        time.sleep(5)
        
        # Probar healthcheck
        print("Probando healthcheck...")
        try:
            response = requests.get("http://localhost:8000/health", timeout=10)
            if response.status_code == 200:
                print("Healthcheck exitoso")
                health_data = response.json()
                print(f"Status: {health_data.get('status', 'unknown')}")
                print(f"Service: {health_data.get('service', 'unknown')}")
            else:
                print(f"Healthcheck fallo - Status: {response.status_code}")
        except Exception as e:
            print(f"Error en healthcheck: {e}")
        
        # Probar documentacion
        print("Probando documentacion...")
        try:
            response = requests.get("http://localhost:8000/docs", timeout=10)
            if response.status_code == 200:
                print("Documentacion disponible")
                print("URL: http://192.168.18.3:8000/docs")
            else:
                print(f"Documentacion fallo - Status: {response.status_code}")
        except Exception as e:
            print(f"Error en documentacion: {e}")
        
        print("\n=== CONTENEDOR FUNCIONANDO ===")
        print("Servidor ejecutandose en segundo plano")
        print("Para acceder desde otros dispositivos:")
        print("  - URL: http://192.168.18.3:8000")
        print("  - Docs: http://192.168.18.3:8000/docs")
        print("  - Health: http://192.168.18.3:8000/health")
        print("\nPresiona Ctrl+C para detener el servidor")
        
        # Mantener el proceso corriendo
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\nDeteniendo servidor...")
            process.terminate()
            process.wait()
            print("Servidor detenido")
        
        return True
        
    except Exception as e:
        print(f"Error iniciando contenedor: {e}")
        return False

def main():
    """Funcion principal."""
    print("=== CONTENEDOR CON HOSTNAME PARA PRUEBAS EXTERNAS ===")
    
    success = start_container_with_hostname()
    
    if success:
        print("Contenedor iniciado exitosamente")
    else:
        print("Error iniciando contenedor")
        sys.exit(1)

if __name__ == "__main__":
    main()

