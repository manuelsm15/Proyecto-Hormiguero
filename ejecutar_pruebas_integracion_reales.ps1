# Script PowerShell para ejecutar pruebas de integración reales
# Inicia el servicio y ejecuta las pruebas

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PRUEBAS DE INTEGRACION REALES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Verificar si el servicio ya está corriendo
$serviceRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "[INFO] Servicio ya está corriendo" -ForegroundColor Yellow
        $serviceRunning = $true
    }
} catch {
    Write-Host "[INFO] Servicio no está corriendo, iniciando..." -ForegroundColor Yellow
}

# Iniciar servicio si no está corriendo
$process = $null
if (-not $serviceRunning) {
    Write-Host "[INFO] Iniciando servicio FastAPI..." -ForegroundColor Yellow
    $process = Start-Process -FilePath "python" -ArgumentList "main.py" -PassThru -NoNewWindow
    Start-Sleep -Seconds 5
    
    # Verificar que el servicio inició
    $maxRetries = 10
    $retry = 0
    while ($retry -lt $maxRetries) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Host "[OK] Servicio iniciado correctamente" -ForegroundColor Green
                break
            }
        } catch {
            $retry++
            Start-Sleep -Seconds 1
        }
    }
    
    if ($retry -eq $maxRetries) {
        Write-Host "[ERROR] No se pudo iniciar el servicio" -ForegroundColor Red
        exit 1
    }
}

# Ejecutar pruebas
Write-Host ""
Write-Host "[INFO] Ejecutando pruebas de integración reales..." -ForegroundColor Yellow
python test_integracion_real_completo.py

# Guardar código de salida
$exitCode = $LASTEXITCODE

# Detener servicio si lo iniciamos
if ($process -and -not $serviceRunning) {
    Write-Host ""
    Write-Host "[INFO] Deteniendo servicio..." -ForegroundColor Yellow
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Servicio detenido" -ForegroundColor Green
}

exit $exitCode



