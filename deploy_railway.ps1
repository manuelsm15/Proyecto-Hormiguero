# Script de Deployment para Railway
# Ejecuta: .\deploy_railway.ps1

Write-Host "🚂 Railway Deployment Script" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""

# Verificar que Railway CLI esté instalado
if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Railway CLI no está instalado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Instálalo con uno de estos métodos:" -ForegroundColor Yellow
    Write-Host "  1. npm i -g @railway/cli" -ForegroundColor White
    Write-Host "  2. iwr https://railway.app/install.ps1 | iex" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ Railway CLI encontrado" -ForegroundColor Green
railway --version
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "railway.toml")) {
    Write-Host "❌ No se encontró railway.toml" -ForegroundColor Red
    Write-Host "Asegúrate de estar en el directorio raíz del proyecto" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Archivos de configuración encontrados" -ForegroundColor Green
Write-Host ""

# Verificar login
Write-Host "🔐 Verificando login en Railway..." -ForegroundColor Yellow
$loginCheck = railway whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  No estás logueado en Railway" -ForegroundColor Yellow
    Write-Host "Iniciando login..." -ForegroundColor Yellow
    railway login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error en el login" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Ya estás logueado" -ForegroundColor Green
    Write-Host $loginCheck
}
Write-Host ""

# Verificar si el proyecto está inicializado
Write-Host "🔍 Verificando proyecto Railway..." -ForegroundColor Yellow
if (-not (Test-Path ".railway")) {
    Write-Host "⚠️  Proyecto no inicializado" -ForegroundColor Yellow
    Write-Host "Inicializando proyecto..." -ForegroundColor Yellow
    railway init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error inicializando proyecto" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Proyecto ya inicializado" -ForegroundColor Green
}
Write-Host ""

# Desplegar
Write-Host "🚀 Iniciando deployment..." -ForegroundColor Cyan
Write-Host ""
railway up

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Deployment completado exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Próximos pasos:" -ForegroundColor Yellow
    Write-Host "  1. Obtener URL: railway domain" -ForegroundColor White
    Write-Host "  2. Ver logs: railway logs" -ForegroundColor White
    Write-Host "  3. Verificar health: curl https://tu-dominio.up.railway.app/health" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Error en el deployment" -ForegroundColor Red
    Write-Host "Revisa los logs arriba para más detalles" -ForegroundColor Yellow
    exit 1
}


