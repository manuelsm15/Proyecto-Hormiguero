#!/usr/bin/env python3
"""
Script para crear túnel ngrok para acceso externo temporal.
"""

import os
import subprocess
import sys
import time
import requests
from pathlib import Path

def print_header(title):
    """Imprime un encabezado formateado."""
    print(f"\n{'='*60}")
    print(f">>> {title}")
    print(f"{'='*60}")

def check_ngrok():
    """Verifica que ngrok esté instalado."""
    print_header("VERIFICANDO NGROK")
    
    try:
        result = subprocess.run("ngrok version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("OK: ngrok está instalado")
            return True
    except:
        pass
    
    print("ngrok no está instalado")
    print("Opciones:")
    print("1. Descargar desde: https://ngrok.com/download")
    print("2. Instalar con chocolatey: choco install ngrok")
    print("3. Usar Railway (recomendado)")
    return False

def start_ngrok_tunnel():
    """Inicia túnel ngrok."""
    print_header("INICIANDO TUNEL NGROK")
    
    print("Iniciando túnel ngrok en puerto 8000...")
    print("Esto creará una URL pública temporal")
    
    try:
        # Iniciar ngrok en background
        process = subprocess.Popen(
            ["ngrok", "http", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Esperar a que ngrok se inicie
        time.sleep(5)
        
        # Obtener URL del túnel
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("tunnels"):
                    tunnel = data["tunnels"][0]
                    public_url = tunnel["public_url"]
                    print(f"OK: Túnel creado: {public_url}")
                    return public_url, process
        except:
            pass
        
        print("ERROR: No se pudo obtener la URL del túnel")
        process.terminate()
        return None, None
        
    except Exception as e:
        print(f"ERROR: No se pudo iniciar ngrok: {e}")
        return None, None

def show_ngrok_info(public_url):
    """Muestra información del túnel ngrok."""
    print_header("INFORMACION DEL TUNEL")
    
    print(f"URL Pública: {public_url}")
    print(f"Documentación: {public_url}/docs")
    print(f"Health Check: {public_url}/health")
    print(f"API Principal: {public_url}")
    
    print("\nIMPORTANTE:")
    print("- Esta URL es TEMPORAL")
    print("- Se cerrará cuando detengas ngrok")
    print("- Para acceso permanente, usa Railway")
    
    print("\nPara tu compañero:")
    print(f"1. Comparte esta URL: {public_url}")
    print("2. Puede acceder desde cualquier lugar")
    print("3. La URL cambiará si reinicias ngrok")

def test_ngrok_tunnel(public_url):
    """Prueba el túnel ngrok."""
    if not public_url:
        return False
    
    print_header("PROBANDO TUNEL NGROK")
    
    try:
        response = requests.get(f"{public_url}/health", timeout=30)
        if response.status_code == 200:
            print("OK: Túnel funcionando correctamente")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"ERROR: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: No se pudo probar el túnel: {e}")
        return False

def main():
    """Función principal."""
    print("TUNEL NGROK - ACCESO EXTERNO TEMPORAL")
    print("Subsistema de Recolección - Universidad Cenfotec")
    print("="*60)
    
    # Verificar ngrok
    if not check_ngrok():
        print("\n¿Deseas usar Railway en su lugar? (s/n)")
        respuesta = input().lower()
        if respuesta == 's':
            print("Ejecuta: python scripts/deploy_railway_external.py")
        return 1
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("ERROR: El servidor local no está corriendo")
            print("Ejecuta primero: python scripts/start_server.py")
            return 1
    except:
        print("ERROR: El servidor local no está corriendo")
        print("Ejecuta primero: python scripts/start_server.py")
        return 1
    
    print("OK: Servidor local funcionando")
    
    # Iniciar túnel
    public_url, process = start_ngrok_tunnel()
    if not public_url:
        return 1
    
    # Mostrar información
    show_ngrok_info(public_url)
    
    # Probar túnel
    test_ngrok_tunnel(public_url)
    
    print(f"\n{'='*60}")
    print("TUNEL NGROK ACTIVO")
    print("Presiona Ctrl+C para detener el túnel")
    print(f"{'='*60}")
    
    try:
        # Mantener el proceso activo
        process.wait()
    except KeyboardInterrupt:
        print("\nDeteniendo túnel ngrok...")
        process.terminate()
        print("Túnel cerrado")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

