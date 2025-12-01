# Script PowerShell para desplegar en Cloudflare Pages

Write-Host "🚀 Desplegando Hormiguero en Cloudflare Pages..." -ForegroundColor Green

# Verificar que wrangler esté instalado
if (-not (Get-Command wrangler -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Wrangler CLI no está instalado" -ForegroundColor Red
    Write-Host "📦 Instalando Wrangler..." -ForegroundColor Yellow
    npm install -g wrangler
}

# Login en Cloudflare (si no está logueado)
Write-Host "🔐 Verificando autenticación..." -ForegroundColor Yellow
wrangler whoami
if ($LASTEXITCODE -ne 0) {
    wrangler login
}

# Desplegar
Write-Host "📤 Desplegando proyecto..." -ForegroundColor Yellow
wrangler pages deploy . --project-name=hormiguero

Write-Host "✅ Deployment completado!" -ForegroundColor Green
Write-Host "🌐 Revisa tu proyecto en: https://hormiguero.pages.dev" -ForegroundColor Cyan


