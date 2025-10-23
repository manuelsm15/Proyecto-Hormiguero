#!/usr/bin/env python3
"""
Script rápido para desplegar en Railway.
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Función principal."""
    print("DEPLOYMENT RAPIDO EN RAILWAY")
    print("Subsistema de Recolección - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("Pasos para desplegar en Railway:")
    print("="*60)
    
    print("\n1. INSTALAR RAILWAY CLI:")
    print("   npm install -g @railway/cli")
    
    print("\n2. LOGIN EN RAILWAY:")
    print("   railway login")
    print("   (Se abrirá una ventana del navegador)")
    
    print("\n3. CREAR PROYECTO:")
    print("   railway init")
    
    print("\n4. DESPLEGAR:")
    print("   railway up")
    
    print("\n5. OBTENER URL:")
    print("   railway domain")
    
    print("\n" + "="*60)
    print("INSTRUCCIONES MANUALES:")
    print("="*60)
    
    print("\nEjecuta estos comandos uno por uno:")
    print("\n# 1. Instalar Railway CLI")
    print("npm install -g @railway/cli")
    
    print("\n# 2. Login (se abrirá navegador)")
    print("railway login")
    
    print("\n# 3. Crear proyecto")
    print("railway init")
    
    print("\n# 4. Desplegar")
    print("railway up")
    
    print("\n# 5. Obtener URL pública")
    print("railway domain")
    
    print("\n" + "="*60)
    print("RESULTADO:")
    print("="*60)
    print("Railway te dará una URL como:")
    print("https://tu-proyecto.up.railway.app")
    print("\nComparte esta URL con tu compañero!")
    print("Ejemplo: https://recoleccion-subsistema.up.railway.app")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
