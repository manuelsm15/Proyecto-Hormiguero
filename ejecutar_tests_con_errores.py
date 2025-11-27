"""Ejecutar tests y mostrar errores claramente."""
import sys
import subprocess

print("="*80)
print("EJECUTANDO TESTS DE COBERTURA FALTANTE")
print("="*80)

# Ejecutar tests uno por uno para ver errores específicos
tests = [
    "test_health_check_con_error",
    "test_consultar_alimentos_filtro_disponible",
    "test_crear_alimento_exitoso",
]

for test in tests:
    print(f"\n{'='*80}")
    print(f"Ejecutando: {test}")
    print('='*80)
    
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            f"tests/test_api_cobertura_missing.py::TestAPICoberturaMissing::{test}",
            "-v", "-s", "--tb=short"
        ],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode != 0:
        print(f"❌ Test {test} FALLÓ")
    else:
        print(f"✅ Test {test} PASÓ")


