"""
Script para ejecutar solo las pruebas BDD (behave) con Allure.
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

# Ejecutar behave con Allure
cmd = [
    sys.executable, "-m", "behave",
    "features/",
    "-f", "allure_behave.formatter:AllureFormatter",
    "-o", "allure-results",
    "--no-capture",
    "--no-capture-stderr"
]

print("Ejecutando pruebas BDD (behave) con Allure...")
result = subprocess.run(cmd)

sys.exit(result.returncode)



