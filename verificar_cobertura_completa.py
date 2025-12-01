"""
Script para verificar la cobertura completa del controlador de API.
"""
import subprocess
import sys
import re

def ejecutar_y_capturar(cmd):
    """Ejecuta un comando y captura la salida."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            errors='ignore'
        )
        return result.stdout + result.stderr, result.returncode
    except Exception as e:
        return f"Error: {e}", 1

def extraer_cobertura(salida):
    """Extrae el porcentaje de cobertura de la salida."""
    # Buscar patrón: "TOTAL     XXX    YYY    ZZZ%"
    patron = r'TOTAL\s+\d+\s+\d+\s+(\d+)%'
    match = re.search(patron, salida)
    if match:
        return int(match.group(1))
    
    # Buscar en formato de línea: "Name ... Stmts   Miss  Cover"
    patron2 = r'recoleccion_controller\.py\s+\d+\s+\d+\s+(\d+)%'
    match = re.search(patron2, salida)
    if match:
        return int(match.group(1))
    
    return None

print("="*80)
print("VERIFICACIÓN DE COBERTURA DEL CONTROLADOR DE API")
print("="*80)

# 1. Ejecutar tests de cobertura faltante
print("\n1. Ejecutando tests de cobertura faltante...")
salida1, codigo1 = ejecutar_y_capturar(
    "python -m pytest tests/test_api_cobertura_missing.py -v --tb=line -q"
)
print(salida1[-500:] if len(salida1) > 500 else salida1)

# 2. Verificar cobertura
print("\n2. Verificando cobertura del controlador de API...")
salida2, codigo2 = ejecutar_y_capturar(
    "python -m pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py "
    "--cov=src/recoleccion/api/recoleccion_controller "
    "--cov-report=term-missing --cov-report=html -q --tb=no"
)

# Extraer cobertura
cobertura = extraer_cobertura(salida2)
print(salida2[-1000:] if len(salida2) > 1000 else salida2)

# 3. Resumen
print("\n" + "="*80)
print("RESUMEN")
print("="*80)
if cobertura:
    print(f"Cobertura actual: {cobertura}%")
    if cobertura >= 80:
        print("✅ Objetivo alcanzado (≥80%)")
    else:
        print(f"⚠️  Falta {80 - cobertura}% para alcanzar el objetivo")
else:
    print("⚠️  No se pudo determinar la cobertura")

print("\nRevisa el reporte HTML en: htmlcov/index.html")
print("\nArchivos creados:")
print("  - tests/test_api_cobertura_missing.py")
print("  - docs/proyecto/ANALISIS_COBERTURA_MISSING.md")
print("  - RESUMEN_MISSING_COBERTURA.md")
print("  - REPORTE_COBERTURA_API.md")



