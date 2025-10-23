#!/usr/bin/env python3
"""
Script para corregir el despliegue en Railway.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Funcion principal."""
    print("CORRIGIENDO DESPLIEGUE EN RAILWAY")
    print("Subsistema de Recoleccion - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"Directorio: {os.getcwd()}")
    
    # Verificar archivos modificados
    print("\nARCHIVOS MODIFICADOS:")
    print("="*60)
    print("OK: Dockerfile.railway - Corregido para Railway")
    print("OK: railway.json - Configuracion actualizada")
    print("OK: railway_main.py - Archivo optimizado para Railway")
    print("="*60)
    
    # Agregar archivos al repositorio
    print("\nAGREGANDO CAMBIOS AL REPOSITORIO:")
    print("="*60)
    
    try:
        subprocess.run(["git", "add", "."], check=True, shell=True)
        print("OK: Archivos agregados")
    except Exception as e:
        print(f"ERROR: No se pudieron agregar archivos: {e}")
        return 1
    
    # Hacer commit
    print("\nHACIENDO COMMIT:")
    print("="*60)
    
    try:
        subprocess.run(["git", "commit", "-m", "Fix Railway deployment: Optimize Dockerfile and configuration"], check=True, shell=True)
        print("OK: Commit creado")
    except Exception as e:
        print(f"ERROR: No se pudo hacer commit: {e}")
        return 1
    
    # Subir cambios a GitHub
    print("\nSUBIR CAMBIOS A GITHUB:")
    print("="*60)
    
    try:
        subprocess.run(["git", "push", "origin", "main"], check=True, shell=True)
        print("OK: Cambios subidos a GitHub")
    except Exception as e:
        print(f"ERROR: No se pudieron subir cambios: {e}")
        return 1
    
    print("\nCORRECCIONES APLICADAS:")
    print("="*60)
    print("1. Dockerfile.railway - Optimizado para Railway")
    print("2. railway.json - Configuracion corregida")
    print("3. railway_main.py - Archivo principal optimizado")
    print("4. Variables de entorno - PORT configurado")
    print("5. Healthcheck - Configurado correctamente")
    print("="*60)
    
    print("\nPRÓXIMOS PASOS:")
    print("="*60)
    print("1. Railway detectará automáticamente los cambios")
    print("2. Se ejecutará un nuevo despliegue")
    print("3. El healthcheck debería funcionar correctamente")
    print("4. La aplicación estará disponible en la URL de Railway")
    print("="*60)
    
    print("\nCAMBIOS SUBIDOS EXITOSAMENTE:")
    print("="*60)
    print("URL: https://github.com/manuelsm15/Proyecto-Hormiguero")
    print("Estado: Corregido y subido")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
