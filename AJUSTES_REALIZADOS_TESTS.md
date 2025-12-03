# Ajustes Realizados en los Tests de Cobertura

## Correcciones Aplicadas

### 1. Patch de persistence_service
- **Problema**: El `persistence_service` se importa dentro de las funciones del controlador
- **Solución**: Cambiado el patch de `src.recoleccion.services.persistence_service.persistence_service` a `src.recoleccion.api.recoleccion_controller.persistence_service`

### 2. Mocks Async
- **Problema**: Los métodos async necesitan ser mockeados con `AsyncMock`, no con `.return_value` directamente
- **Solución**: Cambiado todos los mocks de métodos async para usar `AsyncMock`:
  - `mock_entorno_service.is_disponible = AsyncMock(return_value=True)`
  - `mock_comunicacion_service.solicitar_hormigas = AsyncMock(return_value="mensaje_001")`
  - `mock_comunicacion_service.consultar_respuesta_hormigas = AsyncMock(return_value=[...])`

### 3. Tests que requieren app.state
- **Problema**: Algunos endpoints usan `app.state.recoleccion_service`
- **Solución**: Los tests crean una nueva app y configuran `app.state.recoleccion_service` antes de usar `TestClient`

### 4. Test de procesar recolección
- **Problema**: Necesita configurar `app.state.recoleccion_service` y usar `TestClient` con la app configurada
- **Solución**: Ajustado para crear la app, configurar el servicio y usar `TestClient` con la app

## Estado Actual

- ✅ Todos los patches corregidos
- ✅ Todos los mocks async corregidos
- ✅ Tests que requieren app.state configurados correctamente
- ⏳ Pendiente: Ejecutar tests y verificar que funcionan

## Próximos Pasos

1. Ejecutar los tests: `pytest tests/test_api_cobertura_missing.py -v`
2. Revisar errores que puedan quedar
3. Ajustar según sea necesario
4. Verificar cobertura final




