"""
Test directo de persistencia con logs detallados para ver qué está fallando.
"""
import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.recoleccion.database.database_manager import SqlServerDatabaseManager
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.estado_tarea import EstadoTarea
from src.recoleccion.models.estado_hormiga import EstadoHormiga
from src.recoleccion.services.persistence_service import PersistenceService

async def test_completo():
    print("="*80)
    print("TEST DIRECTO DE PERSISTENCIA CON LOGS DETALLADOS")
    print("="*80)
    
    # Conectar a BD
    print("\n1. Conectando a BD...")
    db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
    persistence = PersistenceService()
    persistence.db = db
    
    print(f"   Esquema detectado: {db.schema_type}")
    
    # Obtener un alimento existente de la BD
    print("\n2. Obteniendo alimento existente de BD...")
    alimentos = await persistence.obtener_alimentos()
    if not alimentos:
        print("   ERROR: No hay alimentos en BD")
        return
    
    alimento = alimentos[0]
    print(f"   Alimento encontrado: {alimento.id} ({alimento.nombre})")
    print(f"   Tipo de ID: {type(alimento.id)}")
    
    # Crear tarea
    print("\n3. Creando tarea...")
    tarea_id = f"TEST_DIRECT_{os.getpid()}"
    tarea = TareaRecoleccion(id=tarea_id, alimento=alimento)
    print(f"   Tarea ID: {tarea_id}")
    print(f"   Alimento ID: {tarea.alimento.id} (tipo: {type(tarea.alimento.id)})")
    
    # Guardar tarea
    print("\n4. Guardando tarea en BD...")
    resultado = await persistence.guardar_tarea(tarea)
    print(f"   Resultado: {resultado}")
    if not resultado:
        error = persistence.db.last_error
        print(f"   ERROR: {error}")
        if error:
            import traceback
            traceback.print_exc()
    else:
        print("   Tarea guardada exitosamente")
    
    # Verificar que se guardó
    print("\n5. Verificando tarea en BD...")
    cursor = db.connection.cursor()
    try:
        db._exec(cursor, "SELECT COUNT(*) FROM dbo.Tareas WHERE id = ?", (tarea_id,))
        count = cursor.fetchone()[0]
        print(f"   Tareas encontradas: {count}")
        if count > 0:
            db._exec(cursor, "SELECT id, alimento_id, estado, hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea_id,))
            row = cursor.fetchone()
            if row:
                print(f"   Datos: id={row[0]}, alimento_id={row[1]}, estado={row[2]}, hormigas_asignadas={row[3]}")
    except Exception as e:
        print(f"   Error verificando: {e}")
    
    # Agregar hormigas
    print("\n6. Agregando hormigas a la tarea...")
    h1 = Hormiga(id="H_TEST_1", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
    h2 = Hormiga(id="H_TEST_2", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
    h3 = Hormiga(id="H_TEST_3", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
    tarea.agregar_hormiga(h1)
    tarea.agregar_hormiga(h2)
    tarea.agregar_hormiga(h3)
    print(f"   Hormigas agregadas: {len(tarea.hormigas_asignadas)}")
    
    # Crear lote
    print("\n7. Creando lote de hormigas...")
    lote_id = f"LOTE_TEST_{os.getpid()}"
    exito, error = await persistence.crear_lote_hormigas(lote_id, tarea_id, 3, 3)
    print(f"   Resultado: {exito}, Error: {error}")
    if not exito:
        print(f"   ERROR creando lote: {error}")
    
    # Aceptar lote
    if exito:
        print("\n8. Aceptando lote...")
        exito2, error2 = await persistence.aceptar_lote_hormigas(lote_id)
        print(f"   Resultado: {exito2}, Error: {error2}")
    
    # Guardar hormigas en lote
    if exito:
        print("\n9. Guardando hormigas en lote...")
        resultado = await persistence.guardar_hormigas_en_lote(lote_id, [h1, h2, h3])
        print(f"   Resultado: {resultado}")
    
    # Guardar tarea con hormigas
    print("\n10. Guardando tarea con hormigas...")
    tarea.hormigas_lote_id = lote_id
    resultado = await persistence.guardar_tarea(tarea)
    print(f"   Resultado: {resultado}")
    if not resultado:
        error = persistence.db.last_error
        print(f"   ERROR: {error}")
    
    # Verificación final
    print("\n11. Verificación final en BD...")
    try:
        # Tarea
        db._exec(cursor, "SELECT COUNT(*) FROM dbo.Tareas WHERE id = ?", (tarea_id,))
        count = cursor.fetchone()[0]
        print(f"   Tareas: {count}")
        
        # Lote
        db._exec(cursor, "SELECT COUNT(*) FROM dbo.lotes_hormigas WHERE lote_id = ?", (lote_id,))
        count = cursor.fetchone()[0]
        print(f"   Lotes: {count}")
        
        # Asignaciones
        db._exec(cursor, "SELECT COUNT(*) FROM dbo.asignaciones_hormiga_tarea WHERE tarea_id = ?", (tarea_id,))
        count = cursor.fetchone()[0]
        print(f"   Asignaciones: {count}")
    except Exception as e:
        print(f"   Error en verificación: {e}")
        import traceback
        traceback.print_exc()
    
    db.connection.close()
    print("\n" + "="*80)
    print("TEST COMPLETADO")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_completo())



