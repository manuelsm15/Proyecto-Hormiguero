#!/usr/bin/env python3
"""
Script para resolver conflictos de merge automáticamente.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Funcion principal."""
    print("RESOLVIENDO CONFLICTOS DE MERGE")
    print("Subsistema de Recoleccion - Universidad Cenfotec")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"Directorio: {os.getcwd()}")
    
    # Intentar encontrar Git
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
        return 1
    
    # Verificar estado
    print("\nVERIFICANDO ESTADO:")
    print("="*60)
    
    try:
        result = subprocess.run([git_cmd, "status"], capture_output=True, text=True, shell=True)
        print("Estado del repositorio:")
        print(result.stdout)
    except Exception as e:
        print(f"ERROR: No se pudo verificar estado: {e}")
        return 1
    
    # Resolver conflictos en Dockerfile.railway
    print("\nRESOLVIENDO CONFLICTOS EN Dockerfile.railway:")
    print("="*60)
    
    dockerfile_content = """# Usa una imagen base de Python ligera
FROM python:3.12-slim-buster

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    gcc \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p allure-results allure-report htmlcov

# Expone el puerto en el que la aplicación se ejecutará
EXPOSE 8000

# Comando para iniciar la aplicación usando el archivo optimizado para Railway
CMD ["python", "railway_main.py"]
"""
    
    with open("Dockerfile.railway", "w", encoding="utf-8") as f:
        f.write(dockerfile_content)
    
    print("OK: Dockerfile.railway resuelto")
    
    # Resolver conflictos en railway.json
    print("\nRESOLVIENDO CONFLICTOS EN railway.json:")
    print("="*60)
    
    railway_json_content = """{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.railway"
  },
  "deploy": {
    "startCommand": "python railway_main.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
"""
    
    with open("railway.json", "w", encoding="utf-8") as f:
        f.write(railway_json_content)
    
    print("OK: railway.json resuelto")
    
    # Agregar archivos resueltos
    print("\nAGREGANDO ARCHIVOS RESUELTOS:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "add", "Dockerfile.railway", "railway.json"], check=True, shell=True)
        print("OK: Archivos resueltos agregados")
    except Exception as e:
        print(f"ERROR: No se pudieron agregar archivos: {e}")
        return 1
    
    # Hacer commit de resolución
    print("\nHACIENDO COMMIT DE RESOLUCION:")
    print("="*60)
    
    try:
        subprocess.run([git_cmd, "commit", "-m", "Resolve merge conflicts: Fix Railway deployment configuration"], check=True, shell=True)
        print("OK: Commit de resolución creado")
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
    
    print("\nCONFLICTOS RESUELTOS EXITOSAMENTE:")
    print("="*60)
    print("1. Dockerfile.railway - Conflictos resueltos")
    print("2. railway.json - Conflictos resueltos")
    print("3. Commit de resolución creado")
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
