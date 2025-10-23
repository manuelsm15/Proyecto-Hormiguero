#!/usr/bin/env python3
"""
Script para configurar Windows Firewall para acceso externo.
"""

import subprocess
import sys

def print_header(title):
    """Imprime un encabezado formateado."""
    print(f"\n{'='*60}")
    print(f">>> {title}")
    print(f"{'='*60}")

def configure_firewall():
    """Configura Windows Firewall para permitir puerto 8000."""
    print_header("CONFIGURANDO WINDOWS FIREWALL")
    
    # Comando para agregar regla de firewall
    firewall_cmd = """
    netsh advfirewall firewall add rule name="Subsistema Recoleccion" dir=in action=allow protocol=TCP localport=8000
    """
    
    try:
        print("Agregando regla de firewall para puerto 8000...")
        result = subprocess.run(
            firewall_cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print("OK: Regla de firewall agregada exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: No se pudo configurar el firewall: {e}")
        print("Configuración manual requerida:")
        print("1. Abrir Windows Defender Firewall")
        print("2. Ir a 'Configuración avanzada'")
        print("3. Crear nueva regla de entrada")
        print("4. Puerto TCP 8000")
        print("5. Permitir conexión")
        return False

def show_access_info():
    """Muestra información de acceso externo."""
    print_header("INFORMACION DE ACCESO EXTERNO")
    
    print("URLs para tu compañero:")
    print("- API Principal: http://45.239.67.86:8000")
    print("- Documentación: http://45.239.67.86:8000/docs")
    print("- Health Check: http://45.239.67.86:8000/health")
    
    print("\nPasos para tu compañero:")
    print("1. Abrir navegador")
    print("2. Ir a: http://45.239.67.86:8000/docs")
    print("3. Explorar todas las APIs")
    print("4. Probar endpoints")
    
    print("\nComandos de prueba para tu compañero:")
    print("# Probar conectividad:")
    print("curl http://45.239.67.86:8000/health")
    print("# Ver documentación:")
    print("# Abrir: http://45.239.67.86:8000/docs")

def test_external_access():
    """Prueba el acceso externo."""
    print_header("PROBANDO ACCESO EXTERNO")
    
    import requests
    try:
        print("Probando acceso externo...")
        response = requests.get("http://45.239.67.86:8000/health", timeout=10)
        if response.status_code == 200:
            print("OK: Acceso externo funcionando")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"ERROR: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: No se pudo probar acceso externo: {e}")
        print("Posibles causas:")
        print("1. Port forwarding no configurado")
        print("2. Firewall bloqueando conexiones")
        print("3. Router no permite conexiones externas")
        return False

def main():
    """Función principal."""
    print("CONFIGURACION DE ACCESO EXTERNO")
    print("Subsistema de Recolección - Universidad Cenfotec")
    print("="*60)
    
    # Configurar firewall
    configure_firewall()
    
    # Mostrar información
    show_access_info()
    
    # Probar acceso
    print("\n¿Deseas probar el acceso externo? (s/n)")
    respuesta = input().lower()
    if respuesta == 's':
        test_external_access()
    
    print(f"\n{'='*60}")
    print("CONFIGURACION COMPLETADA")
    print("Tu compañero puede acceder desde cualquier lugar")
    print("URL: http://45.239.67.86:8000")
    print(f"{'='*60}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
