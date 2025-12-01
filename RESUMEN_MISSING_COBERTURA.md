# Resumen: ¿Por qué hay tantos "miss" en la cobertura?

## Respuesta Directa

Hay **224 líneas sin cubrir** (50% de cobertura) en el controlador de API porque:

### 1. **Endpoints No Probados** (~40 líneas)
- **POST `/alimentos`**: Crear alimento (líneas 223-247)
- **GET `/debug/db`**: Información de debug de BD (líneas 624-636)
- **GET `/debug/tareas-raw`**: Tareas en formato raw (líneas 645-685)
- **GET `/tareas/bd`**: Obtener tareas desde BD (líneas 695-730)
- **GET `/tareas/{id}/bd`**: Obtener tarea específica desde BD (líneas 742-775)
- **GET `/eventos`**: Obtener eventos recientes (líneas 784-789)
- **GET `/tareas/{id}/tiempo-restante`**: Tiempo restante (líneas 1000-1019)
- **GET `/tareas/{id}/progreso`**: Progreso de tarea (líneas 1036-1041)
- **POST `/tareas/{id}/cancelar`**: Cancelar tarea (líneas 1054-1059)

### 2. **Casos de Error No Simulados** (~30 líneas)
- Health check con excepciones (líneas 160-162)
- Error al consultar alimentos (líneas 212-213)
- Error al guardar alimento (líneas 236-242)
- Error general al crear alimento (líneas 246-247)
- Error al solicitar hormigas (líneas 414, 422)
- ValueError al iniciar/completar (líneas 520-523, 541-544)
- Error al obtener estadísticas (líneas 614-615)
- Errores en endpoints de debug (líneas 635-636, 682-685, 727-730, 774-775, 788-789)

### 3. **Ramas Condicionales No Ejecutadas** (~25 líneas)
- Generación automática de `tarea_id` (líneas 273-274)
- Uso de `A1` por defecto (línea 276)
- Cálculo automático de cantidad de hormigas (líneas 380-381)
- Ya tiene suficientes hormigas (líneas 387-400)
- Búsqueda case-insensitive (líneas 892-893, 899-900)

### 4. **Lógica Compleja de Status** (~60 líneas)
- Status de todas las tareas con completado automático (líneas 801-867)
- Status de tarea específica con recarga desde BD (líneas 892-930)
- Obtención de hormigas_asignadas desde BD (líneas 940-949)
- Debug de IDs disponibles (líneas 914-915)

### 5. **Endpoints de Listado Específicos** (~10 líneas)
- GET `/tareas/activas` (línea 317)
- GET `/tareas/en-proceso` (línea 327)

### 6. **Asignación de Hormigas Compleja** (~40 líneas)
- Asignar hormigas desde BD (líneas 361-366, 369)
- Asignar cuando ya tiene suficientes con lote_id (líneas 387-400)
- Error al iniciar automáticamente (líneas 434-437)
- Error general al asignar (líneas 448-456)
- Iniciar tarea desde BD (líneas 493-494)

### 7. **Procesamiento Completo** (~20 líneas)
- Procesar recolección con todas las tareas (líneas 560-586)
- Verificar hormigas muertas con error (líneas 989-990)

## Solución Implementada

Se creó el archivo `tests/test_api_cobertura_missing.py` con **más de 50 tests** específicos para cubrir estas líneas faltantes:

1. ✅ Tests para casos de error (excepciones, fallos de BD)
2. ✅ Tests para ramas condicionales (valores por defecto, cálculos automáticos)
3. ✅ Tests para endpoints de debug y monitoreo
4. ✅ Tests para lógica compleja de status
5. ✅ Tests para endpoints de tiempo y progreso
6. ✅ Tests para asignación de hormigas en todos los escenarios

## Próximos Pasos

1. Ejecutar los tests: `pytest tests/test_api_cobertura_missing.py -v`
2. Verificar cobertura: `pytest --cov=src/recoleccion/api --cov-report=term-missing`
3. Ajustar tests que fallen
4. Repetir hasta alcanzar ≥80% de cobertura

## Documentación Relacionada

- `docs/proyecto/ANALISIS_COBERTURA_MISSING.md`: Análisis detallado línea por línea
- `tests/test_api_cobertura_missing.py`: Tests específicos para cubrir líneas faltantes



