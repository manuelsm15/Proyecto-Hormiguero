# Script para iniciar el servidor y ejecutar las pruebas automáticamente

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Iniciar Servidor y Ejecutar Pruebas" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del proyecto
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

# Verificar si el servicio ya está corriendo
$portInUse = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
$serverJob = $null
$serverStartedByScript = $false

if ($portInUse) {
    Write-Host "El puerto 8000 ya está en uso. Verificando si el servicio está disponible..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction Stop
        if ($response.status -eq "healthy") {
            Write-Host "[OK] Servicio ya está corriendo y disponible" -ForegroundColor Green
            $serverReady = $true
        } else {
            Write-Host "El servicio no está respondiendo correctamente. Iniciando nuevo servidor..." -ForegroundColor Yellow
            $serverReady = $false
        }
    } catch {
        Write-Host "El servicio no está disponible. Iniciando nuevo servidor..." -ForegroundColor Yellow
        $serverReady = $false
    }
} else {
    $serverReady = $false
}

# Si el servicio no está disponible, iniciarlo
if (-not $serverReady) {
    Write-Host "Iniciando servidor en segundo plano..." -ForegroundColor Green
    Write-Host ""
    
    # Iniciar servidor en segundo plano
    $serverJob = Start-Job -ScriptBlock {
        Set-Location $using:projectRoot
        python main.py
    }
    $serverStartedByScript = $true
    
    # Esperar a que el servidor inicie
    Write-Host "Esperando a que el servidor inicie..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Verificar que el servidor esté disponible
    $maxRetries = 10
    $retryCount = 0
    $serverReady = $false
    
    while ($retryCount -lt $maxRetries -and -not $serverReady) {
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction Stop
            if ($response.status -eq "healthy") {
                $serverReady = $true
                Write-Host "[OK] Servidor iniciado correctamente" -ForegroundColor Green
            }
        } catch {
            $retryCount++
            Write-Host "  Intento $retryCount/$maxRetries..." -ForegroundColor Yellow
            Start-Sleep -Seconds 2
        }
    }
    
    if (-not $serverReady) {
        Write-Host "ERROR: No se pudo conectar al servidor después de $maxRetries intentos" -ForegroundColor Red
        if ($serverJob) {
            Stop-Job $serverJob
            Remove-Job $serverJob
        }
        exit 1
    }
}

Write-Host ""
Write-Host "Ejecutando pruebas..." -ForegroundColor Green
Write-Host ""

# Ejecutar pruebas
python scripts/prueba_completa_sistema_lotes.py

$testExitCode = $LASTEXITCODE

Write-Host ""
# Solo detener el servidor si lo iniciamos nosotros
if ($serverStartedByScript -and $serverJob) {
    Write-Host "Deteniendo servidor..." -ForegroundColor Yellow
    Stop-Job $serverJob
    Remove-Job $serverJob
} else {
    Write-Host "El servidor no fue iniciado por este script. No se detendrá." -ForegroundColor Cyan
}

Write-Host ""
if ($testExitCode -eq 0) {
    Write-Host "[OK] Pruebas completadas exitosamente" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Algunas pruebas fallaron" -ForegroundColor Red
}

Write-Host ""
Write-Host "Resultados guardados en: allure-results/" -ForegroundColor Cyan
Write-Host "Para generar el reporte HTML:" -ForegroundColor Cyan
Write-Host "  python scripts/generate_allure_report.py" -ForegroundColor Cyan

exit $testExitCode

