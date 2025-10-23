#!/usr/bin/env python3
"""
Script simplificado para iniciar el servidor de producción.
"""

import os
import sys
import subprocess
import socket
from pathlib import Path

def get_local_ip():
    """Obtiene la IP local de la máquina."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    """Función principal."""
    print("INICIANDO SERVIDOR DE PRODUCCION")
    print("Subsistema de Recolección - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Obtener IP local
    local_ip = get_local_ip()
    
    print(f"IP Local: {local_ip}")
    print(f"Directorio: {os.getcwd()}")
    
    # Crear configuración de producción
    config_content = '''
import uvicorn
from src.recoleccion.api.recoleccion_controller import create_app
from src.recoleccion.services.mock_entorno_service import MockEntornoService
from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService

# Crear instancias de los servicios mock
entorno_service = MockEntornoService()
comunicacion_service = MockComunicacionService()

# Crear la aplicación FastAPI
app = create_app(entorno_service, comunicacion_service)

if __name__ == "__main__":
    print("🚀 Iniciando servidor de producción...")
    print(f"🌐 Acceso local: http://localhost:8000")
    print(f"🌐 Acceso remoto: http://{local_ip}:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("="*60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
'''
    
    with open("production_main.py", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("✅ Configuración creada")
    print("🚀 Iniciando servidor...")
    print("="*60)
    
    # Mostrar información de acceso
    print(f"URLs disponibles:")
    print(f"- Local: http://localhost:8000")
    print(f"- Remoto: http://{local_ip}:8000")
    print(f"- Documentación: http://{local_ip}:8000/docs")
    print(f"- Health Check: http://{local_ip}:8000/health")
    print("="*60)
    print("Para detener el servidor, presiona Ctrl+C")
    print("="*60)
    
    try:
        # Iniciar servidor
        subprocess.run(["python", "production_main.py"], check=True)
    except KeyboardInterrupt:
        print("\n✅ Servidor detenido")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

