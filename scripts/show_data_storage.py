"""
Script para mostrar dónde se almacenan los datos y eventos del subsistema.
"""

import os
import sqlite3
import json
from datetime import datetime
from pathlib import Path

def show_data_storage_info():
    """Muestra información sobre el almacenamiento de datos."""
    print("=== INFORMACIÓN DE ALMACENAMIENTO DE DATOS ===")
    
    # 1. Verificar archivos de base de datos
    print("\n1. ARCHIVOS DE BASE DE DATOS:")
    db_files = [
        "recoleccion.db",
        "test_recoleccion.db",
        "allure-results",
        "allure-report",
        "htmlcov"
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            size = os.path.getsize(db_file)
            print(f"  OK {db_file} - {size} bytes")
        else:
            print(f"  NO {db_file} - No existe")
    
    # 2. Verificar base de datos principal
    print("\n2. BASE DE DATOS PRINCIPAL (recoleccion.db):")
    if os.path.exists("recoleccion.db"):
        try:
            conn = sqlite3.connect("recoleccion.db")
            cursor = conn.cursor()
            
            # Obtener información de tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print(f"  Tablas encontradas: {len(tables)}")
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"    - {table_name}: {count} registros")
            
            conn.close()
        except Exception as e:
            print(f"  Error accediendo a la base de datos: {e}")
    else:
        print("  Base de datos no existe aún")
    
    # 3. Verificar logs y reportes
    print("\n3. LOGS Y REPORTES:")
    log_dirs = [
        "logs",
        "allure-results",
        "allure-report",
        "htmlcov"
    ]
    
    for log_dir in log_dirs:
        if os.path.exists(log_dir):
            files = list(Path(log_dir).rglob("*"))
            print(f"  OK {log_dir} - {len(files)} archivos")
        else:
            print(f"  NO {log_dir} - No existe")
    
    # 4. Mostrar estructura de almacenamiento
    print("\n4. ESTRUCTURA DE ALMACENAMIENTO:")
    print("""
    Proyecto Hormiguero/
    ├── recoleccion.db          # Base de datos SQLite principal
    ├── logs/                   # Archivos de log
    ├── allure-results/         # Resultados de pruebas Allure
    ├── allure-report/          # Reportes HTML de Allure
    ├── htmlcov/                # Reportes de cobertura
    └── src/recoleccion/
        ├── database/           # Gestor de base de datos
        ├── services/           # Servicios de persistencia
        └── models/             # Modelos de datos
    """)
    
    # 5. Explicar tipos de datos almacenados
    print("\n5. TIPOS DE DATOS ALMACENADOS:")
    print("""
    TABLAS DE BASE DE DATOS:
    ├── alimentos          # Informacion de alimentos disponibles
    ├── tareas            # Tareas de recoleccion
    ├── hormigas          # Informacion de hormigas
    ├── asignaciones_hormiga_tarea  # Relacion hormiga-tarea
    ├── mensajes          # Mensajes entre subsistemas
    └── eventos           # Log de actividades del sistema
    
    DATOS EN MEMORIA (temporales):
    ├── tareas_activas    # Lista de tareas en proceso
    ├── tareas_completadas # Lista de tareas finalizadas
    ├── mensajes_pendientes # Mensajes sin procesar
    └── cache_datos       # Datos en cache para rendimiento
    """)
    
    # 6. Mostrar configuración de persistencia
    print("\n6. CONFIGURACIÓN DE PERSISTENCIA:")
    print("""
    CONFIGURACION ACTUAL:
    ├── Base de datos: SQLite (recoleccion.db)
    ├── Persistencia: Automatica en todas las operaciones
    ├── Logs: Registro de todos los eventos
    ├── Backup: Manual (copiar recoleccion.db)
    └── Recuperacion: Automatica al reiniciar
    """)

def show_database_schema():
    """Muestra el esquema de la base de datos."""
    print("\n=== ESQUEMA DE BASE DE DATOS ===")
    
    if not os.path.exists("recoleccion.db"):
        print("Base de datos no existe. Se creará al ejecutar la aplicación.")
        return
    
    try:
        conn = sqlite3.connect("recoleccion.db")
        cursor = conn.cursor()
        
        # Obtener esquema de todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\nTABLA: {table_name}")
            
            # Obtener estructura de la tabla
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                not_null = "NOT NULL" if col[3] else ""
                primary_key = "PRIMARY KEY" if col[5] else ""
                print(f"  - {col_name}: {col_type} {not_null} {primary_key}")
        
        conn.close()
    except Exception as e:
        print(f"Error mostrando esquema: {e}")

def main():
    """Función principal."""
    print("ANALISIS DE ALMACENAMIENTO DE DATOS DEL SUBSISTEMA DE RECOLECCION")
    
    show_data_storage_info()
    show_database_schema()
    
    print("\n=== RESUMEN ===")
    print("""
    UBICACION DE DATOS:
    ├── Base de datos: ./recoleccion.db
    ├── Logs: ./logs/
    ├── Reportes: ./allure-results/, ./allure-report/
    └── Cobertura: ./htmlcov/
    
    PERSISTENCIA:
    ├── Automatica en todas las operaciones
    ├── Recuperacion al reiniciar
    ├── Logs de eventos completos
    └── Estadisticas en tiempo real
    
    EVENTOS REGISTRADOS:
    ├── Creacion de tareas
    ├── Asignacion de hormigas
    ├── Cambios de estado
    ├── Completado de tareas
    ├── Mensajes entre subsistemas
    └── Errores y excepciones
    """)

if __name__ == "__main__":
    main()
