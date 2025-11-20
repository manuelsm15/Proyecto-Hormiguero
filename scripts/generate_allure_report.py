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
        print("ADVERTENCIA: Allure CLI no está instalado")
        print("")
        print("Generando reporte HTML alternativo...")
        print("")
        
        # Intentar usar el generador HTML alternativo
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, str(Path(__file__).parent / "generate_html_report.py")],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=project_root
            )
            
            if result.returncode == 0:
                print("[OK] Reporte HTML generado exitosamente")
                print("Ubicacion: test-report.html")
                print("\nPara abrir el reporte:")
                print("  - Abre el archivo: test-report.html")
                print("  - O ejecuta: start test-report.html (Windows)")
            else:
                print("[ERROR] No se pudo generar el reporte HTML")
                if result.stderr:
                    print(f"Error: {result.stderr[:200]}")
                print("\nLos resultados estan guardados en: allure-results/")
                print("Puedes leer los archivos JSON directamente o instalar Allure CLI:")
                print("")
                print("Windows (con Chocolatey):")
                print("  choco install allure-commandline")
                print("")
                print("O descargar desde:")
                print("  https://github.com/allure-framework/allure2/releases")
        except Exception as e:
            print(f"[ERROR] Error al generar reporte HTML: {e}")
            print("\nLos resultados están guardados en: allure-results/")
            print("Puedes leer los archivos JSON directamente o instalar Allure CLI:")
            print("")
            print("Windows (con Chocolatey):")
            print("  choco install allure-commandline")
            print("")
            print("O descargar desde:")
            print("  https://github.com/allure-framework/allure2/releases")
        
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
