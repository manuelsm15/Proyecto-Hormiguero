# Guía de Comandos para Probar la API desde CMD/PowerShell

## Requisitos Previos

Asegúrate de tener el servidor corriendo:
```powershell
python main.py
```

O si usas Railway, usa tu URL pública.

---

## Variables de Entorno

Define tu URL base (ajusta según tu entorno):

```powershell
# Para localhost
$baseUrl = "http://localhost:8000"

# Para Railway (reemplaza con tu URL real)
# $baseUrl = "https://TU_DOMINIO.railway.app"
```

---

## PRUEBAS GET - Endpoints de Consulta

### 1. Health Check
```powershell
Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
```

### 2. Información del Servicio
```powershell
Invoke-RestMethod -Uri "$baseUrl/" -Method GET
```

### 3. Listar Alimentos (sin filtros)
```powershell
Invoke-RestMethod -Uri "$baseUrl/alimentos" -Method GET
```

### 3.1. Alimentos por Zona
```powershell
Invoke-RestMethod -Uri "$baseUrl/alimentos?zona_id=1" -Method GET
```

### 3.2. Alimentos por Estado
```powershell
Invoke-RestMethod -Uri "$baseUrl/alimentos?estado=disponible" -Method GET
```

### 4. Listar Todas las Tareas
```powershell
Invoke-RestMethod -Uri "$baseUrl/tareas" -Method GET
```

### 5. Tareas Activas
```powershell
Invoke-RestMethod -Uri "$baseUrl/tareas/activas" -Method GET
```

### 6. Tareas Completadas
```powershell
Invoke-RestMethod -Uri "$baseUrl/tareas/completadas" -Method GET
```

### 7. Tareas en Proceso
```powershell
Invoke-RestMethod -Uri "$baseUrl/tareas/en-proceso" -Method GET
```

### 8. Estadísticas
```powershell
Invoke-RestMethod -Uri "$baseUrl/estadisticas" -Method GET
```

### 9. Tareas desde Base de Datos
```powershell
Invoke-RestMethod -Uri "$baseUrl/tareas/bd" -Method GET
```

### 10. Eventos Recientes
```powershell
Invoke-RestMethod -Uri "$baseUrl/eventos?limite=10" -Method GET
```

### 11. Tarea Específica por ID
```powershell
# Reemplaza TAREA_ID con un ID real
$tareaId = "tarea_20251029_182356"
Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/bd" -Method GET
```

### 12. Tiempo Restante de Tarea
```powershell
$tareaId = "tarea_20251029_182356"
Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/tiempo-restante" -Method GET
```

### 13. Progreso de Tarea
```powershell
$tareaId = "tarea_20251029_182356"
Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/progreso" -Method GET
```

---

## PRUEBAS POST - Creación y Modificación

### 1. Crear Tarea (con valores por defecto)
```powershell
Invoke-RestMethod -Uri "$baseUrl/tareas" -Method POST
```

### 2. Crear Tarea con Parámetros Específicos
```powershell
# Con tarea_id y alimento_id
Invoke-RestMethod -Uri "$baseUrl/tareas?tarea_id=tarea_test_001&alimento_id=A1" -Method POST

# Solo tarea_id
Invoke-RestMethod -Uri "$baseUrl/tareas?tarea_id=mi_tarea_001" -Method POST

# Solo alimento_id
Invoke-RestMethod -Uri "$baseUrl/tareas?alimento_id=A2" -Method POST
```

### 3. Iniciar Tarea
```powershell
$tareaId = "tarea_test_001"
Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/iniciar" -Method POST
```

### 4. Procesar Recolección Completa
```powershell
Invoke-RestMethod -Uri "$baseUrl/procesar" -Method POST
```

### 5. Completar Tarea
```powershell
$tareaId = "tarea_test_001"
$cantidad = 10
Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/completar?cantidad_recolectada=$cantidad" -Method POST
```

### 6. Verificar Hormigas Muertas
```powershell
Invoke-RestMethod -Uri "$baseUrl/verificar-hormigas" -Method POST
```

### 7. Cancelar Tarea
```powershell
$tareaId = "tarea_test_001"
Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/cancelar" -Method POST
```

---

## Ejemplos de Flujo Completo

### Flujo 1: Crear → Iniciar → Completar Tarea

```powershell
# 1. Crear tarea
$response = Invoke-RestMethod -Uri "$baseUrl/tareas?tarea_id=mi_tarea&alimento_id=A1" -Method POST
$tareaId = $response.id
Write-Host "Tarea creada: $tareaId"

# 2. Iniciar tarea
Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/iniciar" -Method POST
Write-Host "Tarea iniciada"

# 3. Ver progreso (opcional)
Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/progreso" -Method GET

# 4. Completar tarea
Invoke-RestMethod -Uri "$baseUrl/tareas/$tareaId/completar?cantidad_recolectada=10" -Method POST
Write-Host "Tarea completada"
```

### Flujo 2: Consultar → Procesar → Ver Estadísticas

```powershell
# 1. Ver alimentos disponibles
Invoke-RestMethod -Uri "$baseUrl/alimentos" -Method GET

# 2. Ejecutar proceso completo
Invoke-RestMethod -Uri "$baseUrl/procesar" -Method POST

# 3. Ver tareas creadas
Invoke-RestMethod -Uri "$baseUrl/tareas" -Method GET

# 4. Ver estadísticas
Invoke-RestMethod -Uri "$baseUrl/estadisticas" -Method GET
```

---

## Alternativa con cURL (si está instalado)

### GET
```powershell
# Health check
curl.exe -X GET "$baseUrl/health"

# Alimentos
curl.exe -X GET "$baseUrl/alimentos"

# Tareas
curl.exe -X GET "$baseUrl/tareas"
```

### POST
```powershell
# Crear tarea
curl.exe -X POST "$baseUrl/tareas"

# Crear tarea con parámetros
curl.exe -X POST "$baseUrl/tareas?tarea_id=test&alimento_id=A1"

# Procesar
curl.exe -X POST "$baseUrl/procesar"
```

---

## Ver Respuestas Formateadas

Para ver las respuestas JSON de forma más legible, puedes usar:

```powershell
# Método 1: Convertir a JSON formateado
$response = Invoke-RestMethod -Uri "$baseUrl/tareas" -Method GET
$response | ConvertTo-Json -Depth 10

# Método 2: Usar Format-List
$response | Format-List

# Método 3: Filtrar campos específicos
$response | Select-Object id, estado, alimento | Format-Table
```

---

## Manejo de Errores

Si encuentras errores, puedes ver más detalles con:

```powershell
try {
    Invoke-RestMethod -Uri "$baseUrl/tareas/invalid_id" -Method GET
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    Write-Host "Status: $($_.Exception.Response.StatusCode.value__)"
}
```

---

## Notas Importantes

1. **IDs de Tarea**: Los IDs se generan automáticamente si no los proporcionas. Guarda el ID de la respuesta para usarlo en operaciones posteriores.

2. **Alimentos Disponibles**: Los IDs de alimentos son: `A1` (Fruta), `A2` (Semilla), `A3` (Hoja)

3. **Estados de Tarea**: `pendiente` → `en_proceso` → `completada`

4. **Procesar**: El endpoint `/procesar` ejecuta todo el flujo automáticamente y puede tardar unos segundos.

5. **Para Railway**: Cambia `$baseUrl` por tu URL de Railway cuando quieras probar en producción.

