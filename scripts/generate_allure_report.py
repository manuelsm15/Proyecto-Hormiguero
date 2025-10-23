#!/usr/bin/env python3
"""
Script para generar el reporte de Allure.
"""

import subprocess
import sys
import os
from pathlib import Path


def main():
    """Función principal."""
    print("Generando reporte de Allure...")
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Verificar que existe el directorio de resultados
    allure_results_dir = Path("allure-results")
    if not allure_results_dir.exists():
        print("❌ No se encontró el directorio allure-results")
        print("Ejecuta primero las pruebas BDD con: python scripts/run_tests.py")
        return 1
    
    # Generar reporte
    try:
        result = subprocess.run(
            ["allure", "generate", "allure-results", "--clean", "-o", "allure-report"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("OK: Reporte de Allure generado exitosamente")
            print("Ubicacion: allure-report/index.html")
            print("\nPara abrir el reporte, ejecuta:")
            print("allure open allure-report")
        else:
            print("ERROR: Error al generar el reporte de Allure")
            print("STDERR:", result.stderr)
            return 1
            
    except FileNotFoundError:
        print("ERROR: Allure no esta instalado")
        print("Instala Allure con: pip install allure-pytest")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
