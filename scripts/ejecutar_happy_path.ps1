# Script para ejecutar el Happy Path completo de las APIs
# Uso: .\scripts\ejecutar_happy_path.ps1

param(
    [string]$BaseUrl = "http://localhost:8000",
    [int]$TiempoRecoleccion = 10  # Tiempo en segundos para pruebas rápidas
)

Write-Host "=== Happy Path - Flujo Completo de APIs ===" -ForegroundColor Green
Write-Host "Base URL: $BaseUrl" -ForegroundColor Cyan
Write-Host "Tiempo de recolección: $TiempoRecoleccion segundos" -ForegroundColor Cyan
Write-Host ""

# Función para hacer requests con manejo de errores
function Invoke-SafeRestMethod {
    param(
        [string]$Uri,
        [string]$Method = "GET",
        [object]$Body = $null,
        [string]$ContentType = "application/json"
    )
    
    try {
        if ($Body) {
            $jsonBody = $Body | ConvertTo-Json -Depth 10
            return Invoke-RestMethod -Uri $Uri -Method $Method -Body $jsonBody -ContentType $ContentType
        } else {
            return Invoke-RestMethod -Uri $Uri -Method $Method
        }
    } catch {
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Response) {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            Write-Host "Response: $responseBody" -ForegroundColor Red
        }
        throw
    }
}

try {
    # 1. Health Check
    Write-Host "1. Verificando salud del servicio..." -ForegroundColor Yellow
    $health = Invoke-SafeRestMethod -Uri "$BaseUrl/health" -Method GET
    Write-Host "   Status: $($health.status)" -ForegroundColor Green
    Write-Host ""

    # 2. Crear Alimento
    Write-Host "2. Creando alimento..." -ForegroundColor Yellow
    $alimentoBody = @{
        nombre = "Fruta Tropical"
        cantidad_hormigas_necesarias = 2
        puntos_stock = 15
        tiempo_recoleccion = $TiempoRecoleccion
        disponible = $true
    }
    
    $alimento = Invoke-SafeRestMethod -Uri "$BaseUrl/alimentos" -Method POST -Body $alimentoBody
    $alimentoId = $alimento.id
    Write-Host "   Alimento creado: $alimentoId - $($alimento.nombre)" -ForegroundColor Green
    Write-Host "   Requiere $($alimento.cantidad_hormigas_necesarias) hormigas" -ForegroundColor Cyan
    Write-Host "   Tiempo de recolección: $($alimento.tiempo_recoleccion) segundos" -ForegroundColor Cyan
    Write-Host ""

    # 3. Consultar Alimentos
    Write-Host "3. Consultando alimentos disponibles..." -ForegroundColor Yellow
    $alimentos = Invoke-SafeRestMethod -Uri "$BaseUrl/alimentos?estado=disponible" -Method GET
    Write-Host "   Total alimentos disponibles: $($alimentos.Count)" -ForegroundColor Green
    Write-Host ""

    # 4. Crear Tarea
    Write-Host "4. Creando tarea de recolección..." -ForegroundColor Yellow
    $tareaBody = @{
        tarea_id = "T1001"
        alimento_id = $alimentoId
    }
    
    $tarea = Invoke-SafeRestMethod -Uri "$BaseUrl/tareas" -Method POST -Body $tareaBody
    $tareaId = $tarea.id
    Write-Host "   Tarea creada: $tareaId" -ForegroundColor Green
    Write-Host "   Estado inicial: $($tarea.estado)" -ForegroundColor Cyan
    Write-Host ""

    # 5. Asignar Hormigas
    Write-Host "5. Asignando hormigas a la tarea..." -ForegroundColor Yellow
    $asignarBody = @{
        hormigas_lote_id = "LOTE_001"
        cantidad = 2
    }
    
    $asignacion = Invoke-SafeRestMethod -Uri "$BaseUrl/tareas/$tareaId/asignar-hormigas" -Method POST -Body $asignarBody
    Write-Host "   Hormigas asignadas: $($asignacion.hormigas_asignadas)" -ForegroundColor Green
    Write-Host "   Hormigas requeridas: $($asignacion.hormigas_requeridas)" -ForegroundColor Cyan
    Write-Host "   Estado: $($asignacion.estado)" -ForegroundColor Green
    Write-Host "   Iniciada automáticamente: $($asignacion.iniciada)" -ForegroundColor $(if ($asignacion.iniciada) { "Green" } else { "Yellow" })
    Write-Host ""

    # 6. Iniciar Tarea (solo si no se inició automáticamente)
    if (-not $asignacion.iniciada) {
        Write-Host "6. Iniciando la tarea..." -ForegroundColor Yellow
        $iniciarBody = @{
            hormigas_lote_id = "LOTE_001"
        }
        
        $inicio = Invoke-SafeRestMethod -Uri "$BaseUrl/tareas/$tareaId/iniciar" -Method POST -Body $iniciarBody
        Write-Host "   Tarea iniciada exitosamente" -ForegroundColor Green
        Write-Host "   Estado: $($inicio.estado)" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "6. Tarea ya iniciada automáticamente, saltando paso de inicio..." -ForegroundColor Cyan
        Write-Host ""
    }

    # 7. Verificar Estado
    Write-Host "7. Verificando estado de la tarea..." -ForegroundColor Yellow
    $status = Invoke-SafeRestMethod -Uri "$BaseUrl/tareas/$tareaId/status" -Method GET
    Write-Host "   Estado: $($status.estado)" -ForegroundColor Green
    Write-Host "   Hormigas lote ID: $($status.hormigas_lote_id)" -ForegroundColor Cyan
    Write-Host "   Inicio: $($status.inicio)" -ForegroundColor Cyan
    Write-Host "   Fin: $($status.fin)" -ForegroundColor Cyan
    Write-Host ""

    # 8. Monitorear Tiempo Restante
    Write-Host "8. Monitoreando tiempo restante..." -ForegroundColor Yellow
    try {
        $tiempo = Invoke-SafeRestMethod -Uri "$BaseUrl/tareas/$tareaId/tiempo-restante" -Method GET
        Write-Host "   Tiempo total: $($tiempo.tiempo_total_asignado_segundos) segundos" -ForegroundColor Cyan
        Write-Host "   Tiempo restante: $($tiempo.tiempo_restante_segundos) segundos" -ForegroundColor Green
        Write-Host "   Progreso: $($tiempo.progreso_porcentaje)%" -ForegroundColor Green
        Write-Host ""
    } catch {
        Write-Host "   No se pudo obtener tiempo restante (puede que la tarea ya esté completada)" -ForegroundColor Yellow
        Write-Host ""
    }

    # 9. Esperar y verificar estado final
    Write-Host "9. Esperando completado automático..." -ForegroundColor Yellow
    Write-Host "   Esperando $($TiempoRecoleccion + 2) segundos para que se complete la tarea..." -ForegroundColor Cyan
    Start-Sleep -Seconds ($TiempoRecoleccion + 2)

    Write-Host "   Verificando estado final..." -ForegroundColor Cyan
    $statusFinal = Invoke-SafeRestMethod -Uri "$BaseUrl/tareas/$tareaId/status" -Method GET
    Write-Host "   Estado final: $($statusFinal.estado)" -ForegroundColor Green
    Write-Host "   Completada automáticamente: $($statusFinal.completada_automaticamente)" -ForegroundColor $(if ($statusFinal.completada_automaticamente) { "Green" } else { "Yellow" })
    Write-Host "   Inicio: $($statusFinal.inicio)" -ForegroundColor Cyan
    Write-Host "   Fin: $($statusFinal.fin)" -ForegroundColor Cyan
    Write-Host ""

    # 10. Consultar Todas las Tareas
    Write-Host "10. Consultando todas las tareas..." -ForegroundColor Yellow
    $todasTareas = Invoke-SafeRestMethod -Uri "$BaseUrl/tareas/status" -Method GET
    Write-Host "   Total tareas: $($todasTareas.total_tareas)" -ForegroundColor Green
    Write-Host "   Tareas completadas automáticamente: $($todasTareas.tareas_completadas_automaticamente)" -ForegroundColor Green
    Write-Host ""

    # 11. Estadísticas
    Write-Host "11. Consultando estadísticas..." -ForegroundColor Yellow
    $stats = Invoke-SafeRestMethod -Uri "$BaseUrl/estadisticas" -Method GET
    Write-Host "   Tareas activas: $($stats.tareas_activas)" -ForegroundColor Green
    Write-Host "   Tareas completadas: $($stats.tareas_completadas)" -ForegroundColor Green
    Write-Host ""

    Write-Host "=== Happy Path Completado Exitosamente ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Resumen:" -ForegroundColor Cyan
    Write-Host "  - Alimento creado: $alimentoId" -ForegroundColor White
    Write-Host "  - Tarea creada: $tareaId" -ForegroundColor White
    Write-Host "  - Estado final: $($statusFinal.estado)" -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "=== ERROR EN EL FLUJO ===" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    exit 1
}


