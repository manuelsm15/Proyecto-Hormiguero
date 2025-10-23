#!/usr/bin/env python3
"""
Script para subir el proyecto a GitHub usando Git.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    """Funcion principal."""
    print("SUBIR PROYECTO A GITHUB")
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
        print("3. Configurar Git:")
        print("   git config --global user.name 'Manuel'")
        print("   git config --global user.email 'manuelsm15@gmail.com'")
        print("4. Inicializar repositorio:")
        print("   git init")
        print("5. Agregar archivos:")
        print("   git add .")
        print("6. Hacer commit:")
        print("   git commit -m 'Initial commit: Subsistema de Recoleccion'")
        print("7. Conectar con GitHub:")
        print("   git remote add origin https://github.com/manuelsm15/Proyecto-Hormiguero.git")
        print("8. Subir a GitHub:")
        print("   git push -u origin main")
        print("="*60)
        return 1
    
    # Configurar Git
    print("\nCONFIGURANDO GIT:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "config", "--global", "user.name", "Manuel"], check=True, shell=True)
        subprocess.run([git_cmd, "config", "--global", "user.email", "manuelsm15@gmail.com"], check=True, shell=True)
        print("OK: Git configurado")
    except Exception as e:
        print(f"ERROR: No se pudo configurar Git: {e}")
        return 1
    
    # Inicializar repositorio
    print("\nINICIALIZANDO REPOSITORIO:")
    print("="*60)
    
    try:
        if os.path.exists(".git"):
            print("OK: Repositorio Git ya existe")
        else:
            subprocess.run([git_cmd, "init"], check=True, shell=True)
            print("OK: Repositorio Git inicializado")
    except Exception as e:
        print(f"ERROR: No se pudo inicializar repositorio: {e}")
        return 1
    
    # Agregar archivos
    print("\nAGREGANDO ARCHIVOS:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "add", "."], check=True, shell=True)
        print("OK: Archivos agregados")
    except Exception as e:
        print(f"ERROR: No se pudieron agregar archivos: {e}")
        return 1
    
    # Hacer commit
    print("\nHACIENDO COMMIT:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "commit", "-m", "Initial commit: Subsistema de Recoleccion de Alimentos"], check=True, shell=True)
        print("OK: Commit creado")
    except Exception as e:
        print(f"ERROR: No se pudo hacer commit: {e}")
        return 1
    
    # Conectar con GitHub
    print("\nCONECTANDO CON GITHUB:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "remote", "add", "origin", "https://github.com/manuelsm15/Proyecto-Hormiguero.git"], check=True, shell=True)
        print("OK: Remote origin agregado")
    except Exception as e:
        print(f"ERROR: No se pudo conectar con GitHub: {e}")
        return 1
    
    # Cambiar branch a main
    print("\nCAMBIANDO BRANCH A MAIN:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "branch", "-M", "main"], check=True, shell=True)
        print("OK: Branch cambiado a main")
    except Exception as e:
        print(f"ERROR: No se pudo cambiar branch: {e}")
        return 1
    
    # Subir a GitHub
    print("\nSUBIR A GITHUB:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "push", "-u", "origin", "main"], check=True, shell=True)
        print("OK: Proyecto subido a GitHub")
    except Exception as e:
        print(f"ERROR: No se pudo subir a GitHub: {e}")
        print("NOTA: Puede requerir autenticacion")
        return 1
    
    print("\nPROYECTO SUBIDO EXITOSAMENTE:")
    print("="*60)
    print("URL: https://github.com/manuelsm15/Proyecto-Hormiguero")
    print("Estado: Subido correctamente")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

