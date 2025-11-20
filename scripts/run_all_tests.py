"""
Script maestro para ejecutar todas las pruebas del subsistema.
"""

import subprocess
import sys
import time
from datetime import datetime

def run_test_script(script_name, description):
    """Ejecuta un script de prueba y reporta el resultado."""
    print(f"\n{'='*60}")
    print(f"EJECUTANDO: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=300)
        
        print(f"Exit code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"ERROR: Timeout ejecutando {script_name}")
        return False
    except Exception as e:
        print(f"ERROR ejecutando {script_name}: {e}")
        return False

def main():
    """Función principal."""
    print("SCRIPT MAESTRO DE PRUEBAS DEL SUBSISTEMA DE RECOLECCION")
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Lista de pruebas a ejecutar
    tests = [
        ("scripts/test_full_functionality.py", "Prueba de funcionalidad completa"),
        ("scripts/test_real_time_features.py", "Prueba de características de tiempo real"),
        ("scripts/test_persistence.py", "Prueba de persistencia de datos"),
        ("scripts/test_complete_api.py", "Prueba completa de APIs"),
        ("scripts/test_recoleccion_features.py", "Prueba de características de recolección")
    ]
    
    results = []
    
    # Ejecutar cada prueba
    for script, description in tests:
        print(f"\nIniciando: {description}")
        success = run_test_script(script, description)
        results.append((script, description, success))
        
        if success:
            print(f"OK - {description} EXITOSA")
        else:
            print(f"ERROR - {description} FALLO")
        
        # Esperar un poco entre pruebas
        time.sleep(2)
    
    # Resumen final
    print(f"\n{'='*60}")
    print("RESUMEN FINAL DE PRUEBAS")
    print(f"{'='*60}")
    
    total = len(results)
    passed = sum(1 for _, _, success in results if success)
    failed = total - passed
    
    print(f"Total de pruebas: {total}")
    print(f"Exitosas: {passed}")
    print(f"Fallidas: {failed}")
    print(f"Porcentaje de éxito: {(passed/total)*100:.1f}%")
    
    print(f"\nDetalles por prueba:")
    for script, description, success in results:
        status = "OK" if success else "ERROR"
        print(f"  {status} - {description}")
    
    if passed == total:
        print(f"\nOK TODAS LAS PRUEBAS EXITOSAS!")
        return 0
    else:
        print(f"\nERROR ALGUNAS PRUEBAS FALLARON!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)









