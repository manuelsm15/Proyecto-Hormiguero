#!/usr/bin/env python3
"""
Script para desplegar el Subsistema de Recolección en Railway para acceso externo.
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

def check_railway_cli():
    """Verifica que Railway CLI esté instalado."""
    print_header("VERIFICANDO RAILWAY CLI")
    
    if not run_command("railway --version", "Verificar Railway CLI"):
        print("Instalando Railway CLI...")
        if not run_command("npm install -g @railway/cli", "Instalar Railway CLI"):
            print("ERROR: No se pudo instalar Railway CLI")
            print("Instala Node.js primero: https://nodejs.org/")
            return False
    
    print("OK: Railway CLI está instalado")
    return True

def setup_railway_project():
    """Configura el proyecto en Railway."""
    print_header("CONFIGURANDO PROYECTO EN RAILWAY")
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"Directorio: {os.getcwd()}")
    
    # Verificar archivos necesarios
    required_files = ["requirements.txt", "main.py", "railway.toml"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"ERROR: Archivo {file} no encontrado")
            return False
    
    print("OK: Archivos de configuración encontrados")
    return True

def deploy_to_railway():
    """Despliega el proyecto a Railway."""
    print_header("DESPLEGANDO A RAILWAY")
    
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
    
    # Desplegar
    print("Desplegando aplicación...")
    if not run_command("railway up", "Desplegar a Railway"):
        print("ERROR: Falló el despliegue")
        return False
    
    # Obtener URL
    print("Obteniendo URL del proyecto...")
    result = subprocess.run("railway domain", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        url = result.stdout.strip()
        print(f"OK: Aplicación desplegada en: {url}")
        return url
    else:
        print("WARNING: No se pudo obtener la URL")
        return None

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
    
    print("\nComandos de prueba:")
    if url:
        print(f"# Probar conectividad:")
        print(f"curl {url}/health")
        print(f"# Ver documentación:")
        print(f"# Abrir en navegador: {url}/docs")

def test_deployment(url):
    """Prueba el deployment."""
    if not url:
        print("No hay URL para probar")
        return False
    
    print_header("PROBANDO DEPLOYMENT")
    
    import requests
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

def main():
    """Función principal."""
    print("DEPLOYMENT EXTERNO - RAILWAY")
    print("Subsistema de Recolección - Universidad Cenfotec")
    print("="*60)
    
    # Verificar Railway CLI
    if not check_railway_cli():
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
    respuesta = input().lower()
    if respuesta == 's':
        test_deployment(url)
    
    print(f"\n{'='*60}")
    print("DEPLOYMENT EXTERNO COMPLETADO")
    print("Tu compañero puede acceder desde cualquier lugar")
    print(f"{'='*60}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
