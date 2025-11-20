"""
Script para construir y ejecutar el contenedor Docker del subsistema de recolección.
"""

import subprocess
import sys
import time
import requests
from datetime import datetime

def build_docker_image():
    """Construye la imagen Docker."""
    print("=== CONSTRUYENDO IMAGEN DOCKER ===")
    try:
        result = subprocess.run([
            "docker", "build", "-t", "recoleccion-api", "."
        ], capture_output=True, text=True, check=True)
        
        print("OK - Imagen Docker construida exitosamente")
        print("Imagen: recoleccion-api")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR - Fallo al construir imagen Docker: {e}")
        print(f"STDERR: {e.stderr}")
        return False
    except FileNotFoundError:
        print("ERROR - Docker no está instalado o no está en el PATH")
        return False

def run_docker_container():
    """Ejecuta el contenedor Docker."""
    print("\n=== EJECUTANDO CONTENEDOR DOCKER ===")
    try:
        # Detener contenedor existente si existe
        subprocess.run(["docker", "stop", "recoleccion-container"], 
                      capture_output=True, text=True)
        subprocess.run(["docker", "rm", "recoleccion-container"], 
                      capture_output=True, text=True)
        
        # Ejecutar nuevo contenedor
        result = subprocess.run([
            "docker", "run", "-d",
            "--name", "recoleccion-container",
            "-p", "8000:8000",
            "-e", "PYTHONPATH=/app",
            "-e", "LOG_LEVEL=INFO",
            "recoleccion-api"
        ], capture_output=True, text=True, check=True)
        
        container_id = result.stdout.strip()
        print(f"OK - Contenedor ejecutándose")
        print(f"Container ID: {container_id}")
        print(f"Puerto: 8000")
        print(f"URL: http://localhost:8000")
        print(f"Documentación: http://localhost:8000/docs")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR - Fallo al ejecutar contenedor: {e}")
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
                print("OK - Servicio disponible")
                return True
        except:
            pass
        
        attempt += 1
        print(f"Intento {attempt}/{max_attempts} - Esperando servicio...")
        time.sleep(2)
    
    print("ERROR - Servicio no disponible después de 60 segundos")
    return False

def test_api_endpoints():
    """Prueba los endpoints de la API."""
    print("\n=== PROBANDO ENDPOINTS DE API ===")
    
    base_url = "http://localhost:8000"
    endpoints = [
        ("/", "GET", "Endpoint raiz"),
        ("/health", "GET", "Healthcheck"),
        ("/alimentos", "GET", "Lista de alimentos"),
        ("/tareas", "GET", "Lista de tareas"),
        ("/tareas", "POST", "Crear tarea"),
        ("/tareas/activas", "GET", "Tareas activas"),
        ("/tareas/completadas", "GET", "Tareas completadas"),
        ("/tareas/en-proceso", "GET", "Tareas en proceso"),
        ("/procesar", "POST", "Procesar recolección"),
        ("/verificar-hormigas", "POST", "Verificar hormigas"),
        ("/estadisticas", "GET", "Estadísticas"),
        ("/docs", "GET", "Documentación Swagger")
    ]
    
    results = []
    
    for endpoint, method, description in endpoints:
        print(f"\nProbando {description}...")
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            else:
                if endpoint == "/tareas":
                    response = requests.post(f"{base_url}{endpoint}", 
                                           params={"tarea_id": "test_docker", "alimento_id": "A1"}, 
                                           timeout=5)
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
    
    print(f"\n=== RESUMEN DE PRUEBAS ===")
    print(f"Total de endpoints: {total}")
    print(f"Exitosos: {passed}")
    print(f"Fallidos: {failed}")
    print(f"Porcentaje de éxito: {(passed/total)*100:.1f}%")
    
    return passed == total

def show_docker_info():
    """Muestra información del contenedor Docker."""
    print("\n=== INFORMACIÓN DEL CONTENEDOR ===")
    try:
        # Mostrar contenedores en ejecución
        result = subprocess.run([
            "docker", "ps", "--filter", "name=recoleccion-container"
        ], capture_output=True, text=True, check=True)
        
        print("Contenedores en ejecución:")
        print(result.stdout)
        
        # Mostrar logs del contenedor
        print("\nÚltimos logs del contenedor:")
        result = subprocess.run([
            "docker", "logs", "--tail", "10", "recoleccion-container"
        ], capture_output=True, text=True, check=True)
        
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR - No se pudo obtener información del contenedor: {e}")

def main():
    """Función principal."""
    print("DOCKER BUILD AND RUN - SUBSISTEMA DE RECOLECCION")
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Construir imagen Docker
    if not build_docker_image():
        print("\nERROR - No se pudo construir la imagen Docker")
        return 1
    
    # 2. Ejecutar contenedor
    if not run_docker_container():
        print("\nERROR - No se pudo ejecutar el contenedor")
        return 1
    
    # 3. Esperar servicio
    if not wait_for_service():
        print("\nERROR - Servicio no disponible")
        return 1
    
    # 4. Probar endpoints
    if not test_api_endpoints():
        print("\nERROR - Algunos endpoints fallaron")
        return 1
    
    # 5. Mostrar información
    show_docker_info()
    
    print("\n=== DOCKER SETUP COMPLETADO ===")
    print("✅ Imagen construida")
    print("✅ Contenedor ejecutándose")
    print("✅ Servicio disponible")
    print("✅ APIs funcionando")
    print("\n🌐 URLs disponibles:")
    print("  - API: http://localhost:8000")
    print("  - Health: http://localhost:8000/health")
    print("  - Docs: http://localhost:8000/docs")
    print("  - OpenAPI: http://localhost:8000/openapi.json")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)









