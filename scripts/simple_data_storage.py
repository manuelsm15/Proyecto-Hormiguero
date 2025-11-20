"""
Script simple para mostrar el almacenamiento de datos.
"""

import os
import sqlite3
from pathlib import Path

def show_simple_storage():
    """Muestra información simple del almacenamiento."""
    print("=== ALMACENAMIENTO DE DATOS DEL SUBSISTEMA ===")
    
    # 1. Verificar archivos existentes
    print("\n1. ARCHIVOS EXISTENTES:")
    files_to_check = [
        "recoleccion.db",
        "test_recoleccion.db", 
        "allure-results",
        "allure-report",
        "htmlcov",
        "logs"
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            if os.path.isfile(file):
                size = os.path.getsize(file)
                print(f"  OK {file} - {size} bytes")
            else:
                files_count = len(list(Path(file).rglob("*")))
                print(f"  OK {file}/ - {files_count} archivos")
        else:
            print(f"  NO {file} - No existe")
    
    # 2. Verificar base de datos
    print("\n2. BASE DE DATOS:")
    if os.path.exists("recoleccion.db"):
        try:
            conn = sqlite3.connect("recoleccion.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"  Base de datos existe con {len(tables)} tablas")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"    - {table[0]}: {count} registros")
            conn.close()
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print("  Base de datos no existe")
    
    # 3. Explicar almacenamiento actual
    print("\n3. ALMACENAMIENTO ACTUAL:")
    print("""
    ACTUALMENTE:
    - Los datos se almacenan EN MEMORIA
    - No hay persistencia en base de datos
    - Los datos se pierden al reiniciar
    - Solo hay archivos de reportes (allure, htmlcov)
    """)
    
    # 4. Explicar solución propuesta
    print("\n4. SOLUCION PROPUESTA:")
    print("""
    IMPLEMENTAR PERSISTENCIA:
    - Base de datos SQLite (recoleccion.db)
    - Tablas para: alimentos, tareas, hormigas, mensajes, eventos
    - Persistencia automática en todas las operaciones
    - Recuperación de datos al reiniciar
    - Logs de eventos completos
    """)
    
    # 5. Mostrar estructura propuesta
    print("\n5. ESTRUCTURA PROPUESTA:")
    print("""
    recoleccion.db:
    ├── alimentos (id, nombre, cantidad_hormigas, puntos_stock, tiempo_recoleccion)
    ├── tareas (id, alimento_id, estado, fecha_inicio, fecha_fin, alimento_recolectado)
    ├── hormigas (id, capacidad_carga, estado, tiempo_vida, subsistema_origen)
    ├── asignaciones_hormiga_tarea (tarea_id, hormiga_id)
    ├── mensajes (id, tipo, contenido, origen, destino, fecha_creacion)
    └── eventos (id, tipo_evento, descripcion, datos_adicionales, fecha_evento)
    """)

def main():
    """Función principal."""
    print("ANALISIS DE ALMACENAMIENTO DE DATOS")
    show_simple_storage()
    
    print("\n=== RESUMEN ===")
    print("""
    ESTADO ACTUAL:
    - Sin base de datos persistente
    - Datos solo en memoria
    - Se pierden al reiniciar
    
    SOLUCION:
    - Implementar SQLite
    - Persistencia automática
    - Recuperación de datos
    - Logs de eventos
    """)

if __name__ == "__main__":
    main()









