"""
Script para ejecutar tests de cobertura y mostrar resultados.
"""
import subprocess
import sys

def ejecutar_comando(cmd):
    """Ejecuta un comando y muestra la salida."""
    print(f"\n{'='*80}")
    print(f"Ejecutando: {cmd}")
    print('='*80)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    return result.returncode == 0

# 1. Ejecutar tests de cobertura faltante
print("\n1. Ejecutando tests de cobertura faltante...")
exito1 = ejecutar_comando("python -m pytest tests/test_api_cobertura_missing.py -v --tb=short")

# 2. Verificar cobertura actual
print("\n2. Verificando cobertura del controlador de API...")
exito2 = ejecutar_comando("python -m pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py --cov=src/recoleccion/api/recoleccion_controller --cov-report=term-missing --cov-report=html -q")

# 3. Mostrar resumen
print("\n" + "="*80)
print("RESUMEN")
print("="*80)
if exito1 and exito2:
    print("✅ Tests ejecutados correctamente")
else:
    print("⚠️  Algunos tests fallaron. Revisa la salida anterior.")
print("\nRevisa el reporte HTML en: htmlcov/index.html")


