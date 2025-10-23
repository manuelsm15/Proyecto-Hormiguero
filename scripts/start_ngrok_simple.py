#!/usr/bin/env python3
"""
Script simple para iniciar ngrok y obtener URL pública.
"""

import subprocess
import time
import requests
import sys

def main():
    """Función principal."""
    print("INICIANDO TUNEL NGROK")
    print("Subsistema de Recolección - Universidad Cenfotec")
    print("="*60)
    
    # Verificar que el servidor local esté funcionando
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("ERROR: El servidor local no está funcionando")
            print("Ejecuta primero: python scripts/start_server.py")
            return 1
    except:
        print("ERROR: El servidor local no está funcionando")
        print("Ejecuta primero: python scripts/start_server.py")
        return 1
    
    print("OK: Servidor local funcionando")
    
    # Iniciar ngrok
    print("\nIniciando túnel ngrok...")
    print("Esto creará una URL pública temporal")
    print("Presiona Ctrl+C para detener")
    
    try:
        # Ejecutar ngrok
        subprocess.run(["ngrok", "http", "8000"], check=True)
    except KeyboardInterrupt:
        print("\nTúnel ngrok detenido")
    except FileNotFoundError:
        print("ERROR: ngrok no está instalado")
        print("Descarga desde: https://ngrok.com/download")
        print("O usa Railway: python scripts/deploy_railway_external.py")
        return 1
    except subprocess.CalledProcessError as e:
        print(f"ERROR: ngrok falló: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

