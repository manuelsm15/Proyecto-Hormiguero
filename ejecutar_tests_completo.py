"""Script para ejecutar tests y mostrar resultados."""
import subprocess
import sys

print("="*80)
print("EJECUTANDO TESTS DE COBERTURA FALTANTE")
print("="*80)

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_api_cobertura_missing.py", "-v", "--tb=short", "--no-header"],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore'
)

salida = result.stdout + result.stderr

# Guardar en archivo
with open("resultados_tests_cobertura.txt", "w", encoding="utf-8") as f:
    f.write(salida)

print(salida)
print(f"\n{'='*80}")
print(f"Código de salida: {result.returncode}")
print(f"Total de líneas de salida: {len(salida)}")
print(f"{'='*80}")

# Contar tests
import re
tests_passed = len(re.findall(r'PASSED', salida))
tests_failed = len(re.findall(r'FAILED', salida))
tests_error = len(re.findall(r'ERROR', salida))

print(f"\nRESUMEN:")
print(f"  Tests pasados: {tests_passed}")
print(f"  Tests fallidos: {tests_failed}")
print(f"  Tests con error: {tests_error}")
print(f"\nResultados guardados en: resultados_tests_cobertura.txt")




