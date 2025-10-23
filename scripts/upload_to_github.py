#!/usr/bin/env python3
"""
Script para subir el proyecto a GitHub.
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
    
    # Crear README.md
    print("\nCREANDO README.md:")
    print("="*60)
    
    readme_content = """# Subsistema de Recolección de Alimentos

## 🐜 Simulación de Colonia de Hormigas - Universidad Cenfotec

### 📋 Descripción
Subsistema de recolección de alimentos para la simulación de una colonia de hormigas, desarrollado siguiendo metodologías TDD y BDD.

### 🚀 Características
- **TDD (Test-Driven Development)**: Desarrollo guiado por pruebas
- **BDD (Behavior-Driven Development)**: Desarrollo guiado por comportamiento
- **Cobertura de código**: ≥80% con reportes Allure
- **APIs REST**: FastAPI con documentación automática
- **Timer en tiempo real**: Gestión de tareas con tiempo real
- **Docker**: Containerización para despliegue

### 🛠️ Tecnologías
- **Python 3.12**
- **FastAPI** - Framework web
- **Pytest** - Testing
- **Behave** - BDD
- **Allure** - Reportes
- **Docker** - Containerización
- **Railway** - Despliegue

### 📁 Estructura del Proyecto
```
src/
├── recoleccion/
│   ├── api/           # Controladores REST
│   ├── models/        # Modelos de datos
│   └── services/       # Lógica de negocio
tests/                  # Pruebas unitarias
features/               # Pruebas BDD
scripts/                # Scripts de automatización
```

### 🚀 Instalación y Uso

#### Requisitos
- Python 3.12+
- pip

#### Instalación
```bash
# Clonar repositorio
git clone https://github.com/manuelsm15/Proyecto-Hormiguero.git
cd Proyecto-Hormiguero

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar pruebas
python scripts/run_tests.py

# Iniciar servidor
python main.py
```

#### URLs Disponibles
- **API Principal**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 🧪 Testing

#### Pruebas Unitarias
```bash
python -m pytest tests/ -v --cov=src --cov-report=html
```

#### Pruebas BDD
```bash
behave features/ -o allure-results
```

#### Reportes Allure
```bash
python scripts/generate_allure_report.py
```

### 🐳 Docker

#### Construir imagen
```bash
docker build -f Dockerfile.railway -t subsistema-recoleccion .
```

#### Ejecutar contenedor
```bash
docker run -p 8000:8000 subsistema-recoleccion
```

### 🚀 Despliegue en Railway

#### Configuración automática
```bash
# Login en Railway
railway login

# Inicializar proyecto
railway init

# Desplegar
railway up

# Obtener URL
railway domain
```

### 📊 APIs Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información del subsistema |
| `/health` | GET | Health check |
| `/alimentos` | GET | Alimentos disponibles |
| `/tareas` | POST | Crear tareas |
| `/tareas` | GET | Listar tareas |
| `/tareas/en-proceso` | GET | Tareas con timer |
| `/procesar` | POST | Procesamiento automático |
| `/estadisticas` | GET | Estadísticas |

### 🎯 Alimentos Disponibles
- **A1**: Fruta (3 hormigas, 10 puntos, 300s)
- **A2**: Semilla (2 hormigas, 5 puntos, 180s)
- **A3**: Hoja (1 hormiga, 3 puntos, 120s)

### 📈 Cobertura de Código
- **Total**: 88%
- **Servicios**: 86%
- **Modelos**: 76-100%
- **APIs**: 100%

### 👥 Autores
- **Manuel** - Universidad Cenfotec
- **Email**: manuelsm15@gmail.com

### 📄 Licencia
Este proyecto es parte del curso de Universidad Cenfotec.

### 🔗 Enlaces
- **GitHub**: https://github.com/manuelsm15/Proyecto-Hormiguero
- **Railway**: https://TU_PROYECTO-production.up.railway.app
- **Documentación**: https://TU_PROYECTO-production.up.railway.app/docs
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("OK: README.md creado")
    
    # Mostrar instrucciones para Git
    print("\nINSTRUCCIONES PARA GIT:")
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
    
    print("\nARCHIVOS LISTOS:")
    print("="*60)
    print("OK: main.py - Aplicacion principal")
    print("OK: requirements.txt - Dependencias")
    print("OK: Dockerfile.railway - Docker para Railway")
    print("OK: railway.json - Configuracion de Railway")
    print("OK: .gitignore - Archivos a ignorar")
    print("OK: README.md - Documentacion del proyecto")
    print("="*60)
    
    print("\nREPOSITORIO GITHUB:")
    print("="*60)
    print("URL: https://github.com/manuelsm15/Proyecto-Hormiguero")
    print("Estado: Listo para subir")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

