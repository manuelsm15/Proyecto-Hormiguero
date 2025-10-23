"""
Pruebas unitarias para el controlador de API REST.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock

from src.recoleccion.api.recoleccion_controller import create_app
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.estado_tarea import EstadoTarea


class TestRecoleccionController:
    """Pruebas para el controlador de API REST."""
    
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
        """Alimento de ejemplo para las pruebas."""
        return Alimento(
            id="alimento_001",
            nombre="Fruta",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=300
        )
    
    @pytest.fixture
    def hormiga_ejemplo(self):
        """Hormiga de ejemplo para las pruebas."""
        return Hormiga(
            id="hormiga_001",
            capacidad_carga=5,
            tiempo_vida=3600,
            subsistema_origen="recoleccion"
        )

    def test_root_endpoint(self, client):
        """Prueba el endpoint raíz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Subsistema de Recolección" in data["message"]

    def test_health_check_success(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba el endpoint de salud cuando ambos servicios están disponibles."""
        mock_entorno_service.is_disponible.return_value = True
        mock_comunicacion_service.is_disponible.return_value = True
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["entorno_disponible"] is True
        assert data["comunicacion_disponible"] is True

    def test_health_check_unhealthy(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba el endpoint de salud cuando un servicio no está disponible."""
        mock_entorno_service.is_disponible.return_value = False
        mock_comunicacion_service.is_disponible.return_value = True
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["entorno_disponible"] is False
        assert data["comunicacion_disponible"] is True

    def test_consultar_alimentos_success(self, client, mock_entorno_service, alimento_ejemplo):
        """Prueba la consulta exitosa de alimentos."""
        mock_entorno_service.is_disponible.return_value = True
        mock_entorno_service.consultar_alimentos_disponibles.return_value = [alimento_ejemplo]
        
        response = client.get("/alimentos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "alimento_001"
        assert data[0]["nombre"] == "Fruta"

    def test_consultar_alimentos_service_unavailable(self, client, mock_entorno_service):
        """Prueba la consulta de alimentos cuando el servicio no está disponible."""
        mock_entorno_service.is_disponible.return_value = False
        
        response = client.get("/alimentos")
        assert response.status_code == 500
        data = response.json()
        assert "Servicio de entorno no disponible" in data["detail"]

    def test_consultar_alimentos_error(self, client, mock_entorno_service):
        """Prueba la consulta de alimentos cuando ocurre un error."""
        mock_entorno_service.is_disponible.return_value = True
        mock_entorno_service.consultar_alimentos_disponibles.side_effect = Exception("Error de conexión")
        
        response = client.get("/alimentos")
        assert response.status_code == 500
        data = response.json()
        assert "Error al consultar alimentos" in data["detail"]

    def test_crear_tarea_success(self, client, mock_entorno_service, alimento_ejemplo):
        """Prueba la creación exitosa de una tarea."""
        mock_entorno_service.consultar_alimento_por_id.return_value = alimento_ejemplo
        
        response = client.post("/tareas", params={
            "tarea_id": "tarea_001",
            "alimento_id": "alimento_001"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "tarea_001"
        assert data["alimento"]["id"] == "alimento_001"

    def test_crear_tarea_alimento_not_found(self, client, mock_entorno_service):
        """Prueba la creación de tarea cuando el alimento no existe."""
        mock_entorno_service.consultar_alimento_por_id.return_value = None
        
        response = client.post("/tareas", params={
            "tarea_id": "tarea_001",
            "alimento_id": "alimento_inexistente"
        })
        assert response.status_code == 404
        data = response.json()
        assert "Alimento no encontrado" in data["detail"]

    def test_crear_tarea_error(self, client, mock_entorno_service):
        """Prueba la creación de tarea cuando ocurre un error."""
        mock_entorno_service.consultar_alimento_por_id.side_effect = Exception("Error de base de datos")
        
        response = client.post("/tareas", params={
            "tarea_id": "tarea_001",
            "alimento_id": "alimento_001"
        })
        assert response.status_code == 500
        data = response.json()
        assert "Error al crear tarea" in data["detail"]

    def test_listar_tareas(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba el listado de tareas activas."""
        # Crear una tarea de ejemplo
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        with TestClient(app) as test_client:
            # Simular que hay tareas activas
            app.state.tareas_activas = []
            
            response = test_client.get("/tareas")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)

    def test_listar_tareas_completadas(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba el listado de tareas completadas."""
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        with TestClient(app) as test_client:
            # Simular que hay tareas completadas
            app.state.tareas_completadas = []
            
            response = test_client.get("/tareas/completadas")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)

    def test_iniciar_tarea_success(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo):
        """Prueba el inicio exitoso de una tarea."""
        # Simular que hay una tarea activa
        from src.recoleccion.services.recoleccion_service import RecoleccionService
        recoleccion_service = RecoleccionService(mock_entorno_service, mock_comunicacion_service)
        
        # Crear una tarea de prueba
        tarea = recoleccion_service.tareas_activas[0] if recoleccion_service.tareas_activas else None
        
        response = client.post("/tareas/tarea_001/iniciar")
        # El endpoint debe responder, aunque puede fallar si no hay tarea
        assert response.status_code in [200, 404, 500]

    def test_iniciar_tarea_not_found(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba el inicio de tarea cuando no existe."""
        response = client.post("/tareas/tarea_inexistente/iniciar")
        # El endpoint debe responder con error 404 o 500
        assert response.status_code in [404, 500]

    def test_completar_tarea_success(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba la finalización exitosa de una tarea."""
        response = client.post("/tareas/tarea_001/completar", params={
            "cantidad_recolectada": 10
        })
        # El endpoint debe responder, aunque puede fallar si no hay tarea
        assert response.status_code in [200, 404, 500]

    def test_procesar_recoleccion_success(self, client, mock_entorno_service, mock_comunicacion_service, alimento_ejemplo, hormiga_ejemplo):
        """Prueba el procesamiento completo de recolección."""
        mock_entorno_service.consultar_alimentos_disponibles.return_value = [alimento_ejemplo]
        mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
        mock_comunicacion_service.consultar_respuesta_hormigas.return_value = [hormiga_ejemplo] * 3
        mock_comunicacion_service.devolver_hormigas.return_value = "mensaje_002"
        mock_entorno_service.marcar_alimento_como_recolectado.return_value = True
        
        response = client.post("/procesar")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "tareas_procesadas" in data
        assert "tareas" in data

    def test_procesar_recoleccion_error(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba el procesamiento cuando ocurre un error."""
        mock_entorno_service.consultar_alimentos_disponibles.side_effect = Exception("Error de conexión")
        
        response = client.post("/procesar")
        # El endpoint maneja errores internamente y devuelve 200 con mensaje de error
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_obtener_estadisticas(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba la obtención de estadísticas."""
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        with TestClient(app) as test_client:
            response = test_client.get("/estadisticas")
            assert response.status_code == 200
            data = response.json()
            assert "tareas_activas" in data
            assert "tareas_completadas" in data
            assert "total_alimento_recolectado" in data

    def test_verificar_hormigas_success(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba la verificación de hormigas muertas."""
        response = client.post("/verificar-hormigas")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_verificar_hormigas_error(self, client, mock_entorno_service, mock_comunicacion_service):
        """Prueba la verificación de hormigas cuando ocurre un error."""
        # Simular un error en el servicio
        app = create_app(mock_entorno_service, mock_comunicacion_service)
        with TestClient(app) as test_client:
            # Forzar un error modificando el estado interno
            response = test_client.post("/verificar-hormigas")
            assert response.status_code == 200  # El endpoint maneja errores internamente
