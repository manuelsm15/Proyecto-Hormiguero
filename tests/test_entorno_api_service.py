"""
Tests unitarios para EntornoAPIService para subir cobertura >80%.
"""

import pytest
from unittest.mock import AsyncMock

from src.recoleccion.services.entorno_api_service import EntornoAPIService
from src.recoleccion.models.alimento import Alimento


class FakeResponse:
    def __init__(self, status_code: int, json_data=None):
        self.status_code = status_code
        self._json = json_data or {}

    def json(self):
        return self._json


@pytest.mark.asyncio
async def test_entorno_api_make_request_200():
    """_make_request debe devolver json y marcar _disponible=True en 200."""
    service = EntornoAPIService(base_url="http://fake")

    async def fake_request(method, url, **kwargs):
        assert method == "GET"
        return FakeResponse(200, {"ok": True})

    service.client.request = fake_request  # type: ignore[assignment]

    data = await service._make_request("GET", "/resources")
    assert data == {"ok": True}
    assert service._disponible is True


@pytest.mark.asyncio
async def test_entorno_api_make_request_404():
    """_make_request debe devolver None en 404 y mantener _disponible=True."""
    service = EntornoAPIService(base_url="http://fake")

    async def fake_request(method, url, **kwargs):
        return FakeResponse(404, {})

    service.client.request = fake_request  # type: ignore[assignment]

    data = await service._make_request("GET", "/resources/999")
    assert data is None
    assert service._disponible is True


@pytest.mark.asyncio
async def test_entorno_api_make_request_500():
    """_make_request debe devolver None y marcar _disponible=False en 500."""
    service = EntornoAPIService(base_url="http://fake")

    async def fake_request(method, url, **kwargs):
        return FakeResponse(500, {})

    service.client.request = fake_request  # type: ignore[assignment]

    data = await service._make_request("GET", "/resources")
    assert data is None
    assert service._disponible is False


@pytest.mark.asyncio
async def test_entorno_api_make_request_exception():
    """_make_request debe manejar excepciones y marcar _disponible=False."""
    service = EntornoAPIService(base_url="http://fake")

    async def fake_request(method, url, **kwargs):
        raise RuntimeError("fallo de red")

    service.client.request = fake_request  # type: ignore[assignment]

    data = await service._make_request("GET", "/resources")
    assert data is None
    assert service._disponible is False


def test_entorno_api_mapear_recurso_a_alimento_basico():
    """_mapear_recurso_a_alimento debe crear un Alimento con los campos correctos."""
    service = EntornoAPIService(base_url="http://fake")

    recurso = {
        "id": 10,
        "nombre": "Fruta Roja",
        "cantidad_requerida_hormigas": 4,
        "cantidad_unitaria": 20,
        "duracion_recoleccion": 120,
        "estado": "disponible",
    }

    alimento = service._mapear_recurso_a_alimento(recurso)
    assert isinstance(alimento, Alimento)
    assert alimento.id == "10"
    assert alimento.nombre == "Fruta Roja"
    assert alimento.cantidad_hormigas_necesarias == 4
    assert alimento.puntos_stock == 20
    assert alimento.tiempo_recoleccion == 120
    assert alimento.disponible is True


@pytest.mark.asyncio
async def test_entorno_api_consultar_alimentos_disponibles_lista():
    """consultar_alimentos_disponibles debe mapear listas de recursos a Alimento."""
    service = EntornoAPIService(base_url="http://fake")

    recursos = [
        {
            "id": 1,
            "nombre": "Fruta",
            "cantidad_requerida_hormigas": 3,
            "cantidad_unitaria": 10,
            "duracion_recoleccion": 60,
            "estado": "disponible",
        },
        {
            "id": 2,
            "nombre": "Semilla",
            "cantidad_requerida_hormigas": 2,
            "cantidad_unitaria": 5,
            "duracion_recoleccion": 30,
            "estado": "recolectado",
        },
    ]

    # Mockear _make_request para devolver lista
    service._make_request = AsyncMock(return_value=recursos)  # type: ignore[assignment]

    alimentos = await service.consultar_alimentos_disponibles()
    assert len(alimentos) == 2
    assert all(isinstance(a, Alimento) for a in alimentos)


@pytest.mark.asyncio
async def test_entorno_api_consultar_alimentos_disponibles_dict():
    """consultar_alimentos_disponibles debe aceptar un dict y devolver lista de un elemento."""
    service = EntornoAPIService(base_url="http://fake")

    recurso = {
        "id": 1,
        "nombre": "Fruta Única",
        "cantidad_requerida_hormigas": 3,
        "cantidad_unitaria": 10,
        "duracion_recoleccion": 60,
        "estado": "disponible",
    }

    service._make_request = AsyncMock(return_value=recurso)  # type: ignore[assignment]

    alimentos = await service.consultar_alimentos_disponibles()
    assert len(alimentos) == 1
    assert alimentos[0].nombre == "Fruta Única"


@pytest.mark.asyncio
async def test_entorno_api_consultar_alimentos_disponibles_sin_respuesta():
    """Si _make_request devuelve None en todos los endpoints, se devuelve lista vacía."""
    service = EntornoAPIService(base_url="http://fake")

    async def fake_make_request(method, endpoint, **kwargs):
        return None

    service._make_request = fake_make_request  # type: ignore[assignment]

    alimentos = await service.consultar_alimentos_disponibles()
    assert alimentos == []


@pytest.mark.asyncio
async def test_entorno_api_consultar_alimento_por_id_not_found():
    """consultar_alimento_por_id debe devolver None si _make_request devuelve None."""
    service = EntornoAPIService(base_url="http://fake")
    service._make_request = AsyncMock(return_value=None)  # type: ignore[assignment]

    alimento = await service.consultar_alimento_por_id("999")
    assert alimento is None


@pytest.mark.asyncio
async def test_entorno_api_marcar_alimento_como_recolectado_flujo_completo():
    """marcar_alimento_como_recolectado debe calcular nuevo estado y llamar PUT."""
    service = EntornoAPIService(base_url="http://fake")

    # Primero GET del recurso actual
    recurso_actual = {
        "id": 1,
        "nombre": "Fruta",
        "cantidad_unitaria": 10,
        "duracion_recoleccion": 60,
        "cantidad_requerida_hormigas": 3,
        "estado": "disponible",
    }

    llamadas = []

    async def fake_make_request(method, endpoint, **kwargs):
        llamadas.append((method, endpoint, kwargs))
        if method == "GET":
            return recurso_actual
        if method == "PUT":
            # Simular actualización exitosa
            return {"ok": True}
        return None

    service._make_request = fake_make_request  # type: ignore[assignment]

    ok = await service.marcar_alimento_como_recolectado("1", cantidad_recolectada=10)
    assert ok is True

    # Debe haberse hecho un GET y luego un PUT
    assert any(c[0] == "GET" for c in llamadas)
    assert any(c[0] == "PUT" for c in llamadas)


@pytest.mark.asyncio
async def test_entorno_api_is_disponible_usa_make_request():
    """is_disponible debe usar _make_request y reflejar _disponible."""
    service = EntornoAPIService(base_url="http://fake")
    service._make_request = AsyncMock(return_value=[{"id": 1}])  # type: ignore[assignment]

    disponible = await service.is_disponible()
    assert disponible is True



