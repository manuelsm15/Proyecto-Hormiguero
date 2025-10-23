#!/usr/bin/env python3
"""
Script simplificado para deployment en Railway con Docker.
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Función principal."""
    print("DEPLOYMENT RAILWAY CON DOCKER")
    print("Subsistema de Recolección - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("Pasos para desplegar en Railway con Docker:")
    print("="*60)
    
    print("\n1. INSTALAR RAILWAY CLI:")
    print("   npm install -g @railway/cli")
    
    print("\n2. LOGIN EN RAILWAY:")
    print("   railway login")
    print("   (Se abrirá una ventana del navegador)")
    
    print("\n3. CREAR PROYECTO:")
    print("   railway init")
    
    print("\n4. CONFIGURAR DOCKER:")
    print("   railway variables set RAILWAY_DOCKERFILE_PATH=Dockerfile.railway")
    
    print("\n5. DESPLEGAR:")
    print("   railway up")
    
    print("\n6. OBTENER URL:")
    print("   railway domain")
    
    print("\n" + "="*60)
    print("COMANDOS COMPLETOS:")
    print("="*60)
    
    print("\n# Ejecuta estos comandos uno por uno:")
    print("\n# 1. Instalar Railway CLI")
    print("npm install -g @railway/cli")
    
    print("\n# 2. Login (se abrirá navegador)")
    print("railway login")
    
    print("\n# 3. Crear proyecto")
    print("railway init")
    
    print("\n# 4. Configurar Docker")
    print("railway variables set RAILWAY_DOCKERFILE_PATH=Dockerfile.railway")
    
    print("\n# 5. Desplegar")
    print("railway up")
    
    print("\n# 6. Obtener URL pública")
    print("railway domain")
    
    print("\n" + "="*60)
    print("RESULTADO:")
    print("="*60)
    print("Railway te dará una URL como:")
    print("https://tu-proyecto.up.railway.app")
    print("\nComparte esta URL con tu compañero!")
    print("Ejemplo: https://recoleccion-subsistema.up.railway.app")
    
    print("\n" + "="*60)
    print("VENTAJAS DE ESTE MÉTODO:")
    print("="*60)
    print("OK: Usa Docker para consistencia")
    print("OK: URL permanente y estable")
    print("OK: Acceso desde cualquier lugar")
    print("OK: HTTPS automático")
    print("OK: Monitoreo incluido")
    print("OK: Escalabilidad automática")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
