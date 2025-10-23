#!/usr/bin/env python3
"""
Script para desplegar el proyecto en Railway.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    """Funcion principal."""
    print("DESPLEGANDO EN RAILWAY")
    print("Subsistema de Recoleccion - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"Directorio: {os.getcwd()}")
    
    # Verificar que Railway CLI este instalado
    try:
        result = subprocess.run(["railway", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"OK: Railway CLI instalado - {result.stdout.strip()}")
        else:
            print("ERROR: Railway CLI no esta instalado")
            return 1
    except Exception as e:
        print(f"ERROR: Railway CLI no disponible: {e}")
        return 1
    
    print("\nINSTRUCCIONES PARA DESPLEGAR:")
    print("="*60)
    print("1. Abrir navegador: https://railway.app")
    print("2. Hacer login con GitHub")
    print("3. Crear nuevo proyecto")
    print("4. Conectar repositorio GitHub")
    print("5. Configurar variables de entorno")
    print("="*60)
    
    print("\nCOMANDOS ALTERNATIVOS:")
    print("="*60)
    print("1. railway login")
    print("2. railway init")
    print("3. railway up")
    print("="*60)
    
    print("\nARCHIVOS CREADOS:")
    print("="*60)
    print("✅ railway.json - Configuracion de Railway")
    print("✅ Dockerfile.railway - Docker para Railway")
    print("✅ requirements.txt - Dependencias Python")
    print("="*60)
    
    print("\nURL FINAL SERA:")
    print("="*60)
    print("https://TU_PROYECTO-production.up.railway.app")
    print("https://TU_PROYECTO-production.up.railway.app/docs")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
