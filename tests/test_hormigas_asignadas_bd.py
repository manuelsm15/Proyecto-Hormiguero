"""
Tests específicos para validar que hormigas_asignadas se guarda correctamente en la BD.
"""
import pytest
import os
from src.recoleccion.database.database_manager import DatabaseManager
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.estado_tarea import EstadoTarea
from src.recoleccion.models.estado_hormiga import EstadoHormiga


class TestHormigasAsignadasBD:
    """Tests para validar hormigas_asignadas en la base de datos."""
    
    @pytest.fixture
    def db(self):
        """Fixture para crear una base de datos de prueba."""
        db_path = "test_hormigas_asignadas.db"
        # Limpiar si existe
        if os.path.exists(db_path):
            os.remove(db_path)
        db = DatabaseManager(db_path)
        yield db
        # Limpiar después de las pruebas
        if os.path.exists(db_path):
            try:
                db.cerrar()
                os.remove(db_path)
            except:
                pass
    
    @pytest.fixture
    def alimento_ejemplo(self):
        """Fixture para crear un alimento de ejemplo."""
        return Alimento(
            id="A1",
            nombre="Fruta",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=300
        )
    
    def test_guardar_tarea_sin_hormigas_debe_guardar_cero(self, db, alimento_ejemplo):
        """Test que verifica que una tarea sin hormigas guarda 0 en hormigas_asignadas."""
        # Arrange
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        
        # Act
        db.guardar_alimento(alimento_ejemplo)
        db.guardar_tarea(tarea)
        
        # Assert - Verificar columna directamente
        cursor = db.connection.cursor()
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", ("T1",))
        result = cursor.fetchone()
        
        assert result is not None
        assert result[0] == 0, f"Se esperaba 0, se encontró {result[0]}"
    
    def test_guardar_tarea_con_hormigas_debe_guardar_cantidad(self, db, alimento_ejemplo):
        """Test que verifica que una tarea con hormigas guarda la cantidad correcta."""
        # Arrange
        tarea = TareaRecoleccion(id="T2", alimento=alimento_ejemplo)
        h1 = Hormiga(id="H1", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        h2 = Hormiga(id="H2", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        h3 = Hormiga(id="H3", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        
        tarea.agregar_hormiga(h1)
        tarea.agregar_hormiga(h2)
        tarea.agregar_hormiga(h3)
        
        # Act
        db.guardar_alimento(alimento_ejemplo)
        db.guardar_tarea(tarea)
        
        # Assert - Verificar columna directamente
        cursor = db.connection.cursor()
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", ("T2",))
        result = cursor.fetchone()
        
        assert result is not None
        assert result[0] == 3, f"Se esperaba 3, se encontró {result[0]}"
    
    def test_iniciar_tarea_mantiene_hormigas_asignadas(self, db, alimento_ejemplo):
        """Test que verifica que al iniciar una tarea, hormigas_asignadas se mantiene."""
        # Arrange
        tarea = TareaRecoleccion(id="T3", alimento=alimento_ejemplo)
        h1 = Hormiga(id="H1", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        h2 = Hormiga(id="H2", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        h3 = Hormiga(id="H3", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        
        tarea.agregar_hormiga(h1)
        tarea.agregar_hormiga(h2)
        tarea.agregar_hormiga(h3)
        
        # Act - Guardar, iniciar y guardar de nuevo
        db.guardar_alimento(alimento_ejemplo)
        db.guardar_tarea(tarea)
        
        # Verificar que se guardó correctamente antes de iniciar
        cursor = db.connection.cursor()
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", ("T3",))
        result_antes = cursor.fetchone()
        assert result_antes[0] == 3, "Debe tener 3 hormigas antes de iniciar"
        
        # Iniciar tarea
        tarea.iniciar_tarea()
        db.guardar_tarea(tarea)
        
        # Assert - Verificar que se mantiene después de iniciar
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", ("T3",))
        result_despues = cursor.fetchone()
        
        assert result_despues is not None
        assert result_despues[0] == 3, f"Se esperaba 3 después de iniciar, se encontró {result_despues[0]}"
    
    def test_completar_tarea_mantiene_hormigas_asignadas(self, db, alimento_ejemplo):
        """Test que verifica que al completar una tarea, hormigas_asignadas se mantiene."""
        # Arrange
        tarea = TareaRecoleccion(id="T4", alimento=alimento_ejemplo)
        h1 = Hormiga(id="H1", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        h2 = Hormiga(id="H2", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        h3 = Hormiga(id="H3", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        
        tarea.agregar_hormiga(h1)
        tarea.agregar_hormiga(h2)
        tarea.agregar_hormiga(h3)
        tarea.iniciar_tarea()
        
        # Act - Guardar, completar y guardar de nuevo
        db.guardar_alimento(alimento_ejemplo)
        db.guardar_tarea(tarea)
        
        # Verificar que se guardó correctamente antes de completar
        cursor = db.connection.cursor()
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", ("T4",))
        result_antes = cursor.fetchone()
        assert result_antes[0] == 3, "Debe tener 3 hormigas antes de completar"
        
        # Completar tarea
        tarea.completar_tarea(10)
        db.guardar_tarea(tarea)
        
        # Assert - Verificar que se mantiene después de completar
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", ("T4",))
        result_despues = cursor.fetchone()
        
        assert result_despues is not None
        assert result_despues[0] == 3, f"Se esperaba 3 después de completar, se encontró {result_despues[0]}"
    
    def test_actualizar_estado_no_elimina_hormigas_asignadas(self, db, alimento_ejemplo):
        """Test que verifica que actualizar_estado_tarea no elimina hormigas_asignadas."""
        # Arrange
        tarea = TareaRecoleccion(id="T5", alimento=alimento_ejemplo)
        h1 = Hormiga(id="H1", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        h2 = Hormiga(id="H2", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        h3 = Hormiga(id="H3", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        
        tarea.agregar_hormiga(h1)
        tarea.agregar_hormiga(h2)
        tarea.agregar_hormiga(h3)
        
        # Act - Guardar tarea con hormigas
        db.guardar_alimento(alimento_ejemplo)
        db.guardar_tarea(tarea)
        
        # Verificar que se guardó correctamente
        cursor = db.connection.cursor()
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", ("T5",))
        result_antes = cursor.fetchone()
        assert result_antes[0] == 3, "Debe tener 3 hormigas antes de actualizar estado"
        
        # Actualizar estado usando el método actualizar_estado_tarea
        db.actualizar_estado_tarea("T5", EstadoTarea.EN_PROCESO.value)
        
        # Assert - Verificar que hormigas_asignadas se mantiene
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", ("T5",))
        result_despues = cursor.fetchone()
        
        assert result_despues is not None
        assert result_despues[0] == 3, f"Se esperaba 3 después de actualizar estado, se encontró {result_despues[0]}"
    
    def test_agregar_mas_hormigas_actualiza_valor(self, db, alimento_ejemplo):
        """Test que verifica que agregar más hormigas actualiza el valor correctamente."""
        # Arrange
        tarea = TareaRecoleccion(id="T6", alimento=alimento_ejemplo)
        h1 = Hormiga(id="H1", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        h2 = Hormiga(id="H2", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        
        tarea.agregar_hormiga(h1)
        tarea.agregar_hormiga(h2)
        
        # Act - Guardar con 2 hormigas
        db.guardar_alimento(alimento_ejemplo)
        db.guardar_tarea(tarea)
        
        # Verificar que tiene 2
        cursor = db.connection.cursor()
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", ("T6",))
        result = cursor.fetchone()
        assert result[0] == 2, "Debe tener 2 hormigas inicialmente"
        
        # Agregar una hormiga más
        h3 = Hormiga(id="H3", estado=EstadoHormiga.DISPONIBLE, capacidad_carga=5)
        tarea.agregar_hormiga(h3)
        db.guardar_tarea(tarea)
        
        # Assert - Verificar que ahora tiene 3
        cursor.execute("SELECT hormigas_asignadas FROM tareas WHERE id = ?", ("T6",))
        result = cursor.fetchone()
        assert result[0] == 3, f"Se esperaba 3 después de agregar una hormiga, se encontró {result[0]}"



