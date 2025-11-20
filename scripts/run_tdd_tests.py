"""
Script para ejecutar solo las pruebas TDD (pytest) con Allure.
"""

import subprocess
import sys
import os
from pathlib import Path

# Cambiar al directorio raíz del proyecto
project_root = Path(__file__).parent.parent
os.chdir(project_root)

# Crear directorios necesarios
Path("allure-results").mkdir(exist_ok=True)
Path("htmlcov").mkdir(exist_ok=True)

# Ejecutar pytest con Allure
cmd = [
    sys.executable, "-m", "pytest",
    "tests/",
    "-v",
    "--tb=short",
    "--cov=src",
    "--cov-report=html:htmlcov",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
    "--allure-results-dir=allure-results"
]

print("Ejecutando pruebas TDD (pytest) con Allure...")
result = subprocess.run(cmd)

sys.exit(result.returncode)



