# Estrategia TDD para APIs del Subsistema de Recolección

## 1. Introducción

Este documento describe la estrategia de Test-Driven Development (TDD) aplicada específicamente a las APIs REST del subsistema de Recolección de Alimentos. La metodología TDD garantiza que cada endpoint esté completamente probado antes de su implementación final.

## 2. Metodología TDD para APIs

### 2.1 Ciclo Rojo-Verde-Refactor para APIs

El desarrollo de cada endpoint sigue el ciclo TDD:

1. **🔴 Rojo**: Escribir test que falle
   - Definir el comportamiento esperado del endpoint
   - Escribir test con `TestClient` de FastAPI
   - Verificar que el test falle (endpoint no existe o no funciona)

2. **🟢 Verde**: Implementar código mínimo para que pase
   - Implementar el endpoint con la funcionalidad mínima
   - Verificar que el test pase
   - Asegurar que el endpoint responda correctamente

3. **🔵 Refactor**: Mejorar código manteniendo tests pasando
   - Mejorar la implementación del endpoint
   - Agregar validaciones y manejo de errores
   - Optimizar código manteniendo todos los tests pasando

### 2.2 Estructura de Tests para APIs

Cada test de API debe incluir:

- **Arrange**: Configurar mocks y datos de prueba
- **Act**: Realizar la petición HTTP al endpoint
- **Assert**: Verificar la respuesta (status code, body, headers)

## 3. Propuesta de Tests para Endpoints

### 3.1 Endpoints de Salud y Estado

#### GET `/health`

**Propuesta de Test**:

```python
def test_health_check_success(client, mock_entorno_service, mock_comunicacion_service):
    """Prueba el endpoint de salud cuando ambos servicios están disponibles."""
    # Arrange
    mock_entorno_service.is_disponible.return_value = True
    mock_comunicacion_service.is_disponible.return_value = True
    
    # Act
    response = client.get("/health")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["entorno_disponible"] is True
    assert data["comunicacion_disponible"] is True
```

**Ciclo TDD**:
1. 🔴 **Rojo**: Test escrito, endpoint no existe → falla
2. 🟢 **Verde**: Implementar endpoint básico → test pasa
3. 🔵 **Refactor**: Agregar validaciones y manejo de errores

#### GET `/`

**Propuesta de Test**:

```python
def test_root_endpoint(client):
    """Prueba el endpoint raíz."""
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Subsistema de Recolección" in data["message"]
```

### 3.2 Endpoints de Alimentos

#### GET `/alimentos`

**Propuesta de Tests**:

```python
def test_consultar_alimentos_success(client, mock_entorno_service, alimento_ejemplo):
    """Prueba la consulta exitosa de alimentos."""
    # Arrange
    mock_entorno_service.is_disponible.return_value = True
    mock_entorno_service.consultar_alimentos_disponibles.return_value = [alimento_ejemplo]
    
    # Act
    response = client.get("/alimentos")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "alimento_001"
    assert data[0]["nombre"] == "Fruta"

def test_consultar_alimentos_con_filtro_disponible(client, mock_entorno_service):
    """Prueba la consulta de alimentos con filtro de estado disponible."""
    # Arrange
    alimento_disponible = Alimento(id="A1", nombre="Fruta", ...)
    alimento_no_disponible = Alimento(id="A2", nombre="Semilla", disponible=False, ...)
    
    mock_entorno_service.is_disponible.return_value = False
    mock_persistence.obtener_alimentos.return_value = [
        alimento_disponible, alimento_no_disponible
    ]
    
    # Act
    response = client.get("/alimentos?estado=disponible")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "A1"
    assert data[0]["disponible"] is True
```

**Ciclo TDD**:
1. 🔴 **Rojo**: Test escrito, endpoint no filtra → falla
2. 🟢 **Verde**: Implementar filtrado básico → test pasa
3. 🔵 **Refactor**: Mejorar lógica de filtrado y agregar más casos

#### POST `/alimentos`

**Propuesta de Tests**:

```python
def test_crear_alimento_success(client, mock_entorno_service, mock_comunicacion_service):
    """Prueba la creación exitosa de un alimento."""
    # Arrange
    with patch('persistence_service') as mock_persistence:
        mock_persistence.guardar_alimento.return_value = True
        
        # Act
        response = client.post("/alimentos", json={
            "nombre": "Nueva Fruta",
            "cantidad_hormigas_necesarias": 2,
            "puntos_stock": 5,
            "tiempo_recoleccion": 180
        })
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Nueva Fruta"
        assert data["cantidad_hormigas_necesarias"] == 2

def test_crear_alimento_error_persistencia(client, mock_entorno_service, mock_comunicacion_service):
    """Prueba la creación de alimento cuando falla la persistencia."""
    # Arrange
    with patch('persistence_service') as mock_persistence:
        mock_persistence.guardar_alimento.return_value = False
        mock_persistence.obtener_ultimo_error.return_value = "Error de BD"
        
        # Act
        response = client.post("/alimentos", json={
            "nombre": "Fruta",
            "cantidad_hormigas_necesarias": 2,
            "puntos_stock": 5,
            "tiempo_recoleccion": 180
        })
        
        # Assert
        assert response.status_code == 500
        data = response.json()
        assert "No se pudo guardar" in data["detail"]
```

### 3.3 Endpoints de Tareas

#### POST `/tareas`

**Propuesta de Tests**:

```python
def test_crear_tarea_success(client, mock_entorno_service, alimento_ejemplo):
    """Prueba la creación exitosa de una tarea."""
    # Arrange
    mock_entorno_service.consultar_alimento_por_id.return_value = alimento_ejemplo
    
    # Act
    response = client.post("/tareas", params={
        "tarea_id": "tarea_001",
        "alimento_id": "alimento_001"
    })
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "tarea_001"
    assert data["alimento"]["id"] == "alimento_001"

def test_crear_tarea_alimento_not_found(client, mock_entorno_service):
    """Prueba la creación de tarea cuando el alimento no existe."""
    # Arrange
    mock_entorno_service.consultar_alimento_por_id.return_value = None
    
    # Act
    response = client.post("/tareas", params={
        "tarea_id": "tarea_001",
        "alimento_id": "alimento_inexistente"
    })
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Alimento no encontrado" in data["detail"]

def test_crear_tarea_con_alimento_no_disponible(client, mock_entorno_service):
    """Prueba que no se puede crear una tarea con un alimento no disponible."""
    # Arrange
    alimento_no_disponible = Alimento(..., disponible=False)
    mock_entorno_service.consultar_alimento_por_id.return_value = alimento_no_disponible
    
    # Act
    response = client.post("/tareas", json={
        "tarea_id": "T1001",
        "alimento_id": "alimento_002"
    })
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "no está disponible" in data["detail"].lower()
```

#### GET `/tareas`

**Propuesta de Tests**:

```python
def test_listar_tareas(client, mock_entorno_service, mock_comunicacion_service):
    """Prueba el listado de todas las tareas."""
    # Arrange
    app = create_app(mock_entorno_service, mock_comunicacion_service)
    app.state.tareas_activas = []
    app.state.tareas_completadas = []
    
    # Act
    response = client.get("/tareas")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_listar_tareas_activas(client, mock_entorno_service, mock_comunicacion_service, tarea_ejemplo):
    """Prueba el listado de tareas activas."""
    # Arrange
    recoleccion_service = RecoleccionService(...)
    recoleccion_service.tareas_activas.append(tarea_ejemplo)
    
    app = create_app(...)
    app.state.recoleccion_service = recoleccion_service
    
    # Act
    response = client.get("/tareas/activas")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
```

#### POST `/tareas/{tarea_id}/asignar-hormigas`

**Propuesta de Tests**:

```python
def test_asignar_hormigas_con_lote_id_e_inicio_automatico(
    client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo
):
    """Prueba la asignación de hormigas con lote_id que inicia automáticamente la tarea."""
    # Arrange
    recoleccion_service = RecoleccionService(...)
    tarea = TareaRecoleccion(id="tarea_001", alimento=alimento_ejemplo)
    recoleccion_service.tareas_activas.append(tarea)
    
    mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
    mock_comunicacion_service.consultar_respuesta_hormigas.return_value = [hormiga_ejemplo] * 3
    
    app = create_app(...)
    app.state.recoleccion_service = recoleccion_service
    
    # Act
    response = client.post(
        "/tareas/tarea_001/asignar-hormigas",
        json={
            "hormigas_lote_id": "LOTE_001",
            "cantidad": 3
        }
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["iniciada"] is True
    assert data["hormigas_lote_id"] == "LOTE_001"
    assert data["estado"] == "en_proceso"

def test_asignar_hormigas_cantidad_insuficiente(
    client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo
):
    """Prueba la asignación de hormigas con cantidad insuficiente."""
    # Arrange
    recoleccion_service = RecoleccionService(...)
    tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
    recoleccion_service.tareas_activas.append(tarea)
    
    mock_comunicacion_service.consultar_respuesta_hormigas.return_value = []  # Sin hormigas
    
    # Act
    response = client.post(
        "/tareas/T1/asignar-hormigas",
        json={"cantidad": 3}
    )
    
    # Assert
    assert response.status_code in [400, 500]
```

#### POST `/tareas/{tarea_id}/iniciar`

**Propuesta de Tests**:

```python
def test_iniciar_tarea_success(
    client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo
):
    """Prueba el inicio exitoso de una tarea."""
    # Arrange
    recoleccion_service = RecoleccionService(...)
    tarea = TareaRecoleccion(id="tarea_001", alimento=alimento_ejemplo)
    tarea.hormigas_asignadas = [hormiga_ejemplo] * 3
    recoleccion_service.tareas_activas.append(tarea)
    
    app = create_app(...)
    app.state.recoleccion_service = recoleccion_service
    
    # Act
    response = client.post(
        "/tareas/tarea_001/iniciar",
        json={"hormigas_lote_id": "LOTE_001"}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["hormigas_lote_id"] == "LOTE_001"
    assert data["estado"] == "en_proceso"

def test_iniciar_tarea_sin_hormigas_suficientes(
    client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo
):
    """Prueba iniciar tarea sin suficientes hormigas."""
    # Arrange
    recoleccion_service = RecoleccionService(...)
    tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
    # No asignar hormigas (requiere 3, tiene 0)
    recoleccion_service.tareas_activas.append(tarea)
    
    # Act
    response = client.post(
        "/tareas/T1/iniciar",
        json={"hormigas_lote_id": "LOTE_001"}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "suficientes hormigas" in data["detail"].lower()
```

#### POST `/tareas/{tarea_id}/completar`

**Propuesta de Tests**:

```python
def test_completar_tarea_success(
    client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo
):
    """Prueba la finalización exitosa de una tarea."""
    # Arrange
    recoleccion_service = RecoleccionService(...)
    tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
    tarea.hormigas_asignadas = [hormiga_ejemplo] * 3
    tarea.estado = EstadoTarea.EN_PROCESO
    tarea.fecha_inicio = datetime.now()
    recoleccion_service.tareas_activas.append(tarea)
    
    with patch('persistence_service') as mock_persistence:
        mock_persistence.guardar_tarea.return_value = True
        mock_persistence.actualizar_alimento_disponibilidad.return_value = True
        
        # Act
        response = client.post(
            "/tareas/T1/completar",
            params={"cantidad_recolectada": 10}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "completada"

def test_completar_tarea_not_found(client, mock_entorno_service, mock_comunicacion_service):
    """Prueba completar una tarea que no existe."""
    # Act
    response = client.post(
        "/tareas/TAREA_INEXISTENTE/completar",
        params={"cantidad_recolectada": 10}
    )
    
    # Assert
    assert response.status_code == 404
```

### 3.4 Endpoints de Status y Monitoreo

#### GET `/tareas/status`

**Propuesta de Tests**:

```python
def test_obtener_status_todas_tareas(
    client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo
):
    """Prueba obtener el status de todas las tareas."""
    # Arrange
    recoleccion_service = RecoleccionService(...)
    tarea1 = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
    tarea2 = TareaRecoleccion(id="T2", alimento=alimento_ejemplo)
    recoleccion_service.tareas_activas.append(tarea1)
    recoleccion_service.tareas_completadas.append(tarea2)
    
    app = create_app(...)
    app.state.recoleccion_service = recoleccion_service
    
    # Act
    response = client.get("/tareas/status")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_obtener_status_tarea_especifica(
    client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo
):
    """Prueba obtener el status de una tarea específica."""
    # Arrange
    recoleccion_service = RecoleccionService(...)
    tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
    tarea.hormigas_asignadas = [hormiga_ejemplo] * 3
    tarea.hormigas_lote_id = "LOTE_001"
    tarea.estado = EstadoTarea.EN_PROCESO
    tarea.fecha_inicio = datetime.now()
    recoleccion_service.tareas_activas.append(tarea)
    
    # Act
    response = client.get("/tareas/T1/status")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "T1"
    assert data["hormigas_lote_id"] == "LOTE_001"
    assert data["estado"] == "en_proceso"
```

## 4. Casos de Prueba por Categoría

### 4.1 Casos Nominales (Happy Path)

- ✅ Crear alimento exitosamente
- ✅ Consultar alimentos disponibles
- ✅ Crear tarea exitosamente
- ✅ Asignar hormigas exitosamente
- ✅ Iniciar tarea exitosamente
- ✅ Completar tarea exitosamente
- ✅ Obtener status de tareas

### 4.2 Casos de Límite

- ✅ Crear tarea sin proporcionar `tarea_id` (genera automáticamente)
- ✅ Crear tarea sin proporcionar `alimento_id` (usa A1 por defecto)
- ✅ Asignar hormigas cuando ya tiene suficientes
- ✅ Iniciar tarea que ya está en proceso
- ✅ Completar tarea que no está en proceso

### 4.3 Casos Negativos (Error Handling)

- ✅ Crear tarea con alimento inexistente (404)
- ✅ Crear tarea con alimento no disponible (400)
- ✅ Asignar hormigas a tarea inexistente (404)
- ✅ Asignar hormigas con cantidad insuficiente (400)
- ✅ Iniciar tarea sin suficientes hormigas (400)
- ✅ Iniciar tarea inexistente (404)
- ✅ Completar tarea inexistente (404)
- ✅ Error de persistencia al crear alimento (500)
- ✅ Error de conexión al servicio de entorno (500)

## 5. Estrategia de Cobertura

### 5.1 Objetivo de Cobertura

- **Cobertura de Líneas**: ≥ 80%
- **Cobertura de Ramas**: Todas las ramas if/else cubiertas
- **Cobertura de Endpoints**: 100% de endpoints probados

### 5.2 Métricas Actuales

- **Cobertura Actual**: 50% (mejorable)
- **Endpoints Cubiertos**: 15/25 endpoints
- **Tests Existentes**: 25 tests
- **Tests Necesarios**: ~40 tests (estimado)

### 5.3 Plan de Mejora

1. **Fase 1**: Agregar tests para endpoints faltantes
   - Endpoints de debug
   - Endpoints de estadísticas
   - Endpoints de filtrado

2. **Fase 2**: Agregar tests para casos de error
   - Manejo de excepciones
   - Validaciones de entrada
   - Errores de persistencia

3. **Fase 3**: Agregar tests para casos límite
   - Valores nulos
   - Valores vacíos
   - Valores extremos

## 6. Herramientas y Configuración

### 6.1 Herramientas Utilizadas

- **pytest**: Framework de testing
- **FastAPI TestClient**: Cliente de prueba para APIs
- **unittest.mock**: Mocking de dependencias
- **pytest-cov**: Medición de cobertura

### 6.2 Configuración

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = 
    --cov=src/recoleccion/api
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

## 7. Evidencia de TDD

### 7.1 Commits de TDD

Los commits muestran el ciclo TDD:

```
commit abc123 - test: agregar test para endpoint POST /alimentos
commit def456 - feat: implementar endpoint POST /alimentos
commit ghi789 - refactor: mejorar validaciones en POST /alimentos
```

### 7.2 Ejemplos de Ciclos Completos

**Ejemplo 1: Endpoint POST /tareas**

1. 🔴 **Rojo**: `test_crear_tarea_success` escrito → falla (endpoint no existe)
2. 🟢 **Verde**: Implementar endpoint básico → test pasa
3. 🔵 **Refactor**: Agregar validaciones y manejo de errores

**Ejemplo 2: Endpoint POST /tareas/{id}/asignar-hormigas**

1. 🔴 **Rojo**: `test_asignar_hormigas_con_lote_id` escrito → falla
2. 🟢 **Verde**: Implementar asignación básica → test pasa
3. 🔵 **Refactor**: Agregar inicio automático con lote_id

## 8. Referencias

- FastAPI Testing: https://fastapi.tiangolo.com/tutorial/testing/
- Pytest Documentation: https://docs.pytest.org/
- Test-Driven Development: By Example (Beck, 2003)





