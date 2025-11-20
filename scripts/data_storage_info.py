"""
Script para mostrar información del almacenamiento de datos.
"""

import os
import sqlite3
from pathlib import Path

def show_storage_info():
    """Muestra información del almacenamiento."""
    print("=== ALMACENAMIENTO DE DATOS DEL SUBSISTEMA ===")
    
    # 1. Verificar archivos
    print("\n1. ARCHIVOS EXISTENTES:")
    files = ["recoleccion.db", "test_recoleccion.db", "allure-results", "allure-report", "htmlcov", "logs"]
    
    for file in files:
        if os.path.exists(file):
            if os.path.isfile(file):
                size = os.path.getsize(file)
                print(f"  OK {file} - {size} bytes")
            else:
                count = len(list(Path(file).rglob("*")))
                print(f"  OK {file}/ - {count} archivos")
        else:
            print(f"  NO {file} - No existe")
    
    # 2. Base de datos
    print("\n2. BASE DE DATOS:")
    if os.path.exists("recoleccion.db"):
        try:
            conn = sqlite3.connect("recoleccion.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"  Base de datos existe con {len(tables)} tablas")
            conn.close()
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print("  Base de datos no existe")
    
    # 3. Estado actual
    print("\n3. ESTADO ACTUAL:")
    print("  - Los datos se almacenan EN MEMORIA")
    print("  - No hay persistencia en base de datos")
    print("  - Los datos se pierden al reiniciar")
    print("  - Solo hay archivos de reportes")
    
    # 4. Solución
    print("\n4. SOLUCION PROPUESTA:")
    print("  - Implementar SQLite (recoleccion.db)")
    print("  - Tablas para: alimentos, tareas, hormigas, mensajes, eventos")
    print("  - Persistencia automatica en todas las operaciones")
    print("  - Recuperacion de datos al reiniciar")
    print("  - Logs de eventos completos")

def main():
    """Función principal."""
    print("ANALISIS DE ALMACENAMIENTO DE DATOS")
    show_storage_info()
    
    print("\n=== RESUMEN ===")
    print("ESTADO ACTUAL: Sin base de datos persistente")
    print("SOLUCION: Implementar SQLite con persistencia automatica")

if __name__ == "__main__":
    main()









