# Script para iniciar el servidor FastAPI del subsistema de recolección

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Iniciando Servidor de Recoleccion" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del proyecto
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

# Verificar que el puerto 8000 esté disponible
$portInUse = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "ADVERTENCIA: El puerto 8000 ya está en uso!" -ForegroundColor Yellow
    Write-Host "Por favor, cierra el proceso que está usando el puerto 8000" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Proceso usando el puerto:" -ForegroundColor Yellow
    Get-Process -Id ($portInUse.OwningProcess) | Select-Object Id, ProcessName
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "Iniciando servidor en http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Para detener el servidor, presiona Ctrl+C" -ForegroundColor Yellow
Write-Host ""

python main.py

