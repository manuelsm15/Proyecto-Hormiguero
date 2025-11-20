# -*- coding: utf-8 -*-
"""
Ejecuta únicamente las pruebas de integración contra servicios reales.
Se salta automáticamente si no están configuradas BASE_API_URL/ENTORNO_API_URL/COMUNICACION_API_URL.
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("\n=== Pruebas de Integración (Servicios Reales) ===\n")

    entorno = os.getenv("ENTORNO_API_URL", "")
    comm = os.getenv("COMUNICACION_API_URL", "")
    base = os.getenv("BASE_API_URL", "")

    print(f"BASE_API_URL           : {base or '-'}")
    print(f"ENTORNO_API_URL        : {entorno or '-'}")
    print(f"COMUNICACION_API_URL   : {comm or '-'}\n")

    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_integration_real_services.py",
        "-v",
        "-m", "integration",
        "--tb=short",
        "--allure-results-dir=allure-results"
    ]

    print("Ejecutando:", " ".join(cmd))
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()


