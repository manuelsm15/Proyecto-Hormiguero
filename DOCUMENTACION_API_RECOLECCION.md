# 📚 Documentación Completa de APIs - Subsistema de Recolección

## 🎯 Información General

**Base URL:** `http://localhost:8000`  
**Versión:** 1.0.0  
**Servicio:** Subsistema de Recolección de Alimentos

---

## 📋 Índice

1. [APIs de Salud y Estado](#apis-de-salud-y-estado)
2. [APIs de Alimentos](#apis-de-alimentos)
3. [APIs de Tareas](#apis-de-tareas)
4. [APIs de Estado y Monitoreo](#apis-de-estado-y-monitoreo)
5. [APIs de Procesamiento](#apis-de-procesamiento)
6. [APIs de Debug](#apis-de-debug)
7. [Flujo Completo de Ejemplo](#flujo-completo-de-ejemplo)

---

## 🔍 APIs de Salud y Estado

### 1. Health Check

**GET** `/health`

Verifica el estado del servicio.

**Respuesta Exitosa (200):**
```json
{
  "status": "healthy",
  "service": "subsistema-recoleccion",
  "version": "1.0.0",
  "entorno_disponible": true,
  "comunicacion_disponible": true
}
```

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Ejemplo con PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
```

---

### 2. Información del Servicio

**GET** `/`

Obtiene información básica del servicio.

**Respuesta Exitosa (200):**
```json
{
  "message": "Subsistema de Recolección de Alimentos - Universidad Cenfotec"
}
```

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/"
```

**Ejemplo con PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/" -Method GET
```

---

## 🍎 APIs de Alimentos

### 3. Consultar Alimentos

**GET** `/alimentos`

Obtiene la lista de alimentos disponibles. Permite filtrar por zona y estado.

**Parámetros de Query (Opcionales):**
- `zona_id` (int): ID de la zona para filtrar recursos
- `estado` (string): Estado del recurso (`disponible`, `recolectado`, `no_disponible`)

**Respuesta Exitosa (200):**
```json
[
  {
    "id": "A1",
    "nombre": "Fruta",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 10,
    "tiempo_recoleccion": 60,
    "disponible": true,
    "fecha_creacion": "2024-01-15T10:30:00"
  },
  {
    "id": "A2",
    "nombre": "Semilla",
    "cantidad_hormigas_necesarias": 3,
    "puntos_stock": 15,
    "tiempo_recoleccion": 90,
    "disponible": true,
    "fecha_creacion": "2024-01-15T10:31:00"
  }
]
```

**Ejemplos:**

**Sin filtros:**
```bash
curl -X GET "http://localhost:8000/alimentos"
```

**Con filtro de estado:**
```bash
curl -X GET "http://localhost:8000/alimentos?estado=disponible"
```

**Con PowerShell:**
```powershell
# Sin filtros
Invoke-RestMethod -Uri "http://localhost:8000/alimentos" -Method GET

# Con filtro de estado
Invoke-RestMethod -Uri "http://localhost:8000/alimentos?estado=disponible" -Method GET
```

---

### 4. Crear Alimento

**POST** `/alimentos`

Crea un nuevo alimento en el sistema.

**Body (JSON):**
```json
{
  "id": "A3",
  "nombre": "Hoja",
  "cantidad_hormigas_necesarias": 2,
  "puntos_stock": 8,
  "tiempo_recoleccion": 45,
  "disponible": true
}
```

**Campos:**
- `id` (string, opcional): ID del alimento. Si no se proporciona, se genera automáticamente.
- `nombre` (string, requerido): Nombre del alimento.
- `cantidad_hormigas_necesarias` (int, requerido): Número de hormigas necesarias para recolectar.
- `puntos_stock` (int, requerido): Puntos de stock que vale el alimento.
- `tiempo_recoleccion` (int, requerido): Tiempo en segundos para recolectar.
- `disponible` (bool, opcional): Si el alimento está disponible. Por defecto: `true`.

**Respuesta Exitosa (200):**
```json
{
  "id": "A3",
  "nombre": "Hoja",
  "cantidad_hormigas_necesarias": 2,
  "puntos_stock": 8,
  "tiempo_recoleccion": 45,
  "disponible": true,
  "fecha_creacion": "2024-01-15T10:35:00"
}
```

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/alimentos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Hoja",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 8,
    "tiempo_recoleccion": 45,
    "disponible": true
  }'
```

**Ejemplo con PowerShell:**
```powershell
$body = @{
    nombre = "Hoja"
    cantidad_hormigas_necesarias = 2
    puntos_stock = 8
    tiempo_recoleccion = 45
    disponible = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/alimentos" -Method POST -Body $body -ContentType "application/json"
```

---

## 📝 APIs de Tareas

### 5. Crear Tarea

**POST** `/tareas`

Crea una nueva tarea de recolección. Valida que el alimento esté disponible.

**Parámetros de Query (Opcionales):**
- `tarea_id` (string): ID de la tarea. Si no se proporciona, se genera automáticamente.
- `alimento_id` (string): ID del alimento. Por defecto: `A1`.

**Body (JSON, Opcional):**
```json
{
  "tarea_id": "T1001",
  "alimento_id": "A1"
}
```

**Respuesta Exitosa (200):**
```json
{
  "id": "T1001",
  "alimento": {
    "id": "A1",
    "nombre": "Fruta",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 10,
    "tiempo_recoleccion": 60,
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

**Errores Posibles:**
- `404`: Alimento no encontrado
- `400`: El alimento no está disponible (agotado)

**Ejemplo con cURL:**
```bash
# Con parámetros en query
curl -X POST "http://localhost:8000/tareas?tarea_id=T1001&alimento_id=A1"

# Con body JSON
curl -X POST "http://localhost:8000/tareas" \
  -H "Content-Type: application/json" \
  -d '{
    "tarea_id": "T1001",
    "alimento_id": "A1"
  }'
```

**Ejemplo con PowerShell:**
```powershell
# Con parámetros en query
Invoke-RestMethod -Uri "http://localhost:8000/tareas?tarea_id=T1001&alimento_id=A1" -Method POST

# Con body JSON
$body = @{
    tarea_id = "T1001"
    alimento_id = "A1"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/tareas" -Method POST -Body $body -ContentType "application/json"
```

---

### 6. Listar Todas las Tareas

**GET** `/tareas`

Obtiene todas las tareas (activas y completadas) desde memoria.

**Respuesta Exitosa (200):**
```json
[
  {
    "id": "T1001",
    "alimento": {
      "id": "A1",
      "nombre": "Fruta",
      "cantidad_hormigas_necesarias": 2,
      "puntos_stock": 10,
      "tiempo_recoleccion": 60,
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

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/tareas"
```

**Ejemplo con PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/tareas" -Method GET
```

---

### 7. Listar Tareas Activas

**GET** `/tareas/activas`

Obtiene solo las tareas activas (pendientes y en proceso).

**Respuesta Exitosa (200):**
```json
[
  {
    "id": "T1001",
    "alimento": {
      "id": "A1",
      "nombre": "Fruta"
    },
    "estado": "en_proceso",
    "hormigas_lote_id": "LOTE_001"
  }
]
```

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/tareas/activas"
```

---

### 8. Listar Tareas Completadas

**GET** `/tareas/completadas`

Obtiene solo las tareas completadas.

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/tareas/completadas"
```

---

### 9. Listar Tareas en Proceso

**GET** `/tareas/en-proceso`

Obtiene solo las tareas en proceso.

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/tareas/en-proceso"
```

---

### 10. Asignar Hormigas a Tarea

**POST** `/tareas/{tarea_id}/asignar-hormigas`

Asigna hormigas a una tarea. Si se proporciona `hormigas_lote_id` y hay suficientes hormigas, inicia la tarea automáticamente.

**Parámetros de Path:**
- `tarea_id` (string): ID de la tarea

**Parámetros de Query (Opcionales):**
- `cantidad` (int): Cantidad de hormigas a asignar. Si no se proporciona, se calcula automáticamente.

**Body (JSON, Opcional):**
```json
{
  "hormigas_lote_id": "LOTE_001",
  "cantidad": 2
}
```

**Campos del Body:**
- `hormigas_lote_id` (string, opcional): ID del lote de hormigas. Si se proporciona y hay suficientes hormigas, inicia la tarea automáticamente.
- `cantidad` (int, opcional): Cantidad de hormigas a asignar.

**Respuesta Exitosa (200) - Con inicio automático:**
```json
{
  "message": "Se asignaron 2 hormigas a la tarea T1001 y se inició automáticamente",
  "tarea_id": "T1001",
  "hormigas_asignadas": 2,
  "hormigas_requeridas": 2,
  "hormigas_lote_id": "LOTE_001",
  "estado": "en_proceso",
  "iniciada": true
}
```

**Respuesta Exitosa (200) - Sin inicio automático:**
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

**Errores Posibles:**
- `404`: Tarea no encontrada
- `400`: No se pudieron obtener hormigas del servicio de comunicación

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_001",
    "cantidad": 2
  }'
```

**Ejemplo con PowerShell:**
```powershell
$body = @{
    hormigas_lote_id = "LOTE_001"
    cantidad = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/tareas/T1001/asignar-hormigas" -Method POST -Body $body -ContentType "application/json"
```

---

### 11. Iniciar Tarea

**POST** `/tareas/{tarea_id}/iniciar`

Inicia una tarea de recolección. Requiere que la tarea tenga suficientes hormigas asignadas y un lote de hormigas.

**Parámetros de Path:**
- `tarea_id` (string): ID de la tarea

**Body (JSON, Requerido):**
```json
{
  "hormigas_lote_id": "LOTE_001"
}
```

**Campos del Body:**
- `hormigas_lote_id` (string, requerido): ID del lote de hormigas que contiene el número de hormigas requeridas.

**Respuesta Exitosa (200):**
```json
{
  "message": "Tarea T1001 iniciada exitosamente",
  "tarea_id": "T1001",
  "estado": "en_proceso",
  "hormigas_asignadas": 2,
  "hormigas_lote_id": "LOTE_001"
}
```

**Errores Posibles:**
- `404`: Tarea no encontrada en memoria ni en base de datos
- `400`: No se puede iniciar la tarea sin suficientes hormigas

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/iniciar" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_001"
  }'
```

**Ejemplo con PowerShell:**
```powershell
$body = @{
    hormigas_lote_id = "LOTE_001"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/tareas/T1001/iniciar" -Method POST -Body $body -ContentType "application/json"
```

---

### 12. Completar Tarea

**POST** `/tareas/{tarea_id}/completar`

Completa una tarea de recolección manualmente.

**Parámetros de Path:**
- `tarea_id` (string): ID de la tarea

**Parámetros de Query:**
- `cantidad_recolectada` (int, requerido): Cantidad de alimento recolectado

**Respuesta Exitosa (200):**
```json
{
  "message": "Tarea T1001 completada exitosamente"
}
```

**Nota:** Al completar una tarea, el alimento se marca como no disponible (`disponible: false`).

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/completar?cantidad_recolectada=10"
```

**Ejemplo con PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/tareas/T1001/completar?cantidad_recolectada=10" -Method POST
```

---

### 13. Cancelar Tarea

**POST** `/tareas/{tarea_id}/cancelar`

Cancela una tarea en proceso.

**Parámetros de Path:**
- `tarea_id` (string): ID de la tarea

**Respuesta Exitosa (200):**
```json
{
  "message": "Tarea T1001 cancelada exitosamente"
}
```

**Errores Posibles:**
- `404`: Tarea no encontrada o no en proceso

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/cancelar"
```

---

## 📊 APIs de Estado y Monitoreo

### 14. Obtener Estado de Todas las Tareas

**GET** `/tareas/status`

Obtiene el estado de todas las tareas desde la base de datos. Incluye información detallada para compartir con otros subsistemas. **Verifica automáticamente si alguna tarea debe completarse por tiempo transcurrido.**

**Respuesta Exitosa (200):**
```json
{
  "base_datos": {
    "engine": "sqlserver",
    "server": "SHIRORYUU",
    "database": "Hormiguero"
  },
  "total_tareas": 3,
  "tareas_completadas_automaticamente": 1,
  "tareas": [
    {
      "tarea_id": "T1001",
      "estado": "completada",
      "alimento": {
        "id": "A1",
        "nombre": "Fruta"
      },
      "hormigas_lote_id": "LOTE_001",
      "inicio": "2024-01-15T10:40:00",
      "fin": "2024-01-15T10:41:00",
      "alimento_recolectado": 10
    },
    {
      "tarea_id": "T1002",
      "estado": "en_proceso",
      "alimento": {
        "id": "A2",
        "nombre": "Semilla"
      },
      "hormigas_lote_id": "LOTE_002",
      "inicio": "2024-01-15T10:45:00",
      "fin": null,
      "alimento_recolectado": 0
    }
  ]
}
```

**Características Importantes:**
- Verifica automáticamente si las tareas en proceso deben completarse por tiempo
- Si una tarea se completa automáticamente, `fecha_fin` se establece como `fecha_inicio + tiempo_recoleccion`
- Incluye `hormigas_lote_id` para compartir con otros subsistemas

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/tareas/status"
```

**Ejemplo con PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/tareas/status" -Method GET
```

---

### 15. Obtener Estado de una Tarea Específica

**GET** `/tareas/{tarea_id}/status`

Obtiene el estado detallado de una tarea específica desde la base de datos. **Verifica automáticamente si la tarea debe completarse por tiempo transcurrido.**

**Parámetros de Path:**
- `tarea_id` (string): ID de la tarea

**Respuesta Exitosa (200):**
```json
{
  "base_datos": {
    "engine": "sqlserver",
    "server": "SHIRORYUU",
    "database": "Hormiguero"
  },
  "tarea_id": "T1001",
  "estado": "completada",
  "completada_automaticamente": true,
  "alimento": {
    "id": "A1",
    "nombre": "Fruta"
  },
  "hormigas_lote_id": "LOTE_001",
  "inicio": "2024-01-15T10:40:00",
  "fin": "2024-01-15T10:41:00",
  "alimento_recolectado": 10
}
```

**Campos de la Respuesta:**
- `completada_automaticamente` (bool): Indica si la tarea se completó automáticamente en esta consulta
- `hormigas_lote_id` (string): ID del lote de hormigas asignado
- `inicio` (string, ISO 8601): Fecha y hora de inicio
- `fin` (string, ISO 8601): Fecha y hora de finalización (null si no está completada)

**Errores Posibles:**
- `404`: Tarea no encontrada en la base de datos

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/tareas/T1001/status"
```

**Ejemplo con PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/tareas/T1001/status" -Method GET
```

---

### 16. Obtener Tiempo Restante de Tarea

**GET** `/tareas/{tarea_id}/tiempo-restante`

Obtiene el tiempo restante de una tarea en proceso.

**Parámetros de Path:**
- `tarea_id` (string): ID de la tarea

**Respuesta Exitosa (200):**
```json
{
  "tarea_id": "T1001",
  "tiempo_total_asignado_segundos": 60,
  "tiempo_total_asignado_minutos": 1.0,
  "tiempo_restante_segundos": 30,
  "tiempo_restante_minutos": 0.5,
  "tiempo_transcurrido_segundos": 30,
  "progreso_porcentaje": 50.0
}
```

**Errores Posibles:**
- `404`: Tarea no encontrada o no en proceso

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/tareas/T1001/tiempo-restante"
```

---

### 17. Obtener Progreso de Tarea

**GET** `/tareas/{tarea_id}/progreso`

Obtiene el progreso porcentual de una tarea en proceso.

**Parámetros de Path:**
- `tarea_id` (string): ID de la tarea

**Respuesta Exitosa (200):**
```json
{
  "tarea_id": "T1001",
  "progreso_porcentaje": 50.0,
  "estado": "en_proceso"
}
```

**Errores Posibles:**
- `404`: Tarea no encontrada o no en proceso

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/tareas/T1001/progreso"
```

---

### 18. Obtener Estadísticas

**GET** `/estadisticas`

Obtiene estadísticas del servicio, combinando datos de memoria y base de datos.

**Respuesta Exitosa (200):**
```json
{
  "tareas_activas": 2,
  "tareas_completadas": 5,
  "total_alimentos_recolectados": 50,
  "base_datos": {
    "total_alimentos": 10,
    "total_tareas": 7
  },
  "tareas_memoria": {
    "activas": 2,
    "completadas": 5
  }
}
```

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/estadisticas"
```

---

### 19. Obtener Tareas desde Base de Datos

**GET** `/tareas/bd`

Obtiene todas las tareas directamente desde la base de datos (no desde memoria).

**Respuesta Exitosa (200):**
```json
[
  {
    "id": "T1001",
    "alimento": {
      "id": "A1",
      "nombre": "Fruta",
      "cantidad_hormigas_necesarias": 2,
      "puntos_stock": 10,
      "tiempo_recoleccion": 60,
      "disponible": false
    },
    "hormigas_asignadas": [
      {
        "id": "H001",
        "capacidad_carga": 5,
        "estado": "activa",
        "tiempo_vida": 1000,
        "subsistema_origen": "recoleccion"
      }
    ],
    "estado": "completada",
    "fecha_inicio": "2024-01-15T10:40:00",
    "fecha_fin": "2024-01-15T10:41:00",
    "alimento_recolectado": 10
  }
]
```

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/tareas/bd"
```

---

### 20. Obtener Tarea Específica desde Base de Datos

**GET** `/tareas/{tarea_id}/bd`

Obtiene una tarea específica desde la base de datos por ID.

**Parámetros de Path:**
- `tarea_id` (string): ID de la tarea

**Respuesta Exitosa (200):**
```json
{
  "id": "T1001",
  "alimento": {
    "id": "A1",
    "nombre": "Fruta",
    "cantidad_hormigas_necesarias": 2
  },
  "hormigas_asignadas": [
    {
      "id": "H001",
      "estado": "activa"
    }
  ],
  "estado": "completada",
  "alimento_recolectado": 10
}
```

**Errores Posibles:**
- `404`: Tarea no encontrada en BD

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/tareas/T1001/bd"
```

---

### 21. Obtener Eventos Recientes

**GET** `/eventos`

Obtiene eventos recientes del subsistema.

**Parámetros de Query (Opcionales):**
- `limite` (int): Número máximo de eventos a retornar (1-1000). Por defecto: 50

**Respuesta Exitosa (200):**
```json
{
  "eventos": [
    {
      "tipo": "tarea_completada",
      "descripcion": "Tarea T1001 completada",
      "fecha": "2024-01-15T10:41:00",
      "datos_adicionales": {
        "tarea_id": "T1001",
        "alimento_id": "A1"
      }
    }
  ],
  "total": 1
}
```

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/eventos?limite=10"
```

---

## ⚙️ APIs de Procesamiento

### 22. Procesar Recolección Completa

**POST** `/procesar`

Ejecuta el proceso completo de recolección automáticamente (crea tareas, asigna hormigas, inicia y completa).

**Respuesta Exitosa (200):**
```json
{
  "message": "Proceso de recolección completado",
  "tareas_procesadas": 3,
  "tareas": [
    {
      "id": "tarea_20240115_104500",
      "alimento": {
        "id": "A1",
        "nombre": "Fruta",
        "cantidad_hormigas_necesarias": 2,
        "puntos_stock": 10,
        "tiempo_recoleccion": 60,
        "disponible": false
      },
      "hormigas_asignadas": [
        {
          "id": "H001",
          "capacidad_carga": 5,
          "estado": "activa",
          "tiempo_vida": 1000,
          "fecha_creacion": "2024-01-15T10:00:00",
          "subsistema_origen": "recoleccion"
        }
      ],
      "estado": "completada",
      "fecha_inicio": "2024-01-15T10:40:00",
      "fecha_fin": "2024-01-15T10:41:00",
      "alimento_recolectado": 10
    }
  ]
}
```

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/procesar"
```

**Ejemplo con PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/procesar" -Method POST
```

---

### 23. Verificar Hormigas Muertas

**POST** `/verificar-hormigas`

Verifica y maneja hormigas muertas en las tareas activas.

**Respuesta Exitosa (200):**
```json
{
  "message": "Verificación de hormigas completada"
}
```

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/verificar-hormigas"
```

---

## 🐛 APIs de Debug

### 24. Información de Base de Datos

**GET** `/debug/db`

Devuelve detalles del motor de BD activo y conteos básicos.

**Respuesta Exitosa (200):**
```json
{
  "engine": "sqlserver",
  "implementation": "SqlServerDatabaseManager",
  "server": "SHIRORYUU",
  "database": "Hormiguero",
  "odbc_driver": "ODBC Driver 17 for SQL Server",
  "alimentos_en_bd": 5,
  "tareas_en_bd": 10,
  "ids_tareas": ["T1001", "T1002", "T1003"]
}
```

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/debug/db"
```

---

### 25. Tareas Raw desde SQL Server

**GET** `/debug/tareas-raw`

Endpoint de depuración: muestra las tareas directamente desde SQL Server sin procesar.

**Respuesta Exitosa (200):**
```json
{
  "total_tareas": 10,
  "total_alimentos": 5,
  "alimento_ids_en_tareas": ["1", "2", "3"],
  "alimentos_encontrados": ["1", "2", "3"],
  "tareas_raw": [
    {
      "id": "T1001",
      "alimento_id": 1,
      "estado": "completada",
      "inicio": "2024-01-15T10:40:00",
      "fin": "2024-01-15T10:41:00",
      "cantidad_recolectada": 10
    }
  ]
}
```

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/debug/tareas-raw"
```

---

## 🔄 Flujo Completo de Ejemplo

### Escenario: Crear, Asignar, Iniciar y Monitorear una Tarea

**Paso 1: Verificar salud del servicio**
```bash
curl -X GET "http://localhost:8000/health"
```

**Paso 2: Consultar alimentos disponibles**
```bash
curl -X GET "http://localhost:8000/alimentos?estado=disponible"
```

**Paso 3: Crear una tarea**
```bash
curl -X POST "http://localhost:8000/tareas" \
  -H "Content-Type: application/json" \
  -d '{
    "tarea_id": "T1001",
    "alimento_id": "A1"
  }'
```

**Paso 4: Asignar hormigas e iniciar automáticamente**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_001",
    "cantidad": 2
  }'
```

**Paso 5: Verificar estado de la tarea**
```bash
curl -X GET "http://localhost:8000/tareas/T1001/status"
```

**Paso 6: Monitorear tiempo restante**
```bash
curl -X GET "http://localhost:8000/tareas/T1001/tiempo-restante"
```

**Paso 7: Verificar estado nuevamente (se completará automáticamente si pasó el tiempo)**
```bash
curl -X GET "http://localhost:8000/tareas/T1001/status"
```

**Paso 8: Ver todas las tareas**
```bash
curl -X GET "http://localhost:8000/tareas/status"
```

---

## 📌 Notas Importantes

### Validaciones y Reglas de Negocio

1. **Alimentos Disponibles:**
   - No se pueden crear tareas para alimentos no disponibles (`disponible: false`)
   - Al completar una tarea, el alimento se marca automáticamente como no disponible

2. **Asignación de Hormigas:**
   - Una tarea requiere un número mínimo de hormigas según `cantidad_hormigas_necesarias` del alimento
   - Si se proporciona `hormigas_lote_id` en `asignar-hormigas` y hay suficientes hormigas, la tarea se inicia automáticamente

3. **Inicio de Tareas:**
   - Requiere que la tarea tenga suficientes hormigas asignadas
   - Requiere proporcionar un `hormigas_lote_id`

4. **Completado Automático:**
   - Las tareas en proceso se completan automáticamente cuando `fecha_actual >= fecha_inicio + tiempo_recoleccion`
   - El `fecha_fin` se establece como `fecha_inicio + tiempo_recoleccion` (no la hora actual de verificación)

5. **Estados de Tarea:**
   - `pendiente`: Tarea creada pero no iniciada
   - `en_proceso`: Tarea iniciada y en ejecución
   - `completada`: Tarea finalizada
   - `pausada`: Tarea pausada por falta de hormigas vivas

### Códigos de Estado HTTP

- `200`: Operación exitosa
- `400`: Error de validación o regla de negocio
- `404`: Recurso no encontrado
- `500`: Error interno del servidor

---

## 🔗 Integración con Otros Subsistemas

### Campos Importantes para Compartir

Los endpoints `/tareas/status` y `/tareas/{tarea_id}/status` están diseñados para compartir información con otros subsistemas:

- `tarea_id`: ID único de la tarea
- `hormigas_lote_id`: ID del lote de hormigas asignado (para coordinación con el subsistema de hormigas)
- `alimento.id`: ID del alimento (para coordinación con el subsistema de entorno)
- `estado`: Estado actual de la tarea
- `inicio` y `fin`: Fechas de inicio y finalización en formato ISO 8601

---

## 📞 Soporte

Para más información o reportar problemas, consulta la documentación del proyecto o contacta al equipo de desarrollo.

---

**Última actualización:** 2024-01-15  
**Versión del documento:** 1.0.0


