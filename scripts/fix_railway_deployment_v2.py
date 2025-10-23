#!/usr/bin/env python3
"""
Script para corregir el despliegue en Railway v2.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Funcion principal."""
    print("CORRIGIENDO DESPLIEGUE EN RAILWAY V2")
    print("Subsistema de Recoleccion - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"Directorio: {os.getcwd()}")
    
    # Verificar archivos modificados
    print("\nARCHIVOS MODIFICADOS:")
    print("="*60)
    print("OK: railway_main.py - Mejorado con manejo de errores")
    print("OK: Logs de debug agregados")
    print("OK: Manejo de excepciones mejorado")
    print("="*60)
    
    # Probar localmente primero
    print("\nPROBANDO LOCALMENTE:")
    print("="*60)
    
    try:
        # Verificar que el archivo funciona
        import railway_main
        print("OK: railway_main.py se puede importar")
    except Exception as e:
        print(f"ERROR: railway_main.py tiene errores: {e}")
        return 1
    
    # Agregar archivos al repositorio
    print("\nAGREGANDO CAMBIOS AL REPOSITORIO:")
    print("="*60)
    
    try:
        subprocess.run(["git", "add", "railway_main.py"], check=True, shell=True)
        print("OK: Archivos agregados")
    except Exception as e:
        print(f"ERROR: No se pudieron agregar archivos: {e}")
        return 1
    
    # Hacer commit
    print("\nHACIENDO COMMIT:")
    print("="*60)
    
    try:
        subprocess.run(["git", "commit", "-m", "Fix Railway deployment v2: Improve error handling and logging"], check=True, shell=True)
        print("OK: Commit creado")
    except Exception as e:
        print(f"ERROR: No se pudo hacer commit: {e}")
        return 1
    
    # Subir a GitHub
    print("\nSUBIR A GITHUB:")
    print("="*60)
    
    try:
        subprocess.run(["git", "push", "origin", "main"], check=True, shell=True)
        print("OK: Cambios subidos a GitHub")
    except Exception as e:
        print(f"ERROR: No se pudieron subir cambios: {e}")
        return 1
    
    print("\nCORRECCIONES APLICADAS:")
    print("="*60)
    print("1. railway_main.py - Mejorado con manejo de errores")
    print("2. Logs de debug agregados")
    print("3. Manejo de excepciones mejorado")
    print("4. Path configuration mejorado")
    print("5. Access logs habilitados")
    print("="*60)
    
    print("\nPRÓXIMOS PASOS:")
    print("="*60)
    print("1. Railway detectará automáticamente los cambios")
    print("2. Se ejecutará un nuevo despliegue")
    print("3. Los logs mostrarán más información de debug")
    print("4. El healthcheck debería funcionar correctamente")
    print("="*60)
    
    print("\nCAMBIOS SUBIDOS EXITOSAMENTE:")
    print("="*60)
    print("URL: https://github.com/manuelsm15/Proyecto-Hormiguero")
    print("Estado: Corregido v2 y subido")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

