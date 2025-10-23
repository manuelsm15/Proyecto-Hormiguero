#!/usr/bin/env python3
"""
Script para configurar ngrok y crear túnel público.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def main():
    """Función principal."""
    print("CONFIGURANDO NGROK PARA ACCESO EXTERNO")
    print("Subsistema de Recolección - Universidad Cenfotec")
    print("="*60)
    
    # Verificar si ngrok está instalado
    try:
        result = subprocess.run(["ngrok", "version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ ngrok no está instalado")
            print("📥 Instalando ngrok...")
            
            # Instalar ngrok
            subprocess.run([
                "winget", "install", "ngrok.ngrok"
            ], check=True)
            
            print("✅ ngrok instalado")
        else:
            print("✅ ngrok ya está instalado")
    except Exception as e:
        print(f"❌ Error instalando ngrok: {e}")
        return 1
    
    print("\n🔧 CONFIGURACIÓN NECESARIA:")
    print("="*60)
    print("1. Crear cuenta en: https://dashboard.ngrok.com/signup")
    print("2. Obtener authtoken en: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("3. Ejecutar: ngrok config add-authtoken TU_TOKEN")
    print("4. Ejecutar: ngrok http 8000")
    print("="*60)
    
    # Verificar si el servidor está funcionando
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor local funcionando")
        else:
            print("❌ Servidor local no responde")
            return 1
    except Exception as e:
        print(f"❌ Servidor local no está funcionando: {e}")
        print("🚀 Iniciando servidor...")
        
        # Iniciar servidor en background
        subprocess.Popen([
            "python", "scripts/start_external_server.py"
        ], cwd=Path(__file__).parent.parent)
        
        print("⏳ Esperando que el servidor inicie...")
        time.sleep(5)
    
    print("\n🌐 INSTRUCCIONES PARA NGROK:")
    print("="*60)
    print("1. Abrir nueva terminal")
    print("2. Ejecutar: ngrok http 8000")
    print("3. Copiar la URL 'Forwarding' (ej: https://abc123.ngrok.io)")
    print("4. Compartir esa URL con tu compañero")
    print("="*60)
    
    print("\n🧪 PROBAR ACCESO:")
    print("="*60)
    print("Una vez que tengas la URL de ngrok:")
    print("curl https://TU_URL_NGROK.ngrok.io/health")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
