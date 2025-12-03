"""Script para ejecutar tests y mostrar errores claramente."""
import subprocess
import sys
import re

def ejecutar_tests():
    """Ejecuta los tests y retorna la salida."""
    print("="*80)
    print("EJECUTANDO TESTS DE COBERTURA FALTANTE")
    print("="*80)
    
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "tests/test_api_cobertura_missing.py",
            "-v", "--tb=short", "--no-header"
        ],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    return result.stdout + result.stderr, result.returncode

if __name__ == "__main__":
    salida, codigo = ejecutar_tests()
    
    # Guardar en archivo
    with open("errores_tests_cobertura.txt", "w", encoding="utf-8") as f:
        f.write(salida)
    
    print(salida)
    print(f"\n{'='*80}")
    print(f"Código de salida: {codigo}")
    print(f"Errores guardados en: errores_tests_cobertura.txt")
    print(f"{'='*80}")




