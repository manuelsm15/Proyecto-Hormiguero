"""
Script para probar el healthcheck localmente.
"""

import requests
import time
import sys

def test_healthcheck():
    """Prueba el healthcheck localmente."""
    print("🔍 Probando healthcheck localmente...")
    
    try:
        # Probar healthcheck
        response = requests.get("http://localhost:8000/health", timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Healthcheck exitoso")
            return True
        else:
            print("❌ Healthcheck falló")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor")
        print("💡 Asegúrate de que el servidor esté ejecutándose en puerto 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando prueba de healthcheck...")
    
    # Esperar un poco para que el servidor se inicie
    print("⏳ Esperando 3 segundos...")
    time.sleep(3)
    
    success = test_healthcheck()
    
    if success:
        print("🎉 ¡Healthcheck funcionando correctamente!")
        sys.exit(0)
    else:
        print("💥 Healthcheck falló")
        sys.exit(1)

