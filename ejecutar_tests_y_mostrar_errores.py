"""Script para ejecutar tests y mostrar errores claramente."""
import subprocess
import sys

print("Ejecutando tests de cobertura faltante...")
print("="*80)

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_api_cobertura_missing.py", "-v", "--tb=short"],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore'
)

print(result.stdout)
if result.stderr:
    print("\nSTDERR:")
    print(result.stderr)

print(f"\nCódigo de salida: {result.returncode}")

# Guardar en archivo también
with open("errores_tests.txt", "w", encoding="utf-8") as f:
    f.write(result.stdout)
    if result.stderr:
        f.write("\nSTDERR:\n")
        f.write(result.stderr)

print("\nErrores guardados en: errores_tests.txt")




