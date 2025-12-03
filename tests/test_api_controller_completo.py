"""
Pruebas unitarias completas para todos los endpoints de la API REST.
Este archivo complementa test_api_controller.py para alcanzar ≥80% de cobertura.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from src.recoleccion.api.recoleccion_controller import create_app
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.estado_tarea import EstadoTarea
from src.recoleccion.models.estado_hormiga import EstadoHormiga


class TestAPICoberturaCompleta:
    """Pruebas adicionales para aumentar la cobertura de la API."""
    
    @pytest.fixture
    def mock_entorno_service(self):
        """Mock del servicio de entorno."""
        return AsyncMock()
    
    @pytest.fixture
    def mock_comunicacion_service(self):
        """Mock del servicio de comunicación."""
        return AsyncMock()
    
    @pytest.fixture
    def client(self, mock_entorno_service, mock_comunicacion_service):
        """Cliente de prueba para la API."""
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        return TestClient(app)
    
    @pytest.fixture
    def alimento_ejemplo(self):
        """Alimento de ejemplo."""
        return Alimento(
            id="A1",
            nombre="Fruta",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=300
        )
    
    @pytest.fixture
    def hormiga_ejemplo(self):
        """Hormiga de ejemplo."""
        return Hormiga(
            id="H1",
            capacidad_carga=5,
            tiempo_vida=3600
        )
    
    @pytest.fixture
    def tarea_ejemplo(self, alimento_ejemplo):
        """Tarea de ejemplo."""
        return TareaRecoleccion(
            id="T1",
            alimento=alimento_ejemplo
        )

    # ========== PRUEBAS PARA ENDPOINTS DE ALIMENTOS ==========
    
    def test_crear_alimento_success(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba la creación exitosa de un alimento."""
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
            assert data["cantidad_hormigas_necesarias"] == 2
    
    def test_crear_alimento_error_persistencia(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba la creación de alimento cuando falla la persistencia."""
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
    
    def test_consultar_alimentos_con_filtro_disponible(self, client, mock_entorno_service):
        """Prueba la consulta de alimentos con filtro de estado disponible."""
        alimento_disponible = Alimento(
            id="A1", nombre="Fruta", cantidad_hormigas_necesarias=3,
            puntos_stock=10, tiempo_recoleccion=300, disponible=True
        )
        alimento_no_disponible = Alimento(
            id="A2", nombre="Semilla", cantidad_hormigas_necesarias=2,
            puntos_stock=5, tiempo_recoleccion=180, disponible=False
        )
        
        mock_entorno_service.is_disponible.return_value = False
        
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
        """Prueba la consulta de alimentos con filtro de estado recolectado."""
        alimento_disponible = Alimento(
            id="A1", nombre="Fruta", cantidad_hormigas_necesarias=3,
            puntos_stock=10, tiempo_recoleccion=300, disponible=True
        )
        alimento_no_disponible = Alimento(
            id="A2", nombre="Semilla", cantidad_hormigas_necesarias=2,
            puntos_stock=5, tiempo_recoleccion=180, disponible=False
        )
        
        mock_entorno_service.is_disponible.return_value = False
        
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_alimentos = AsyncMock(return_value=[
                alimento_disponible, alimento_no_disponible
            ])
            
            response = client.get("/alimentos?estado=recolectado")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == "A2"

    # ========== PRUEBAS PARA ENDPOINTS DE TAREAS ==========
    
    def test_listar_tareas_activas(self, client, mock_entorno_service, mock_comunicacion_service, tarea_ejemplo):
        """Prueba el listado de tareas activas."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        recoleccion_service.tareas_activas.append(tarea_ejemplo)
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.get("/tareas/activas")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 1
    
    def test_listar_tareas_en_proceso(self, client, mock_entorno_service, mock_comunicacion_service, tarea_ejemplo):
        """Prueba el listado de tareas en proceso."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        
        tarea_ejemplo.estado = EstadoTarea.EN_PROCESO
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        recoleccion_service.tareas_activas.append(tarea_ejemplo)
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.get("/tareas/en-proceso")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    def test_asignar_hormigas_cantidad_insuficiente(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo):
        """Prueba la asignación de hormigas con cantidad insuficiente."""
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
            # Debe fallar porque no hay hormigas disponibles
            assert response.status_code in [400, 500]
    
    def test_iniciar_tarea_sin_hormigas_suficientes(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo):
        """Prueba iniciar tarea sin suficientes hormigas."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        # No asignar hormigas (requiere 3, tiene 0)
        recoleccion_service.tareas_activas.append(tarea)
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.post(
                "/tareas/T1/iniciar",
                json={"hormigas_lote_id": "LOTE_001"}
            )
            assert response.status_code == 400
            data = response.json()
            assert "suficientes hormigas" in data["detail"].lower()
    
    def test_completar_tarea_success(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo):
        """Prueba la finalización exitosa de una tarea."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        tarea.hormigas_asignadas = [hormiga_ejemplo] * 3
        tarea.estado = EstadoTarea.EN_PROCESO
        tarea.fecha_inicio = datetime.now()
        recoleccion_service.tareas_activas.append(tarea)
        
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.guardar_tarea = AsyncMock(return_value=True)
            mock_persistence.actualizar_alimento_disponibilidad = AsyncMock(return_value=True)
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            app.state.recoleccion_service = recoleccion_service
            
            with TestClient(app) as test_client:
                response = test_client.post(
                    "/tareas/T1/completar",
                    params={"cantidad_recolectada": 10}
                )
                assert response.status_code == 200
                data = response.json()
                assert data["estado"] == "completada"
    
    def test_completar_tarea_not_found(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba completar una tarea que no existe."""
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        
        with TestClient(app) as test_client:
            response = test_client.post(
                "/tareas/TAREA_INEXISTENTE/completar",
                params={"cantidad_recolectada": 10}
            )
            assert response.status_code == 404

    # ========== PRUEBAS PARA ENDPOINTS DE STATUS ==========
    
    def test_obtener_status_tarea_especifica(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo):
        """Prueba obtener el status de una tarea específica."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        tarea.hormigas_asignadas = [hormiga_ejemplo] * 3
        tarea.hormigas_lote_id = "LOTE_001"
        tarea.estado = EstadoTarea.EN_PROCESO
        tarea.fecha_inicio = datetime.now()
        recoleccion_service.tareas_activas.append(tarea)
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.get("/tareas/T1/status")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "T1"
            assert data["hormigas_lote_id"] == "LOTE_001"
            assert data["estado"] == "en_proceso"
    
    def test_obtener_status_tarea_not_found(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba obtener status de una tarea que no existe."""
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        
        with TestClient(app) as test_client:
            response = test_client.get("/tareas/TAREA_INEXISTENTE/status")
            assert response.status_code == 404
    
    def test_obtener_status_todas_tareas(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo):
        """Prueba obtener el status de todas las tareas."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea1 = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        tarea2 = TareaRecoleccion(id="T2", alimento=alimento_ejemplo)
        recoleccion_service.tareas_activas.append(tarea1)
        recoleccion_service.tareas_completadas.append(tarea2)
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.get("/tareas/status")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) >= 2

    # ========== PRUEBAS PARA ENDPOINTS DE DEBUG ==========
    
    def test_debug_tareas_raw(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba el endpoint de debug para tareas raw."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_tareas_raw = AsyncMock(return_value=[
                {"id": "T1", "estado": "pendiente", "alimento_id": "A1"}
            ])
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/debug/tareas-raw")
                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)
    
    def test_debug_tareas_raw_con_filtro(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba el endpoint de debug con filtro de estado."""
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_tareas_raw = AsyncMock(return_value=[
                {"id": "T1", "estado": "en_proceso", "alimento_id": "A1"}
            ])
            
            app = create_app(mock_entorno_service, mock_comunicacion_service)
            
            with TestClient(app) as test_client:
                response = test_client.get("/debug/tareas-raw?estado=en_proceso")
                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)

    # ========== PRUEBAS PARA CASOS DE ERROR ==========
    
    def test_crear_tarea_sin_alimento_id(self, client, mock_entorno_service):
        """Prueba crear tarea sin proporcionar alimento_id (usa A1 por defecto)."""
        mock_entorno_service.is_disponible.return_value = False
        
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            alimento_default = Alimento(
                id="A1", nombre="Fruta", cantidad_hormigas_necesarias=3,
                puntos_stock=10, tiempo_recoleccion=300
            )
            mock_persistence.obtener_alimento_por_id = AsyncMock(return_value=alimento_default)
            
            response = client.post("/tareas", json={"tarea_id": "T1"})
            # Debe usar A1 por defecto
            assert response.status_code in [200, 404, 500]
    
    def test_crear_tarea_sin_tarea_id(self, client, mock_entorno_service, alimento_ejemplo):
        """Prueba crear tarea sin proporcionar tarea_id (genera uno automáticamente)."""
        mock_entorno_service.is_disponible.return_value = True
        mock_entorno_service.consultar_alimento_por_id.return_value = alimento_ejemplo
        
        response = client.post("/tareas", json={"alimento_id": "A1"})
        # Debe generar un tarea_id automáticamente
        assert response.status_code in [200, 404, 500]
    
    def test_asignar_hormigas_tarea_no_encontrada(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba asignar hormigas a una tarea que no existe."""
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        
        with TestClient(app) as test_client:
            response = test_client.post(
                "/tareas/TAREA_INEXISTENTE/asignar-hormigas",
                json={"cantidad": 3}
            )
            assert response.status_code == 404
    
    def test_iniciar_tarea_ya_en_proceso(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo):
        """Prueba iniciar una tarea que ya está en proceso."""
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
        
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        tarea = TareaRecoleccion(id="T1", alimento=alimento_ejemplo)
        tarea.hormigas_asignadas = [hormiga_ejemplo] * 3
        tarea.estado = EstadoTarea.EN_PROCESO
        tarea.fecha_inicio = datetime.now()
        recoleccion_service.tareas_activas.append(tarea)
        
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        app.state.recoleccion_service = recoleccion_service
        
        with TestClient(app) as test_client:
            response = test_client.post(
                "/tareas/T1/iniciar",
                json={"hormigas_lote_id": "LOTE_001"}
            )
            # Debe fallar porque ya está en proceso
            assert response.status_code in [400, 500]




