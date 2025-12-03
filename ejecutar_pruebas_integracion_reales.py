"""
Script maestro que inicia el servicio y ejecuta pruebas de integración reales.
"""
import subprocess
import sys
import os
import time
import requests
import signal
from threading import Thread

BASE_URL = "http://localhost:8000"
SERVICE_STARTUP_TIME = 5

def print_header(text):
    print(f"\n{'='*80}")
    print(f"{text}")
    print(f"{'='*80}")

def print_success(message):
    print(f"[OK] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_info(message):
    print(f"[INFO] {message}")

def wait_for_service(max_retries=10):
    """Espera a que el servicio esté disponible."""
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
        print_info(f"Esperando servicio... ({i+1}/{max_retries})")
    return False

def start_service():
    """Inicia el servicio FastAPI en un proceso separado."""
    print_info("Iniciando servicio FastAPI...")
    process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return process

def main():
    print_header("EJECUTOR DE PRUEBAS DE INTEGRACIÓN REALES")
    
    # Verificar si el servicio ya está corriendo
    if wait_for_service(max_retries=3):
        print_success("Servicio ya está corriendo")
        service_process = None
    else:
        # Iniciar servicio
        service_process = start_service()
        print_info(f"Esperando {SERVICE_STARTUP_TIME} segundos para que el servicio inicie...")
        time.sleep(SERVICE_STARTUP_TIME)
        
        # Verificar que el servicio inició
        if not wait_for_service():
            print_error("No se pudo iniciar el servicio")
            if service_process:
                service_process.terminate()
            sys.exit(1)
        
        print_success("Servicio iniciado correctamente")
    
    # Ejecutar pruebas
    print_header("EJECUTANDO PRUEBAS DE INTEGRACIÓN")
    try:
        result = subprocess.run(
            [sys.executable, "test_integracion_real_completo.py"],
            cwd=os.getcwd()
        )
        exit_code = result.returncode
    except Exception as e:
        print_error(f"Error al ejecutar pruebas: {e}")
        exit_code = 1
    
    # Detener servicio si lo iniciamos
    if service_process:
        print_info("Deteniendo servicio...")
        service_process.terminate()
        try:
            service_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            service_process.kill()
        print_success("Servicio detenido")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()



