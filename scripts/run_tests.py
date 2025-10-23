#!/usr/bin/env python3
"""
Script para ejecutar todas las pruebas del subsistema de recolección.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """
    Ejecuta un comando y muestra el resultado.
    
    Args:
        command: Comando a ejecutar
        description: Descripción del comando
        
    Returns:
        True si el comando fue exitoso, False en caso contrario
    """
    print(f"\n{'='*60}")
    print(f"Ejecutando: {description}")
    print(f"Comando: {command}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"ERROR: {description} fallo con codigo {result.returncode}")
        return False
    else:
        print(f"OK: {description} completado exitosamente")
        return True


def main():
    """Función principal."""
    print("Iniciando ejecucion de pruebas del Subsistema de Recoleccion")
    print("Universidad Cenfotec - Proyecto Final")
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Lista de comandos a ejecutar
    commands = [
        ("python -m pytest tests/ -v --tb=short", "Pruebas unitarias con pytest"),
        ("python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing", "Pruebas con cobertura"),
        ("behave features/simple_test.feature -v", "Pruebas BDD con Behave"),
    ]
    
    # Ejecutar comandos
    success_count = 0
    total_commands = len(commands)
    
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
    
    # Resumen final
    print(f"\n{'='*60}")
    print("RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"Comandos exitosos: {success_count}/{total_commands}")
    
    if success_count == total_commands:
        print("TODAS LAS PRUEBAS SE EJECUTARON EXITOSAMENTE!")
        print("\nReportes generados:")
        print("- Cobertura HTML: htmlcov/index.html")
        print("- Reporte Allure: allure-results/")
        print("\nPara ver el reporte de Allure, ejecuta:")
        print("allure serve allure-results")
        return 0
    else:
        print("ALGUNAS PRUEBAS FALLARON. Revisa los logs arriba.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
