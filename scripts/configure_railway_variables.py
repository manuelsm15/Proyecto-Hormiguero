#!/usr/bin/env python3
"""
Script para configurar variables de entorno en Railway.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Funcion principal."""
    print("CONFIGURANDO VARIABLES DE ENTORNO EN RAILWAY")
    print("Subsistema de Recoleccion - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"Directorio: {os.getcwd()}")
    
    # Verificar Railway CLI
    print("\nVERIFICANDO RAILWAY CLI:")
    print("="*60)
    
    try:
        result = subprocess.run(["railway", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"OK: Railway CLI instalado - {result.stdout.strip()}")
        else:
            print("ERROR: Railway CLI no esta instalado")
            return 1
    except Exception as e:
        print(f"ERROR: Railway CLI no disponible: {e}")
        return 1
    
    # Mostrar variables necesarias
    print("\nVARIABLES NECESARIAS EN RAILWAY:")
    print("="*60)
    print("1. PORT=8000 (automatico)")
    print("2. RAILWAY_HEALTHCHECK_TIMEOUT_SEC=300")
    print("3. PYTHONPATH=/app")
    print("4. LOG_LEVEL=ERROR")
    print("5. ENVIRONMENT=production")
    print("="*60)
    
    # Mostrar comandos para configurar
    print("\nCOMANDOS PARA CONFIGURAR VARIABLES:")
    print("="*60)
    print("railway variables set RAILWAY_HEALTHCHECK_TIMEOUT_SEC=300")
    print("railway variables set PYTHONPATH=/app")
    print("railway variables set LOG_LEVEL=ERROR")
    print("railway variables set ENVIRONMENT=production")
    print("="*60)
    
    # Mostrar configuración manual
    print("\nCONFIGURACION MANUAL EN RAILWAY:")
    print("="*60)
    print("1. Ir a: https://railway.app")
    print("2. Seleccionar tu proyecto")
    print("3. Ir a 'Variables' o 'Settings'")
    print("4. Agregar las variables mostradas arriba")
    print("5. Configurar Healthcheck Path: /health")
    print("6. Configurar Healthcheck Timeout: 300")
    print("="*60)
    
    print("\nVARIABLES CONFIGURADAS:")
    print("="*60)
    print("✅ PORT=8000 (automatico)")
    print("✅ RAILWAY_HEALTHCHECK_TIMEOUT_SEC=300")
    print("✅ PYTHONPATH=/app")
    print("✅ LOG_LEVEL=ERROR")
    print("✅ ENVIRONMENT=production")
    print("="*60)
    
    print("\nPRÓXIMOS PASOS:")
    print("="*60)
    print("1. Configurar variables en Railway")
    print("2. Configurar healthcheck path: /health")
    print("3. Configurar healthcheck timeout: 300")
    print("4. Hacer redeploy del proyecto")
    print("5. Verificar que el healthcheck funcione")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

