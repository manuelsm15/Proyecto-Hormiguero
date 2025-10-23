#!/usr/bin/env python3
"""
Script para hostear el Subsistema de Recolección en producción.
Permite acceso desde cualquier máquina en la red local.
"""

import os
import sys
import subprocess
import socket
import threading
import time
from pathlib import Path

def get_local_ip():
    """Obtiene la IP local de la máquina."""
    try:
        # Conectar a una dirección externa para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def print_header(title):
    """Imprime un encabezado formateado."""
    print(f"\n{'='*60}")
    print(f">>> {title}")
    print(f"{'='*60}")

def run_command(command, description):
    """Ejecuta un comando y maneja errores."""
    print(f"\nEjecutando: {description}")
    print(f"Comando: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"OK: {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} falló")
        print(f"Error: {e.stderr}")
        return False

def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    print_header("VERIFICANDO DEPENDENCIAS")
    
    # Verificar Python
    if not run_command("python --version", "Verificar Python"):
        print("ERROR: Python no está instalado")
        return False
    
    # Verificar pip
    if not run_command("pip --version", "Verificar pip"):
        print("ERROR: pip no está instalado")
        return False
    
    # Instalar dependencias
    if not run_command("pip install -r requirements.txt", "Instalar dependencias"):
        print("ERROR: No se pudieron instalar las dependencias")
        return False
    
    print("OK: Todas las dependencias están instaladas")
    return True

def create_production_config():
    """Crea configuración de producción."""
    print_header("CREANDO CONFIGURACION DE PRODUCCION")
    
    # Crear archivo de configuración de producción
    config_content = """
# Configuración de producción para el Subsistema de Recolección
import uvicorn
from src.recoleccion.api.recoleccion_controller import create_app
from src.recoleccion.services.mock_entorno_service import MockEntornoService
from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService

# Crear instancias de los servicios mock
entorno_service = MockEntornoService()
comunicacion_service = MockComunicacionService()

# Crear la aplicación FastAPI
app = create_app(entorno_service, comunicacion_service)

def main():
    \"\"\"Función principal para ejecutar en producción.\"\"\"
    # Configuración para acceso desde cualquier IP
    uvicorn.run(
        app,
        host="0.0.0.0",  # Permitir acceso desde cualquier IP
        port=8000,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
"""
    
    with open("production_main.py", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("OK: Configuración de producción creada")
    return True

def start_server():
    """Inicia el servidor de producción."""
    print_header("INICIANDO SERVIDOR DE PRODUCCION")
    
    # Obtener IP local
    local_ip = get_local_ip()
    
    print(f"IP Local detectada: {local_ip}")
    print("Iniciando servidor en modo producción...")
    print("Presiona Ctrl+C para detener el servidor")
    
    # Iniciar servidor
    try:
        subprocess.run([
            "python", "production_main.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: El servidor falló: {e}")
        return False
    
    return True

def show_access_info():
    """Muestra información de acceso."""
    print_header("INFORMACION DE ACCESO")
    
    local_ip = get_local_ip()
    
    print("URLs disponibles:")
    print(f"- API Principal: http://{local_ip}:8000")
    print(f"- Documentación Swagger: http://{local_ip}:8000/docs")
    print(f"- Documentación ReDoc: http://{local_ip}:8000/redoc")
    print(f"- Health Check: http://{local_ip}:8000/health")
    print(f"- Local (solo tu máquina): http://localhost:8000")
    
    print("\nPara que tu compañero acceda:")
    print(f"1. Comparte esta IP: {local_ip}")
    print(f"2. Tu compañero debe usar: http://{local_ip}:8000")
    print("3. Asegúrate de que el firewall permita el puerto 8000")
    
    print("\nComandos de prueba:")
    print(f"# Desde tu máquina:")
    print(f"curl http://localhost:8000/health")
    print(f"# Desde otra máquina:")
    print(f"curl http://{local_ip}:8000/health")

def run_tests():
    """Ejecuta las pruebas."""
    print_header("EJECUTANDO PRUEBAS")
    
    # Ejecutar pruebas unitarias
    if run_command("python -m pytest tests/ -v", "Pruebas unitarias"):
        print("OK: Pruebas unitarias completadas")
    
    # Ejecutar pruebas con cobertura
    if run_command("python -m pytest tests/ --cov=src --cov-report=html", "Pruebas con cobertura"):
        print("OK: Pruebas con cobertura completadas")
    
    # Ejecutar pruebas BDD
    if run_command("behave features/simple_test.feature -v", "Pruebas BDD"):
        print("OK: Pruebas BDD completadas")

def main():
    """Función principal."""
    print("HOSTING DE PRODUCCION - SUBSISTEMA DE RECOLECCION")
    print("Universidad Cenfotec - Proyecto Final")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"Directorio de trabajo: {os.getcwd()}")
    
    # Verificar dependencias
    if not check_dependencies():
        return 1
    
    # Crear configuración de producción
    if not create_production_config():
        return 1
    
    # Mostrar información de acceso
    show_access_info()
    
    # Preguntar si ejecutar pruebas
    print("\n¿Deseas ejecutar las pruebas antes de iniciar el servidor? (s/n)")
    respuesta = input().lower()
    if respuesta == 's':
        run_tests()
    
    print(f"\n{'='*60}")
    print("INICIANDO SERVIDOR DE PRODUCCION")
    print("El servidor estará disponible para acceso local y remoto")
    print("Presiona Ctrl+C para detener el servidor")
    print(f"{'='*60}")
    
    # Iniciar servidor
    start_server()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

