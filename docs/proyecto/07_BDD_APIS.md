# Estrategia BDD para APIs del Subsistema de Recolección

## 1. Introducción

Este documento describe la estrategia de Behavior-Driven Development (BDD) aplicada específicamente a las APIs REST del subsistema de Recolección de Alimentos. BDD permite describir el comportamiento esperado de las APIs en un lenguaje natural y legible.

## 2. Metodología BDD para APIs

### 2.1 Estructura de Escenarios BDD

Cada escenario BDD sigue el formato Given-When-Then:

- **Given**: Estado inicial del sistema
- **When**: Acción que se realiza (llamada a API)
- **Then**: Resultado esperado (respuesta de API)

### 2.2 Lenguaje Gherkin

Los escenarios se escriben en lenguaje Gherkin, que es legible tanto para desarrolladores como para stakeholders:

```gherkin
Feature: Gestión de Alimentos
  Como usuario del sistema
  Necesito poder consultar y crear alimentos
  Para gestionar los recursos disponibles

  Scenario: Consultar alimentos disponibles
    Given que hay alimentos disponibles en el sistema
    When consulto los alimentos disponibles mediante GET /alimentos
    Then debo recibir una lista de alimentos
    And cada alimento debe tener sus propiedades correctas
    And el código de respuesta debe ser 200
```

## 3. Escenarios BDD por Endpoint

### 3.1 Feature: Gestión de Alimentos

#### Escenario: Consultar alimentos disponibles exitosamente

```gherkin
Feature: Gestión de Alimentos
  Como encargado de recolección
  Necesito poder consultar alimentos disponibles
  Para crear tareas de recolección

  Scenario: Consultar alimentos disponibles exitosamente
    Given que hay alimentos disponibles en el entorno
    When realizo una petición GET a /alimentos
    Then debo recibir un código de respuesta 200
    And la respuesta debe ser una lista de alimentos
    And cada alimento debe tener:
      | campo                        | tipo     |
      | id                           | string   |
      | nombre                       | string   |
      | cantidad_hormigas_necesarias | integer  |
      | puntos_stock                 | integer  |
      | tiempo_recoleccion           | integer  |
      | disponible                   | boolean  |
```

#### Escenario: Consultar alimentos con filtro de estado

```gherkin
  Scenario: Consultar alimentos con filtro de estado disponible
    Given que hay alimentos disponibles y no disponibles en el sistema
    When realizo una petición GET a /alimentos?estado=disponible
    Then debo recibir un código de respuesta 200
    And la respuesta debe contener solo alimentos disponibles
    And todos los alimentos en la respuesta deben tener disponible=true
```

#### Escenario: Crear alimento exitosamente

```gherkin
  Scenario: Crear alimento exitosamente
    Given que tengo los datos de un nuevo alimento:
      | nombre                       | cantidad_hormigas_necesarias | puntos_stock | tiempo_recoleccion |
      | Nueva Fruta                  | 2                           | 5            | 180                |
    When realizo una petición POST a /alimentos con el cuerpo JSON:
      """
      {
        "nombre": "Nueva Fruta",
        "cantidad_hormigas_necesarias": 2,
        "puntos_stock": 5,
        "tiempo_recoleccion": 180
      }
      """
    Then debo recibir un código de respuesta 200
    And la respuesta debe contener el alimento creado
    And el alimento debe tener un ID generado automáticamente
    And el alimento debe estar disponible por defecto
```

#### Escenario: Error al crear alimento por fallo de persistencia

```gherkin
  Scenario: Error al crear alimento por fallo de persistencia
    Given que la base de datos no está disponible
    When realizo una petición POST a /alimentos con datos válidos
    Then debo recibir un código de respuesta 500
    And el mensaje de error debe indicar que no se pudo guardar el alimento
```

### 3.2 Feature: Gestión de Tareas

#### Escenario: Crear tarea de recolección exitosamente

```gherkin
Feature: Gestión de Tareas de Recolección
  Como encargado de recolección
  Necesito poder crear tareas de recolección
  Para organizar el trabajo de las hormigas

  Scenario: Crear tarea de recolección exitosamente
    Given que tengo un alimento disponible con ID "A1"
    When realizo una petición POST a /tareas con:
      | parámetro  | valor      |
      | tarea_id   | T1001      |
      | alimento_id| A1         |
    Then debo recibir un código de respuesta 200
    And la respuesta debe contener la tarea creada
    And la tarea debe tener estado "pendiente"
    And la tarea debe tener el alimento asignado
```

#### Escenario: Fallar al crear tarea con alimento no disponible

```gherkin
  Scenario: Fallar al crear tarea con alimento no disponible
    Given que tengo un alimento que no está disponible con ID "A2"
    When intento crear una tarea de recolección para ese alimento
    Then debo recibir un código de respuesta 400
    And el mensaje de error debe indicar que el alimento no está disponible
    And el mensaje debe mencionar que el alimento está agotado
```

#### Escenario: Fallar al crear tarea con alimento inexistente

```gherkin
  Scenario: Fallar al crear tarea con alimento inexistente
    Given que no existe un alimento con ID "ALIMENTO_INEXISTENTE"
    When intento crear una tarea de recolección para ese alimento
    Then debo recibir un código de respuesta 404
    And el mensaje de error debe indicar "Alimento no encontrado"
```

#### Escenario: Listar todas las tareas

```gherkin
  Scenario: Listar todas las tareas
    Given que hay tareas activas y completadas en el sistema
    When realizo una petición GET a /tareas
    Then debo recibir un código de respuesta 200
    And la respuesta debe ser una lista de tareas
    And la lista debe incluir tanto tareas activas como completadas
```

#### Escenario: Listar solo tareas activas

```gherkin
  Scenario: Listar solo tareas activas
    Given que hay tareas activas y completadas en el sistema
    When realizo una petición GET a /tareas/activas
    Then debo recibir un código de respuesta 200
    And la respuesta debe ser una lista de tareas
    And todas las tareas deben estar en estado "pendiente" o "en_proceso"
```

### 3.3 Feature: Asignación de Hormigas

#### Escenario: Asignar hormigas a tarea exitosamente

```gherkin
Feature: Asignación de Hormigas a Tareas
  Como encargado de recolección
  Necesito poder asignar hormigas a tareas
  Para que las hormigas puedan realizar el trabajo

  Scenario: Asignar hormigas a tarea exitosamente
    Given que tengo una tarea con ID "T1001" en estado "pendiente"
    And la tarea requiere 3 hormigas
    When realizo una petición POST a /tareas/T1001/asignar-hormigas con:
      | campo | valor |
      | cantidad | 3 |
    Then debo recibir un código de respuesta 200
    And la respuesta debe indicar que se asignaron 3 hormigas
    And la tarea debe tener 3 hormigas asignadas
    And la tarea debe seguir en estado "pendiente"
```

#### Escenario: Asignar hormigas con lote_id e inicio automático

```gherkin
  Scenario: Asignar hormigas con lote_id e inicio automático
    Given que tengo una tarea con ID "T1001" en estado "pendiente"
    And la tarea requiere 3 hormigas
    When realizo una petición POST a /tareas/T1001/asignar-hormigas con:
      | campo           | valor     |
      | hormigas_lote_id| LOTE_001  |
      | cantidad        | 3         |
    Then debo recibir un código de respuesta 200
    And la respuesta debe indicar que la tarea se inició automáticamente
    And la tarea debe tener estado "en_proceso"
    And la tarea debe tener el lote_id "LOTE_001" asignado
```

#### Escenario: Fallar al asignar hormigas con cantidad insuficiente

```gherkin
  Scenario: Fallar al asignar hormigas con cantidad insuficiente
    Given que tengo una tarea con ID "T1001" que requiere 3 hormigas
    And el servicio de comunicación no puede proporcionar hormigas
    When intento asignar hormigas a la tarea
    Then debo recibir un código de respuesta 400 o 500
    And el mensaje de error debe indicar que no se pudieron obtener hormigas
```

#### Escenario: Fallar al asignar hormigas a tarea inexistente

```gherkin
  Scenario: Fallar al asignar hormigas a tarea inexistente
    Given que no existe una tarea con ID "TAREA_INEXISTENTE"
    When intento asignar hormigas a esa tarea
    Then debo recibir un código de respuesta 404
    And el mensaje de error debe indicar "Tarea no encontrada"
```

### 3.4 Feature: Inicio de Tareas

#### Escenario: Iniciar tarea exitosamente

```gherkin
Feature: Inicio de Tareas de Recolección
  Como encargado de recolección
  Necesito poder iniciar tareas
  Para comenzar el proceso de recolección

  Scenario: Iniciar tarea exitosamente
    Given que tengo una tarea con ID "T1001" en estado "pendiente"
    And la tarea tiene 3 hormigas asignadas
    And la tarea requiere 3 hormigas
    When realizo una petición POST a /tareas/T1001/iniciar con:
      | campo           | valor     |
      | hormigas_lote_id| LOTE_001  |
    Then debo recibir un código de respuesta 200
    And la respuesta debe indicar que la tarea se inició exitosamente
    And la tarea debe tener estado "en_proceso"
    And la tarea debe tener fecha_inicio establecida
    And la tarea debe tener el lote_id "LOTE_001" asignado
```

#### Escenario: Fallar al iniciar tarea sin suficientes hormigas

```gherkin
  Scenario: Fallar al iniciar tarea sin suficientes hormigas
    Given que tengo una tarea con ID "T1001" en estado "pendiente"
    And la tarea requiere 3 hormigas
    And la tarea tiene 0 hormigas asignadas
    When intento iniciar la tarea
    Then debo recibir un código de respuesta 400
    And el mensaje de error debe indicar que no hay suficientes hormigas
    And el mensaje debe mostrar la cantidad requerida y la cantidad actual
```

#### Escenario: Fallar al iniciar tarea inexistente

```gherkin
  Scenario: Fallar al iniciar tarea inexistente
    Given que no existe una tarea con ID "TAREA_INEXISTENTE"
    When intento iniciar esa tarea
    Then debo recibir un código de respuesta 404
    And el mensaje de error debe indicar "Tarea no encontrada"
```

### 3.5 Feature: Completado de Tareas

#### Escenario: Completar tarea exitosamente

```gherkin
Feature: Completado de Tareas de Recolección
  Como encargado de recolección
  Necesito poder completar tareas
  Para finalizar el proceso de recolección

  Scenario: Completar tarea exitosamente
    Given que tengo una tarea con ID "T1001" en estado "en_proceso"
    And la tarea tiene fecha_inicio establecida
    When realizo una petición POST a /tareas/T1001/completar con:
      | parámetro            | valor |
      | cantidad_recolectada | 10    |
    Then debo recibir un código de respuesta 200
    And la respuesta debe indicar que la tarea se completó exitosamente
    And la tarea debe tener estado "completada"
    And la tarea debe tener fecha_fin establecida
    And la tarea debe tener cantidad_recolectada = 10
    And el alimento asociado debe estar marcado como no disponible
```

#### Escenario: Fallar al completar tarea inexistente

```gherkin
  Scenario: Fallar al completar tarea inexistente
    Given que no existe una tarea con ID "TAREA_INEXISTENTE"
    When intento completar esa tarea
    Then debo recibir un código de respuesta 404
    And el mensaje de error debe indicar "Tarea no encontrada"
```

### 3.6 Feature: Consulta de Status

#### Escenario: Obtener status de todas las tareas

```gherkin
Feature: Consulta de Status de Tareas
  Como encargado de recolección
  Necesito poder consultar el estado de las tareas
  Para monitorear el progreso del trabajo

  Scenario: Obtener status de todas las tareas
    Given que hay tareas activas y completadas en el sistema
    When realizo una petición GET a /tareas/status
    Then debo recibir un código de respuesta 200
    And la respuesta debe ser una lista de tareas con su status
    And cada tarea debe incluir:
      | campo              | tipo     |
      | id                  | string   |
      | estado              | string   |
      | hormigas_asignadas  | integer  |
      | hormigas_lote_id    | string   |
      | fecha_inicio        | datetime |
      | fecha_fin           | datetime |
```

#### Escenario: Obtener status de tarea específica

```gherkin
  Scenario: Obtener status de tarea específica
    Given que tengo una tarea con ID "T1001" en estado "en_proceso"
    And la tarea tiene lote_id "LOTE_001"
    When realizo una petición GET a /tareas/T1001/status
    Then debo recibir un código de respuesta 200
    And la respuesta debe contener el status de la tarea
    And el status debe incluir:
      | campo             | valor esperado |
      | id                 | T1001         |
      | estado             | en_proceso    |
      | hormigas_lote_id   | LOTE_001      |
      | hormigas_asignadas | 3             |
```

#### Escenario: Fallar al obtener status de tarea inexistente

```gherkin
  Scenario: Fallar al obtener status de tarea inexistente
    Given que no existe una tarea con ID "TAREA_INEXISTENTE"
    When intento obtener el status de esa tarea
    Then debo recibir un código de respuesta 404
    And el mensaje de error debe indicar "Tarea no encontrada"
```

## 4. Implementación de Steps BDD

### 4.1 Steps para Alimentos

```python
@given("que hay alimentos disponibles en el entorno")
def step_impl(context):
    """Configura alimentos disponibles en el mock."""
    context.alimentos = [
        Alimento(id="A1", nombre="Fruta", ...),
        Alimento(id="A2", nombre="Semilla", ...)
    ]
    context.mock_entorno_service.consultar_alimentos_disponibles.return_value = context.alimentos

@when("realizo una petición GET a /alimentos")
def step_impl(context):
    """Realiza petición GET a /alimentos."""
    context.response = context.client.get("/alimentos")

@then("debo recibir un código de respuesta {status_code:d}")
def step_impl(context, status_code):
    """Verifica el código de respuesta."""
    assert context.response.status_code == status_code

@then("la respuesta debe ser una lista de alimentos")
def step_impl(context):
    """Verifica que la respuesta sea una lista."""
    data = context.response.json()
    assert isinstance(data, list)
    assert len(data) > 0
```

### 4.2 Steps para Tareas

```python
@given("que tengo un alimento disponible con ID {alimento_id}")
def step_impl(context, alimento_id):
    """Configura un alimento disponible."""
    context.alimento = Alimento(id=alimento_id, nombre="Fruta", disponible=True, ...)
    context.mock_entorno_service.consultar_alimento_por_id.return_value = context.alimento

@when("realizo una petición POST a /tareas con:")
def step_impl(context):
    """Realiza petición POST a /tareas con parámetros de la tabla."""
    params = {}
    for row in context.table:
        params[row['parámetro']] = row['valor']
    context.response = context.client.post("/tareas", params=params)

@then("la tarea debe tener estado {estado}")
def step_impl(context, estado):
    """Verifica el estado de la tarea."""
    data = context.response.json()
    assert data["estado"] == estado
```

## 5. Ejecución de Tests BDD

### 5.1 Comando para Ejecutar

```bash
behave features/api_recoleccion.feature -v
```

### 5.2 Generar Reporte

```bash
behave features/api_recoleccion.feature -f html -o behave-report-api.html
```

## 6. Integración con TDD

Los escenarios BDD complementan los tests unitarios TDD:

- **TDD**: Pruebas técnicas de implementación
- **BDD**: Pruebas de comportamiento desde la perspectiva del usuario

Ambos enfoques trabajan juntos para garantizar:
- ✅ Funcionalidad correcta (TDD)
- ✅ Comportamiento esperado (BDD)
- ✅ Documentación viva (BDD)

## 7. Referencias

- Behave Documentation: https://behave.readthedocs.io/
- Gherkin Syntax: https://cucumber.io/docs/gherkin/
- BDD in Action (Smart, 2014)





