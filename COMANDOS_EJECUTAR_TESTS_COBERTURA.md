# Comandos para Ejecutar Tests y Ver Cobertura

## 1. Ejecutar Tests de Cobertura Faltante

```bash
# Ejecutar todos los tests de cobertura faltante con salida detallada
pytest tests/test_api_cobertura_missing.py -v

# Ejecutar con más detalles (muestra prints y stdout)
pytest tests/test_api_cobertura_missing.py -v -s

# Ejecutar un test específico
pytest tests/test_api_cobertura_missing.py::TestAPICoberturaMissing::test_crear_alimento_exitoso -v

# Ejecutar y detenerse en el primer error
pytest tests/test_api_cobertura_missing.py -v -x
```

## 2. Verificar Cobertura Completa

```bash
# Verificar cobertura de todos los tests (antiguos + nuevos)
pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py --cov=src/recoleccion/api/recoleccion_controller --cov-report=term-missing --cov-report=html

# Solo ver el porcentaje de cobertura (más rápido)
pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py --cov=src/recoleccion/api/recoleccion_controller --cov-report=term -q

# Ver cobertura con líneas faltantes específicas
pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py --cov=src/recoleccion/api/recoleccion_controller --cov-report=term-missing
```

## 3. Ver Reporte HTML de Cobertura

```bash
# Generar reporte HTML (se crea en htmlcov/)
pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py --cov=src/recoleccion/api/recoleccion_controller --cov-report=html

# Luego abrir en el navegador:
# htmlcov/index.html
```

## 4. Comandos Útiles para Debugging

```bash
# Ver solo los tests que fallan
pytest tests/test_api_cobertura_missing.py -v --tb=short

# Ver traza completa de errores
pytest tests/test_api_cobertura_missing.py -v --tb=long

# Ejecutar tests y mostrar prints
pytest tests/test_api_cobertura_missing.py -v -s

# Contar cuántos tests pasan/fallan
pytest tests/test_api_cobertura_missing.py -v --tb=no | findstr /C:"PASSED" /C:"FAILED"
```

## 5. Comandos en PowerShell (Windows)

```powershell
# Ejecutar tests
python -m pytest tests/test_api_cobertura_missing.py -v

# Verificar cobertura
python -m pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py --cov=src/recoleccion/api/recoleccion_controller --cov-report=term-missing --cov-report=html

# Ver resultados guardados en archivo
python -m pytest tests/test_api_cobertura_missing.py -v > resultados_tests.txt 2>&1
Get-Content resultados_tests.txt
```

## 6. Script Python para Ejecutar Todo

Crea un archivo `ejecutar_todo.py`:

```python
import subprocess
import sys

print("="*80)
print("EJECUTANDO TESTS Y VERIFICANDO COBERTURA")
print("="*80)

# 1. Ejecutar tests
print("\n1. Ejecutando tests de cobertura faltante...")
result1 = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_api_cobertura_missing.py", "-v"],
    capture_output=True,
    text=True
)
print(result1.stdout)
if result1.stderr:
    print("STDERR:", result1.stderr)

# 2. Verificar cobertura
print("\n2. Verificando cobertura...")
result2 = subprocess.run(
    [
        sys.executable, "-m", "pytest",
        "tests/test_api_controller.py",
        "tests/test_api_cobertura_missing.py",
        "--cov=src/recoleccion/api/recoleccion_controller",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-q"
    ],
    capture_output=True,
    text=True
)
print(result2.stdout)
if result2.stderr:
    print("STDERR:", result2.stderr)

print("\n" + "="*80)
print("RESUMEN")
print("="*80)
print("Revisa el reporte HTML en: htmlcov/index.html")
```

Ejecutar con:
```bash
python ejecutar_todo.py
```

## 7. Interpretar Resultados

### Salida de Tests
- `PASSED` = Test pasó correctamente
- `FAILED` = Test falló (revisar el error)
- `ERROR` = Error en el test mismo (no en el código probado)

### Salida de Cobertura
- `TOTAL` = Resumen de cobertura total
- `recoleccion_controller.py` = Cobertura específica del controlador
- Líneas en `Missing` = Líneas que no están cubiertas

### Objetivo
- **Cobertura objetivo**: ≥80%
- **Cobertura actual**: Se mostrará en la salida del comando de cobertura

## 8. Si Hay Errores

1. **Revisar el error específico** en la salida del test
2. **Identificar el problema**: mock, fixture, o lógica del test
3. **Ajustar el test** según el error
4. **Ejecutar de nuevo** hasta que pase

## Ejemplo de Uso Completo

```bash
# Paso 1: Ejecutar tests
pytest tests/test_api_cobertura_missing.py -v

# Paso 2: Si hay errores, revisarlos y corregirlos
# Luego ejecutar de nuevo

# Paso 3: Verificar cobertura
pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py --cov=src/recoleccion/api/recoleccion_controller --cov-report=term-missing --cov-report=html

# Paso 4: Abrir htmlcov/index.html en el navegador para ver detalles
```




