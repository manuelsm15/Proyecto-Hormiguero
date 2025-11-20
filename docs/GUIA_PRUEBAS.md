# Guía de Pruebas - TDD y BDD con Allure

Esta guía explica cómo ejecutar todas las pruebas del subsistema de recolección usando metodologías TDD (Test-Driven Development) y BDD (Behavior-Driven Development) con reportes de Allure.

## 📋 Requisitos Previos

Asegúrate de tener instaladas todas las dependencias:

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `pytest` - Para pruebas TDD
- `pytest-cov` - Para cobertura de código
- `pytest-asyncio` - Para pruebas asíncronas
- `allure-pytest` - Para reportes Allure con pytest
- `behave` - Para pruebas BDD
- `allure-behave` - Para reportes Allure con behave

## 🧪 Tipos de Pruebas

### Pruebas TDD (Test-Driven Development)

Las pruebas TDD están ubicadas en el directorio `tests/` y utilizan `pytest`:

- `test_models.py` - Pruebas de modelos de datos
- `test_recoleccion_service.py` - Pruebas del servicio de recolección
- `test_api_controller.py` - Pruebas del controlador REST
- `test_mock_services.py` - Pruebas de servicios mock
- `test_timer_service.py` - Pruebas del servicio de temporizador

### Pruebas BDD (Behavior-Driven Development)

Las pruebas BDD están en el directorio `features/` y utilizan `behave`:

- `recoleccion.feature` - Escenarios principales de recolección
- `recoleccion_simple.feature` - Escenarios simplificados
- `features/steps/recoleccion_steps.py` - Implementación de steps

## 🚀 Ejecutar Pruebas

### Opción 1: Ejecutar TODAS las Pruebas (Recomendado)

```bash
python scripts/run_tests_complete.py
```

Este script ejecuta:
1. ✅ Pruebas TDD (pytest) con cobertura y Allure
2. ✅ Pruebas BDD (behave) con Allure
3. ✅ Genera reporte HTML de Allure combinado

### Opción 2: Ejecutar Solo Pruebas TDD

```bash
python scripts/run_tdd_tests.py
```

O manualmente:

```bash
pytest tests/ -v --cov=src --cov-report=html --allure-results-dir=allure-results
```

### Opción 3: Ejecutar Solo Pruebas BDD

```bash
python scripts/run_bdd_tests.py
```

O manualmente:

```bash
behave features/ -f allure_behave.formatter:AllureFormatter -o allure-results
```

### Opción 4: Ejecutar Pruebas Específicas

#### Ejecutar un archivo de prueba específico:

```bash
pytest tests/test_recoleccion_service.py -v
```

#### Ejecutar un test específico:

```bash
pytest tests/test_recoleccion_service.py::TestRecoleccionService::test_consultar_alimentos_disponibles_exitoso -v
```

#### Ejecutar un escenario BDD específico:

```bash
behave features/recoleccion.feature:12
```

## 📊 Ver Reportes

### Reporte de Allure

Después de ejecutar las pruebas, genera el reporte HTML:

```bash
python scripts/generate_allure_report.py
```

O manualmente:

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

El reporte incluye:
- ✅ Resumen de ejecución
- ✅ Resultados por suite
- ✅ Cobertura de código
- ✅ Screenshots y attachments
- ✅ Timeline de ejecución

### Reporte de Cobertura HTML

El reporte de cobertura se genera automáticamente en:

```
htmlcov/index.html
```

Abre este archivo en tu navegador para ver:
- ✅ Cobertura por módulo
- ✅ Líneas no cubiertas
- ✅ Métricas de cobertura

## 📈 Criterios de Aceptación

### Cobertura de Código

El proyecto requiere **mínimo 80% de cobertura**:

```bash
pytest tests/ --cov=src --cov-fail-under=80
```

### Pruebas por Categoría

- **Unitarias**: Todas deben pasar
- **Integración**: Todas deben pasar
- **BDD**: Todos los escenarios deben pasar

## 🔍 Estructura de Directorios

```
Proyecto Hormiguero/
├── tests/                    # Pruebas TDD (pytest)
│   ├── test_models.py
│   ├── test_recoleccion_service.py
│   ├── test_api_controller.py
│   └── ...
├── features/                 # Pruebas BDD (behave)
│   ├── recoleccion.feature
│   └── steps/
│       └── recoleccion_steps.py
├── allure-results/           # Resultados de Allure (generado)
├── allure-report/            # Reporte HTML de Allure (generado)
├── htmlcov/                  # Reporte de cobertura (generado)
└── scripts/
    ├── run_tests_complete.py  # Script maestro
    ├── run_tdd_tests.py       # Solo TDD
    ├── run_bdd_tests.py       # Solo BDD
    └── generate_allure_report.py
```

## ⚙️ Configuración

### pytest.ini

```ini
[tool:pytest]
testpaths = tests
addopts = 
    --cov=src
    --cov-report=html:htmlcov
    --cov-fail-under=80
    --allure-results-dir=allure-results
```

### behave.ini

```ini
[behave]
format = pretty
default_tags = -skip
```

## 🐛 Solución de Problemas

### Allure no encontrado

```bash
# Instalar Allure CLI (requiere Java)
# Windows: choco install allure-commandline
# Linux: apt-get install allure
# Mac: brew install allure

# O usar el script Python
python scripts/generate_allure_report.py
```

### behave no encontrado

```bash
pip install behave allure-behave
```

### Pruebas asíncronas fallan

Asegúrate de usar `@pytest.mark.asyncio`:

```python
@pytest.mark.asyncio
async def test_mi_prueba():
    ...
```

## 📝 Agregar Nuevas Pruebas

### Nueva Prueba TDD

1. Crear archivo `tests/test_nuevo_servicio.py`
2. Importar pytest y el módulo a probar
3. Escribir pruebas siguiendo patrón AAA (Arrange-Act-Assert)

```python
import pytest
from src.recoleccion.services.mi_servicio import MiServicio

class TestMiServicio:
    @pytest.mark.asyncio
    async def test_funcionalidad(self):
        # Arrange
        servicio = MiServicio()
        
        # Act
        resultado = await servicio.mi_metodo()
        
        # Assert
        assert resultado == esperado
```

### Nuevo Escenario BDD

1. Agregar escenario en `features/recoleccion.feature`
2. Implementar steps en `features/steps/recoleccion_steps.py`

```gherkin
Scenario: Nueva funcionalidad
    Given que tengo una condición
    When ejecuto una acción
    Then debo obtener un resultado
```

## ✅ Checklist de Pruebas

Antes de hacer commit, verifica:

- [ ] Todas las pruebas TDD pasan: `pytest tests/ -v`
- [ ] Todas las pruebas BDD pasan: `behave features/`
- [ ] Cobertura ≥ 80%: `pytest --cov=src --cov-fail-under=80`
- [ ] Reporte de Allure generado correctamente
- [ ] No hay warnings críticos

## 🔗 Referencias

- [Documentación de pytest](https://docs.pytest.org/)
- [Documentación de behave](https://behave.readthedocs.io/)
- [Documentación de Allure](https://docs.qameta.io/allure/)
- [Metodología TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Metodología BDD](https://martinfowler.com/bliki/GivenWhenThen.html)



