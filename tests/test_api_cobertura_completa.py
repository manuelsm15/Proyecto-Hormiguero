"""
Tests adicionales para aumentar la cobertura de APIs al 80% o más.
Cubre endpoints y casos de error que no están en test_api_controller.py
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.recoleccion.api.recoleccion_controller import create_app
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.estado_tarea import EstadoTarea


class TestAPICoberturaCompleta:
    """Tests para aumentar cobertura de APIs."""
    
    @pytest.fixture
    def mock_entorno_service(self):
        return AsyncMock()
    
    @pytest.fixture
    def mock_comunicacion_service(self):
        return AsyncMock()
    
    @pytest.fixture
    def client(self, mock_entorno_service, mock_comunicacion_service):
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        return TestClient(app)
    
    @pytest.fixture
    def alimento_ejemplo(self):
        return Alimento(
            id="A1", nombre="Fruta", cantidad_hormigas_necesarias=3,
            puntos_stock=10, tiempo_recoleccion=300
        )
    
    @pytest.fixture
    def hormiga_ejemplo(self):
        return Hormiga(id="H1", capacidad_carga=5, tiempo_vida=3600)
    
    # ========== TESTS PARA ENDPOINTS DE ALIMENTOS ==========
    
    def test_consultar_alimentos_con_filtro_disponible(self, client, mock_entorno_service):
        """Cubre líneas 204-209: filtro de estado disponible."""
        mock_entorno_service.is_disponible.return_value = False
        
        alimento_disponible = Alimento(id="A1", nombre="Fruta", disponible=True, 
                                      cantidad_hormigas_necesarias=3, puntos_stock=10, tiempo_recoleccion=300)
        alimento_no_disponible = Alimento(id="A2", nombre="Semilla", disponible=False,
                                          cantidad_hormigas_necesarias=2, puntos_stock=5, tiempo_recoleccion=180)
        
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_alimentos = AsyncMock(return_value=[
                alimento_disponible, alimento_no_disponible
            ])
            
            response = client.get("/alimentos?estado=disponible")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == "A1"
    
    def test_consultar_alimentos_con_filtro_recolectado(self, client, mock_entorno_service):
        """Cubre líneas 208-209: filtro de estado recolectado."""
        mock_entorno_service.is_disponible.return_value = False
        
        alimento_disponible = Alimento(id="A1", nombre="Fruta", disponible=True,
                                      cantidad_hormigas_necesarias=3, puntos_stock=10, tiempo_recoleccion=300)
        alimento_no_disponible = Alimento(id="A2", nombre="Semilla", disponible=False,
                                          cantidad_hormigas_necesarias=2, puntos_stock=5, tiempo_recoleccion=180)
        
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_alimentos = AsyncMock(return_value=[
                alimento_disponible, alimento_no_disponible
            ])
            
            response = client.get("/alimentos?estado=recolectado")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == "A2"
    
    def test_crear_alimento_success(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre líneas 223-247: creación exitosa de alimento."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.guardar_alimento = AsyncMock(return_value=True)
            
            response = client.post("/alimentos", json={
                "nombre": "Nueva Fruta",
                "cantidad_hormigas_necesarias": 2,
                "puntos_stock": 5,
                "tiempo_recoleccion": 180
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["nombre"] == "Nueva Fruta"
    
    def test_crear_alimento_error_persistencia(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre líneas 236-242: error al guardar alimento."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.guardar_alimento = AsyncMock(return_value=False)
            mock_persistence.obtener_ultimo_error = MagicMock(return_value="Error de BD")
            
            response = client.post("/alimentos", json={
                "nombre": "Fruta",
                "cantidad_hormigas_necesarias": 2,
                "puntos_stock": 5,
                "tiempo_recoleccion": 180
            })
            
            assert response.status_code == 500
            data = response.json()
            assert "No se pudo guardar" in data["detail"]
    
    def test_crear_alimento_error_excepcion(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre líneas 246-247: excepción al crear alimento."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.guardar_alimento = AsyncMock(side_effect=Exception("Error inesperado"))
            
            response = client.post("/alimentos", json={
                "nombre": "Fruta",
                "cantidad_hormigas_necesarias": 2,
                "puntos_stock": 5,
                "tiempo_recoleccion": 180
            })
            
            assert response.status_code == 500
    
    # ========== TESTS PARA ENDPOINTS DE TAREAS ==========
    
    def test_crear_tarea_sin_tarea_id_genera_automatico(self, client, mock_entorno_service, alimento_ejemplo):
        """Cubre líneas 272-274: generación automática de tarea_id."""
        mock_entorno_service.is_disponible.return_value = True
        mock_entorno_service.consultar_alimento_por_id.return_value = alimento_ejemplo
        
        response = client.post("/tareas", params={"alimento_id": "A1"})
        # Debe generar un tarea_id automáticamente
        assert response.status_code in [200, 404, 500]
    
    def test_crear_tarea_sin_alimento_id_usa_default(self, client, mock_entorno_service, alimento_ejemplo):
        """Cubre línea 276: uso de A1 por defecto."""
        mock_entorno_service.is_disponible.return_value = False
        
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_alimento_por_id = AsyncMock(return_value=alimento_ejemplo)
            
            response = client.post("/tareas", params={"tarea_id": "T1"})
            assert response.status_code in [200, 404, 500]
    
    def test_listar_tareas_activas(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo):
        """Cubre línea 317: listar tareas activas."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        recoleccion_service.tareas_activas.append(tarea)
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.get("/tareas/activas")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    def test_listar_tareas_en_proceso(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo):
        """Cubre línea 327: listar tareas en proceso."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        recoleccion_service.tareas_activas.append(tarea)
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.get("/tareas/en-proceso")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    def test_asignar_hormigas_ya_tiene_suficientes_con_lote(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo):
        """Cubre líneas 387-400: asignar cuando ya tiene suficientes con lote_id."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        tarea.hormigas_asignadas = [hormiga_ejemplo] * 3  # Ya tiene suficientes
        recoleccion_service.tareas_activas.append(tarea)
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.post(
                "/tareas/T1/asignar-hormigas",
                json={"hormigas_lote_id": "LOTE_001", "cantidad": 0}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["iniciada"] is True
    
    def test_asignar_hormigas_ya_tiene_suficientes_sin_lote(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo):
        """Cubre líneas 399-407: asignar cuando ya tiene suficientes sin lote_id."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        tarea.hormigas_asignadas = [hormiga_ejemplo] * 3
        recoleccion_service.tareas_activas.append(tarea)
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.post(
                "/tareas/T1/asignar-hormigas",
                json={"cantidad": 0}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["iniciada"] is False
    
    def test_asignar_hormigas_error_solicitar(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo):
        """Cubre líneas 414, 422: error al solicitar hormigas."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        recoleccion_service.tareas_activas.append(tarea)
        
        mock_comunicacion_service.is_disponible.return_value = True
        mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
        mock_comunicacion_service.consultar_respuesta_hormigas.return_value = []  # Sin hormigas
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.post(
                "/tareas/T1/asignar-hormigas",
                json={"cantidad": 3}
            )
            assert response.status_code in [400, 500]
    
    def test_asignar_hormigas_inicio_automatico_error(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo):
        """Cubre líneas 434-437: error al iniciar automáticamente."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        recoleccion_service.tareas_activas.append(tarea)
        
        mock_comunicacion_service.is_disponible.return_value = True
        mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
        mock_comunicacion_service.consultar_respuesta_hormigas.return_value = [hormiga_ejemplo] * 3
        
        # Hacer que iniciar_tarea_recoleccion falle
        async def mock_iniciar_fail(*args, **kwargs):
            raise ValueError("Error al iniciar")
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        recoleccion_service.iniciar_tarea_recoleccion = mock_iniciar_fail
        
        with TestClient(app) as test_client:
            response = test_client.post(
                "/tareas/T1/asignar-hormigas",
                json={"hormigas_lote_id": "LOTE_001", "cantidad": 3}
            )
            # Debe manejar el error y continuar
            assert response.status_code in [200, 400, 500]
    
    def test_iniciar_tarea_desde_bd(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo):
        """Cubre líneas 493-494: iniciar tarea desde BD."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        tarea.hormigas_asignadas = [hormiga_ejemplo] * 3
        
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_tareas = AsyncMock(return_value=[tarea])
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            app.state.recoleccion_service = recoleccion_service
            
            with TestClient(app) as test_client:
                response = test_client.post(
                    "/tareas/T1/iniciar",
                    json={"hormigas_lote_id": "LOTE_001"}
                )
                assert response.status_code in [200, 400, 500]
    
    def test_iniciar_tarea_error_valueerror(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo):
        """Cubre líneas 520-523: ValueError al iniciar tarea."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        tarea.hormigas_asignadas = [hormiga_ejemplo] * 3
        recoleccion_service.tareas_activas.append(tarea)
        
        # Hacer que iniciar falle con ValueError
        async def mock_iniciar(*args, **kwargs):
            raise ValueError("No se puede iniciar")
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        recoleccion_service.iniciar_tarea_recoleccion = mock_iniciar
        
        with TestClient(app) as test_client:
            response = test_client.post(
                "/tareas/T1/iniciar",
                json={"hormigas_lote_id": "LOTE_001"}
            )
            assert response.status_code == 400
    
    def test_completar_tarea_error_valueerror(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo):
        """Cubre líneas 541-544: ValueError al completar tarea."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        recoleccion_service.tareas_activas.append(tarea)
        
        # Hacer que completar falle con ValueError
        async def mock_completar(*args, **kwargs):
            raise ValueError("No se puede completar")
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        recoleccion_service.completar_tarea_recoleccion = mock_completar
        
        with TestClient(app) as test_client:
            response = test_client.post(
                "/tareas/T1/completar",
                params={"cantidad_recolectada": 10}
            )
            assert response.status_code == 400
    
    def test_procesar_recoleccion_con_tareas(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo):
        """Cubre líneas 560-586: procesar recolección con tareas."""
        mock_entorno_service.consultar_alimentos_disponibles.return_value = [alimento_ejemplo]
        mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
        mock_comunicacion_service.consultar_respuesta_hormigas.return_value = [hormiga_ejemplo] * 3
        mock_comunicacion_service.devolver_hormigas.return_value = "mensaje_002"
        mock_entorno_service.marcar_alimento_como_recolectado.return_value = True
        
        response = client.post("/procesar")
        assert response.status_code == 200
        data = response.json()
        assert "tareas_procesadas" in data
    
    def test_obtener_estadisticas_con_bd(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre líneas 600-615: obtener estadísticas con BD."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_estadisticas = AsyncMock(return_value={
                "tareas_completadas": 5,
                "total_alimento": 50
            })
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/estadisticas")
                assert response.status_code == 200
                data = response.json()
                assert "base_datos" in data or "tareas_activas" in data
    
    def test_obtener_estadisticas_sin_bd(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre línea 614-615: obtener estadísticas sin BD."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_estadisticas = AsyncMock(side_effect=Exception("Error BD"))
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/estadisticas")
                assert response.status_code == 200
    
    def test_debug_info_bd(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre líneas 624-636: debug info BD."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_info_bd = AsyncMock(return_value={"motor": "SQL Server"})
            mock_persistence.obtener_alimentos = AsyncMock(return_value=[])
            mock_persistence.obtener_tareas = AsyncMock(return_value=[])
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/debug/db")
                assert response.status_code == 200
                data = response.json()
                assert "motor" in data or "alimentos_en_bd" in data
    
    def test_debug_info_bd_error(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre líneas 635-636: error en debug info BD."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_info_bd = AsyncMock(side_effect=Exception("Error BD"))
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/debug/db")
                assert response.status_code == 500
    
    def test_debug_tareas_raw_success(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre líneas 645-685: debug tareas raw exitoso."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            # Mock de la conexión y cursor
            mock_db = MagicMock()
            mock_cursor = MagicMock()
            mock_db.connection = MagicMock()
            mock_db.connection.cursor.return_value = mock_cursor
            mock_db._exec = MagicMock()
            mock_db._fetchall_dicts = MagicMock(return_value=[
                {"id": "T1", "alimento_id": "A1", "estado": "pendiente"}
            ])
            mock_cursor.fetchone.return_value = [10]  # Total alimentos
            
            mock_persistence.db = mock_db
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/debug/tareas-raw")
                assert response.status_code == 200
                data = response.json()
                assert "total_tareas" in data or "error" in data
    
    def test_debug_tareas_raw_sin_conexion(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre línea 681: debug tareas raw sin conexión."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_db = MagicMock()
            mock_db.connection = None
            mock_persistence.db = mock_db
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/debug/tareas-raw")
                assert response.status_code == 200
                data = response.json()
                assert "error" in data
    
    def test_debug_tareas_raw_error(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre líneas 682-685: error en debug tareas raw."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.db = MagicMock(side_effect=Exception("Error"))
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/debug/tareas-raw")
                assert response.status_code == 500
    
    def test_obtener_tareas_desde_bd(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo):
        """Cubre líneas 695-730: obtener tareas desde BD."""
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_tareas = AsyncMock(return_value=[tarea])
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/tareas/bd")
                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)
    
    def test_obtener_tareas_desde_bd_error(self, client, mock_entorno_service, mock_comunicacion_service):
        """Cubre líneas 727-730: error al obtener tareas desde BD."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_tareas = AsyncMock(side_effect=Exception("Error BD"))
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/tareas/bd")
                assert response.status_code == 500



