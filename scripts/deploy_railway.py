#!/usr/bin/env python3
"""
Script para deployment en Railway.
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Función principal para deployment."""
    print("🚀 Iniciando deployment en Railway...")
    
    # Verificar que estamos en el directorio correcto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Verificar que Railway CLI está instalado
    try:
        result = subprocess.run(["railway", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Railway CLI encontrado: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Railway CLI no encontrado. Instalando...")
        print("Por favor instala Railway CLI desde: https://railway.app/cli")
        return 1
    
    # Ejecutar pruebas antes del deployment
    print("🧪 Ejecutando pruebas antes del deployment...")
    try:
        result = subprocess.run([
            "python", "-m", "pytest", "tests/", "--tb=short", "-q"
        ], check=True)
        print("✅ Todas las pruebas pasaron")
    except subprocess.CalledProcessError:
        print("❌ Algunas pruebas fallaron. Deployment cancelado.")
        return 1
    
    # Login a Railway (si es necesario)
    print("🔐 Verificando autenticación con Railway...")
    try:
        subprocess.run(["railway", "whoami"], check=True, capture_output=True)
        print("✅ Autenticado en Railway")
    except subprocess.CalledProcessError:
        print("❌ No autenticado. Ejecuta: railway login")
        return 1
    
    # Deploy
    print("🚀 Iniciando deployment...")
    try:
        subprocess.run(["railway", "deploy"], check=True)
        print("✅ Deployment exitoso!")
        print("🌐 Tu aplicación está disponible en Railway")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en deployment: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
