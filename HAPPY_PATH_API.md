# 🎯 Happy Path - Flujo Completo de Ejecución de APIs

Este documento muestra el flujo completo y exitoso de uso de todas las APIs del subsistema de recolección, desde la creación de un alimento hasta la verificación del estado final.

---

## 📋 Índice del Flujo

1. [Verificar Salud del Servicio](#1-verificar-salud-del-servicio)
2. [Crear un Alimento](#2-crear-un-alimento)
3. [Consultar Alimentos Disponibles](#3-consultar-alimentos-disponibles)
4. [Crear una Tarea de Recolección](#4-crear-una-tarea-de-recolección)
5. [Asignar Hormigas a la Tarea](#5-asignar-hormigas-a-la-tarea)
6. [Iniciar la Tarea](#6-iniciar-la-tarea)
7. [Verificar Estado de la Tarea](#7-verificar-estado-de-la-tarea)
8. [Monitorear Tiempo Restante](#8-monitorear-tiempo-restante)
9. [Verificar Estado Nuevamente (Completado Automático)](#9-verificar-estado-nuevamente-completado-automático)
10. [Consultar Todas las Tareas](#10-consultar-todas-las-tareas)
11. [Verificar Estadísticas](#11-verificar-estadísticas)

---

## 🚀 Flujo Completo Paso a Paso

### 1. Verificar Salud del Servicio

**Endpoint:**
```
GET http://localhost:8000/health
```

**Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Response Exitosa (200):**
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

### 2. Crear un Alimento

**Endpoint:**
```
POST http://localhost:8000/alimentos
```

**Request:**
```bash
curl -X POST "http://localhost:8000/alimentos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Fruta Tropical",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 15,
    "tiempo_recoleccion": 120,
    "disponible": true
  }'
```

**Response Exitosa (200):**
```json
{
  "id": "A20240115143000",
  "nombre": "Fruta Tropical",
  "cantidad_hormigas_necesarias": 2,
  "puntos_stock": 15,
  "tiempo_recoleccion": 120,
  "disponible": true,
  "fecha_creacion": "2024-01-15T14:30:00"
}
```

**💡 Guarda el `id` del alimento** (ejemplo: `A20240115143000`) para usarlo en el siguiente paso.

---

### 3. Consultar Alimentos Disponibles

**Endpoint:**
```
GET http://localhost:8000/alimentos?estado=disponible
```

**Request:**
```bash
curl -X GET "http://localhost:8000/alimentos?estado=disponible"
```

**Response Exitosa (200):**
```json
[
  {
    "id": "A20240115143000",
    "nombre": "Fruta Tropical",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 15,
    "tiempo_recoleccion": 120,
    "disponible": true,
    "fecha_creacion": "2024-01-15T14:30:00"
  },
  {
    "id": "A1",
    "nombre": "Fruta",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 10,
    "tiempo_recoleccion": 60,
    "disponible": true,
    "fecha_creacion": "2024-01-15T10:00:00"
  }
]
```

---

### 4. Crear una Tarea de Recolección

**Endpoint:**
```
POST http://localhost:8000/tareas
```

**Request:**
```bash
curl -X POST "http://localhost:8000/tareas" \
  -H "Content-Type: application/json" \
  -d '{
    "tarea_id": "T1001",
    "alimento_id": "A20240115143000"
  }'
```

**Response Exitosa (200):**
```json
{
  "id": "T1001",
  "alimento": {
    "id": "A20240115143000",
    "nombre": "Fruta Tropical",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 15,
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

**💡 Guarda el `id` de la tarea** (ejemplo: `T1001`) para los siguientes pasos.

---

### 5. Asignar Hormigas a la Tarea

**Endpoint:**
```
POST http://localhost:8000/tareas/T1001/asignar-hormigas
```

**Request:**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_001",
    "cantidad": 2
  }'
```

**Response Exitosa (200) - Con inicio automático:**
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

**💡 Nota:** Si la tarea se inicia automáticamente, puedes saltar al paso 7. Si no, continúa con el paso 6.

---

### 6. Iniciar la Tarea

**⚠️ Solo necesario si la tarea NO se inició automáticamente en el paso anterior.**

**Endpoint:**
```
POST http://localhost:8000/tareas/T1001/iniciar
```

**Request:**
```bash
curl -X POST "http://localhost:8000/tareas/T1001/iniciar" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_001"
  }'
```

**Response Exitosa (200):**
```json
{
  "message": "Tarea T1001 iniciada exitosamente",
  "tarea_id": "T1001",
  "estado": "en_proceso",
  "hormigas_asignadas": 2,
  "hormigas_lote_id": "LOTE_001"
}
```

---

### 7. Verificar Estado de la Tarea

**Endpoint:**
```
GET http://localhost:8000/tareas/T1001/status
```

**Request:**
```bash
curl -X GET "http://localhost:8000/tareas/T1001/status"
```

**Response Exitosa (200):**
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
    "id": "A20240115143000",
    "nombre": "Fruta Tropical"
  },
  "hormigas_lote_id": "LOTE_001",
  "inicio": "2024-01-15T14:35:00",
  "fin": null,
  "alimento_recolectado": 0
}
```

---

### 8. Monitorear Tiempo Restante

**Endpoint:**
```
GET http://localhost:8000/tareas/T1001/tiempo-restante
```

**Request:**
```bash
curl -X GET "http://localhost:8000/tareas/T1001/tiempo-restante"
```

**Response Exitosa (200):**
```json
{
  "tarea_id": "T1001",
  "tiempo_total_asignado_segundos": 120,
  "tiempo_total_asignado_minutos": 2.0,
  "tiempo_restante_segundos": 95,
  "tiempo_restante_minutos": 1.58,
  "tiempo_transcurrido_segundos": 25,
  "progreso_porcentaje": 20.83
}
```

**💡 Puedes consultar este endpoint varias veces para monitorear el progreso.**

---

### 9. Verificar Estado Nuevamente (Completado Automático)

**💡 Espera al menos 120 segundos (tiempo_recoleccion) o ajusta el tiempo en el alimento para pruebas más rápidas.**

**Endpoint:**
```
GET http://localhost:8000/tareas/T1001/status
```

**Request:**
```bash
curl -X GET "http://localhost:8000/tareas/T1001/status"
```

**Response Exitosa (200) - Tarea Completada:**
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
    "id": "A20240115143000",
    "nombre": "Fruta Tropical"
  },
  "hormigas_lote_id": "LOTE_001",
  "inicio": "2024-01-15T14:35:00",
  "fin": "2024-01-15T14:37:00",
  "alimento_recolectado": 0
}
```

**💡 Nota:** El sistema completa automáticamente la tarea cuando `fecha_actual >= fecha_inicio + tiempo_recoleccion`. El `fecha_fin` se establece como `fecha_inicio + tiempo_recoleccion` (no la hora actual de verificación).

---

### 10. Consultar Todas las Tareas

**Endpoint:**
```
GET http://localhost:8000/tareas/status
```

**Request:**
```bash
curl -X GET "http://localhost:8000/tareas/status"
```

**Response Exitosa (200):**
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
      "tarea_id": "T1001",
      "estado": "completada",
      "alimento": {
        "id": "A20240115143000",
        "nombre": "Fruta Tropical"
      },
      "hormigas_lote_id": "LOTE_001",
      "inicio": "2024-01-15T14:35:00",
      "fin": "2024-01-15T14:37:00",
      "alimento_recolectado": 0
    }
  ]
}
```

---

### 11. Verificar Estadísticas

**Endpoint:**
```
GET http://localhost:8000/estadisticas
```

**Request:**
```bash
curl -X GET "http://localhost:8000/estadisticas"
```

**Response Exitosa (200):**
```json
{
  "tareas_activas": 0,
  "tareas_completadas": 1,
  "total_alimentos_recolectados": 0,
  "base_datos": {
    "total_alimentos": 3,
    "total_tareas": 1
  },
  "tareas_memoria": {
    "activas": 0,
    "completadas": 1
  }
}
```

---

## 📝 Script Completo en PowerShell

Aquí tienes un script completo de PowerShell que ejecuta todo el flujo:

```powershell
# Configurar URL base
$baseUrl = "http://localhost:8000"

Write-Host "=== Happy Path - Flujo Completo de APIs ===" -ForegroundColor Green

# 1. Health Check
Write-Host "`n1. Verificando salud del servicio..." -ForegroundColor Yellow
$health = Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
Write-Host "Status: $($health.status)" -ForegroundColor Green

# 2. Crear Alimento
Write-Host "`n2. Creando alimento..." -ForegroundColor Yellow
$alimentoBody = @{
    nombre = "Fruta Tropical"
    cantidad_hormigas_necesarias = 2
    puntos_stock = 15
    tiempo_recoleccion = 120
    disponible = $true
} | ConvertTo-Json

$alimento = Invoke-RestMethod -Uri "$baseUrl/alimentos" -Method POST -Body $alimentoBody -ContentType "application/json"
$alimentoId = $alimento.id
Write-Host "Alimento creado: $alimentoId - $($alimento.nombre)" -ForegroundColor Green

# 3. Consultar Alimentos
Write-Host "`n3. Consultando alimentos disponibles..." -ForegroundColor Yellow
$alimentos = Invoke-RestMethod -Uri "$baseUrl/alimentos?estado=disponible" -Method GET
Write-Host "Total alimentos disponibles: $($alimentos.Count)" -ForegroundColor Green

# 4. Crear Tarea
Write-Host "`n4. Creando tarea de recolección..." -ForegroundColor Yellow
$tareaBody = @{
    tarea_id = "T1001"
    alimento_id = $alimentoId
} | ConvertTo-Json

$tarea = Invoke-RestMethod -Uri "$baseUrl/tareas" -Method POST -Body $tareaBody -ContentType "application/json"
$tareaId = $tarea.id
Write-Host "Tarea creada: $tareaId - Estado: $($tarea.estado)" -ForegroundColor Green

# 5. Asignar Hormigas
Write-Host "`n5. Asignando hormigas a la tarea..." -ForegroundColor Yellow
$asignarBody = @{
    hormigas_lote_id = "LOTE_001"
    cantidad = 2
} | ConvertTo-Json

$asignacion = Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/asignar-hormigas" -Method POST -Body $asignarBody -ContentType "application/json"
Write-Host "Hormigas asignadas: $($asignacion.hormigas_asignadas)" -ForegroundColor Green
Write-Host "Estado: $($asignacion.estado)" -ForegroundColor Green
Write-Host "Iniciada: $($asignacion.iniciada)" -ForegroundColor Green

# 6. Verificar Estado
Write-Host "`n6. Verificando estado de la tarea..." -ForegroundColor Yellow
$status = Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/status" -Method GET
Write-Host "Estado: $($status.estado)" -ForegroundColor Green
Write-Host "Hormigas lote ID: $($status.hormigas_lote_id)" -ForegroundColor Green
Write-Host "Inicio: $($status.inicio)" -ForegroundColor Green

# 7. Monitorear Tiempo Restante
Write-Host "`n7. Monitoreando tiempo restante..." -ForegroundColor Yellow
$tiempo = Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/tiempo-restante" -Method GET
Write-Host "Tiempo restante: $($tiempo.tiempo_restante_segundos) segundos" -ForegroundColor Green
Write-Host "Progreso: $($tiempo.progreso_porcentaje)%" -ForegroundColor Green

# 8. Verificar Estado Final (después de esperar)
Write-Host "`n8. Esperando completado automático..." -ForegroundColor Yellow
Write-Host "Esperando 5 segundos antes de verificar estado final..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

$statusFinal = Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/status" -Method GET
Write-Host "Estado final: $($statusFinal.estado)" -ForegroundColor Green
Write-Host "Completada automáticamente: $($statusFinal.completada_automaticamente)" -ForegroundColor Green

# 9. Consultar Todas las Tareas
Write-Host "`n9. Consultando todas las tareas..." -ForegroundColor Yellow
$todasTareas = Invoke-RestMethod -Uri "$baseUrl/tareas/status" -Method GET
Write-Host "Total tareas: $($todasTareas.total_tareas)" -ForegroundColor Green
Write-Host "Tareas completadas automáticamente: $($todasTareas.tareas_completadas_automaticamente)" -ForegroundColor Green

# 10. Estadísticas
Write-Host "`n10. Consultando estadísticas..." -ForegroundColor Yellow
$stats = Invoke-RestMethod -Uri "$baseUrl/estadisticas" -Method GET
Write-Host "Tareas activas: $($stats.tareas_activas)" -ForegroundColor Green
Write-Host "Tareas completadas: $($stats.tareas_completadas)" -ForegroundColor Green

Write-Host "`n=== Happy Path Completado ===" -ForegroundColor Green
```

---

## 📝 Script Completo en Bash (cURL)

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "=== Happy Path - Flujo Completo de APIs ==="

# 1. Health Check
echo -e "\n1. Verificando salud del servicio..."
curl -s -X GET "$BASE_URL/health" | jq '.'

# 2. Crear Alimento
echo -e "\n2. Creando alimento..."
ALIMENTO_RESPONSE=$(curl -s -X POST "$BASE_URL/alimentos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Fruta Tropical",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 15,
    "tiempo_recoleccion": 120,
    "disponible": true
  }')

ALIMENTO_ID=$(echo $ALIMENTO_RESPONSE | jq -r '.id')
echo "Alimento creado: $ALIMENTO_ID"
echo $ALIMENTO_RESPONSE | jq '.'

# 3. Consultar Alimentos
echo -e "\n3. Consultando alimentos disponibles..."
curl -s -X GET "$BASE_URL/alimentos?estado=disponible" | jq '.'

# 4. Crear Tarea
echo -e "\n4. Creando tarea de recolección..."
TAREA_RESPONSE=$(curl -s -X POST "$BASE_URL/tareas" \
  -H "Content-Type: application/json" \
  -d "{
    \"tarea_id\": \"T1001\",
    \"alimento_id\": \"$ALIMENTO_ID\"
  }")

TAREA_ID=$(echo $TAREA_RESPONSE | jq -r '.id')
echo "Tarea creada: $TAREA_ID"
echo $TAREA_RESPONSE | jq '.'

# 5. Asignar Hormigas
echo -e "\n5. Asignando hormigas a la tarea..."
ASIGNACION_RESPONSE=$(curl -s -X POST "$BASE_URL/tareas/$TAREA_ID/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_001",
    "cantidad": 2
  }')
echo $ASIGNACION_RESPONSE | jq '.'

# 6. Verificar Estado
echo -e "\n6. Verificando estado de la tarea..."
curl -s -X GET "$BASE_URL/tareas/$TAREA_ID/status" | jq '.'

# 7. Monitorear Tiempo Restante
echo -e "\n7. Monitoreando tiempo restante..."
curl -s -X GET "$BASE_URL/tareas/$TAREA_ID/tiempo-restante" | jq '.'

# 8. Esperar y verificar estado final
echo -e "\n8. Esperando completado automático..."
echo "Esperando 5 segundos..."
sleep 5

echo -e "\nVerificando estado final..."
curl -s -X GET "$BASE_URL/tareas/$TAREA_ID/status" | jq '.'

# 9. Consultar Todas las Tareas
echo -e "\n9. Consultando todas las tareas..."
curl -s -X GET "$BASE_URL/tareas/status" | jq '.'

# 10. Estadísticas
echo -e "\n10. Consultando estadísticas..."
curl -s -X GET "$BASE_URL/estadisticas" | jq '.'

echo -e "\n=== Happy Path Completado ==="
```

---

## 🎯 Flujo Alternativo: Procesamiento Automático

Si prefieres un proceso más automatizado, puedes usar el endpoint `/procesar`:

**Endpoint:**
```
POST http://localhost:8000/procesar
```

**Request:**
```bash
curl -X POST "http://localhost:8000/procesar"
```

Este endpoint ejecuta automáticamente:
- Crea tareas para alimentos disponibles
- Asigna hormigas
- Inicia las tareas
- Completa las tareas

---

## 📊 Diagrama del Flujo

```
┌─────────────────┐
│  Health Check   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Crear Alimento  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Consultar       │
│ Alimentos       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Crear Tarea     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Asignar         │
│ Hormigas        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Iniciar Tarea   │ (opcional si se inició automáticamente)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Verificar       │
│ Estado          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Monitorear      │
│ Tiempo          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Verificar       │
│ Estado Final    │ (completado automático)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Consultar       │
│ Todas Tareas    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Estadísticas    │
└─────────────────┘
```

---

## ⚠️ Notas Importantes

1. **IDs Generados:** Algunos IDs se generan automáticamente. Guarda los IDs de las respuestas para usarlos en pasos posteriores.

2. **Tiempo de Recolección:** Para pruebas más rápidas, puedes crear alimentos con `tiempo_recoleccion` menor (ej: 10 segundos).

3. **Completado Automático:** El sistema completa automáticamente las tareas cuando `fecha_actual >= fecha_inicio + tiempo_recoleccion`.

4. **Alimentos No Disponibles:** Una vez que un alimento es recolectado, su flag `disponible` se establece en `false` y no se pueden crear nuevas tareas para él.

5. **Asignación Automática:** Si proporcionas `hormigas_lote_id` en `asignar-hormigas` y hay suficientes hormigas, la tarea se inicia automáticamente.

---

**Última actualización:** 2024-01-15


