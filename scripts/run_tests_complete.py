"""
Script maestro para ejecutar todas las pruebas (TDD y BDD) con Allure.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# Cambiar al directorio raíz del proyecto
project_root = Path(__file__).parent.parent
os.chdir(project_root)


def print_section(title):
    """Imprime una sección con formato."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def run_command(command, description, capture_output=True):
    """Ejecuta un comando y reporta el resultado."""
    print(f"Ejecutando: {description}")
    print(f"Comando: {' '.join(command) if isinstance(command, list) else command}\n")
    
    try:
        if isinstance(command, str):
            result = subprocess.run(
                command,
                shell=True,
                capture_output=capture_output,
                text=True
            )
        else:
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=600
            )
        
        if capture_output:
            if result.stdout:
                print(result.stdout)
            if result.stderr and result.returncode != 0:
                print("STDERR:", result.stderr, file=sys.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"ERROR: Timeout ejecutando comando")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def main():
    """Función principal."""
    print_section("SUITE COMPLETA DE PRUEBAS - TDD y BDD con Allure")
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Crear directorios necesarios
    Path("allure-results").mkdir(exist_ok=True)
    Path("htmlcov").mkdir(exist_ok=True)
    
    results = {}
    
    # 1. PRUEBAS TDD CON PYTEST + ALLURE
    print_section("1. PRUEBAS TDD (pytest)")
    
    pytest_cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=src",
        "--cov-report=html:htmlcov",
        "--cov-report=term-missing",
        "--allure-results-dir=allure-results"
    ]
    
    pytest_success = run_command(pytest_cmd, "Pruebas unitarias con pytest + Allure")
    results["TDD (pytest)"] = pytest_success
    
    # 2. PRUEBAS BDD CON BEHAVE + ALLURE
    print_section("2. PRUEBAS BDD (behave)")
    
    # Verificar si existe behave
    try:
        subprocess.run([sys.executable, "-m", "behave", "--version"], 
                     capture_output=True, check=True)
        
        behave_cmd = [
            sys.executable, "-m", "behave",
            "features/",
            "-f", "allure_behave.formatter:AllureFormatter",
            "-o", "allure-results",
            "--no-capture",
            "--no-capture-stderr"
        ]
        
        behave_success = run_command(behave_cmd, "Pruebas BDD con behave + Allure")
        results["BDD (behave)"] = behave_success
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ADVERTENCIA: behave no está disponible, saltando pruebas BDD")
        results["BDD (behave)"] = None
    
    # 3. GENERAR REPORTE DE ALLURE
    print_section("3. GENERAR REPORTE DE ALLURE")
    
    try:
        # Verificar si Allure CLI está disponible
        subprocess.run(["allure", "--version"], 
                     capture_output=True, check=True)
        
        allure_generate_cmd = [
            "allure", "generate",
            "allure-results",
            "--clean",
            "-o", "allure-report"
        ]
        
        allure_success = run_command(
            allure_generate_cmd, 
            "Generar reporte HTML de Allure",
            capture_output=False
        )
        results["Allure Report"] = allure_success
        
        if allure_success:
            print("\n" + "=" * 70)
            print("  REPORTE DE ALLURE GENERADO EXITOSAMENTE")
            print("=" * 70)
            print("\nPara ver el reporte:")
            print("  1. Abrir: allure-report/index.html")
            print("  2. O ejecutar: allure open allure-report")
            print("=" * 70 + "\n")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ADVERTENCIA: Allure CLI no está disponible")
        print("Los resultados están en: allure-results/")
        print("Para generar el reporte, instala Allure CLI o usa:")
        print("  python scripts/generate_allure_report.py")
        results["Allure Report"] = None
    
    # RESUMEN FINAL
    print_section("RESUMEN FINAL")
    
    total = len([v for v in results.values() if v is not None])
    passed = sum(1 for v in results.values() if v is True)
    
    print("Resultados por suite de pruebas:")
    for suite, success in results.items():
        if success is None:
            status = "SKIP"
        elif success:
            status = "✓ OK"
        else:
            status = "✗ FALLO"
        print(f"  {status:10} - {suite}")
    
    print(f"\nTotal: {total} suites")
    print(f"Exitosas: {passed}")
    print(f"Fallidas: {total - passed}")
    
    if passed == total and total > 0:
        print("\n" + "=" * 70)
        print("  ✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 70)
        return 0
    elif total == 0:
        print("\n" + "=" * 70)
        print("  ⚠ ADVERTENCIA: No se pudieron ejecutar las pruebas")
        print("=" * 70)
        return 1
    else:
        print("\n" + "=" * 70)
        print("  ✗ ALGUNAS PRUEBAS FALLARON")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())



