# Análisis de Líneas Sin Cobertura (Missing) en el Controlador de API

## Resumen Ejecutivo

El controlador de API (`recoleccion_controller.py`) tiene **224 líneas sin cubrir** de un total de 447 líneas, lo que representa una cobertura del **50%**. Este documento explica las razones principales por las que hay tantas líneas sin cubrir y propone estrategias para mejorar la cobertura.

## Razones Principales de Líneas Sin Cobertura

### 1. **Endpoints No Probados** (Líneas 160-162, 205-213, 223-247)

#### Health Check con Excepciones (160-162)
```python
except Exception as e:
    # En caso de error, devolver unhealthy pero no lanzar excepción
    return {
        "status": "unhealthy",
        "error": str(e)
    }
```
**Razón**: Los tests actuales no simulan excepciones en los servicios durante el health check.

#### Filtros de Estado en Alimentos (205-209)
```python
if estado:
    estado_l = estado.lower()
    if estado_l in ("disponible", "disponibles"):
        alimentos = [a for a in alimentos if a.disponible]
    elif estado_l in ("recolectado", "no_disponible"):
        alimentos = [a for a in alimentos if not a.disponible]
```
**Razón**: Los tests no prueban los filtros de estado (`estado=disponible`, `estado=recolectado`).

#### Crear Alimento (223-247)
```python
alimento = Alimento(
    id=payload.id or f"A{datetime.now().strftime('%Y%m%d%H%M%S')}",
    nombre=payload.nombre,
    ...
)
ok = await persistence_service.guardar_alimento(alimento)
if not ok:
    last_error = persistence_service.obtener_ultimo_error()
    ...
```
**Razón**: No hay tests para el endpoint POST `/alimentos` que crea nuevos alimentos.

### 2. **Casos de Error No Probados** (Líneas 212-213, 236-242, 246-247)

#### Excepciones en Consulta de Alimentos (212-213)
```python
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error al consultar alimentos: {str(e)}")
```
**Razón**: Los tests no simulan excepciones inesperadas en la consulta de alimentos.

#### Error al Guardar Alimento (236-242)
```python
if not ok:
    last_error = persistence_service.obtener_ultimo_error()
    detalle = f"No se pudo guardar el alimento en BD"
    if last_error:
        detalle = f"{detalle}: {last_error}"
    raise HTTPException(status_code=500, detail=detalle)
```
**Razón**: No se prueba el caso donde `guardar_alimento` retorna `False`.

### 3. **Ramas Condicionales No Ejecutadas** (Líneas 273-274, 276, 380-381, 387-400)

#### Generación Automática de IDs (273-276)
```python
if not tarea_id:
    from datetime import datetime
    tarea_id = f"tarea_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if not alimento_id:
    alimento_id = "A1"  # Usar A1 por defecto
```
**Razón**: Los tests siempre proporcionan `tarea_id` y `alimento_id`, nunca prueban la generación automática.

#### Cálculo Automático de Cantidad (380-381)
```python
if not cantidad:
    cantidad_necesaria = tarea.alimento.cantidad_hormigas_necesarias - len(tarea.hormigas_asignadas)
    cantidad_necesaria = max(0, cantidad_necesaria)
```
**Razón**: Los tests siempre proporcionan `cantidad`, nunca prueban el cálculo automático.

#### Ya Tiene Suficientes Hormigas (387-400)
```python
if cantidad_necesaria <= 0:
    if hormigas_lote_id:
        tarea.hormigas_lote_id = hormigas_lote_id
        await servicio_a_usar.iniciar_tarea_recoleccion(tarea, hormigas_lote_id)
        return {...}
    else:
        return {...}
```
**Razón**: No se prueba el caso donde la tarea ya tiene suficientes hormigas asignadas.

### 4. **Endpoints de Debug y Monitoreo** (Líneas 624-636, 645-685, 695-730, 742-775, 784-789)

#### Debug Info BD (624-636)
```python
@app.get("/debug/db", ...)
async def debug_info_bd():
    info_bd = await persistence_service.obtener_info_bd()
    alimentos = await persistence_service.obtener_alimentos()
    ...
```
**Razón**: Endpoints de debug no son probados en los tests unitarios.

#### Debug Tareas Raw (645-685)
```python
@app.get("/debug/tareas-raw", ...)
async def debug_tareas_raw():
    if not db.connection:
        return {"error": "No hay conexión a BD"}
    ...
```
**Razón**: Endpoints de debug interno no están cubiertos.

#### Obtener Tareas desde BD (695-730)
```python
@app.get("/tareas/bd", ...)
async def obtener_tareas_desde_bd():
    tareas = await persistence_service.obtener_tareas()
    ...
```
**Razón**: Endpoint alternativo para obtener tareas desde BD no está probado.

#### Obtener Tarea Específica desde BD (742-775)
```python
@app.get("/tareas/{tarea_id}/bd", ...)
async def obtener_tarea_desde_bd(tarea_id: str):
    tareas = await persistence_service.obtener_tareas()
    tarea = next((t for t in tareas if t.id == tarea_id), None)
    if not tarea:
        raise HTTPException(status_code=404, ...)
```
**Razón**: Endpoint alternativo no está cubierto.

#### Obtener Eventos (784-789)
```python
@app.get("/eventos", ...)
async def obtener_eventos():
    eventos = await persistence_service.obtener_eventos_recientes()
    ...
```
**Razón**: Endpoint de eventos no está probado.

### 5. **Status y Monitoreo Complejo** (Líneas 801-867, 892-930, 940-949)

#### Status de Todas las Tareas (801-867)
```python
@app.get("/tareas/status", ...)
async def obtener_status_todas_tareas():
    # Verificar y completar tareas automáticamente si es necesario
    tareas_completadas_auto = []
    for t in tareas:
        completada = await servicio_a_usar.verificar_y_completar_tarea_por_tiempo(tarea_a_verificar)
        if completada:
            tareas_completadas_auto.append(t.id)
    ...
```
**Razón**: Lógica compleja de completado automático no está probada.

#### Status de Tarea Específica (892-930, 940-949)
```python
@app.get("/tareas/{tarea_id}/status", ...)
async def obtener_status_tarea(tarea_id: str):
    # Búsqueda case-insensitive
    tarea = next((t for t in tareas if t.id.lower() == tarea_id.lower()), None)
    ...
    # Obtener hormigas_asignadas desde BD si no están en memoria
    if not tarea.hormigas_asignadas:
        ...
```
**Razón**: Lógica compleja de búsqueda y carga desde BD no está cubierta.

### 6. **Manejo de Errores Específicos** (Líneas 520-523, 541-544, 614-615)

#### ValueError al Iniciar (520-523)
```python
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
```
**Razón**: No se simula un `ValueError` al iniciar una tarea.

#### ValueError al Completar (541-544)
```python
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
```
**Razón**: No se simula un `ValueError` al completar una tarea.

#### Estadísticas sin BD (614-615)
```python
except Exception:
    # Si falla, devolver estadísticas básicas sin BD
    pass
```
**Razón**: No se prueba el caso donde falla la obtención de estadísticas desde BD.

### 7. **Endpoints de Tiempo y Progreso** (Líneas 1000-1019, 1036-1041, 1054-1059)

#### Tiempo Restante (1000-1019)
```python
@app.get("/tareas/{tarea_id}/tiempo-restante", ...)
async def obtener_tiempo_restante(tarea_id: str):
    tiempo = timer_service.get_tiempo_restante(tarea_id)
    if tiempo is None:
        raise HTTPException(status_code=404, ...)
```
**Razón**: Endpoints de tiempo restante no están probados.

#### Progreso (1036-1041)
```python
@app.get("/tareas/{tarea_id}/progreso", ...)
async def obtener_progreso(tarea_id: str):
    progreso = timer_service.get_progreso(tarea_id)
    if progreso is None:
        raise HTTPException(status_code=404, ...)
```
**Razón**: Endpoints de progreso no están probados.

#### Cancelar Tarea (1054-1059)
```python
@app.post("/tareas/{tarea_id}/cancelar", ...)
async def cancelar_tarea(tarea_id: str):
    cancelada = await timer_service.cancelar_tarea(tarea_id)
    if not cancelada:
        raise HTTPException(status_code=404, ...)
```
**Razón**: Endpoint de cancelar tarea no está probado.

## Estrategia para Mejorar la Cobertura

### Fase 1: Casos de Error Básicos
1. ✅ Health check con excepciones
2. ✅ Filtros de estado en alimentos
3. ✅ Crear alimento (éxito y error)
4. ✅ Excepciones en consulta de alimentos

### Fase 2: Ramas Condicionales
1. ✅ Generación automática de IDs
2. ✅ Cálculo automático de cantidad
3. ✅ Ya tiene suficientes hormigas (con y sin lote_id)

### Fase 3: Endpoints de Debug
1. ✅ Debug info BD
2. ✅ Debug tareas raw
3. ✅ Obtener tareas desde BD
4. ✅ Obtener tarea específica desde BD
5. ✅ Obtener eventos

### Fase 4: Status y Monitoreo
1. ✅ Status de todas las tareas
2. ✅ Status de tarea específica
3. ✅ Completado automático por tiempo
4. ✅ Carga de hormigas desde BD

### Fase 5: Endpoints de Tiempo
1. ✅ Tiempo restante
2. ✅ Progreso
3. ✅ Cancelar tarea

## Métricas Objetivo

- **Cobertura Actual**: 50% (223/447 líneas)
- **Cobertura Objetivo**: ≥80% (≥358/447 líneas)
- **Líneas a Cubrir**: ~135 líneas adicionales

## Conclusión

Las líneas sin cubrir se deben principalmente a:
1. **Endpoints no probados** (debug, monitoreo, tiempo)
2. **Casos de error no simulados** (excepciones, fallos de BD)
3. **Ramas condicionales no ejecutadas** (valores por defecto, cálculos automáticos)
4. **Lógica compleja no probada** (completado automático, búsqueda case-insensitive)

El archivo `test_api_cobertura_missing.py` contiene tests específicos para cubrir estas líneas faltantes.


