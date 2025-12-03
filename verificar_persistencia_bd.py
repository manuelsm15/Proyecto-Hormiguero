"""
Script para verificar directamente qué está pasando con la persistencia.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.recoleccion.database.database_manager import SqlServerDatabaseManager
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.estado_tarea import EstadoTarea
from src.recoleccion.models.estado_hormiga import EstadoHormiga
from src.recoleccion.services.persistence_service import PersistenceService
import asyncio

async def test_persistencia():
    print("="*80)
    print("PRUEBA DIRECTA DE PERSISTENCIA")
    print("="*80)
    
    # Conectar a BD
    db = SqlServerDatabaseManager("SHIRORYUU", "Hormiguero")
    persistence = PersistenceService()
    persistence.db = db
    
    # Crear datos de prueba
    alimento = Alimento(
        id="TEST_ALIMENTO",
        nombre="Alimento Test",
        cantidad_hormigas_necesarias=3,
        puntos_stock=10,
        tiempo_recoleccion=60
    )
    
    tarea = TareaRecoleccion(id="TEST_TAREA", alimento=alimento)
    
    h1 = Hormiga(id="H1", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
    h2 = Hormiga(id="H2", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
    h3 = Hormiga(id="H3", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
    
    tarea.agregar_hormiga(h1)
    tarea.agregar_hormiga(h2)
    tarea.agregar_hormiga(h3)
    
    lote_id = "TEST_LOTE"
    
    # 1. Guardar alimento
    print("\n1. Guardando alimento...")
    resultado = await persistence.guardar_alimento(alimento)
    print(f"   Resultado: {resultado}")
    if not resultado:
        print(f"   Error: {persistence.db.last_error}")
    
    # 2. Guardar tarea
    print("\n2. Guardando tarea...")
    resultado = await persistence.guardar_tarea(tarea)
    print(f"   Resultado: {resultado}")
    if not resultado:
        print(f"   Error: {persistence.db.last_error}")
    
    # 3. Crear lote
    print("\n3. Creando lote...")
    exito, error = await persistence.crear_lote_hormigas(lote_id, tarea.id, 3, 3)
    print(f"   Resultado: {exito}, Error: {error}")
    
    # 4. Aceptar lote
    if exito:
        print("\n4. Aceptando lote...")
        exito2, error2 = await persistence.aceptar_lote_hormigas(lote_id)
        print(f"   Resultado: {exito2}, Error: {error2}")
    
    # 5. Guardar hormigas en lote
    if exito:
        print("\n5. Guardando hormigas en lote...")
        resultado = await persistence.guardar_hormigas_en_lote(lote_id, [h1, h2, h3])
        print(f"   Resultado: {resultado}")
    
    # 6. Verificar en BD
    print("\n6. Verificando en BD...")
    cursor = db.connection.cursor()
    
    # Verificar tarea
    db._exec(cursor, "SELECT COUNT(*) FROM dbo.Tareas WHERE id = ?", (tarea.id,))
    count = cursor.fetchone()[0]
    print(f"   Tareas encontradas: {count}")
    
    # Verificar lote
    db._exec(cursor, "SELECT COUNT(*) FROM dbo.lotes_hormigas WHERE lote_id = ?", (lote_id,))
    count = cursor.fetchone()[0]
    print(f"   Lotes encontrados: {count}")
    
    # Verificar asignaciones
    db._exec(cursor, "SELECT COUNT(*) FROM dbo.asignaciones_hormiga_tarea WHERE tarea_id = ?", (tarea.id,))
    count = cursor.fetchone()[0]
    print(f"   Asignaciones encontradas: {count}")
    
    db.connection.close()

if __name__ == "__main__":
    asyncio.run(test_persistencia())



