# 📋 Procesos de Pruebas del Sistema de Lotes de Hormigas

Este documento detalla todos los procesos (GET/POST) con sus respectivos bodies que se ejecutarán en las pruebas completas del sistema.

---

## 🔄 Flujo Completo de Pruebas

### PASO 1: Health Check

**Método:** `GET`  
**URL:** `http://localhost:8000/health`  
**Body:** `N/A`

**Response Esperado:**
```json
{
  "status": "healthy",
  "service": "subsistema-recoleccion",
  "version": "1.0.0",
  "entorno_disponible": true,
  "comunicacion_disponible": true
}
```

---

### PASO 2: Crear Alimento

**Método:** `POST`  
**URL:** `http://localhost:8000/alimentos`  
**Body:**
```json
{
  "nombre": "Fruta de Prueba",
  "cantidad_hormigas_necesarias": 3,
  "puntos_stock": 15,
  "tiempo_recoleccion": 10,
  "disponible": true
}
```

**Response Esperado:**
```json
{
  "id": "A20251119210356",
  "nombre": "Fruta de Prueba",
  "cantidad_hormigas_necesarias": 3,
  "puntos_stock": 15,
  "tiempo_recoleccion": 10,
  "disponible": true,
  "fecha_creacion": "2025-11-19T21:03:56.077786"
}
```

**Nota:** Guardar el `id` del alimento para el siguiente paso.

---

### PASO 3: Crear Tarea

**Método:** `POST`  
**URL:** `http://localhost:8000/tareas`  
**Body:**
```json
{
  "tarea_id": "TAREA_PRUEBA_20251119210357",
  "alimento_id": "A20251119210356"
}
```

**Response Esperado:**
```json
{
  "id": "TAREA_PRUEBA_20251119210357",
  "alimento": {
    "id": "A20251119210356",
    "nombre": "Fruta de Prueba",
    "cantidad_hormigas_necesarias": 3,
    "puntos_stock": 15,
    "tiempo_recoleccion": 10,
    "disponible": true
  },
  "hormigas_asignadas": [],
  "hormigas_lote_id": null,
  "estado": "pendiente",
  "fecha_inicio": null,
  "fecha_fin": null,
  "alimento_recolectado": 0
}
```

**Nota:** Guardar el `id` de la tarea para los siguientes pasos.

---

### PASO 4: Verificar Estado Inicial

**Método:** `GET`  
**URL:** `http://localhost:8000/tareas/TAREA_PRUEBA_20251119210357/status`  
**Body:** `N/A`

**Response Esperado:**
```json
{
  "base_datos": {
    "engine": "sqlserver",
    "server": "SHIRORYUU",
    "database": "Hormiguero"
  },
  "tarea_id": "TAREA_PRUEBA_20251119210357",
  "estado": "pendiente",
  "completada_automaticamente": false,
  "alimento": {
    "id": "A20251119210356",
    "nombre": "Fruta de Prueba"
  },
  "hormigas_lote_id": null,
  "inicio": null,
  "fin": null,
  "alimento_recolectado": 0
}
```

---

### PASO 5: Intentar Asignar Hormigas con Cantidad INSUFICIENTE (Debe Fallar)

**Método:** `POST`  
**URL:** `http://localhost:8000/tareas/TAREA_PRUEBA_20251119210357/asignar-hormigas`  
**Body:**
```json
{
  "hormigas_lote_id": "LOTE_PRUEBA_001",
  "cantidad": 2
}
```

**Response Esperado (Error 400):**
```json
{
  "detail": "El lote tiene cantidad insuficiente de hormigas. Enviadas: 2, Requeridas: 3"
}
```

**Validación:** Este paso DEBE fallar con status 400.

---

### PASO 6: Asignar Hormigas con Cantidad SUFICIENTE (Igual a Requerida)

**Método:** `POST`  
**URL:** `http://localhost:8000/tareas/TAREA_PRUEBA_20251119210357/asignar-hormigas`  
**Body:**
```json
{
  "hormigas_lote_id": "LOTE_PRUEBA_001",
  "cantidad": 3
}
```

**Response Esperado (Éxito 200):**
```json
{
  "message": "Se asignaron 3 hormigas a la tarea TAREA_PRUEBA_20251119210357",
  "tarea_id": "TAREA_PRUEBA_20251119210357",
  "hormigas_asignadas": 3,
  "hormigas_requeridas": 3,
  "hormigas_lote_id": "LOTE_PRUEBA_001",
  "estado": "pendiente",
  "iniciada": false
}
```

**Nota:** Si `iniciada: true`, la tarea se inició automáticamente y se puede saltar el paso 8.

---

### PASO 7: Verificar Estado Después de Asignación

**Método:** `GET`  
**URL:** `http://localhost:8000/tareas/TAREA_PRUEBA_20251119210357/status`  
**Body:** `N/A`

**Response Esperado:**
```json
{
  "base_datos": {
    "engine": "sqlserver",
    "server": "SHIRORYUU",
    "database": "Hormiguero"
  },
  "tarea_id": "TAREA_PRUEBA_20251119210357",
  "estado": "pendiente",
  "completada_automaticamente": false,
  "alimento": {
    "id": "A20251119210356",
    "nombre": "Fruta de Prueba"
  },
  "hormigas_lote_id": "LOTE_PRUEBA_001",
  "inicio": null,
  "fin": null,
  "alimento_recolectado": 0
}
```

**Validación:** Verificar que `hormigas_lote_id` esté presente.

---

### PASO 8: Iniciar la Tarea (Si no se inició automáticamente)

**Método:** `POST`  
**URL:** `http://localhost:8000/tareas/TAREA_PRUEBA_20251119210357/iniciar`  
**Body:**
```json
{
  "hormigas_lote_id": "LOTE_PRUEBA_001"
}
```

**Response Esperado (Éxito 200):**
```json
{
  "message": "Tarea TAREA_PRUEBA_20251119210357 iniciada exitosamente",
  "tarea_id": "TAREA_PRUEBA_20251119210357",
  "estado": "en_proceso",
  "hormigas_asignadas": 3,
  "hormigas_lote_id": "LOTE_PRUEBA_001"
}
```

**Nota:** Si la tarea ya estaba iniciada, puede retornar error 400.

---

### PASO 9: Verificar Tiempo Restante

**Método:** `GET`  
**URL:** `http://localhost:8000/tareas/TAREA_PRUEBA_20251119210357/tiempo-restante`  
**Body:** `N/A`

**Response Esperado:**
```json
{
  "tarea_id": "TAREA_PRUEBA_20251119210357",
  "tiempo_total_asignado_segundos": 10,
  "tiempo_total_asignado_minutos": 0.17,
  "tiempo_restante_segundos": 9,
  "tiempo_restante_minutos": 0.15,
  "tiempo_transcurrido_segundos": 1,
  "progreso_porcentaje": 10.0
}
```

---

### PASO 10: Esperar y Verificar Completado Automático

**Espera:** 12 segundos (10 segundos de recolección + 2 de margen)

**Método:** `GET`  
**URL:** `http://localhost:8000/tareas/TAREA_PRUEBA_20251119210357/status`  
**Body:** `N/A`

**Response Esperado (Tarea Completada):**
```json
{
  "base_datos": {
    "engine": "sqlserver",
    "server": "SHIRORYUU",
    "database": "Hormiguero"
  },
  "tarea_id": "TAREA_PRUEBA_20251119210357",
  "estado": "completada",
  "completada_automaticamente": true,
  "alimento": {
    "id": "A20251119210356",
    "nombre": "Fruta de Prueba"
  },
  "hormigas_lote_id": "LOTE_PRUEBA_001",
  "inicio": "2025-11-19T21:04:00",
  "fin": "2025-11-19T21:04:10",
  "alimento_recolectado": 0
}
```

**Validación:** 
- `estado` debe ser `"completada"`
- `completada_automaticamente` debe ser `true`
- `fin` debe ser `inicio + tiempo_recoleccion` (10 segundos)

---

### PASO 11: Verificar Todas las Tareas

**Método:** `GET`  
**URL:** `http://localhost:8000/tareas/status`  
**Body:** `N/A`

**Response Esperado:**
```json
{
  "base_datos": {
    "engine": "sqlserver",
    "server": "SHIRORYUU",
    "database": "Hormiguero"
  },
  "total_tareas": 1,
  "tareas_completadas_automaticamente": 1,
  "tareas": [
    {
      "tarea_id": "TAREA_PRUEBA_20251119210357",
      "estado": "completada",
      "alimento": {
        "id": "A20251119210356",
        "nombre": "Fruta de Prueba"
      },
      "hormigas_lote_id": "LOTE_PRUEBA_001",
      "inicio": "2025-11-19T21:04:00",
      "fin": "2025-11-19T21:04:10",
      "alimento_recolectado": 0
    }
  ]
}
```

---

### PASO 12: Verificar Estadísticas

**Método:** `GET`  
**URL:** `http://localhost:8000/estadisticas`  
**Body:** `N/A`

**Response Esperado:**
```json
{
  "tareas_activas": 0,
  "tareas_completadas": 1,
  "total_alimentos_recolectados": 0,
  "base_datos": {
    "total_alimentos": 2,
    "total_tareas": 1
  },
  "tareas_memoria": {
    "activas": 0,
    "completadas": 1
  }
}
```

---

## 📊 Resumen de Validaciones

### Validaciones de Cantidad

1. ✅ **Cantidad Insuficiente (Paso 5):**
   - Enviadas: 2
   - Requeridas: 3
   - **Resultado Esperado:** Error 400 con mensaje descriptivo

2. ✅ **Cantidad Suficiente (Paso 6):**
   - Enviadas: 3
   - Requeridas: 3
   - **Resultado Esperado:** Éxito 200, lote creado y aceptado

### Validaciones de Lote

1. ✅ **Lote Creado:** El lote se crea en la tabla `lotes_hormigas`
2. ✅ **Lote Aceptado:** El lote cambia de estado `pendiente` a `aceptado`
3. ✅ **Lote en Uso:** Al iniciar la tarea, el lote se marca como `en_uso`
4. ✅ **Hormigas Guardadas:** Las hormigas se guardan en `asignaciones_hormiga_tarea` con `lote_id`

### Validaciones de Tarea

1. ✅ **Estado Inicial:** `pendiente`
2. ✅ **Después de Asignar:** `pendiente` (o `en_proceso` si se inició automáticamente)
3. ✅ **Después de Iniciar:** `en_proceso`
4. ✅ **Después de Completar:** `completada` con `completada_automaticamente: true`

---

## 🚀 Ejecutar Pruebas

### Opción 1: Script Automático

```bash
python scripts/prueba_completa_sistema_lotes.py
```

### Opción 2: Manual con cURL

```bash
# Paso 1: Health Check
curl -X GET "http://localhost:8000/health"

# Paso 2: Crear Alimento
curl -X POST "http://localhost:8000/alimentos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Fruta de Prueba",
    "cantidad_hormigas_necesarias": 3,
    "puntos_stock": 15,
    "tiempo_recoleccion": 10,
    "disponible": true
  }'

# Paso 3: Crear Tarea (usar el ID del alimento del paso 2)
curl -X POST "http://localhost:8000/tareas" \
  -H "Content-Type: application/json" \
  -d '{
    "tarea_id": "TAREA_PRUEBA_001",
    "alimento_id": "A20251119210356"
  }'

# ... continuar con los demás pasos
```

### Opción 3: PowerShell

```powershell
# Paso 1: Health Check
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET

# Paso 2: Crear Alimento
$body = @{
    nombre = "Fruta de Prueba"
    cantidad_hormigas_necesarias = 3
    puntos_stock = 15
    tiempo_recoleccion = 10
    disponible = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/alimentos" -Method POST -Body $body -ContentType "application/json"

# ... continuar con los demás pasos
```

---

## 📝 Notas Importantes

1. **IDs Dinámicos:** Los IDs de alimento y tarea se generan automáticamente. Usar los IDs de las respuestas para los siguientes pasos.

2. **Tiempo de Espera:** El paso 10 requiere esperar 12 segundos para que la tarea se complete automáticamente.

3. **Validación de Lote:** El sistema valida que:
   - La cantidad enviada sea >= cantidad requerida
   - El lote no esté en uso
   - El lote exista antes de usarlo

4. **Base de Datos:** Asegurarse de que las tablas `lotes_hormigas` y `asignaciones_hormiga_tarea` (con columna `lote_id`) existan en la base de datos.

---

**Última actualización:** 2024-01-15

