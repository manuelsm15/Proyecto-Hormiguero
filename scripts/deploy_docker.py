#!/usr/bin/env python3
"""
Script para deployment con Docker del Subsistema de Recolección.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

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
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} falló")
        print(f"Error: {e.stderr}")
        return False

def check_docker():
    """Verifica que Docker esté instalado."""
    print_header("VERIFICANDO DOCKER")
    
    # Verificar Docker
    if not run_command("docker --version", "Verificar Docker"):
        print("ERROR: Docker no está instalado")
        print("Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop")
        return False
    
    # Verificar Docker Compose
    if not run_command("docker-compose --version", "Verificar Docker Compose"):
        print("ERROR: Docker Compose no está instalado")
        return False
    
    print("OK: Docker y Docker Compose están instalados")
    return True

def build_and_deploy():
    """Construye y despliega la aplicación."""
    print_header("CONSTRUYENDO Y DESPLEGANDO")
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"Directorio de trabajo: {os.getcwd()}")
    
    # Parar contenedores existentes
    run_command("docker-compose down", "Parar contenedores existentes")
    
    # Construir imagen
    if not run_command("docker-compose build", "Construir imagen Docker"):
        return False
    
    # Iniciar servicios
    if not run_command("docker-compose up -d", "Iniciar servicios"):
        return False
    
    print("OK: Servicios iniciados correctamente")
    return True

def verify_deployment():
    """Verifica que el deployment esté funcionando."""
    print_header("VERIFICANDO DEPLOYMENT")
    
    # Esperar a que los servicios estén listos
    print("Esperando a que los servicios estén listos...")
    time.sleep(10)
    
    # Verificar health check
    if run_command("curl -f http://localhost:8000/health", "Verificar health check"):
        print("OK: API está funcionando correctamente")
    else:
        print("WARNING: No se pudo verificar el health check")
    
    # Mostrar logs
    print("\nMostrando logs de los contenedores:")
    run_command("docker-compose logs --tail=20", "Mostrar logs recientes")
    
    return True

def show_access_info():
    """Muestra información de acceso."""
    print_header("INFORMACION DE ACCESO")
    
    print("URLs disponibles:")
    print("- API Principal: http://localhost:8000")
    print("- Documentación Swagger: http://localhost:8000/docs")
    print("- Documentación ReDoc: http://localhost:8000/redoc")
    print("- Health Check: http://localhost:8000/health")
    print("- Nginx Proxy: http://localhost:80")
    
    print("\nPara acceso desde otra máquina:")
    print("- Reemplaza 'localhost' con la IP de tu máquina")
    print("- Ejemplo: http://192.168.1.100:8000")
    
    print("\nComandos útiles:")
    print("- Ver logs: docker-compose logs -f")
    print("- Parar servicios: docker-compose down")
    print("- Reiniciar: docker-compose restart")
    print("- Estado: docker-compose ps")

def run_tests_in_docker():
    """Ejecuta pruebas dentro del contenedor."""
    print_header("EJECUTANDO PRUEBAS EN DOCKER")
    
    # Ejecutar pruebas unitarias
    if run_command("docker-compose exec recoleccion-api python -m pytest tests/ -v", "Ejecutar pruebas unitarias"):
        print("OK: Pruebas unitarias completadas")
    
    # Ejecutar pruebas con cobertura
    if run_command("docker-compose exec recoleccion-api python -m pytest tests/ --cov=src --cov-report=html", "Ejecutar pruebas con cobertura"):
        print("OK: Pruebas con cobertura completadas")
    
    # Ejecutar pruebas BDD
    if run_command("docker-compose exec recoleccion-api behave features/simple_test.feature -v", "Ejecutar pruebas BDD"):
        print("OK: Pruebas BDD completadas")

def main():
    """Función principal."""
    print("DEPLOYMENT DOCKER - SUBSISTEMA DE RECOLECCION")
    print("Universidad Cenfotec - Proyecto Final")
    print("="*60)
    
    # Verificar Docker
    if not check_docker():
        return 1
    
    # Construir y desplegar
    if not build_and_deploy():
        print("ERROR: Falló el deployment")
        return 1
    
    # Verificar deployment
    verify_deployment()
    
    # Mostrar información de acceso
    show_access_info()
    
    # Preguntar si ejecutar pruebas
    print("\n¿Deseas ejecutar las pruebas en Docker? (s/n)")
    respuesta = input().lower()
    if respuesta == 's':
        run_tests_in_docker()
    
    print(f"\n{'='*60}")
    print("DEPLOYMENT COMPLETADO EXITOSAMENTE")
    print("El subsistema está disponible para pruebas locales y remotas")
    print(f"{'='*60}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
