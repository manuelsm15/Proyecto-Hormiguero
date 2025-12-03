# Documento Principal del Proyecto

**Proyecto**: Subsistema de Recolección de Alimentos  
**Universidad**: Cenfotec  
**Fecha**: 2025-12-01

---

## Resumen del Proyecto

Este proyecto implementa un subsistema de recolección de alimentos para una simulación de colonia de hormigas, desarrollado siguiendo metodologías **TDD** (Test-Driven Development) y **BDD** (Behavior-Driven Development).

---

## Objetivos Alcanzados

### ✅ Cobertura de Código
- **Objetivo**: ≥80% de cobertura
- **Resultado**: **>80%** ✅ **ALCANZADO**
- **Modelos**: 100% ✅
- **Servicios**: >80% ✅
- **APIs**: >80% ✅

### ✅ Testing
- **Tests Unitarios**: 220+ tests ✅
- **Tests de Integración**: 10+ tests ✅
- **Tests BDD**: 29+ escenarios ✅
- **Total**: 250+ tests ✅

### ✅ Calidad de Código
- **Metodología TDD**: Implementada ✅
- **Metodología BDD**: Implementada ✅
- **Reportes Allure**: Configurados ✅
- **Documentación**: Completa ✅

---

## Estructura del Proyecto

```
src/
├── recoleccion/
│   ├── api/           # Controladores REST
│   ├── models/        # Modelos de datos
│   ├── services/      # Lógica de negocio
│   └── database/      # Gestión de base de datos
tests/                  # Pruebas unitarias
features/               # Pruebas BDD
scripts/                # Scripts de automatización
docs/                   # Documentación
```

---

## Tecnologías Utilizadas

- **Python 3.12**
- **FastAPI** - Framework web
- **Pytest** - Testing
- **Behave** - BDD
- **Allure** - Reportes
- **Docker** - Containerización
- **Railway** - Despliegue

---

## Metodologías Aplicadas

### TDD (Test-Driven Development)
- ✅ Desarrollo guiado por pruebas
- ✅ Tests escritos antes del código
- ✅ Refactorización continua
- ✅ Cobertura >80% alcanzada

### BDD (Behavior-Driven Development)
- ✅ Escenarios en formato Gherkin
- ✅ Integración con Behave
- ✅ Documentación viva
- ✅ Reportes Allure

---

## Resultados Finales

### Cobertura de Código
- **Total**: >80% ✅
- **Modelos**: 100% ✅
- **Servicios**: >80% ✅
- **APIs**: >80% ✅

### Tests
- **Total**: 250+ tests ✅
- **Pasando**: 250+ tests ✅
- **Fallidos**: 0 ✅

### Endpoints
- **Total**: 25 endpoints ✅
- **Cubiertos**: 25/25 (100%) ✅

---

## Documentación Relacionada

- [Descripción del Subsistema](01_DESCRIPCION_SUBSISTEMA.md)
- [Estrategia TDD](02_ESTRATEGIA_TDD.md)
- [Reporte de Cobertura](03_REPORTE_COBERTURA.md)
- [Resultados de Aprendizajes](04_RESULTADOS_APRENDIZAJES.md)
- [Referencias](05_REFERENCIAS.md)
- [TDD APIs](06_TDD_APIS.md)
- [BDD APIs](07_BDD_APIS.md)

---

## Comandos Principales

```bash
# Ejecutar todos los tests con cobertura
pytest tests/ -v --cov=src --cov-report=html

# Generar reporte Allure
python scripts/generate_allure_report.py

# Iniciar servidor
python main.py
```

---

## Estado del Proyecto

✅ **COMPLETADO**

- ✅ Cobertura >80% alcanzada
- ✅ Todos los endpoints probados
- ✅ Documentación completa
- ✅ Despliegue configurado

---

**Última actualización**: 2025-12-01





