"""
Pruebas de integración reales con validación exhaustiva de BD.
Verifica que TODOS los datos se guarden correctamente en las tablas.
"""
import requests
import time
import sys
import os
from datetime import datetime

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def print_header(text):
    print(f"\n{'='*80}")
    print(f"{text}")
    print(f"{'='*80}")

def print_section(text):
    print(f"\n{'-'*80}")
    print(f"{text}")
    print(f"{'-'*80}")

def print_success(message):
    print(f"[OK] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_info(message):
    print(f"[INFO] {message}")

def safe_request(method, url, json_data=None, params=None, expected_status=200):
    """Realiza una petición HTTP de forma segura."""
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=TIMEOUT)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, params=params, timeout=TIMEOUT)
        else:
            print_error(f"Método HTTP no soportado: {method}")
            return None
        
        if response.status_code == expected_status:
            return response
        else:
            print_error(f"Status code inesperado: {response.status_code} (esperado: {expected_status})")
            print_error(f"Respuesta: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error en petición: {e}")
        return None

def consultar_bd_directa(tarea_id, lote_id):
    """Consulta directamente la BD para verificar que todo se guardó."""
    print_section("VALIDACIÓN DIRECTA EN BASE DE DATOS")
    
    try:
        from src.recoleccion.database.database_manager import SqlServerDatabaseManager
        
        db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
        cursor = db.connection.cursor()
        
        # 1. Verificar Tarea en dbo.Tareas
        print_info("1. Consultando tabla dbo.Tareas...")
        try:
            db._exec(cursor, """
                SELECT id, alimento_id, estado, inicio, fin,
                       cantidad_recolectada, hormigas_asignadas
                FROM dbo.Tareas
                WHERE id = ?
            """, (tarea_id,))
            
            tarea_row = cursor.fetchone()
            if tarea_row:
                print_success(f"Tarea encontrada en dbo.Tareas: {tarea_id}")
                columns = [description[0] for description in cursor.description]
                for col, val in zip(columns, tarea_row):
                    print_info(f"  {col}: {val}")
                
                # Verificar hormigas_asignadas
                hormigas_idx = columns.index('hormigas_asignadas')
                hormigas_value = tarea_row[hormigas_idx]
                if hormigas_value and hormigas_value > 0:
                    print_success(f"hormigas_asignadas = {hormigas_value} (VALIDADO)")
                else:
                    print_error(f"hormigas_asignadas = {hormigas_value} (ESPERADO: > 0)")
            else:
                print_error(f"Tarea {tarea_id} NO encontrada en dbo.Tareas")
        except Exception as e:
            print_error(f"Error consultando dbo.Tareas: {e}")
        
        # 2. Verificar Lote en lotes_hormigas
        print_info("\n2. Consultando tabla lotes_hormigas...")
        try:
            # Intentar con diferentes nombres de tabla según el esquema
            for tabla in ["dbo.lotes_hormigas", "lotes_hormigas"]:
                try:
                    db._exec(cursor, f"""
                        SELECT TOP 1 *
                        FROM {tabla}
                        WHERE tarea_id = ? OR id = ?
                    """, (tarea_id, lote_id))
                    
                    lote_row = cursor.fetchone()
                    if lote_row:
                        print_success(f"Lote encontrado en {tabla}: {lote_id}")
                        columns = [description[0] for description in cursor.description]
                        for col, val in zip(columns, lote_row):
                            print_info(f"  {col}: {val}")
                        break
                except Exception as e:
                    continue
            else:
                print_error(f"Lote {lote_id} NO encontrado en lotes_hormigas")
        except Exception as e:
            print_error(f"Error consultando lotes_hormigas: {e}")
        
        # 3. Verificar Asignaciones
        print_info("\n3. Consultando tabla asignaciones_hormiga_tarea...")
        try:
            db._exec(cursor, """
                SELECT COUNT(*) as total
                FROM dbo.asignaciones_hormiga_tarea
                WHERE tarea_id = ?
            """, (tarea_id,))
            
            asign_row = cursor.fetchone()
            if asign_row:
                total = asign_row[0]
                print_success(f"Total asignaciones encontradas: {total}")
                if total > 0:
                    # Mostrar detalles
                    db._exec(cursor, """
                        SELECT tarea_id, hormiga_id, lote_id
                        FROM dbo.asignaciones_hormiga_tarea
                        WHERE tarea_id = ?
                    """, (tarea_id,))
                    
                    asignaciones = cursor.fetchall()
                    for i, asign in enumerate(asignaciones, 1):
                        print_info(f"  Asignación {i}: hormiga={asign[1]}, lote={asign[2]}")
                else:
                    print_error("No hay asignaciones guardadas")
        except Exception as e:
            print_error(f"Error consultando asignaciones: {e}")
        
        # 4. Contar registros en cada tabla
        print_info("\n4. Conteo de registros en tablas...")
        try:
            db._exec(cursor, "SELECT COUNT(*) FROM dbo.Tareas")
            total_tareas = cursor.fetchone()[0]
            print_info(f"  Total tareas en dbo.Tareas: {total_tareas}")
        except Exception as e:
            print_error(f"Error contando tareas: {e}")
        
        try:
            # Intentar contar lotes
            for tabla in ["dbo.lotes_hormigas", "lotes_hormigas"]:
                try:
                    db._exec(cursor, f"SELECT COUNT(*) FROM {tabla}")
                    total_lotes = cursor.fetchone()[0]
                    print_info(f"  Total lotes en {tabla}: {total_lotes}")
                    break
                except:
                    continue
        except Exception as e:
            print_error(f"Error contando lotes: {e}")
        
        try:
            db._exec(cursor, "SELECT COUNT(*) FROM dbo.asignaciones_hormiga_tarea")
            total_asign = cursor.fetchone()[0]
            print_info(f"  Total asignaciones: {total_asign}")
        except Exception as e:
            print_error(f"Error contando asignaciones: {e}")
        
        db.connection.close()
        
    except Exception as e:
        print_error(f"Error al conectar a BD: {e}")
        import traceback
        traceback.print_exc()

# Inicio de pruebas
print_header("PRUEBAS DE INTEGRACIÓN REALES CON VALIDACIÓN EXHAUSTIVA DE BD")

# Verificar servicio
print_info("Verificando servicio...")
response = safe_request("GET", f"{BASE_URL}/health")
if not response:
    print_error("El servicio no está disponible")
    sys.exit(1)

print_success("Servicio disponible")

# Obtener alimento existente
print_header("PASO 1: Obtener Alimento")
response = safe_request("GET", f"{BASE_URL}/alimentos")
if not response:
    print_error("No se pudieron obtener alimentos")
    sys.exit(1)

alimentos = response.json()
if not alimentos:
    print_error("No hay alimentos disponibles")
    sys.exit(1)

alimento = alimentos[0]
alimento_id = alimento.get("id")
print_success(f"Usando alimento: {alimento_id} ({alimento.get('nombre')})")

# Crear tarea
print_header("PASO 2: Crear Tarea")
tarea_id = f"TAREA_VALID_{datetime.now().strftime('%Y%m%d%H%M%S')}"
tarea_data = {
    "tarea_id": tarea_id,
    "alimento_id": alimento_id
}

response = safe_request("POST", f"{BASE_URL}/tareas", json_data=tarea_data)
if not response:
    print_error("No se pudo crear la tarea")
    sys.exit(1)

tarea_creada = response.json()
print_success(f"Tarea creada: {tarea_id}")
print_info(f"  Estado: {tarea_creada.get('estado')}")

# Esperar a que se persista
time.sleep(2)

# Asignar hormigas con lote
print_header("PASO 3: Asignar Hormigas con Lote")
lote_id = f"LOTE_VALID_{datetime.now().strftime('%Y%m%d%H%M%S')}"
asignar_data = {
    "hormigas_lote_id": lote_id,
    "cantidad": 3
}

print_info(f"Intentando asignar 3 hormigas con lote_id: {lote_id}")
response = safe_request("POST", f"{BASE_URL}/tareas/{tarea_id}/asignar-hormigas", json_data=asignar_data)

if not response:
    print_error("No se pudieron asignar las hormigas")
    sys.exit(1)

asignacion = response.json()
print_success("Hormigas asignadas")
print_info(f"  Lote ID: {lote_id}")
print_info(f"  Estado: {asignacion.get('estado')}")
print_info(f"  Iniciada: {asignacion.get('iniciada', False)}")

# Esperar a que se persista
time.sleep(2)

# Verificar status
print_header("PASO 4: Verificar Status")
response = safe_request("GET", f"{BASE_URL}/tareas/{tarea_id}/status")
if response:
    status = response.json()
    print_info(f"  Estado: {status.get('estado')}")
    print_info(f"  Hormigas asignadas: {status.get('hormigas_asignadas', 0)}")
    print_info(f"  Lote ID: {status.get('hormigas_lote_id')}")

# Consultar BD directamente
print_header("PASO 5: Validación Directa en Base de Datos")
consultar_bd_directa(tarea_id, lote_id)

print_header("PRUEBAS COMPLETADAS")
print_info(f"Tarea ID: {tarea_id}")
print_info(f"Lote ID: {lote_id}")
print_info("Revisa los resultados arriba para ver qué se guardó en la BD")



