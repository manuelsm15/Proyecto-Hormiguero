#!/usr/bin/env python3
"""
Guia paso a paso para desplegar en Railway usando CLI.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Funcion principal."""
    print("GUIA PARA DESPLEGAR EN RAILWAY")
    print("Subsistema de Recoleccion - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"Directorio: {os.getcwd()}")
    
    print("\nPASO 1: LOGIN EN RAILWAY")
    print("="*60)
    print("Ejecutar: railway login")
    print("Se abrira el navegador para autenticarse")
    print("="*60)
    
    print("\nPASO 2: INICIALIZAR PROYECTO")
    print("="*60)
    print("Ejecutar: railway init")
    print("Esto creara un archivo railway.toml")
    print("="*60)
    
    print("\nPASO 3: CONFIGURAR DOCKERFILE")
    print("="*60)
    print("Railway usara: Dockerfile.railway")
    print("Puerto: 8000")
    print("Comando: uvicorn main:app --host 0.0.0.0 --port 8000")
    print("="*60)
    
    print("\nPASO 4: DESPLEGAR")
    print("="*60)
    print("Ejecutar: railway up")
    print("Esto construira y desplegara la aplicacion")
    print("="*60)
    
    print("\nPASO 5: OBTENER URL")
    print("="*60)
    print("Ejecutar: railway domain")
    print("O ver en el dashboard de Railway")
    print("="*60)
    
    print("\nARCHIVOS NECESARIOS:")
    print("="*60)
    print("✅ railway.json - Configuracion")
    print("✅ Dockerfile.railway - Docker")
    print("✅ requirements.txt - Dependencias")
    print("✅ main.py - Aplicacion principal")
    print("="*60)
    
    print("\nURL FINAL SERA:")
    print("="*60)
    print("https://TU_PROYECTO-production.up.railway.app")
    print("https://TU_PROYECTO-production.up.railway.app/docs")
    print("https://TU_PROYECTO-production.up.railway.app/health")
    print("="*60)
    
    print("\nCOMANDOS COMPLETOS:")
    print("="*60)
    print("railway login")
    print("railway init")
    print("railway up")
    print("railway domain")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

