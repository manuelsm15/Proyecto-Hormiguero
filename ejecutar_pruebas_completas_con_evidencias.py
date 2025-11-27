"""
Script completo que ejecuta todas las pruebas automáticas y muestra las evidencias en BD.
"""
import subprocess
import sys
import os
from datetime import datetime

def print_header(text):
    print(f"\n{'='*80}")
    print(f"{text}")
    print(f"{'='*80}")

def print_section(text):
    print(f"\n{'-'*80}")
    print(f"{text}")
    print(f"{'-'*80}")

def print_success(message):
    print(f"[OK] {message}")

def print_info(message):
    print(f"[INFO] {message}")

# Ejecutar todas las pruebas
print_header("EJECUTANDO TODAS LAS PRUEBAS AUTOMÁTICAS")

# 1. Tests unitarios
print_section("1. Tests Unitarios - Modelos de Tarea")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_models.py::TestTareaRecoleccion", "-v", "--tb=line", "-q"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode == 0:
    print_success("Tests de modelos de tarea: PASSED")
else:
    print(f"Error: {result.stderr}")

# 2. Tests de API
print_section("2. Tests de API - Endpoints de Tareas")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_api_controller.py", "-k", "tarea", "-v", "--tb=line", "-q"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode == 0:
    print_success("Tests de API de tareas: PASSED")
else:
    print(f"Error: {result.stderr}")

# 3. Tests de Servicio
print_section("3. Tests de Servicio - Lógica de Tareas")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_recoleccion_service.py", "-k", "tarea", "-v", "--tb=line", "-q"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode == 0:
    print_success("Tests de servicio de tareas: PASSED")
else:
    print(f"Error: {result.stderr}")

# 4. Tests de hormigas_asignadas en BD
print_section("4. Tests de hormigas_asignadas en Base de Datos")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_hormigas_asignadas_bd.py", "-v", "--tb=line"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode == 0:
    print_success("Tests de hormigas_asignadas en BD: PASSED")
else:
    print(f"Error: {result.stderr}")

# 5. Ejecutar script de evidencias
print_section("5. Generando Evidencias en Base de Datos")
print_info("Ejecutando script de evidencias...")
result = subprocess.run(
    [sys.executable, "test_evidencias_bd_completo.py"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode == 0:
    print_success("Evidencias generadas correctamente")
else:
    print(f"Error: {result.stderr}")

# 6. Resumen final
print_header("RESUMEN FINAL DE PRUEBAS")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=no", "-q"],
    capture_output=True,
    text=True
)
print(result.stdout)

print_header("PRUEBAS COMPLETADAS")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nRevisa los resultados arriba para ver todas las evidencias.")



