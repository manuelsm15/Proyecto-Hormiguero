#!/usr/bin/env python3
"""
Script para sincronizar con GitHub y resolver conflictos.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Funcion principal."""
    print("SINCRONIZANDO CON GITHUB")
    print("Subsistema de Recoleccion - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"Directorio: {os.getcwd()}")
    
    # Intentar encontrar Git en diferentes ubicaciones
    git_paths = [
        "git",
        r"C:\Program Files\Git\bin\git.exe",
        r"C:\Program Files (x86)\Git\bin\git.exe",
        r"C:\Users\manue\AppData\Local\Programs\Git\bin\git.exe"
    ]
    
    git_cmd = None
    for path in git_paths:
        try:
            result = subprocess.run([path, "--version"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                git_cmd = path
                print(f"OK: Git encontrado en {path}")
                break
        except:
            continue
    
    if not git_cmd:
        print("ERROR: Git no encontrado")
        print("INSTRUCCIONES MANUALES:")
        print("="*60)
        print("1. Abrir nueva terminal (PowerShell)")
        print("2. Navegar al proyecto:")
        print("   cd 'C:\\Users\\manue\\Proyecto Hormiguero'")
        print("3. Obtener cambios remotos:")
        print("   git pull origin main")
        print("4. Resolver conflictos si los hay")
        print("5. Agregar cambios:")
        print("   git add .")
        print("6. Hacer commit:")
        print("   git commit -m 'Merge remote changes'")
        print("7. Subir a GitHub:")
        print("   git push origin main")
        print("="*60)
        return 1
    
    # Obtener cambios remotos
    print("\nOBTENIENDO CAMBIOS REMOTOS:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "pull", "origin", "main"], check=True, shell=True)
        print("OK: Cambios remotos obtenidos")
    except Exception as e:
        print(f"ERROR: No se pudieron obtener cambios remotos: {e}")
        print("Intentando con --rebase...")
        try:
            subprocess.run([git_cmd, "pull", "--rebase", "origin", "main"], check=True, shell=True)
            print("OK: Cambios remotos obtenidos con rebase")
        except Exception as e2:
            print(f"ERROR: No se pudieron obtener cambios remotos: {e2}")
            return 1
    
    # Agregar cambios locales
    print("\nAGREGANDO CAMBIOS LOCALES:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "add", "."], check=True, shell=True)
        print("OK: Cambios locales agregados")
    except Exception as e:
        print(f"ERROR: No se pudieron agregar cambios locales: {e}")
        return 1
    
    # Hacer commit
    print("\nHACIENDO COMMIT:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "commit", "-m", "Fix Railway deployment: Optimize Dockerfile and configuration"], check=True, shell=True)
        print("OK: Commit creado")
    except Exception as e:
        print(f"ERROR: No se pudo hacer commit: {e}")
        return 1
    
    # Subir a GitHub
    print("\nSUBIR A GITHUB:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "push", "origin", "main"], check=True, shell=True)
        print("OK: Cambios subidos a GitHub")
    except Exception as e:
        print(f"ERROR: No se pudieron subir cambios: {e}")
        return 1
    
    print("\nSINCRONIZACION COMPLETADA:")
    print("="*60)
    print("1. Cambios remotos obtenidos")
    print("2. Cambios locales agregados")
    print("3. Commit creado")
    print("4. Cambios subidos a GitHub")
    print("="*60)
    
    print("\nPRÓXIMOS PASOS:")
    print("="*60)
    print("1. Railway detectará automáticamente los cambios")
    print("2. Se ejecutará un nuevo despliegue")
    print("3. El healthcheck debería funcionar correctamente")
    print("4. La aplicación estará disponible en la URL de Railway")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

