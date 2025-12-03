"""
Verifica el estado completo de una tarea específica y qué falta para procesarla.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.recoleccion.database.database_manager import SqlServerDatabaseManager

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

def print_warning(message):
    print(f"[ADVERTENCIA] {message}")

tarea_id = "TEST_DIRECT_13372"

print_header(f"VERIFICACIÓN COMPLETA DE TAREA: {tarea_id}")

try:
    db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
    cursor = db.connection.cursor()
    
    # 1. Verificar Tarea
    print_section("1. ESTADO DE LA TAREA")
    db._exec(cursor, """
        SELECT id, alimento_id, estado, inicio, fin,
               cantidad_recolectada, hormigas_asignadas
        FROM dbo.Tareas
        WHERE id = ?
    """, (tarea_id,))
    
    tarea_row = cursor.fetchone()
    if tarea_row:
        columns = [description[0] for description in cursor.description]
        print_success("Tarea encontrada en BD")
        for col, val in zip(columns, tarea_row):
            print_info(f"  {col}: {val}")
        
        estado = tarea_row[columns.index('estado')]
        hormigas_asignadas = tarea_row[columns.index('hormigas_asignadas')]
        inicio = tarea_row[columns.index('inicio')]
        
        print_section("ANÁLISIS DEL ESTADO")
        if estado == 'pendiente':
            print_warning("Estado: PENDIENTE - La tarea no ha sido iniciada")
            print_info("Para procesar la tarea necesita:")
            print_info("  1. Estar en estado 'en_proceso'")
            print_info("  2. Tener fecha_inicio establecida")
            if hormigas_asignadas == 0:
                print_error(f"  - Tiene {hormigas_asignadas} hormigas asignadas (debe tener > 0)")
            else:
                print_success(f"  - Tiene {hormigas_asignadas} hormigas asignadas")
        elif estado == 'en_proceso':
            print_success("Estado: EN_PROCESO - La tarea está iniciada")
            if inicio:
                print_success(f"  Fecha inicio: {inicio}")
            else:
                print_error("  Fecha inicio: NULL - La tarea no tiene fecha de inicio")
        elif estado == 'completada':
            print_success("Estado: COMPLETADA - La tarea ya fue procesada")
        else:
            print_info(f"Estado: {estado}")
    else:
        print_error(f"Tarea {tarea_id} NO encontrada en BD")
    
    # 2. Verificar Lote
    print_section("2. ESTADO DEL LOTE DE HORMIGAS")
    db._exec(cursor, """
        SELECT lote_id, tarea_id, cantidad_hormigas_enviadas, 
               cantidad_hormigas_requeridas, estado, fecha_creacion, fecha_aceptacion
        FROM dbo.lotes_hormigas
        WHERE tarea_id = ?
    """, (tarea_id,))
    
    lote_row = cursor.fetchone()
    if lote_row:
        lote_columns = [description[0] for description in cursor.description]
        print_success("Lote encontrado en BD")
        for col, val in zip(lote_columns, lote_row):
            print_info(f"  {col}: {val}")
        
        lote_id = lote_row[lote_columns.index('lote_id')]
        estado_lote = lote_row[lote_columns.index('estado')]
        cantidad_enviada = lote_row[lote_columns.index('cantidad_hormigas_enviadas')]
        cantidad_requerida = lote_row[lote_columns.index('cantidad_hormigas_requeridas')]
        
        print_section("ANÁLISIS DEL LOTE")
        if estado_lote == 'pendiente':
            print_warning("Estado del lote: PENDIENTE - El lote no ha sido aceptado")
            print_info("Para procesar la tarea, el lote debe estar en estado 'aceptado' o 'en_uso'")
        elif estado_lote == 'aceptado':
            print_success("Estado del lote: ACEPTADO")
            print_warning("El lote está aceptado pero no en uso. La tarea debería iniciarse para marcar el lote como 'en_uso'")
        elif estado_lote == 'en_uso':
            print_success("Estado del lote: EN_USO - El lote está siendo usado por la tarea")
        else:
            print_info(f"Estado del lote: {estado_lote}")
        
        if cantidad_enviada >= cantidad_requerida:
            print_success(f"Cantidad suficiente: {cantidad_enviada} >= {cantidad_requerida}")
        else:
            print_error(f"Cantidad insuficiente: {cantidad_enviada} < {cantidad_requerida}")
    else:
        print_error("Lote NO encontrado en BD para esta tarea")
        lote_id = None
    
    # 3. Verificar Asignaciones
    print_section("3. ASIGNACIONES DE HORMIGAS")
    db._exec(cursor, """
        SELECT COUNT(*) as total, 
               COUNT(CASE WHEN lote_id IS NOT NULL THEN 1 END) as con_lote,
               COUNT(CASE WHEN lote_id IS NULL THEN 1 END) as sin_lote
        FROM dbo.asignaciones_hormiga_tarea
        WHERE tarea_id = ?
    """, (tarea_id,))
    
    asign_row = cursor.fetchone()
    if asign_row:
        total = asign_row[0]
        con_lote = asign_row[1]
        sin_lote = asign_row[2]
        print_info(f"Total asignaciones: {total}")
        print_info(f"  Con lote_id: {con_lote}")
        print_info(f"  Sin lote_id: {sin_lote}")
        
        if total > 0:
            print_success("Hay asignaciones guardadas")
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
    else:
        print_error("No se pudieron obtener asignaciones")
    
    # 4. Verificar Alimento
    if tarea_row:
        alimento_id = tarea_row[columns.index('alimento_id')]
        print_section("4. INFORMACIÓN DEL ALIMENTO")
        db._exec(cursor, """
            SELECT id, nombre, cantidad_hormigas_necesarias, tiempo_recoleccion, disponible
            FROM dbo.Alimentos
            WHERE id = ?
        """, (alimento_id,))
        
        alimento_row = cursor.fetchone()
        if alimento_row:
            alimento_columns = [description[0] for description in cursor.description]
            print_success("Alimento encontrado")
            for col, val in zip(alimento_columns, alimento_row):
                print_info(f"  {col}: {val}")
        else:
            print_error(f"Alimento {alimento_id} no encontrado")
    
    # 5. Resumen de qué falta
    print_section("RESUMEN: QUÉ FALTA PARA PROCESAR LA TAREA")
    
    problemas = []
    soluciones = []
    
    if not tarea_row:
        problemas.append("La tarea no existe en BD")
    else:
        estado = tarea_row[columns.index('estado')]
        hormigas_asignadas = tarea_row[columns.index('hormigas_asignadas')]
        inicio = tarea_row[columns.index('inicio')]
        
        if estado == 'pendiente':
            problemas.append("La tarea está en estado 'pendiente' (no iniciada)")
            soluciones.append("Iniciar la tarea usando: POST /tareas/{tarea_id}/iniciar")
        
        if estado == 'en_proceso' and not inicio:
            problemas.append("La tarea está en 'en_proceso' pero no tiene fecha_inicio")
            soluciones.append("La tarea necesita ser iniciada correctamente")
        
        if hormigas_asignadas == 0:
            problemas.append(f"La tarea tiene {hormigas_asignadas} hormigas asignadas")
            soluciones.append("Asignar hormigas a la tarea")
        else:
            print_success(f"La tarea tiene {hormigas_asignadas} hormigas asignadas")
    
    if not lote_row:
        problemas.append("No hay lote asociado a la tarea")
        soluciones.append("Crear y asignar un lote de hormigas")
    else:
        estado_lote = lote_row[lote_columns.index('estado')]
        if estado_lote == 'pendiente':
            problemas.append("El lote está en estado 'pendiente' (no aceptado)")
            soluciones.append("Aceptar el lote")
        elif estado_lote == 'aceptado':
            problemas.append("El lote está aceptado pero la tarea no está iniciada")
            soluciones.append("Iniciar la tarea para marcar el lote como 'en_uso'")
    
    if asign_row and asign_row[0] == 0:
        problemas.append("No hay asignaciones de hormigas guardadas")
        soluciones.append("Guardar las asignaciones de hormigas en la BD")
    
    if problemas:
        print_error("PROBLEMAS ENCONTRADOS:")
        for i, problema in enumerate(problemas, 1):
            print_error(f"  {i}. {problema}")
        
        print_section("SOLUCIONES:")
        for i, solucion in enumerate(soluciones, 1):
            print_info(f"  {i}. {solucion}")
    else:
        print_success("No se encontraron problemas. La tarea debería poder procesarse.")
    
    db.connection.close()
    
except Exception as e:
    print_error(f"Error: {e}")
    import traceback
    traceback.print_exc()

print_header("VERIFICACIÓN COMPLETADA")



