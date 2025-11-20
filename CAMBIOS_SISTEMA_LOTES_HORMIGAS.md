# 🔄 Cambios en el Sistema de Asignación de Hormigas - Sistema de Lotes

Este documento describe los cambios realizados para implementar un sistema de lotes de hormigas con validaciones completas.

---

## 📋 Resumen de Cambios

### Objetivo
Implementar un sistema de lotes de hormigas que:
- Valide la cantidad de hormigas enviadas vs requeridas
- Guarde las asignaciones en una tabla dedicada
- Permita relacionar tareas con lotes mediante IDs
- Valide que los lotes no estén en uso
- Elimine la necesidad de almacenar `hormigas_asignadas` directamente en la tabla de tareas

---

## 🗄️ Cambios en Base de Datos

### Nueva Tabla: `lotes_hormigas`

**SQLite y SQL Server:**

```sql
CREATE TABLE lotes_hormigas (
    lote_id TEXT PRIMARY KEY,
    tarea_id TEXT NOT NULL,
    cantidad_hormigas_enviadas INTEGER NOT NULL,
    cantidad_hormigas_requeridas INTEGER NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_aceptacion TIMESTAMP,
    FOREIGN KEY (tarea_id) REFERENCES tareas (id)
)
```

**Estados posibles:**
- `pendiente`: Lote creado pero no aceptado
- `aceptado`: Lote aceptado y listo para usar
- `en_uso`: Lote actualmente en uso por una tarea

### Modificación: `asignaciones_hormiga_tarea`

**Nueva columna agregada:**
- `lote_id TEXT`: ID del lote al que pertenece la asignación

**Estructura actualizada:**
```sql
CREATE TABLE asignaciones_hormiga_tarea (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarea_id TEXT NOT NULL,
    hormiga_id TEXT NOT NULL,
    lote_id TEXT,  -- NUEVA COLUMNA
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tarea_id) REFERENCES tareas (id),
    FOREIGN KEY (hormiga_id) REFERENCES hormigas (id),
    FOREIGN KEY (lote_id) REFERENCES lotes_hormigas (lote_id)
)
```

---

## 🔧 Nuevos Métodos en DatabaseManager

### SQLite y SQL Server

1. **`crear_lote_hormigas(lote_id, tarea_id, cantidad_enviada, cantidad_requerida)`**
   - Crea un lote de hormigas
   - **Validación**: Solo crea si `cantidad_enviada >= cantidad_requerida`
   - Retorna `False` con mensaje de error si la cantidad es insuficiente

2. **`aceptar_lote_hormigas(lote_id)`**
   - Acepta un lote (cambia estado de `pendiente` a `aceptado`)
   - **Validación**: Verifica que el lote no esté en uso
   - Retorna `False` si el lote está en uso o no existe

3. **`marcar_lote_en_uso(lote_id)`**
   - Marca un lote como `en_uso`
   - Se usa cuando se inicia una tarea con ese lote

4. **`verificar_lote_disponible(lote_id, cantidad_requerida)`**
   - Verifica que:
     - El lote existe
     - No está en uso
     - Tiene cantidad suficiente de hormigas
   - Retorna tupla `(es_valido, mensaje_error)`

5. **`guardar_hormigas_en_lote(lote_id, hormigas)`**
   - Guarda las hormigas asignadas en un lote
   - Crea las hormigas si no existen
   - Crea las asignaciones con el `lote_id`

6. **`obtener_hormigas_por_lote(lote_id)`**
   - Obtiene todas las hormigas de un lote
   - Usa la relación `asignaciones_hormiga_tarea.lote_id`

---

## 🔄 Cambios en Servicios

### `PersistenceService`

**Nuevos métodos agregados:**
- `crear_lote_hormigas()` - Wrapper para crear lotes
- `aceptar_lote_hormigas()` - Wrapper para aceptar lotes
- `marcar_lote_en_uso()` - Wrapper para marcar lotes en uso
- `verificar_lote_disponible()` - Wrapper para verificar disponibilidad
- `guardar_hormigas_en_lote()` - Wrapper para guardar hormigas
- `obtener_hormigas_por_lote()` - Wrapper para obtener hormigas

Todos los métodos incluyen logging de eventos.

### `RecoleccionService`

**Modificación: `asignar_hormigas_a_tarea()`**

**Antes:**
```python
async def asignar_hormigas_a_tarea(tarea, hormigas):
    # Asignaba directamente sin validación
    for hormiga in hormigas:
        tarea.agregar_hormiga(hormiga)
    # Guardaba en BD
```

**Ahora:**
```python
async def asignar_hormigas_a_tarea(tarea, hormigas, lote_id=None):
    # 1. Valida cantidad_enviada >= cantidad_requerida
    # 2. Crea lote en BD (falla si cantidad insuficiente)
    # 3. Acepta el lote
    # 4. Guarda hormigas en el lote
    # 5. Asigna lote_id a la tarea
    # Retorna (exitoso, mensaje_error)
```

**Modificación: `iniciar_tarea_recoleccion()`**

**Nuevas validaciones:**
- Si hay `hormigas_lote_id`, verifica que el lote esté disponible
- Verifica que el lote tenga cantidad suficiente
- Marca el lote como `en_uso` antes de iniciar

### `DatabaseManager.obtener_tareas()`

**Cambio en carga de hormigas:**

**Antes:**
```python
# Cargaba hormigas directamente por tarea_id
SELECT h.* FROM hormigas h
JOIN asignaciones_hormiga_tarea aht ON h.id = aht.hormiga_id
WHERE aht.tarea_id = ?
```

**Ahora:**
```python
# 1. Busca lote_id de la tarea
SELECT lote_id FROM lotes_hormigas WHERE tarea_id = ?

# 2. Si existe lote, carga hormigas desde el lote
SELECT h.* FROM hormigas h
JOIN asignaciones_hormiga_tarea aht ON h.id = aht.hormiga_id
WHERE aht.lote_id = ?

# 3. Si no hay lote, fallback a carga directa (compatibilidad)
```

---

## 📝 Validaciones Implementadas

### 1. Validación de Cantidad al Crear Lote

```python
if cantidad_enviada < cantidad_requerida:
    return False, "El lote tiene cantidad insuficiente de hormigas. Enviadas: X, Requeridas: Y"
```

### 2. Validación de Lote No en Uso

```python
if estado == 'en_uso':
    return False, f"Lote {lote_id} ya está en uso"
```

### 3. Validación de Cantidad al Iniciar Tarea

```python
if cantidad_enviada < cantidad_requerida:
    return False, f"Lote {lote_id} tiene cantidad insuficiente. Tiene: X, Requiere: Y"
```

### 4. Validación de Lote Existente

```python
if not lote_existe:
    return False, f"Lote {lote_id} no encontrado"
```

---

## 🔌 Cambios en API

### Endpoint: `POST /tareas/{tarea_id}/asignar-hormigas`

**Nuevo comportamiento:**
1. Solicita hormigas al servicio de comunicación
2. Llama a `asignar_hormigas_a_tarea()` que:
   - Valida cantidad
   - Crea lote
   - Acepta lote
   - Guarda hormigas
3. Si hay error de validación, retorna 400 con mensaje descriptivo
4. Si se proporciona `hormigas_lote_id` y hay suficientes hormigas, inicia automáticamente

**Mensajes de error posibles:**
- `"El lote tiene cantidad insuficiente de hormigas. Enviadas: X, Requeridas: Y"`
- `"Lote {lote_id} ya está en uso"`
- `"Lote {lote_id} no encontrado"`

---

## 📦 Scripts SQL

### `scripts/crear_tabla_lotes_hormigas_sqlserver.sql`

Script para crear las tablas en SQL Server:
- Crea tabla `lotes_hormigas` si no existe
- Agrega columna `lote_id` a `asignaciones_hormiga_tarea` si no existe
- Agrega foreign keys necesarias

**Uso:**
```sql
-- Ejecutar en SQL Server Management Studio o sqlcmd
sqlcmd -S SHIRORYUU -d Hormiguero -i scripts/crear_tabla_lotes_hormigas_sqlserver.sql
```

---

## 🔄 Flujo Completo

### Asignar Hormigas con Lote

1. **Cliente** → `POST /tareas/T1001/asignar-hormigas`
   ```json
   {
     "hormigas_lote_id": "LOTE_001",
     "cantidad": 3
   }
   ```

2. **API** → Solicita hormigas al servicio de comunicación

3. **API** → `asignar_hormigas_a_tarea(tarea, hormigas, lote_id="LOTE_001")`
   - Valida: `len(hormigas) >= cantidad_requerida`
   - Crea lote en BD: `crear_lote_hormigas()`
   - Acepta lote: `aceptar_lote_hormigas()`
   - Guarda hormigas: `guardar_hormigas_en_lote()`

4. **Si hay suficientes hormigas y lote_id:**
   - `iniciar_tarea_recoleccion(tarea, lote_id)`
   - Verifica lote disponible
   - Marca lote como `en_uso`
   - Inicia timer

5. **Respuesta:**
   ```json
   {
     "message": "Se asignaron 3 hormigas a la tarea T1001 y se inició automáticamente",
     "hormigas_lote_id": "LOTE_001",
     "estado": "en_proceso",
     "iniciada": true
   }
   ```

### Obtener Tareas

1. **Cliente** → `GET /tareas/status`

2. **API** → `obtener_tareas()`
   - Carga tareas desde BD
   - Para cada tarea:
     - Busca `lote_id` en `lotes_hormigas`
     - Si existe, carga hormigas desde `asignaciones_hormiga_tarea` usando `lote_id`
     - Si no existe, fallback a carga directa (compatibilidad)

3. **Respuesta incluye:**
   - `hormigas_lote_id`: ID del lote asociado
   - Hormigas cargadas desde el lote

---

## ⚠️ Notas Importantes

1. **Compatibilidad hacia atrás:**
   - El sistema mantiene compatibilidad con asignaciones directas (sin lote)
   - Si no hay `lote_id`, carga hormigas directamente por `tarea_id`

2. **Eliminación de `hormigas_asignadas` en tabla `tareas`:**
   - La columna `hormigas_asignadas` nunca existió en la tabla `tareas`
   - Las hormigas siempre se obtuvieron desde `asignaciones_hormiga_tarea`
   - Ahora se obtienen desde `asignaciones_hormiga_tarea` usando `lote_id`

3. **Validaciones estrictas:**
   - No se puede crear un lote con cantidad insuficiente
   - No se puede usar un lote que ya está en uso
   - No se puede iniciar una tarea sin validar el lote

4. **Estados del lote:**
   - `pendiente` → Lote creado, esperando aceptación
   - `aceptado` → Lote aceptado, listo para usar
   - `en_uso` → Lote actualmente en uso por una tarea

---

## 🧪 Próximos Pasos

1. **Ejecutar script SQL** en SQL Server para crear las tablas
2. **Probar asignación** con cantidad suficiente
3. **Probar asignación** con cantidad insuficiente (debe fallar)
4. **Probar inicio** de tarea con lote en uso (debe fallar)
5. **Verificar** que las hormigas se cargan correctamente desde lotes

---

**Última actualización:** 2024-01-15

