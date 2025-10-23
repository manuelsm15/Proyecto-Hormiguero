#!/usr/bin/env python3
"""
Script para desplegar automáticamente en Railway usando Docker.
"""

import os
import subprocess
import sys
import time
import requests
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

def check_prerequisites():
    """Verifica prerrequisitos."""
    print_header("VERIFICANDO PRERREQUISITOS")
    
    # Verificar Node.js
    if not run_command("node --version", "Verificar Node.js"):
        print("ERROR: Node.js no está instalado")
        print("Descarga desde: https://nodejs.org/")
        return False
    
    # Verificar npm
    if not run_command("npm --version", "Verificar npm"):
        print("ERROR: npm no está instalado")
        return False
    
    # Verificar archivos necesarios
    required_files = ["requirements.txt", "main.py", "Dockerfile.railway"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"ERROR: Archivo {file} no encontrado")
            return False
    
    print("OK: Todos los prerrequisitos están disponibles")
    return True

def install_railway_cli():
    """Instala Railway CLI."""
    print_header("INSTALANDO RAILWAY CLI")
    
    if run_command("railway --version", "Verificar Railway CLI"):
        print("OK: Railway CLI ya está instalado")
        return True
    
    print("Instalando Railway CLI...")
    if run_command("npm install -g @railway/cli", "Instalar Railway CLI"):
        print("OK: Railway CLI instalado exitosamente")
        return True
    else:
        print("ERROR: No se pudo instalar Railway CLI")
        return False

def setup_railway_project():
    """Configura el proyecto en Railway."""
    print_header("CONFIGURANDO PROYECTO EN RAILWAY")
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"Directorio: {os.getcwd()}")
    
    # Login a Railway
    print("Iniciando sesión en Railway...")
    print("Se abrirá una ventana del navegador para autenticación")
    if not run_command("railway login", "Login en Railway"):
        print("ERROR: No se pudo iniciar sesión en Railway")
        return False
    
    # Crear proyecto
    print("Creando proyecto en Railway...")
    if not run_command("railway init", "Inicializar proyecto Railway"):
        print("ERROR: No se pudo crear el proyecto")
        return False
    
    return True

def deploy_to_railway():
    """Despliega el proyecto a Railway."""
    print_header("DESPLEGANDO A RAILWAY")
    
    # Desplegar usando Docker
    print("Desplegando aplicación con Docker...")
    if not run_command("railway up", "Desplegar a Railway"):
        print("ERROR: Falló el despliegue")
        return None
    
    # Esperar a que el deployment esté listo
    print("Esperando a que el deployment esté listo...")
    time.sleep(30)
    
    # Obtener URL
    print("Obteniendo URL del proyecto...")
    result = subprocess.run("railway domain", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        url = result.stdout.strip()
        print(f"OK: Aplicación desplegada en: {url}")
        return url
    else:
        print("WARNING: No se pudo obtener la URL automáticamente")
        print("Ejecuta manualmente: railway domain")
        return None

def test_deployment(url):
    """Prueba el deployment."""
    if not url:
        print("No hay URL para probar")
        return False
    
    print_header("PROBANDO DEPLOYMENT")
    
    print("Esperando a que la aplicación esté lista...")
    time.sleep(10)
    
    try:
        response = requests.get(f"{url}/health", timeout=30)
        if response.status_code == 200:
            print("OK: Deployment funcionando correctamente")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"ERROR: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: No se pudo probar el deployment: {e}")
        return False

def show_access_info(url):
    """Muestra información de acceso."""
    print_header("INFORMACION DE ACCESO EXTERNO")
    
    if url:
        print(f"URL Pública: {url}")
        print(f"Documentación: {url}/docs")
        print(f"Health Check: {url}/health")
        print(f"API Principal: {url}")
    else:
        print("URL no disponible. Revisa el despliegue.")
    
    print("\nPara tu compañero:")
    print("1. Comparte la URL pública contigo")
    print("2. Tu compañero puede acceder desde cualquier lugar")
    print("3. No necesita estar en la misma red")
    print("4. La URL es permanente y siempre funciona")
    
    print("\nComandos de prueba:")
    if url:
        print(f"# Probar conectividad:")
        print(f"curl {url}/health")
        print(f"# Ver documentación:")
        print(f"# Abrir en navegador: {url}/docs")
        print(f"# Ejecutar pruebas:")
        print(f"python scripts/test_remote_access.py {url}")

def main():
    """Función principal."""
    print("DEPLOYMENT RAILWAY CON DOCKER")
    print("Subsistema de Recolección - Universidad Cenfotec")
    print("="*60)
    
    # Verificar prerrequisitos
    if not check_prerequisites():
        return 1
    
    # Instalar Railway CLI
    if not install_railway_cli():
        return 1
    
    # Configurar proyecto
    if not setup_railway_project():
        return 1
    
    # Desplegar
    url = deploy_to_railway()
    if not url:
        print("ERROR: Falló el despliegue")
        return 1
    
    # Mostrar información
    show_access_info(url)
    
    # Probar deployment
    print("\n¿Deseas probar el deployment? (s/n)")
    try:
        respuesta = input().lower()
        if respuesta == 's':
            test_deployment(url)
    except:
        print("Saltando prueba automática")
    
    print(f"\n{'='*60}")
    print("DEPLOYMENT COMPLETADO EXITOSAMENTE")
    print("Tu compañero puede acceder desde cualquier lugar")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
