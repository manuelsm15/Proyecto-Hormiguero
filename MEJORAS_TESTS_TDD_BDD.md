# 🧪 Mejoras en Tests TDD y BDD

Este documento describe las mejoras realizadas en los tests TDD (Test-Driven Development) y BDD (Behavior-Driven Development) para validar todas las funcionalidades nuevas agregadas al subsistema de recolección.

---

## 📋 Resumen de Mejoras

### Funcionalidades Nuevas Cubiertas

1. ✅ **Asignación de hormigas con `hormigas_lote_id`**
2. ✅ **Inicio automático de tareas al asignar hormigas con lote_id**
3. ✅ **Inicio de tareas con `hormigas_lote_id`**
4. ✅ **Completado automático de tareas por tiempo transcurrido**
5. ✅ **Validación de alimentos no disponibles al crear tareas**
6. ✅ **Inclusión de `hormigas_lote_id` en status**
7. ✅ **Endpoint de asignar-hormigas con inicio automático**

---

## 🧪 Tests TDD (Test-Driven Development)

### Archivo: `tests/test_recoleccion_service.py`

#### Nuevos Tests Agregados:

1. **`test_iniciar_tarea_con_hormigas_lote_id`**
   - **Propósito**: Verifica que al iniciar una tarea con `hormigas_lote_id`, este se guarda correctamente en la tarea.
   - **Validaciones**:
     - La tarea se inicia correctamente
     - El `hormigas_lote_id` se asigna a la tarea
     - El estado cambia a `EN_PROCESO`

2. **`test_verificar_y_completar_tarea_por_tiempo_exitoso`**
   - **Propósito**: Verifica que una tarea se completa automáticamente cuando ha transcurrido el tiempo de recolección.
   - **Validaciones**:
     - La tarea se completa automáticamente
     - El estado cambia a `COMPLETADA`
     - `fecha_fin` se establece correctamente como `fecha_inicio + tiempo_recoleccion`
     - El alimento se marca como no disponible

3. **`test_verificar_y_completar_tarea_por_tiempo_no_completada`**
   - **Propósito**: Verifica que una tarea NO se completa si no ha transcurrido el tiempo suficiente.
   - **Validaciones**:
     - La tarea permanece en estado `EN_PROCESO`
     - No se establece `fecha_fin`

4. **`test_verificar_y_completar_tarea_por_tiempo_tarea_pendiente`**
   - **Propósito**: Verifica que una tarea pendiente no se completa automáticamente.
   - **Validaciones**:
     - La tarea permanece en estado `PENDIENTE`
     - No se completa automáticamente

5. **`test_crear_tarea_con_alimento_no_disponible_debe_fallar`**
   - **Propósito**: Verifica que no se puede crear una tarea con un alimento no disponible.
   - **Validaciones**:
     - Se lanza una excepción `ValueError`
     - El mensaje indica que el alimento no está disponible

---

### Archivo: `tests/test_api_controller.py`

#### Nuevos Tests Agregados:

1. **`test_asignar_hormigas_con_lote_id_e_inicio_automatico`**
   - **Propósito**: Verifica que al asignar hormigas con `hormigas_lote_id`, la tarea se inicia automáticamente.
   - **Validaciones**:
     - El endpoint responde con código 200
     - `iniciada` es `True`
     - `hormigas_lote_id` se incluye en la respuesta
     - El estado es `en_proceso`

2. **`test_asignar_hormigas_sin_lote_id_no_inicia`**
   - **Propósito**: Verifica que asignar hormigas sin `hormigas_lote_id` NO inicia la tarea automáticamente.
   - **Validaciones**:
     - El endpoint responde con código 200
     - `iniciada` es `False`
     - `hormigas_lote_id` es `None`

3. **`test_iniciar_tarea_con_lote_id`**
   - **Propósito**: Verifica que el endpoint de iniciar tarea acepta y guarda `hormigas_lote_id`.
   - **Validaciones**:
     - El endpoint responde con código 200
     - `hormigas_lote_id` se incluye en la respuesta
     - El estado es `en_proceso`

4. **`test_status_incluye_hormigas_lote_id`**
   - **Propósito**: Verifica que el endpoint de status incluye `hormigas_lote_id`.
   - **Validaciones**:
     - El endpoint responde con código 200
     - `hormigas_lote_id` está presente en la respuesta

---

## 🌱 Tests BDD (Behavior-Driven Development)

### Archivo: `features/recoleccion.feature`

#### Nuevos Escenarios Agregados:

1. **`Asignar hormigas con lote_id`** (`@unitario`)
   - **Given**: Tengo una tarea de recolección y hormigas disponibles
   - **When**: Asigno las hormigas con lote_id "LOTE_001"
   - **Then**: La tarea tiene las hormigas asignadas y el lote_id

2. **`Iniciar tarea automáticamente al asignar hormigas con lote_id`** (`@unitario`)
   - **Given**: Tengo una tarea y hormigas disponibles
   - **When**: Asigno hormigas con lote_id y hay suficientes
   - **Then**: La tarea se inicia automáticamente con el lote_id

3. **`Iniciar tarea con hormigas_lote_id`** (`@unitario`)
   - **Given**: Tengo una tarea con suficientes hormigas
   - **When**: Inicio la tarea con lote_id "LOTE_001"
   - **Then**: La tarea está en proceso con el lote_id asignado

4. **`Completar tarea automáticamente por tiempo transcurrido`** (`@integracion`)
   - **Given**: Tengo una tarea en proceso y ha transcurrido el tiempo completo
   - **When**: Verifico si debe completarse automáticamente
   - **Then**: La tarea se completa y el alimento se marca como no disponible

5. **`No completar tarea si no ha transcurrido el tiempo suficiente`** (`@integracion`)
   - **Given**: Tengo una tarea en proceso y solo ha transcurrido la mitad del tiempo
   - **When**: Verifico si debe completarse automáticamente
   - **Then**: La tarea permanece en proceso

6. **`Verificar status incluye hormigas_lote_id`** (`@integracion`)
   - **Given**: Tengo una tarea en proceso con lote_id
   - **When**: Consulto el status
   - **Then**: El status incluye el lote_id

---

### Archivo: `features/steps/recoleccion_steps.py`

#### Nuevos Steps Agregados:

1. **`@given("que tengo una tarea de recolección")`**
   - Crea una tarea de recolección para usar en los tests

2. **`@when('asigno las hormigas a la tarea con lote_id "{lote_id}"')`**
   - Asigna hormigas a la tarea y establece el lote_id

3. **`@then('la tarea debe tener el hormigas_lote_id "{lote_id}"')`**
   - Verifica que la tarea tiene el lote_id asignado

4. **`@given("la tarea tiene suficientes hormigas")`**
   - Verifica que la tarea tiene suficientes hormigas asignadas

5. **`@then("la tarea debe iniciarse automáticamente")`**
   - Verifica que la tarea se inició automáticamente

6. **`@when('inicio la tarea de recolección con lote_id "{lote_id}"')`**
   - Inicia la tarea con un lote_id específico

7. **`@given("ha transcurrido el tiempo de recolección completo")`**
   - Simula que ha transcurrido el tiempo completo de recolección

8. **`@when("verifico si la tarea debe completarse automáticamente")`**
   - Ejecuta la verificación de completado automático

9. **`@given("solo ha transcurrido la mitad del tiempo de recolección")`**
   - Simula que solo ha transcurrido la mitad del tiempo

10. **`@then("la tarea no debe tener fecha de finalización")`**
    - Verifica que la tarea no tiene fecha_fin

11. **`@then("la fecha de finalización debe ser fecha_inicio + tiempo_recoleccion")`**
    - Verifica que fecha_fin es correcta

12. **`@given('la tarea tiene hormigas_lote_id "{lote_id}"')`**
    - Establece el lote_id en la tarea

13. **`@when("consulto el status de la tarea")`**
    - Simula la consulta de status

14. **`@then('el status debe incluir el hormigas_lote_id "{lote_id}"')`**
    - Verifica que el status incluye el lote_id

---

## 🚀 Cómo Ejecutar los Tests

### Ejecutar Tests TDD

```bash
# Ejecutar todos los tests TDD
pytest tests/

# Ejecutar tests específicos del servicio
pytest tests/test_recoleccion_service.py -v

# Ejecutar tests específicos del controlador
pytest tests/test_api_controller.py -v

# Ejecutar con cobertura
pytest tests/ --cov=src --cov-report=html
```

### Ejecutar Tests BDD

```bash
# Ejecutar todos los tests BDD
behave features/

# Ejecutar un escenario específico
behave features/recoleccion.feature -n "Asignar hormigas con lote_id"

# Ejecutar con tags específicos
behave features/ --tags=@unitario
behave features/ --tags=@integracion
```

### Ejecutar Ambos

```bash
# Ejecutar TDD y BDD
pytest tests/ && behave features/
```

---

## 📊 Cobertura de Tests

### Funcionalidades Cubiertas

| Funcionalidad | TDD | BDD | Estado |
|--------------|-----|-----|--------|
| Asignación con lote_id | ✅ | ✅ | Completo |
| Inicio automático | ✅ | ✅ | Completo |
| Inicio con lote_id | ✅ | ✅ | Completo |
| Completado automático por tiempo | ✅ | ✅ | Completo |
| Validación alimento no disponible | ✅ | ✅ | Completo |
| Status con lote_id | ✅ | ✅ | Completo |
| Endpoint asignar-hormigas | ✅ | ✅ | Completo |

---

## 🔍 Validaciones Específicas

### Completado Automático por Tiempo

Los tests validan que:
- ✅ La tarea se completa cuando `tiempo_transcurrido >= tiempo_recoleccion`
- ✅ `fecha_fin` se calcula como `fecha_inicio + tiempo_recoleccion` (no `datetime.now()`)
- ✅ El alimento se marca como no disponible
- ✅ La tarea NO se completa si no ha transcurrido el tiempo suficiente
- ✅ Las tareas pendientes no se completan automáticamente

### Asignación e Inicio Automático

Los tests validan que:
- ✅ Si se asigna `hormigas_lote_id` y hay suficientes hormigas, la tarea se inicia automáticamente
- ✅ Si NO se asigna `hormigas_lote_id`, la tarea NO se inicia automáticamente
- ✅ El `hormigas_lote_id` se persiste correctamente en la tarea
- ✅ El `hormigas_lote_id` se incluye en las respuestas de status

### Validación de Alimentos

Los tests validan que:
- ✅ No se puede crear una tarea con un alimento no disponible
- ✅ Se lanza una excepción con mensaje claro
- ✅ El mensaje indica que el alimento está agotado

---

## 📝 Notas Importantes

1. **Mocks y Fixtures**: Los tests utilizan mocks para los servicios de entorno y comunicación, permitiendo pruebas aisladas.

2. **Asyncio**: Todos los tests que involucran operaciones asíncronas utilizan `@pytest.mark.asyncio`.

3. **Persistencia**: Los tests verifican que los cambios se persisten correctamente en la base de datos.

4. **Tolerancia de Tiempo**: Los tests de completado automático tienen una tolerancia de 1 segundo para comparaciones de tiempo.

5. **Estado de Tareas**: Los tests verifican que los estados de las tareas cambian correctamente según las operaciones realizadas.

---

## 🎯 Próximos Pasos

Para mantener la calidad de los tests:

1. **Ejecutar tests regularmente**: Después de cada cambio importante
2. **Mantener cobertura alta**: Objetivo > 80%
3. **Agregar tests para nuevas funcionalidades**: Seguir TDD/BDD
4. **Revisar y actualizar tests**: Cuando cambien los requisitos

---

**Última actualización:** 2024-01-15

