"""
Script para debuggear railway_main.py paso a paso.
"""

import os
import sys
import subprocess
import time
import requests

def debug_railway():
    """Debug railway_main.py paso a paso."""
    print("=== DEBUG RAILWAY MAIN ===")
    
    # 1. Verificar directorio
    print("1. Verificando directorio...")
    print(f"Directorio actual: {os.getcwd()}")
    
    # 2. Verificar archivos
    print("2. Verificando archivos...")
    files_to_check = [
        "railway_main.py",
        "src/recoleccion/api/recoleccion_controller.py",
        "src/recoleccion/services/mock_entorno_service.py",
        "src/recoleccion/services/mock_comunicacion_service.py"
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"  OK {file}")
        else:
            print(f"  ERROR {file} - NO ENCONTRADO")
    
    # 3. Probar import
    print("3. Probando import...")
    try:
        import railway_main
        print("  OK Import exitoso")
    except Exception as e:
        print(f"  ERROR en import: {e}")
        return False
    
    # 4. Probar servidor
    print("4. Probando servidor...")
    try:
        # Iniciar servidor
        process = subprocess.Popen([
            sys.executable, "railway_main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Esperar
        print("  Esperando 3 segundos...")
        time.sleep(3)
        
        # Verificar si el proceso sigue corriendo
        if process.poll() is None:
            print("  OK Servidor iniciado")
            
            # Probar healthcheck
            print("  Probando healthcheck...")
            try:
                response = requests.get("http://localhost:8000/health", timeout=5)
                print(f"  Status: {response.status_code}")
                print(f"  Response: {response.json()}")
                
                if response.status_code == 200:
                    print("  OK Healthcheck exitoso")
                else:
                    print("  ERROR Healthcheck fallo")
            except Exception as e:
                print(f"  ERROR en healthcheck: {e}")
            
            # Terminar proceso
            process.terminate()
            process.wait()
            print("  Servidor terminado")
        else:
            print("  ERROR Servidor no se inicio")
            stdout, stderr = process.communicate()
            print(f"  STDOUT: {stdout}")
            print(f"  STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"  ERROR iniciando servidor: {e}")
        return False
    
    print("=== DEBUG COMPLETADO ===")
    return True

if __name__ == "__main__":
    success = debug_railway()
    
    if success:
        print("Debug exitoso - Servidor funcionando")
    else:
        print("Debug fallo - Revisar errores")
