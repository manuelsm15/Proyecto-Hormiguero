"""
Script para manejar Docker y probar las APIs.
"""

import subprocess
import time
import requests
import sys
import os

def check_docker_installed():
    """Verifica si Docker esta instalado."""
    print("Verificando si Docker esta instalado...")
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Docker instalado: {result.stdout.strip()}")
            return True
        else:
            print("Docker no esta instalado")
            return False
    except FileNotFoundError:
        print("Docker no encontrado en el sistema")
        return False

def build_docker_image():
    """Construye la imagen Docker."""
    print("Construyendo imagen Docker...")
    try:
        result = subprocess.run([
            "docker", "build", 
            "-f", "Dockerfile.railway",
            "-t", "hormiguero-recoleccion",
            "."
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Imagen Docker construida exitosamente")
            return True
        else:
            print(f"Error construyendo imagen: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def run_docker_container():
    """Ejecuta el contenedor Docker."""
    print("Ejecutando contenedor Docker...")
    try:
        result = subprocess.run([
            "docker", "run", 
            "-d",  # Detached mode
            "-p", "8000:8000",  # Mapear puerto
            "--name", "hormiguero-test",
            "hormiguero-recoleccion"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Contenedor ejecutandose exitosamente")
            print(f"Container ID: {result.stdout.strip()}")
            return True
        else:
            print(f"Error ejecutando contenedor: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_docker_apis():
    """Prueba las APIs en el contenedor Docker."""
    print("Probando APIs en contenedor Docker...")
    
    base_url = "http://localhost:8000"
    
    # Esperar a que el contenedor se inicie
    print("Esperando 10 segundos para que el contenedor se inicie...")
    time.sleep(10)
    
    # Lista de endpoints a probar
    endpoints = [
        ("/health", "Healthcheck"),
        ("/", "Endpoint raiz"),
        ("/alimentos", "Lista de alimentos"),
        ("/docs", "Documentacion Swagger"),
        ("/tareas", "Lista de tareas"),
        ("/estadisticas", "Estadisticas")
    ]
    
    results = []
    
    for endpoint, description in endpoints:
        print(f"\nProbando {description}...")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
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
    
    print(f"\n=== RESUMEN DE PRUEBAS DOCKER ===")
    print(f"Total de pruebas: {total}")
    print(f"Exitosas: {passed}")
    print(f"Fallidas: {failed}")
    print(f"Porcentaje de exito: {(passed/total)*100:.1f}%")
    
    return passed == total

def stop_docker_container():
    """Detiene y elimina el contenedor Docker."""
    print("Deteniendo contenedor Docker...")
    try:
        # Detener contenedor
        subprocess.run(["docker", "stop", "hormiguero-test"], capture_output=True)
        # Eliminar contenedor
        subprocess.run(["docker", "rm", "hormiguero-test"], capture_output=True)
        print("Contenedor detenido y eliminado")
    except Exception as e:
        print(f"Error deteniendo contenedor: {e}")

def main():
    """Funcion principal."""
    print("=== DOCKER TEST PARA HORMIGUERO RECOLECCION ===")
    
    # 1. Verificar Docker
    if not check_docker_installed():
        print("ERROR: Docker no esta instalado")
        print("Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop")
        sys.exit(1)
    
    # 2. Construir imagen
    if not build_docker_image():
        print("ERROR: No se pudo construir la imagen Docker")
        sys.exit(1)
    
    # 3. Ejecutar contenedor
    if not run_docker_container():
        print("ERROR: No se pudo ejecutar el contenedor Docker")
        sys.exit(1)
    
    # 4. Probar APIs
    try:
        if test_docker_apis():
            print("\nTODAS LAS PRUEBAS DOCKER EXITOSAS!")
            print("El contenedor Docker funciona correctamente")
        else:
            print("\nALGUNAS PRUEBAS DOCKER FALLARON!")
            print("Revisar logs del contenedor")
    finally:
        # 5. Limpiar
        stop_docker_container()
    
    print("\n=== DOCKER TEST COMPLETADO ===")

if __name__ == "__main__":
    main()
