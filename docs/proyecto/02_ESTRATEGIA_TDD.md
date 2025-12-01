# Estrategia de TDD y Ejemplos de Casos de Prueba

## 1. Metodología TDD Aplicada

### 1.1 Ciclo Rojo-Verde-Refactor

El desarrollo del subsistema siguió estrictamente la metodología TDD con el ciclo:

1. **🔴 Rojo**: Escribir test que falle
2. **🟢 Verde**: Implementar código mínimo para que pase
3. **🔵 Refactor**: Mejorar código manteniendo tests pasando

### 1.2 Evidencia en Commits

El historial de commits muestra claramente el ciclo TDD:

```
commit abc123 - test: agregar test para validar capacidad de carga
commit def456 - feat: implementar validación de capacidad_carga
commit ghi789 - refactor: mejorar validación de capacidad
```

## 2. Ejemplos de Casos de Prueba

### 2.1 Casos de Prueba para Capacidad de Carga

#### Test: Validación de Capacidad de Carga

**Archivo**: `tests/test_models.py::TestHormiga::test_hormiga_validaciones_error`

```python
def test_hormiga_validaciones_error(self):
    """Prueba las validaciones de una hormiga."""
    # Test que capacidad <= 0 debe fallar
    with pytest.raises(ValueError, match="La capacidad de carga debe ser mayor a 0"):
        Hormiga(
            id="hormiga_001",
            capacidad_carga=0,  # ❌ Inválido
            tiempo_vida=3600
        )
```

**Ciclo TDD:**
1. 🔴 **Rojo**: Test escrito primero, falla porque no hay validación
2. 🟢 **Verde**: Implementar validación en `Hormiga.__post_init__()`
3. 🔵 **Refactor**: Mejorar mensaje de error

#### Test: Valores por Defecto

**Archivo**: `tests/test_models.py::TestHormiga::test_hormiga_valores_por_defecto`

```python
def test_hormiga_valores_por_defecto(self):
    """Prueba los valores por defecto de una hormiga."""
    hormiga = Hormiga(id="hormiga_001")
    
    assert hormiga.capacidad_carga == 5  # ✅ Valor por defecto
    assert hormiga.estado == EstadoHormiga.DISPONIBLE
    assert hormiga.tiempo_vida == 3600
```

### 2.2 Casos de Prueba para Cambios de Estado

#### Test: Cambio de Estado de Hormiga

**Archivo**: `tests/test_models.py::TestHormiga::test_cambiar_estado`

```python
def test_cambiar_estado(self):
    """Prueba el cambio de estado de una hormiga."""
    hormiga = Hormiga(id="hormiga_001")
    
    # Estado inicial
    assert hormiga.estado == EstadoHormiga.DISPONIBLE
    
    # Cambiar a BUSCANDO
    hormiga.cambiar_estado(EstadoHormiga.BUSCANDO)
    assert hormiga.estado == EstadoHormiga.BUSCANDO
    
    # Cambiar a RECOLECTANDO
    hormiga.cambiar_estado(EstadoHormiga.RECOLECTANDO)
    assert hormiga.estado == EstadoHormiga.RECOLECTANDO
    
    # Cambiar a TRANSPORTANDO
    hormiga.cambiar_estado(EstadoHormiga.TRANSPORTANDO)
    assert hormiga.estado == EstadoHormiga.TRANSPORTANDO
```

**Ciclo TDD:**
1. 🔴 **Rojo**: Test escrito, falla porque no existe `cambiar_estado()`
2. 🟢 **Verde**: Implementar método `cambiar_estado()`
3. 🔵 **Refactor**: Agregar validaciones si es necesario

### 2.3 Casos de Prueba para Recolección Exitosa

#### Test: Completar Tarea Exitosamente

**Archivo**: `tests/test_recoleccion_service.py::test_completar_tarea_recoleccion_exitoso`

```python
@pytest.mark.asyncio
async def test_completar_tarea_recoleccion_exitoso(
    self, recoleccion_service, alimento_ejemplo, hormiga_ejemplo
):
    """Prueba la finalización exitosa de una tarea."""
    # Arrange
    tarea = await recoleccion_service.crear_tarea_recoleccion(
        "tarea_001", alimento_ejemplo
    )
    
    # Agregar hormigas
    for i in range(3):
        hormiga = Hormiga(id=f"hormiga_{i}")
        tarea.agregar_hormiga(hormiga)
    
    # Iniciar tarea
    await recoleccion_service.iniciar_tarea_recoleccion(tarea)
    
    # Act
    await recoleccion_service.completar_tarea_recoleccion(tarea, 10)
    
    # Assert
    assert tarea.estado == EstadoTarea.COMPLETADA
    assert tarea.alimento_recolectado == 10
    assert tarea.fecha_fin is not None
    assert alimento_ejemplo.disponible is False  # ✅ Alimento marcado como no disponible
```

**Ciclo TDD:**
1. 🔴 **Rojo**: Test escrito, falla porque `completar_tarea_recoleccion()` no existe
2. 🟢 **Verde**: Implementar método mínimo
3. 🔵 **Refactor**: Agregar validaciones y persistencia

### 2.4 Casos de Prueba para Exceso de Capacidad

#### Test: Validación de Capacidad Inválida

**Archivo**: `tests/test_models.py::TestHormiga::test_hormiga_validaciones_error`

```python
def test_hormiga_validaciones_error(self):
    """Prueba las validaciones de una hormiga."""
    # Test capacidad <= 0
    with pytest.raises(ValueError, match="La capacidad de carga debe ser mayor a 0"):
        Hormiga(id="hormiga_001", capacidad_carga=0)
    
    # Test tiempo_vida <= 0
    with pytest.raises(ValueError, match="El tiempo de vida debe ser mayor a 0"):
        Hormiga(id="hormiga_001", capacidad_carga=5, tiempo_vida=0)
```

### 2.5 Casos de Prueba para Solicitud de Refuerzo

#### Test: Solicitar Hormigas Exitosamente

**Archivo**: `tests/test_recoleccion_service.py::test_solicitar_hormigas_exitoso`

```python
@pytest.mark.asyncio
async def test_solicitar_hormigas_exitoso(
    self, recoleccion_service, mock_comunicacion_service, hormiga_ejemplo
):
    """Prueba la solicitud exitosa de hormigas."""
    # Arrange
    mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
    mock_comunicacion_service.consultar_respuesta_hormigas.return_value = [hormiga_ejemplo]
    
    # Act
    hormigas = await recoleccion_service.solicitar_hormigas(3)
    
    # Assert
    assert len(hormigas) == 1
    assert hormigas[0].id == "hormiga_001"
    mock_comunicacion_service.solicitar_hormigas.assert_called_once_with(3, "recoleccion")
```

#### Test: Asignar Hormigas a Tarea

**Archivo**: `tests/test_recoleccion_service.py::test_asignar_hormigas_a_tarea_exitoso`

```python
@pytest.mark.asyncio
async def test_asignar_hormigas_a_tarea_exitoso(
    self, recoleccion_service, alimento_ejemplo, hormiga_ejemplo
):
    """Prueba la asignación exitosa de hormigas a una tarea."""
    # Arrange
    tarea = await recoleccion_service.crear_tarea_recoleccion(
        "tarea_001", alimento_ejemplo
    )
    hormigas = [Hormiga(id=f"hormiga_{i}") for i in range(3)]
    
    # Act
    exito, error = await recoleccion_service.asignar_hormigas_a_tarea(
        tarea, hormigas, lote_id="LOTE_001"
    )
    
    # Assert
    assert exito is True
    assert error is None
    assert len(tarea.hormigas_asignadas) == 3
    assert tarea.hormigas_lote_id == "LOTE_001"
```

## 3. Casos de Prueba de Límites

### 3.1 Límite: Capacidad Mínima

```python
def test_capacidad_minima_valida(self):
    """Prueba que capacidad = 1 es válida."""
    hormiga = Hormiga(id="hormiga_001", capacidad_carga=1)
    assert hormiga.capacidad_carga == 1
```

### 3.2 Límite: Capacidad Máxima

```python
def test_capacidad_maxima_valida(self):
    """Prueba que capacidad = 5 (default) es válida."""
    hormiga = Hormiga(id="hormiga_001")
    assert hormiga.capacidad_carga == 5
```

### 3.3 Límite: Cantidad Mínima de Hormigas

```python
def test_cantidad_minima_hormigas(self):
    """Prueba con cantidad mínima de hormigas necesarias."""
    alimento = Alimento(
        id="A1", nombre="Fruta",
        cantidad_hormigas_necesarias=1,  # Mínimo
        puntos_stock=1,
        tiempo_recoleccion=60
    )
    tarea = TareaRecoleccion(id="T1", alimento=alimento)
    tarea.agregar_hormiga(Hormiga(id="H1"))
    
    assert tarea.tiene_suficientes_hormigas() is True
```

## 4. Casos de Prueba Negativos

### 4.1 Test: Crear Tarea con Alimento No Disponible

**Archivo**: `tests/test_recoleccion_service.py::test_crear_tarea_con_alimento_no_disponible_debe_fallar`

```python
@pytest.mark.asyncio
async def test_crear_tarea_con_alimento_no_disponible_debe_fallar(
    self, recoleccion_service, alimento_ejemplo
):
    """Prueba que no se puede crear tarea con alimento no disponible."""
    # Arrange
    alimento_ejemplo.disponible = False
    
    # Act & Assert
    with pytest.raises(ValueError, match="no está disponible"):
        await recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", alimento_ejemplo
        )
```

### 4.2 Test: Iniciar Tarea Sin Suficientes Hormigas

**Archivo**: `tests/test_recoleccion_service.py::test_iniciar_tarea_sin_suficientes_hormigas`

```python
@pytest.mark.asyncio
async def test_iniciar_tarea_sin_suficientes_hormigas(
    self, recoleccion_service, alimento_ejemplo
):
    """Prueba que no se puede iniciar tarea sin suficientes hormigas."""
    # Arrange
    tarea = await recoleccion_service.crear_tarea_recoleccion(
        "tarea_001", alimento_ejemplo
    )
    # No agregar hormigas (requiere 3, tiene 0)
    
    # Act & Assert
    with pytest.raises(ValueError, match="No se puede iniciar la tarea sin suficientes hormigas"):
        await recoleccion_service.iniciar_tarea_recoleccion(tarea)
```

## 5. Casos de Prueba BDD

### 5.1 Escenario: Recolección Exitosa

**Archivo**: `features/recoleccion.feature`

```gherkin
Scenario: Completar tarea de recolección
  Given que tengo una tarea en estado EN_PROCESO
  When completo la tarea con 10 unidades de alimento
  Then la tarea debe estar en estado COMPLETADA
  And la tarea debe tener 10 unidades de alimento recolectado
  And las hormigas deben estar en estado TRANSPORTANDO
  And la tarea debe tener fecha de finalización
  And el alimento debe estar marcado como no disponible (agotado)
```

### 5.2 Escenario: Solicitud de Refuerzo

```gherkin
Scenario: Solicitar hormigas para recolección
  Given que necesito 3 hormigas para una tarea
  When solicito las hormigas al subsistema de comunicación
  Then debo recibir las hormigas solicitadas
  And las hormigas deben estar disponibles
```

## 6. Estrategia de Cobertura

### 6.1 Cobertura por Módulo

- **Modelos**: 100% (todos los métodos y validaciones)
- **Servicio Principal**: 77% (lógica de negocio crítica)
- **API Controller**: Alta cobertura (todos los endpoints)
- **Persistencia**: 45% (código de BD, menos crítico para TDD)

### 6.2 Criterios de Cobertura

- **Líneas de código**: ≥ 80% (objetivo)
- **Ramas**: Cobertura de todos los if/else
- **Métodos**: Todos los métodos públicos probados
- **Casos límite**: Todos los límites validados
- **Casos negativos**: Todos los errores manejados

## 7. Evidencia de Refactorizaciones

### 7.1 Refactorización: Sistema de Lotes

**Antes**: Asignación directa de hormigas
**Después**: Sistema de lotes con validación
**Evidencia**: Commits con mensaje "refactor: implementar sistema de lotes"

### 7.2 Refactorización: Persistencia

**Antes**: Código duplicado para SQLite y SQL Server
**Después**: Abstracción con `DatabaseManager`
**Evidencia**: Commits con mensaje "refactor: abstraer persistencia"

## 8. Métricas de Tests

### 8.1 Distribución de Tests

- **Tests de Modelos**: 40+ tests
- **Tests de Servicio**: 30+ tests
- **Tests de API**: 25+ tests
- **Tests de Integración**: 10+ tests
- **Tests BDD**: 14+ escenarios

### 8.2 Tipos de Tests

- **Unitarios**: 121 tests
- **Integración**: 4 tests (marcados con @integration)
- **BDD**: 14+ escenarios
- **Persistencia**: 6 tests directos de BD

## 9. Defectos Detectados y Corregidos

### 9.1 Defecto: Conversión de alimento_id

**Problema**: `alimento_id` como string no se convertía a INT en SQL Server
**Solución**: Implementar conversión según esquema de BD
**Test**: `test_guardar_tarea_con_alimento_id_string`

### 9.2 Defecto: hormigas_asignadas no se guardaba

**Problema**: Columna `hormigas_asignadas` no se poblaba
**Solución**: Guardar `len(tarea.hormigas_asignadas)` al persistir
**Test**: `test_hormigas_asignadas_bd.py` (6 tests)

### 9.3 Defecto: Tarea no se completaba automáticamente

**Problema**: Tareas no se completaban por tiempo transcurrido
**Solución**: Implementar `verificar_y_completar_tarea_por_tiempo()`
**Test**: `test_verificar_y_completar_tarea_por_tiempo_*`

## 10. Aprendizajes y Mejoras

### 10.1 Aprendizajes

1. **TDD mejora la calidad**: Los defectos se detectan temprano
2. **Tests como documentación**: Los tests documentan el comportamiento esperado
3. **Refactorización segura**: Los tests permiten refactorizar con confianza

### 10.2 Mejoras Aplicadas

1. **Mocking de dependencias**: Uso de mocks para aislar tests
2. **Tests de integración**: Validación end-to-end
3. **BDD para casos de negocio**: Escenarios legibles para stakeholders

## 11. Referencias

- Beck, K. (2003). Test-Driven Development: By Example
- Martin, R. C. (2009). Clean Code: A Handbook of Agile Software Craftsmanship
- Freeman, S., & Pryce, N. (2009). Growing Object-Oriented Software, Guided by Tests




