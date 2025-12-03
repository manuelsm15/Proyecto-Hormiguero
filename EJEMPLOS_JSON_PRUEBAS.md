# Ejemplos JSON para Pruebas de API - Subsistema Recolección

## 📋 Tabla de Contenidos
1. [POST - Crear Alimento](#post---crear-alimento)
2. [GET - Listar Alimentos](#get---listar-alimentos)
3. [POST - Crear Tarea](#post---crear-tarea)
4. [GET - Listar Tareas](#get---listar-tareas)
5. [POST - Asignar Hormigas a Tarea](#post---asignar-hormigas-a-tarea)
6. [POST - Iniciar Tarea](#post---iniciar-tarea)
7. [GET - Status de Tareas](#get---status-de-tareas)
8. [POST - Completar Tarea](#post---completar-tarea)
9. [GET - Health Check](#get---health-check)
10. [GET - Estadísticas](#get---estadísticas)

---

## POST - Crear Alimento

**Endpoint:** `POST http://localhost:8000/alimentos`

**Body JSON:**
```json
{
  "id": "A1",
  "nombre": "Semillas de girasol",
  "cantidad_hormigas_necesarias": 3,
  "puntos_stock": 50,
  "tiempo_recoleccion": 120,
  "disponible": true
}
```

**Ejemplo con curl:**
```bash
curl -X POST "http://localhost:8000/alimentos" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "A1",
    "nombre": "Semillas de girasol",
    "cantidad_hormigas_necesarias": 3,
    "puntos_stock": 50,
    "tiempo_recoleccion": 120,
    "disponible": true
  }'
```

**Más ejemplos de alimentos:**
```json
{
  "id": "A2",
  "nombre": "Hojas frescas",
  "cantidad_hormigas_necesarias": 2,
  "puntos_stock": 30,
  "tiempo_recoleccion": 90,
  "disponible": true
}
```

```json
{
  "id": "A3",
  "nombre": "Frutos secos",
  "cantidad_hormigas_necesarias": 5,
  "puntos_stock": 80,
  "tiempo_recoleccion": 180,
  "disponible": true
}
```

---

## GET - Listar Alimentos

**Endpoint:** `GET http://localhost:8000/alimentos`

**Ejemplo con curl:**
```bash
curl "http://localhost:8000/alimentos"
```

**Con filtro por estado:**
```bash
curl "http://localhost:8000/alimentos?estado=disponible"
```

**Respuesta esperada:**
```json
[
  {
    "id": "A1",
    "nombre": "Semillas de girasol",
    "cantidad_hormigas_necesarias": 3,
    "puntos_stock": 50,
    "tiempo_recoleccion": 120,
    "disponible": true,
    "fecha_creacion": "2024-01-15T10:00:00"
  }
]
```

---

## POST - Crear Tarea

**Endpoint:** `POST http://localhost:8000/tareas`

**Opción 1: Con query parameters**
```bash
curl -X POST "http://localhost:8000/tareas?tarea_id=T1001&alimento_id=A1"
```

**Opción 2: Con body JSON**
```bash
curl -X POST "http://localhost:8000/tareas" \
  -H "Content-Type: application/json" \
  -d '{
    "tarea_id": "T1001",
    "alimento_id": "A1"
  }'
```

**Body JSON completo:**
```json
{
  "tarea_id": "T1001",
  "alimento_id": "A1"
}
```

**Ejemplo sin tarea_id (se genera automáticamente):**
```json
{
  "alimento_id": "A1"
}
```

---

## GET - Listar Tareas

**Endpoint:** `GET http://localhost:8000/tareas`

**Ejemplo con curl:**
```bash
curl "http://localhost:8000/tareas"
```

**Listar solo tareas activas:**
```bash
curl "http://localhost:8000/tareas/activas"
```

**Listar solo tareas completadas:**
```bash
curl "http://localhost:8000/tareas/completadas"
```

**Obtener tarea desde BD:**
```bash
curl "http://localhost:8000/tareas/T1001/bd"
```

---

## POST - Asignar Hormigas a Tarea

**Endpoint:** `POST http://localhost:8000/tareas/{tarea_id}/asignar-hormigas`

**Opción 1: Solo asignar hormigas (sin iniciar)**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/asignar-hormigas?cantidad=2"
```

**Opción 2: Asignar e iniciar automáticamente con lote (RECOMENDADO)**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_H001"
  }'
```

**Body JSON para asignar e iniciar:**
```json
{
  "hormigas_lote_id": "LOTE_H001"
}
```

**Con cantidad específica y lote:**
```json
{
  "hormigas_lote_id": "LOTE_H001",
  "cantidad": 2
}
```

**Respuesta cuando se asigna e inicia automáticamente:**
```json
{
  "message": "Se asignaron 2 hormigas a la tarea T1001 y se inició automáticamente",
  "tarea_id": "T1001",
  "hormigas_asignadas": 2,
  "hormigas_requeridas": 2,
  "hormigas_lote_id": "LOTE_H001",
  "estado": "en_proceso",
  "iniciada": true
}
```

**Respuesta cuando solo se asignan (sin iniciar):**
```json
{
  "message": "Se asignaron 2 hormigas a la tarea T1001",
  "tarea_id": "T1001",
  "hormigas_asignadas": 2,
  "hormigas_requeridas": 2,
  "hormigas_lote_id": null,
  "estado": "pendiente",
  "iniciada": false
}
```

---

## POST - Iniciar Tarea

**Endpoint:** `POST http://localhost:8000/tareas/{tarea_id}/iniciar`

**Body JSON:**
```json
{
  "hormigas_lote_id": "LOTE_H001"
}
```

**Ejemplo con curl:**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/iniciar" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_H001"
  }'
```

**Más ejemplos de lotes:**
```json
{
  "hormigas_lote_id": "LOTE_H002"
}
```

```json
{
  "hormigas_lote_id": "LOTE_ABC123"
}
```

**Respuesta esperada:**
```json
{
  "message": "Tarea T1001 iniciada exitosamente",
  "tarea_id": "T1001",
  "estado": "en_proceso",
  "hormigas_asignadas": 3,
  "hormigas_lote_id": "LOTE_H001"
}
```

---

## GET - Status de Tareas

### Status de todas las tareas

**Endpoint:** `GET http://localhost:8000/tareas/status`

**Ejemplo con curl:**
```bash
curl "http://localhost:8000/tareas/status"
```

**Respuesta esperada:**
```json
{
  "base_datos": {
    "engine": "sqlserver",
    "server": "SHIRORYUU",
    "database": "Hormiguero"
  },
  "total_tareas": 2,
  "tareas_completadas_automaticamente": 0,
  "tareas": [
    {
      "tarea_id": "T1001",
      "estado": "en_proceso",
      "alimento": {
        "id": "A1",
        "nombre": "Semillas de girasol"
      },
      "hormigas_lote_id": "LOTE_H001",
      "inicio": "2024-01-15T10:00:00",
      "fin": null,
      "alimento_recolectado": 0
    },
    {
      "tarea_id": "T1002",
      "estado": "pendiente",
      "alimento": {
        "id": "A2",
        "nombre": "Hojas frescas"
      },
      "hormigas_lote_id": null,
      "inicio": null,
      "fin": null,
      "alimento_recolectado": 0
    }
  ]
}
```

### Status de una tarea específica

**Endpoint:** `GET http://localhost:8000/tareas/{tarea_id}/status`

**Ejemplo con curl:**
```bash
curl "http://localhost:8000/tareas/T1001/status"
```

**Respuesta esperada:**
```json
{
  "base_datos": {
    "engine": "sqlserver",
    "server": "SHIRORYUU",
    "database": "Hormiguero"
  },
  "tarea_id": "T1001",
  "estado": "en_proceso",
  "completada_automaticamente": false,
  "alimento": {
    "id": "A1",
    "nombre": "Semillas de girasol"
  },
  "hormigas_lote_id": "LOTE_H001",
  "inicio": "2024-01-15T10:00:00",
  "fin": null,
  "alimento_recolectado": 0
}
```

---

## POST - Completar Tarea

**Endpoint:** `POST http://localhost:8000/tareas/{tarea_id}/completar?cantidad_recolectada={cantidad}`

**Ejemplo con curl:**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/completar?cantidad_recolectada=50"
```

**Respuesta esperada:**
```json
{
  "message": "Tarea T1001 completada exitosamente"
}
```

---

## POST - Procesar Recolección (Automático)

**Endpoint:** `POST http://localhost:8000/procesar`

**Ejemplo con curl:**
```bash
curl -X POST "http://localhost:8000/procesar"
```

**Respuesta esperada:**
```json
{
  "message": "Proceso de recolección completado",
  "tareas_procesadas": 1,
  "tareas": [
    {
      "id": "T1001",
      "alimento": {
        "id": "A1",
        "nombre": "Semillas de girasol",
        "cantidad_hormigas_necesarias": 3,
        "puntos_stock": 50,
        "tiempo_recoleccion": 120,
        "disponible": true
      },
      "hormigas_asignadas": [...],
      "estado": "completada",
      "fecha_inicio": "2024-01-15T10:00:00",
      "fecha_fin": "2024-01-15T10:02:00",
      "alimento_recolectado": 50
    }
  ]
}
```

---

## GET - Health Check

**Endpoint:** `GET http://localhost:8000/health`

**Ejemplo con curl:**
```bash
curl "http://localhost:8000/health"
```

**Respuesta esperada:**
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

## GET - Estadísticas

**Endpoint:** `GET http://localhost:8000/estadisticas`

**Ejemplo con curl:**
```bash
curl "http://localhost:8000/estadisticas"
```

**Respuesta esperada:**
```json
{
  "tareas_activas": 1,
  "tareas_completadas": 2,
  "total_alimento_recolectado": 130,
  "base_datos": {
    "alimentos_en_bd": 5,
    "tareas_en_bd": 3
  },
  "tareas_memoria": {
    "activas": 1,
    "completadas": 2
  }
}
```

---

## GET - Debug Base de Datos

**Endpoint:** `GET http://localhost:8000/debug/db`

**Ejemplo con curl:**
```bash
curl "http://localhost:8000/debug/db"
```

**Respuesta esperada:**
```json
{
  "engine": "sqlserver",
  "implementation": "SqlServerDatabaseManager",
  "server": "SHIRORYUU",
  "database": "Hormiguero",
  "alimentos_en_bd": 5,
  "tareas_en_bd": 3,
  "ids_tareas": ["T1001", "T1002", "T1003"]
}
```

---

## GET - Eventos

**Endpoint:** `GET http://localhost:8000/eventos?limite=50`

**Ejemplo con curl:**
```bash
curl "http://localhost:8000/eventos?limite=50"
```

**Respuesta esperada:**
```json
{
  "eventos": [
    {
      "id": 1,
      "tipo": "tarea_creada",
      "descripcion": "Tarea T1001 creada",
      "creado_en": "2024-01-15T10:00:00"
    }
  ],
  "total": 1
}
```

---

## 🧪 Flujo Completo de Prueba

### Paso 1: Crear Alimento
```bash
curl -X POST "http://localhost:8000/alimentos" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "A1",
    "nombre": "Semillas de girasol",
    "cantidad_hormigas_necesarias": 3,
    "puntos_stock": 50,
    "tiempo_recoleccion": 120,
    "disponible": true
  }'
```

### Paso 2: Verificar Alimento Creado
```bash
curl "http://localhost:8000/alimentos"
```

### Paso 3: Crear Tarea
```bash
curl -X POST "http://localhost:8000/tareas?tarea_id=T1001&alimento_id=A1"
```

### Paso 4: Asignar Hormigas e Iniciar Automáticamente (TODO EN UNO)
```bash
curl -X POST "http://localhost:8000/tareas/T1001/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_H001"
  }'
```

**O si prefieres hacerlo en dos pasos:**

### Paso 4a: Asignar Hormigas (opcional, solo si no quieres iniciar automáticamente)
```bash
curl -X POST "http://localhost:8000/tareas/T1001/asignar-hormigas?cantidad=2"
```

### Paso 4b: Iniciar Tarea (solo si no usaste el lote en el paso 4a)
```bash
curl -X POST "http://localhost:8000/tareas/T1001/iniciar" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_H001"
  }'
```

### Paso 5: Verificar Status de Tarea
```bash
curl "http://localhost:8000/tareas/T1001/status"
```

### Paso 6: Verificar Status de Todas las Tareas
```bash
curl "http://localhost:8000/tareas/status"
```

### Paso 7: Completar Tarea (opcional, puede completarse automáticamente por tiempo)
```bash
curl -X POST "http://localhost:8000/tareas/T1001/completar?cantidad_recolectada=50"
```

### Paso 8: Ver Estadísticas
```bash
curl "http://localhost:8000/estadisticas"
```

---

## 📝 Notas Importantes

1. **Asignar e Iniciar en un solo paso:** Puedes usar `POST /tareas/{tarea_id}/asignar-hormigas` con `hormigas_lote_id` en el body para asignar las hormigas e iniciar la tarea automáticamente en una sola llamada.

2. **El lote de hormigas (`hormigas_lote_id`)** debe contener exactamente el número de hormigas requeridas por el alimento.

3. **La tarea se completa automáticamente** cuando el tiempo transcurrido desde `inicio` es mayor o igual a `tiempo_recoleccion` del alimento.

4. **La fecha de fin** se calcula como `fecha_inicio + tiempo_recoleccion`, no como la hora actual de verificación.

5. **Todos los datos se persisten en SQL Server** cuando se configura correctamente con las variables de entorno.

6. **El endpoint `/tareas/status`** verifica automáticamente si alguna tarea debe completarse por tiempo transcurrido.

7. **El status siempre incluye `hormigas_lote_id`** en las respuestas de GET `/tareas/status` y GET `/tareas/{tarea_id}/status`.

