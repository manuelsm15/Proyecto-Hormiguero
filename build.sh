#!/bin/bash
# Script de build para Cloudflare Pages
# Fuerza Python 3.12 y actualiza dependencias

set -e

echo "🔧 Configurando Python 3.12..."

# Intentar instalar Python 3.12 si asdf está disponible
if command -v asdf &> /dev/null; then
    echo "📦 Instalando Python 3.12.10 con asdf..."
    asdf install python 3.12.10 || true
    asdf local python 3.12.10 || true
fi

# Verificar versión de Python
python --version || python3 --version

echo "📦 Actualizando pip, setuptools y wheel..."
pip install --upgrade pip setuptools wheel || python3 -m pip install --upgrade pip setuptools wheel

echo "📦 Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt || python3 -m pip install -r requirements.txt

echo "✅ Build completado exitosamente!"

