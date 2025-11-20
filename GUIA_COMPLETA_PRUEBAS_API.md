# 🚀 Guía Completa: Pruebas de APIs desde Cero

## 📋 Índice
1. [Configuración Inicial](#configuración-inicial)
2. [Todos los Endpoints GET](#todos-los-endpoints-get)
3. [Todos los Endpoints POST](#todos-los-endpoints-post)
4. [Flujo Completo de Ejecución](#flujo-completo-de-ejecución)

---

## 🔧 Configuración Inicial

### Paso 1: Abrir el Proyecto
```bash
cd "C:\Users\manue\Proyecto Hormiguero"
```

### Paso 2: Crear Base de Datos y Tablas (Solo la primera vez)
Ejecuta el script para crear la base de datos desde cero:
```bash
crear_base_y_tablas_sqlserver.bat
```

**Esto creará:**
- Base de datos `Hormiguero`
- Tablas: `Alimentos`, `Tareas`, `Eventos`, `Mensajes`
- 3 alimentos iniciales (A1, A2, A3)

### Paso 3: Iniciar el Servicio API
Ejecuta el script para configurar SQL Server e iniciar la API:
```bash
configurar_sqlserver_y_ejecutar.bat
```

**Deja esta ventana abierta** - El servicio estará corriendo en `http://localhost:8000`

### Paso 4: Verificar que el Servicio está Activo
Abre una **nueva ventana de terminal** y ejecuta:

```bash
curl http://localhost:8000/health
```

**Respuesta esperada:**
```json
{
  "status": "ok",
  "service": "recoleccion",
  "version": "1.0.0"
}
```

---

## 📥 Todos los Endpoints GET

### 1. GET / - Información del Servicio
```bash
curl http://localhost:8000/
```

**Respuesta:**
```json
{
  "service": "recoleccion",
  "version": "1.0.0",
  "description": "API del subsistema de recolección"
}
```

---

### 2. GET /health - Estado de Salud
```bash
curl http://localhost:8000/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "service": "recoleccion"
}
```

---

### 3. GET /alimentos - Listar Todos los Alimentos
```bash
curl "http://localhost:8000/alimentos"
```

**Con filtro por estado:**
```bash
curl "http://localhost:8000/alimentos?estado=disponible"
```

**Respuesta:**
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

### 4. GET /tareas - Listar Todas las Tareas
```bash
curl "http://localhost:8000/tareas"
```

**Respuesta:**
```json
[
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
    "hormigas_asignadas": [],
    "hormigas_lote_id": null,
    "estado": "pendiente",
    "fecha_inicio": null,
    "fecha_fin": null,
    "alimento_recolectado": 0
  }
]
```

---

### 5. GET /tareas/activas - Listar Tareas Activas
```bash
curl "http://localhost:8000/tareas/activas"
```

---

### 6. GET /tareas/completadas - Listar Tareas Completadas
```bash
curl "http://localhost:8000/tareas/completadas"
```

---

### 7. GET /tareas/en-proceso - Listar Tareas en Proceso
```bash
curl "http://localhost:8000/tareas/en-proceso"
```

---

### 8. GET /tareas/status - Status de Todas las Tareas (DETALLADO)
```bash
curl "http://localhost:8000/tareas/status"
```

**Respuesta:**
```json
{
  "tareas": [
    {
      "tarea_id": "T1001",
      "alimento_id": 1,
      "alimento_nombre": "Semillas de girasol",
      "estado": "en_proceso",
      "hormigas_lote_id": "LOTE_H001",
      "hormigas_asignadas": 2,
      "hormigas_requeridas": 2,
      "fecha_inicio": "2024-01-15T10:00:00",
      "fecha_fin": "2024-01-15T10:02:00",
      "tiempo_recoleccion": 120,
      "cantidad_recolectada": 0,
      "puntos_stock": 50,
      "tiempo_transcurrido": 45,
      "tiempo_restante": 75
    }
  ],
  "total": 1,
  "en_proceso": 1,
  "completadas": 0,
  "pendientes": 0,
  "base_datos": {
    "engine": "sqlserver",
    "server": "SHIRORYUU",
    "database": "Hormiguero"
  }
}
```

---

### 9. GET /tareas/{tarea_id}/status - Status de una Tarea Específica
```bash
curl "http://localhost:8000/tareas/T1001/status"
```

**Respuesta:**
```json
{
  "tarea_id": "T1001",
  "alimento_id": 1,
  "alimento_nombre": "Semillas de girasol",
  "estado": "en_proceso",
  "hormigas_lote_id": "LOTE_H001",
  "hormigas_asignadas": 2,
  "hormigas_requeridas": 2,
  "fecha_inicio": "2024-01-15T10:00:00",
  "fecha_fin": "2024-01-15T10:02:00",
  "tiempo_recoleccion": 120,
  "cantidad_recolectada": 0,
  "puntos_stock": 50,
  "tiempo_transcurrido": 45,
  "tiempo_restante": 75,
  "base_datos": {
    "engine": "sqlserver",
    "server": "SHIRORYUU",
    "database": "Hormiguero"
  }
}
```

---

### 10. GET /tareas/bd - Listar Tareas desde Base de Datos (RAW)
```bash
curl "http://localhost:8000/tareas/bd"
```

---

### 11. GET /tareas/{tarea_id}/bd - Obtener Tarea desde BD (RAW)
```bash
curl "http://localhost:8000/tareas/T1001/bd"
```

---

### 12. GET /tareas/{tarea_id}/tiempo-restante - Tiempo Restante de Tarea
```bash
curl "http://localhost:8000/tareas/T1001/tiempo-restante"
```

**Respuesta:**
```json
{
  "tarea_id": "T1001",
  "tiempo_restante": 75,
  "tiempo_total": 120,
  "tiempo_transcurrido": 45,
  "porcentaje_completado": 37.5
}
```

---

### 13. GET /tareas/{tarea_id}/progreso - Progreso de Tarea
```bash
curl "http://localhost:8000/tareas/T1001/progreso"
```

**Respuesta:**
```json
{
  "tarea_id": "T1001",
  "estado": "en_proceso",
  "porcentaje_completado": 37.5,
  "tiempo_transcurrido": 45,
  "tiempo_restante": 75
}
```

---

### 14. GET /estadisticas - Estadísticas Generales
```bash
curl "http://localhost:8000/estadisticas"
```

**Respuesta:**
```json
{
  "total_tareas": 5,
  "tareas_pendientes": 2,
  "tareas_en_proceso": 2,
  "tareas_completadas": 1,
  "total_alimentos_recolectados": 150,
  "total_puntos": 750
}
```

---

### 15. GET /eventos - Listar Eventos
```bash
curl "http://localhost:8000/eventos"
```

---

### 16. GET /debug/db - Información de Base de Datos
```bash
curl "http://localhost:8000/debug/db"
```

**Respuesta:**
```json
{
  "engine": "sqlserver",
  "implementation": "SqlServerDatabaseManager",
  "server": "SHIRORYUU",
  "database": "Hormiguero",
  "odbc_driver": "ODBC Driver 17 for SQL Server",
  "alimentos_en_bd": 3,
  "tareas_en_bd": 2,
  "ids_tareas": ["T1001", "T1002"]
}
```

---

### 17. GET /debug/tareas-raw - Tareas RAW desde SQL Server
```bash
curl "http://localhost:8000/debug/tareas-raw"
```

---

## 📤 Todos los Endpoints POST

### 1. POST /alimentos - Crear Alimento
```bash
curl -X POST "http://localhost:8000/alimentos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Manzana",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 30,
    "tiempo_recoleccion": 120,
    "disponible": true
  }'
```

**Body JSON completo:**
```json
{
  "id": "A1",
  "nombre": "Manzana",
  "cantidad_hormigas_necesarias": 2,
  "puntos_stock": 30,
  "tiempo_recoleccion": 120,
  "disponible": true
}
```

**Respuesta:**
```json
{
  "id": "A1",
  "nombre": "Manzana",
  "cantidad_hormigas_necesarias": 2,
  "puntos_stock": 30,
  "tiempo_recoleccion": 120,
  "disponible": true,
  "fecha_creacion": "2024-01-15T10:00:00"
}
```

---

### 2. POST /tareas - Crear Tarea
**Opción 1: Con query parameters**
```bash
curl -X POST "http://localhost:8000/tareas?tarea_id=T1001&alimento_id=1"
```

**Opción 2: Con body JSON (RECOMENDADO)**
```bash
curl -X POST "http://localhost:8000/tareas" \
  -H "Content-Type: application/json" \
  -d '{
    "tarea_id": "T1001",
    "alimento_id": "1"
  }'
```

**Body JSON:**
```json
{
  "tarea_id": "T1001",
  "alimento_id": "1"
}
```

**Respuesta:**
```json
{
  "id": "T1001",
  "alimento": {
    "id": "A1",
    "nombre": "Manzana",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 30,
    "tiempo_recoleccion": 120,
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

---

### 3. POST /tareas/{tarea_id}/asignar-hormigas - Asignar Hormigas e Iniciar (TODO EN UNO)
**Opción A: Asignar e iniciar automáticamente (RECOMENDADO)**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_H001"
  }'
```

**Body JSON:**
```json
{
  "hormigas_lote_id": "LOTE_H001"
}
```

**Con cantidad específica:**
```json
{
  "hormigas_lote_id": "LOTE_H001",
  "cantidad": 2
}
```

**Respuesta (cuando inicia automáticamente):**
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

**Opción B: Solo asignar (sin iniciar)**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/asignar-hormigas?cantidad=2"
```

**Respuesta (solo asignar):**
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

### 4. POST /tareas/{tarea_id}/iniciar - Iniciar Tarea
```bash
curl -X POST "http://localhost:8000/tareas/T1001/iniciar" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_H001"
  }'
```

**Body JSON:**
```json
{
  "hormigas_lote_id": "LOTE_H001"
}
```

**Respuesta:**
```json
{
  "message": "Tarea T1001 iniciada exitosamente",
  "tarea_id": "T1001",
  "estado": "en_proceso",
  "hormigas_lote_id": "LOTE_H001",
  "fecha_inicio": "2024-01-15T10:00:00"
}
```

---

### 5. POST /tareas/{tarea_id}/completar - Completar Tarea Manualmente
```bash
curl -X POST "http://localhost:8000/tareas/T1001/completar?cantidad_recolectada=50"
```

**Con query parameter:**
```
?cantidad_recolectada=50
```

**Respuesta:**
```json
{
  "message": "Tarea T1001 completada",
  "tarea_id": "T1001",
  "cantidad_recolectada": 50,
  "estado": "completada",
  "fecha_fin": "2024-01-15T10:05:00"
}
```

---

### 6. POST /tareas/{tarea_id}/cancelar - Cancelar Tarea
```bash
curl -X POST "http://localhost:8000/tareas/T1001/cancelar"
```

**Respuesta:**
```json
{
  "message": "Tarea T1001 cancelada",
  "tarea_id": "T1001",
  "estado": "cancelada"
}
```

---

### 7. POST /procesar - Procesar Recolección Automática
```bash
curl -X POST "http://localhost:8000/procesar"
```

**Body JSON (opcional):**
```json
{
  "zona_id": 1,
  "estado": "disponible"
}
```

---

### 8. POST /verificar-hormigas - Verificar Hormigas Disponibles
```bash
curl -X POST "http://localhost:8000/verificar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "cantidad": 5
  }'
```

**Body JSON:**
```json
{
  "cantidad": 5
}
```

**Respuesta:**
```json
{
  "hormigas_disponibles": true,
  "cantidad": 5,
  "message": "Hay suficientes hormigas disponibles"
}
```

---

## 🔄 Flujo Completo de Ejecución

### Ejecución Completa Paso a Paso

#### Paso 1: Verificar que el Servicio está Activo
```bash
curl http://localhost:8000/health
```

**Salida esperada:**
```json
{"status": "ok", "service": "recoleccion"}
```

---

#### Paso 2: Verificar Base de Datos
```bash
curl http://localhost:8000/debug/db
```

**Salida esperada:**
```json
{
  "engine": "sqlserver",
  "server": "SHIRORYUU",
  "database": "Hormiguero",
  "alimentos_en_bd": 3,
  "tareas_en_bd": 0
}
```

---

#### Paso 3: Listar Alimentos Existentes
```bash
curl "http://localhost:8000/alimentos"
```

**Salida esperada:** Lista de alimentos (puede estar vacía o tener los 3 iniciales)

---

#### Paso 4: Crear un Nuevo Alimento
```bash
curl -X POST "http://localhost:8000/alimentos" \
  -H "Content-Type: application/json" \
  -d "{
    \"nombre\": \"Manzana Roja\",
    \"cantidad_hormigas_necesarias\": 2,
    \"puntos_stock\": 30,
    \"tiempo_recoleccion\": 60,
    \"disponible\": true
  }"
```

**Salida esperada:**
```json
{
  "id": "A4",
  "nombre": "Manzana Roja",
  "cantidad_hormigas_necesarias": 2,
  "puntos_stock": 30,
  "tiempo_recoleccion": 60,
  "disponible": true
}
```

**Nota:** Anota el `id` del alimento creado (ejemplo: `A4` o el número que te devuelva)

---

#### Paso 5: Verificar Alimento Creado
```bash
curl "http://localhost:8000/alimentos"
```

**Busca** el alimento que acabas de crear en la lista.

---

#### Paso 6: Crear una Tarea
```bash
curl -X POST "http://localhost:8000/tareas" \
  -H "Content-Type: application/json" \
  -d "{
    \"tarea_id\": \"T1001\",
    \"alimento_id\": \"1\"
  }"
```

**Nota:** Usa el `id` del alimento que obtuviste (puede ser `1`, `2`, `3`, o el número que te devolvió al crear)

**Salida esperada:**
```json
{
  "id": "T1001",
  "alimento": {...},
  "estado": "pendiente",
  "hormigas_asignadas": [],
  "hormigas_lote_id": null
}
```

---

#### Paso 7: Asignar Hormigas e Iniciar Tarea (TODO EN UNO)
```bash
curl -X POST "http://localhost:8000/tareas/T1001/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d "{
    \"hormigas_lote_id\": \"LOTE_H001\"
  }"
```

**Salida esperada:**
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

---

#### Paso 8: Verificar Status de la Tarea
```bash
curl "http://localhost:8000/tareas/T1001/status"
```

**Salida esperada:**
```json
{
  "tarea_id": "T1001",
  "alimento_id": 1,
  "alimento_nombre": "Manzana Roja",
  "estado": "en_proceso",
  "hormigas_lote_id": "LOTE_H001",
  "hormigas_asignadas": 2,
  "hormigas_requeridas": 2,
  "fecha_inicio": "2024-01-15T10:00:00",
  "tiempo_recoleccion": 60,
  "tiempo_transcurrido": 5,
  "tiempo_restante": 55
}
```

---

#### Paso 9: Verificar Status de Todas las Tareas
```bash
curl "http://localhost:8000/tareas/status"
```

**Salida esperada:**
```json
{
  "tareas": [
    {
      "tarea_id": "T1001",
      "hormigas_lote_id": "LOTE_H001",
      "estado": "en_proceso",
      ...
    }
  ],
  "total": 1,
  "en_proceso": 1
}
```

---

#### Paso 10: Ver Progreso de la Tarea
```bash
curl "http://localhost:8000/tareas/T1001/progreso"
```

**Salida esperada:**
```json
{
  "tarea_id": "T1001",
  "estado": "en_proceso",
  "porcentaje_completado": 8.33,
  "tiempo_transcurrido": 5,
  "tiempo_restante": 55
}
```

---

#### Paso 11: Esperar o Completar Manualmente

**Opción A: Esperar a que se complete automáticamente** (después de `tiempo_recoleccion` segundos)

**Opción B: Completar manualmente**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/completar?cantidad_recolectada=50"
```

**Salida esperada:**
```json
{
  "message": "Tarea T1001 completada",
  "tarea_id": "T1001",
  "cantidad_recolectada": 50,
  "estado": "completada"
}
```

---

#### Paso 12: Verificar Tarea Completada
```bash
curl "http://localhost:8000/tareas/T1001/status"
```

**Salida esperada:**
```json
{
  "tarea_id": "T1001",
  "estado": "completada",
  "hormigas_lote_id": "LOTE_H001",
  "fecha_fin": "2024-01-15T10:01:00",
  "cantidad_recolectada": 50
}
```

### Paso 12b: Verificar que el Alimento está Agotado
```bash
curl "http://localhost:8000/alimentos"
```

**Busca el alimento que usaste** - Debe tener `"disponible": false`

**O verifica un alimento específico:**
```bash
curl "http://localhost:8000/alimentos?estado=disponible"
```

**El alimento recolectado NO debe aparecer** en esta lista (solo muestra `disponible: true`)

### Paso 12c: Intentar Crear Tarea con Alimento Agotado (debe fallar)
```bash
curl -X POST "http://localhost:8000/tareas" \
  -H "Content-Type: application/json" \
  -d '{
    "tarea_id": "T1002",
    "alimento_id": "1"
  }'
```

**Salida esperada (Error 400):**
```json
{
  "detail": "El alimento 'Manzana Roja' (ID: 1) no está disponible. Estado: agotado"
}
```

---

#### Paso 13: Ver Estadísticas Finales
```bash
curl "http://localhost:8000/estadisticas"
```

**Salida esperada:**
```json
{
  "total_tareas": 1,
  "tareas_completadas": 1,
  "tareas_en_proceso": 0,
  "total_alimentos_recolectados": 50,
  "total_puntos": 1500
}
```

---

#### Paso 14: Ver Eventos Registrados
```bash
curl "http://localhost:8000/eventos"
```

---

## 📝 Notas Importantes

1. **El servicio debe estar corriendo** antes de hacer cualquier petición
2. **El lote de hormigas (`hormigas_lote_id`)** es requerido para iniciar tareas
3. **Las tareas se completan automáticamente** cuando pasa el `tiempo_recoleccion` desde `fecha_inicio`
4. **La fecha de fin** se calcula como `fecha_inicio + tiempo_recoleccion`, no como hora actual
5. **Todos los datos se guardan en SQL Server** en la base `Hormiguero`
6. **El endpoint `/tareas/status`** verifica automáticamente si alguna tarea debe completarse por tiempo
7. **Validación de disponibilidad**: Solo se pueden crear tareas con alimentos disponibles (`disponible = true`)
8. **Actualización automática**: Cuando se completa una tarea, el alimento se marca automáticamente como no disponible (`disponible = false`)
9. **Mensajes de error**: Si intentas crear una tarea con un alimento agotado, recibirás un error 400 con el mensaje correspondiente

---

## 🐛 Solución de Problemas

### Error: "Connection refused"
- Verifica que el servicio esté corriendo: `curl http://localhost:8000/health`
- Si no responde, ejecuta `configurar_sqlserver_y_ejecutar.bat`

### Error: "No se pudo guardar el alimento en BD"
- Verifica que la base de datos esté creada: `curl http://localhost:8000/debug/db`
- Si muestra `engine: sqlite`, ejecuta `configurar_sqlserver_y_ejecutar.bat`

### Error: "Tarea no encontrada"
- Verifica que la tarea exista: `curl "http://localhost:8000/tareas"`
- Usa el `tarea_id` correcto

### Error: "No se puede iniciar la tarea sin suficientes hormigas"
- Primero asigna hormigas: `POST /tareas/{tarea_id}/asignar-hormigas` con `hormigas_lote_id` en el body
- O usa el método TODO EN UNO que asigna e inicia automáticamente

### Error: "El alimento no está disponible. Estado: agotado"
- El alimento ya fue recolectado y marcado como no disponible
- Verifica la disponibilidad del alimento antes de crear la tarea: `GET /alimentos`
- Solo se pueden crear tareas con alimentos que tengan `disponible: true`

---

## ✅ Checklist de Prueba Completa

- [ ] Servicio iniciado y saludable
- [ ] Base de datos verificada (SQL Server)
- [ ] Alimento creado exitosamente
- [ ] Tarea creada exitosamente
- [ ] Hormigas asignadas e iniciada automáticamente
- [ ] Status de tarea muestra `hormigas_lote_id`
- [ ] Tarea completada (automática o manual)
- [ ] Estadísticas actualizadas
- [ ] Eventos registrados

---

¡Listo para probar! 🚀

