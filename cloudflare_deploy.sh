#!/bin/bash
# Script para desplegar en Cloudflare Pages

echo "🚀 Desplegando Hormiguero en Cloudflare Pages..."

# Verificar que wrangler esté instalado
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler CLI no está instalado"
    echo "📦 Instalando Wrangler..."
    npm install -g wrangler
fi

# Login en Cloudflare (si no está logueado)
echo "🔐 Verificando autenticación..."
wrangler whoami || wrangler login

# Desplegar
echo "📤 Desplegando proyecto..."
wrangler pages deploy . --project-name=hormiguero

echo "✅ Deployment completado!"
echo "🌐 Revisa tu proyecto en: https://hormiguero.pages.dev"

