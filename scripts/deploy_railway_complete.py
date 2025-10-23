#!/usr/bin/env python3
"""
Script completo para desplegar en Railway desde cero.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def main():
    """Funcion principal."""
    print("DESPLEGANDO EN RAILWAY DESDE CERO")
    print("Subsistema de Recoleccion - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"Directorio: {os.getcwd()}")
    
    # Verificar archivos necesarios
    print("\nVERIFICANDO ARCHIVOS NECESARIOS:")
    print("="*60)
    
    required_files = [
        "main.py",
        "requirements.txt", 
        "Dockerfile.railway",
        "railway.json"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"OK: {file}")
        else:
            print(f"ERROR: {file} no encontrado")
            return 1
    
    # Verificar que el servidor local funcione
    print("\nVERIFICANDO SERVIDOR LOCAL:")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("OK: Servidor local funcionando")
            print(f"Respuesta: {response.json()}")
        else:
            print("ERROR: Servidor local no responde correctamente")
            return 1
    except Exception as e:
        print(f"ERROR: Servidor local no esta funcionando: {e}")
        print("Iniciando servidor...")
        
        # Iniciar servidor en background
        subprocess.Popen([
            "python", "main.py"
        ], cwd=project_root)
        
        print("Esperando que el servidor inicie...")
        time.sleep(5)
        
        # Verificar nuevamente
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("OK: Servidor local funcionando")
            else:
                print("ERROR: Servidor local no responde")
                return 1
        except Exception as e:
            print(f"ERROR: Servidor local no funciona: {e}")
            return 1
    
    # Verificar Railway CLI
    print("\nVERIFICANDO RAILWAY CLI:")
    print("="*60)
    
    try:
        result = subprocess.run(["railway", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"OK: Railway CLI instalado - {result.stdout.strip()}")
        else:
            print("ERROR: Railway CLI no esta instalado")
            print("Instalando Railway CLI...")
            subprocess.run(["npm", "install", "-g", "@railway/cli"], check=True)
            print("OK: Railway CLI instalado")
    except Exception as e:
        print(f"ERROR: Railway CLI no disponible: {e}")
        return 1
    
    # Mostrar instrucciones de despliegue
    print("\nINSTRUCCIONES PARA DESPLEGAR:")
    print("="*60)
    print("1. Ejecutar: railway login")
    print("2. Ejecutar: railway init")
    print("3. Ejecutar: railway up")
    print("4. Ejecutar: railway domain")
    print("="*60)
    
    print("\nARCHIVOS LISTOS:")
    print("="*60)
    print("OK: main.py - Aplicacion principal")
    print("OK: requirements.txt - Dependencias")
    print("OK: Dockerfile.railway - Docker para Railway")
    print("OK: railway.json - Configuracion de Railway")
    print("="*60)
    
    print("\nURL FINAL SERA:")
    print("="*60)
    print("https://TU_PROYECTO-production.up.railway.app")
    print("https://TU_PROYECTO-production.up.railway.app/docs")
    print("https://TU_PROYECTO-production.up.railway.app/health")
    print("="*60)
    
    print("\nCOMANDOS PARA EJECUTAR:")
    print("="*60)
    print("railway login")
    print("railway init")
    print("railway up")
    print("railway domain")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
