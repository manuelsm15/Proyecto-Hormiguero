"""
Script para gestionar el contenedor Docker del subsistema de recolección.
"""

import subprocess
import sys
import time
import requests
from datetime import datetime

def show_docker_status():
    """Muestra el estado de Docker."""
    print("=== ESTADO DE DOCKER ===")
    try:
        # Verificar si Docker está instalado
        result = subprocess.run(["docker", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Docker instalado: {result.stdout.strip()}")
        
        # Verificar contenedores en ejecución
        result = subprocess.run(["docker", "ps", "--filter", "name=recoleccion-container"], 
                              capture_output=True, text=True, check=True)
        
        if "recoleccion-container" in result.stdout:
            print("✅ Contenedor recoleccion-container en ejecución")
            print(result.stdout)
        else:
            print("❌ Contenedor recoleccion-container no está en ejecución")
        
        # Verificar imágenes
        result = subprocess.run(["docker", "images", "recoleccion-api"], 
                              capture_output=True, text=True, check=True)
        
        if "recoleccion-api" in result.stdout:
            print("✅ Imagen recoleccion-api disponible")
            print(result.stdout)
        else:
            print("❌ Imagen recoleccion-api no disponible")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando Docker: {e}")
        return False
    except FileNotFoundError:
        print("❌ Docker no está instalado o no está en el PATH")
        return False

def stop_container():
    """Detiene el contenedor."""
    print("\n=== DETENIENDO CONTENEDOR ===")
    try:
        result = subprocess.run(["docker", "stop", "recoleccion-container"], 
                              capture_output=True, text=True, check=True)
        print("✅ Contenedor detenido")
        return True
    except subprocess.CalledProcessError:
        print("⚠️ Contenedor no estaba en ejecución")
        return True

def remove_container():
    """Elimina el contenedor."""
    print("\n=== ELIMINANDO CONTENEDOR ===")
    try:
        result = subprocess.run(["docker", "rm", "recoleccion-container"], 
                              capture_output=True, text=True, check=True)
        print("✅ Contenedor eliminado")
        return True
    except subprocess.CalledProcessError:
        print("⚠️ Contenedor no existía")
        return True

def remove_image():
    """Elimina la imagen."""
    print("\n=== ELIMINANDO IMAGEN ===")
    try:
        result = subprocess.run(["docker", "rmi", "recoleccion-api"], 
                              capture_output=True, text=True, check=True)
        print("✅ Imagen eliminada")
        return True
    except subprocess.CalledProcessError:
        print("⚠️ Imagen no existía")
        return True

def build_image():
    """Construye la imagen."""
    print("\n=== CONSTRUYENDO IMAGEN ===")
    try:
        result = subprocess.run(["docker", "build", "-t", "recoleccion-api", "."], 
                              capture_output=True, text=True, check=True)
        print("✅ Imagen construida exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error construyendo imagen: {e}")
        print(f"STDERR: {e.stderr}")
        return False

def run_container():
    """Ejecuta el contenedor."""
    print("\n=== EJECUTANDO CONTENEDOR ===")
    try:
        result = subprocess.run([
            "docker", "run", "-d",
            "--name", "recoleccion-container",
            "-p", "8000:8000",
            "-e", "PYTHONPATH=/app",
            "-e", "LOG_LEVEL=INFO",
            "recoleccion-api"
        ], capture_output=True, text=True, check=True)
        
        container_id = result.stdout.strip()
        print(f"✅ Contenedor ejecutándose")
        print(f"Container ID: {container_id}")
        print(f"Puerto: 8000")
        print(f"URL: http://localhost:8000")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando contenedor: {e}")
        print(f"STDERR: {e.stderr}")
        return False

def wait_for_service():
    """Espera a que el servicio esté disponible."""
    print("\n=== ESPERANDO SERVICIO ===")
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Servicio disponible")
                return True
        except:
            pass
        
        attempt += 1
        print(f"Intento {attempt}/{max_attempts} - Esperando servicio...")
        time.sleep(2)
    
    print("❌ Servicio no disponible después de 60 segundos")
    return False

def test_service():
    """Prueba el servicio."""
    print("\n=== PROBANDO SERVICIO ===")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Servicio funcionando")
            print(f"  - Status: {health_data.get('status', 'N/A')}")
            print(f"  - Service: {health_data.get('service', 'N/A')}")
            print(f"  - Version: {health_data.get('version', 'N/A')}")
            return True
        else:
            print(f"❌ Servicio no disponible (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error probando servicio: {e}")
        return False

def show_logs():
    """Muestra los logs del contenedor."""
    print("\n=== LOGS DEL CONTENEDOR ===")
    try:
        result = subprocess.run(["docker", "logs", "--tail", "20", "recoleccion-container"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error obteniendo logs: {e}")
        return False

def main():
    """Función principal."""
    print("DOCKER MANAGER - SUBSISTEMA DE RECOLECCION")
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if len(sys.argv) < 2:
        print("\nUso: python docker_manager.py [comando]")
        print("\nComandos disponibles:")
        print("  status     - Mostrar estado de Docker")
        print("  build      - Construir imagen")
        print("  run        - Ejecutar contenedor")
        print("  stop       - Detener contenedor")
        print("  remove     - Eliminar contenedor")
        print("  clean      - Limpiar todo (stop + remove + rmi)")
        print("  restart    - Reiniciar contenedor")
        print("  logs       - Mostrar logs")
        print("  test       - Probar servicio")
        print("  full       - Construir + ejecutar + probar")
        return 0
    
    command = sys.argv[1].lower()
    
    if command == "status":
        show_docker_status()
    
    elif command == "build":
        build_image()
    
    elif command == "run":
        run_container()
        wait_for_service()
    
    elif command == "stop":
        stop_container()
    
    elif command == "remove":
        stop_container()
        remove_container()
    
    elif command == "clean":
        stop_container()
        remove_container()
        remove_image()
    
    elif command == "restart":
        stop_container()
        remove_container()
        run_container()
        wait_for_service()
    
    elif command == "logs":
        show_logs()
    
    elif command == "test":
        test_service()
    
    elif command == "full":
        print("=== EJECUTANDO SETUP COMPLETO ===")
        if build_image():
            if run_container():
                if wait_for_service():
                    test_service()
                    print("\n✅ SETUP COMPLETO EXITOSO!")
                    print("\n🌐 URLs disponibles:")
                    print("  - API: http://localhost:8000")
                    print("  - Health: http://localhost:8000/health")
                    print("  - Docs: http://localhost:8000/docs")
                    print("  - OpenAPI: http://localhost:8000/openapi.json")
                else:
                    print("❌ Servicio no disponible")
            else:
                print("❌ No se pudo ejecutar contenedor")
        else:
            print("❌ No se pudo construir imagen")
    
    else:
        print(f"❌ Comando desconocido: {command}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)









