#!/usr/bin/env python3
"""
Script para configurar Git y subir proyecto a GitHub.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    """Funcion principal."""
    print("CONFIGURANDO GIT Y SUBIENDO A GITHUB")
    print("Subsistema de Recoleccion - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"Directorio: {os.getcwd()}")
    
    # Verificar si Git esta instalado
    print("\nVERIFICANDO GIT:")
    print("="*60)
    
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"OK: Git instalado - {result.stdout.strip()}")
        else:
            print("ERROR: Git no esta instalado")
            print("Instalando Git...")
            subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"], check=True)
            print("OK: Git instalado")
            print("NOTA: Reinicia la terminal para que Git este disponible")
            return 1
    except Exception as e:
        print(f"ERROR: Git no disponible: {e}")
        return 1
    
    # Configurar Git
    print("\nCONFIGURANDO GIT:")
    print("="*60)
    
    try:
        subprocess.run(["git", "config", "--global", "user.name", "Manuel"], check=True, shell=True)
        subprocess.run(["git", "config", "--global", "user.email", "manuelsm15@gmail.com"], check=True, shell=True)
        print("OK: Git configurado")
    except Exception as e:
        print(f"ERROR: No se pudo configurar Git: {e}")
        return 1
    
    # Inicializar repositorio Git
    print("\nINICIALIZANDO REPOSITORIO GIT:")
    print("="*60)
    
    try:
        # Verificar si ya es un repositorio Git
        if os.path.exists(".git"):
            print("OK: Repositorio Git ya existe")
        else:
            subprocess.run(["git", "init"], check=True, shell=True)
            print("OK: Repositorio Git inicializado")
    except Exception as e:
        print(f"ERROR: No se pudo inicializar repositorio: {e}")
        return 1
    
    # Crear .gitignore
    print("\nCREANDO .gitignore:")
    print("="*60)
    
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Allure
allure-results/
allure-report/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    print("OK: .gitignore creado")
    
    # Agregar archivos al repositorio
    print("\nAGREGANDO ARCHIVOS AL REPOSITORIO:")
    print("="*60)
    
    try:
        subprocess.run(["git", "add", "."], check=True, shell=True)
        print("OK: Archivos agregados")
    except Exception as e:
        print(f"ERROR: No se pudieron agregar archivos: {e}")
        return 1
    
    # Hacer commit inicial
    print("\nHACIENDO COMMIT INICIAL:")
    print("="*60)
    
    try:
        subprocess.run(["git", "commit", "-m", "Initial commit: Subsistema de Recoleccion de Alimentos"], check=True, shell=True)
        print("OK: Commit inicial creado")
    except Exception as e:
        print(f"ERROR: No se pudo hacer commit: {e}")
        return 1
    
    # Mostrar instrucciones para GitHub
    print("\nINSTRUCCIONES PARA GITHUB:")
    print("="*60)
    print("1. Ir a: https://github.com")
    print("2. Hacer login con tu cuenta: manuelsm15@gmail.com")
    print("3. Crear nuevo repositorio:")
    print("   - Nombre: subsistema-recoleccion-hormigas")
    print("   - Descripcion: Subsistema de Recoleccion de Alimentos - Universidad Cenfotec")
    print("   - Publico")
    print("   - NO inicializar con README")
    print("4. Copiar la URL del repositorio")
    print("5. Ejecutar los comandos que se muestran a continuacion")
    print("="*60)
    
    print("\nCOMANDOS PARA EJECUTAR:")
    print("="*60)
    print("git remote add origin https://github.com/TU_USUARIO/subsistema-recoleccion-hormigas.git")
    print("git branch -M main")
    print("git push -u origin main")
    print("="*60)
    
    print("\nARCHIVOS LISTOS PARA GITHUB:")
    print("="*60)
    print("OK: main.py - Aplicacion principal")
    print("OK: requirements.txt - Dependencias")
    print("OK: Dockerfile.railway - Docker para Railway")
    print("OK: railway.json - Configuracion de Railway")
    print("OK: .gitignore - Archivos a ignorar")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

