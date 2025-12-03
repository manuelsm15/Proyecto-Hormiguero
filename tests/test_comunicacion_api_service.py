"""
Tests unitarios para ComunicacionAPIService para subir cobertura >80%.
"""

import pytest
from unittest.mock import AsyncMock

from src.recoleccion.services.comunicacion_api_service import ComunicacionAPIService
from src.recoleccion.models.mensaje import Mensaje
from src.recoleccion.models.tipo_mensaje import TipoMensaje
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.estado_hormiga import EstadoHormiga


class FakeResponse:
    def __init__(self, status_code: int, json_data=None):
        self.status_code = status_code
        self._json = json_data or {}

    def json(self):
        return self._json


@pytest.mark.asyncio
async def test_comunicacion_api_make_request_200():
    """_make_request debe devolver json y marcar _disponible=True en 200."""
    service = ComunicacionAPIService(base_url="http://fake")

    async def fake_request(method, url, **kwargs):
        assert method == "GET"
        return FakeResponse(200, {"ok": True})

    service.client.request = fake_request  # type: ignore[assignment]

    data = await service._make_request("GET", "/messages")
    assert data == {"ok": True}
    assert service._disponible is True


@pytest.mark.asyncio
async def test_comunicacion_api_make_request_500():
    """_make_request debe devolver None y marcar _disponible=False en 500."""
    service = ComunicacionAPIService(base_url="http://fake")

    async def fake_request(method, url, **kwargs):
        return FakeResponse(500, {})

    service.client.request = fake_request  # type: ignore[assignment]

    data = await service._make_request("GET", "/messages")
    assert data is None
    assert service._disponible is False


@pytest.mark.asyncio
async def test_comunicacion_api_make_request_exception():
    """_make_request debe manejar excepciones y marcar _disponible=False."""
    service = ComunicacionAPIService(base_url="http://fake")

    async def fake_request(method, url, **kwargs):
        raise RuntimeError("fallo de red")

    service.client.request = fake_request  # type: ignore[assignment]

    data = await service._make_request("GET", "/messages")
    assert data is None
    assert service._disponible is False


def test_comunicacion_api_mapear_hormiga_api_a_modelo():
    """_mapear_hormiga_api_a_modelo debe construir una Hormiga válida."""
    service = ComunicacionAPIService(base_url="http://fake")
    hormiga_data = {
        "id": 123,
        "capacidad_carga": 7,
        "tiempo_vida": 1000,
        "subsistema_origen": "recoleccion",
    }
    hormiga = service._mapear_hormiga_api_a_modelo(hormiga_data)
    assert isinstance(hormiga, Hormiga)
    assert hormiga.id == "123"
    assert hormiga.capacidad_carga == 7
    assert hormiga.estado == EstadoHormiga.DISPONIBLE


@pytest.mark.asyncio
async def test_enviar_mensaje_con_respuesta_api():
    """enviar_mensaje debe usar el id devuelto por la API cuando existe."""
    service = ComunicacionAPIService(base_url="http://fake")

    async def fake_make_request(method, endpoint, **kwargs):
        assert endpoint == "/messages"
        return {"id": "msg_api_1"}

    service._make_request = fake_make_request  # type: ignore[assignment]

    mensaje = Mensaje(
        id="",
        tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
        contenido={"x": 1},
        subsistema_origen="recoleccion",
        subsistema_destino="entorno",
    )
    mid = await service.enviar_mensaje(mensaje)
    assert mid == "msg_api_1"
    assert mensaje.id == "msg_api_1"


@pytest.mark.asyncio
async def test_enviar_mensaje_sin_respuesta_genera_id_local():
    """Si _make_request devuelve None, enviar_mensaje debe generar un id local."""
    service = ComunicacionAPIService(base_url="http://fake")
    service._make_request = AsyncMock(return_value=None)  # type: ignore[assignment]

    mensaje = Mensaje(
        id="",
        tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
        contenido={},
        subsistema_origen="recoleccion",
        subsistema_destino="entorno",
    )
    mid = await service.enviar_mensaje(mensaje)
    assert mid.startswith("msg_")
    assert mensaje.id == mid


@pytest.mark.asyncio
async def test_solicitar_hormigas_usa_endpoint_especifico():
    """solicitar_hormigas debe usar /ants/request y devolver el id de la respuesta."""
    service = ComunicacionAPIService(base_url="http://fake")

    async def fake_make_request(method, endpoint, **kwargs):
        assert endpoint == "/ants/request"
        return {"message_id": "req_1"}

    service._make_request = fake_make_request  # type: ignore[assignment]

    mid = await service.solicitar_hormigas(5, "recoleccion")
    assert mid == "req_1"


@pytest.mark.asyncio
async def test_solicitar_hormigas_fallback_enviar_mensaje():
    """Si /ants/request no devuelve id, debe caer a enviar_mensaje."""
    service = ComunicacionAPIService(base_url="http://fake")

    async def fake_make_request(method, endpoint, **kwargs):
        # No devuelve id usable
        return {}

    service._make_request = fake_make_request  # type: ignore[assignment]

    # Parchear enviar_mensaje para ver que se llama
    async def fake_enviar(mensaje: Mensaje) -> str:
        return "desde_enviar"

    service.enviar_mensaje = fake_enviar  # type: ignore[assignment]

    mid = await service.solicitar_hormigas(3, "recoleccion")
    assert mid == "desde_enviar"


@pytest.mark.asyncio
async def test_consultar_respuesta_hormigas_por_endpoint_directo():
    """consultar_respuesta_hormigas debe mapear hormigas devueltas por /ants/response."""
    service = ComunicacionAPIService(base_url="http://fake")

    response_data = {
        "hormigas": [
            {"id": 1, "capacidad_carga": 5, "tiempo_vida": 1000},
            {"id": 2, "capacidad_carga": 6, "tiempo_vida": 1200},
        ]
    }

    async def fake_make_request(method, endpoint, **kwargs):
        assert endpoint == "/ants/response/msg1"
        return response_data

    service._make_request = fake_make_request  # type: ignore[assignment]

    hormigas = await service.consultar_respuesta_hormigas("msg1")
    assert len(hormigas) == 2
    assert all(isinstance(h, Hormiga) for h in hormigas)


@pytest.mark.asyncio
async def test_consultar_respuesta_hormigas_fallback_mensaje_procesado():
    """Si /ants/response devuelve None, debe usar consultar_mensaje y mapear hormigas."""
    service = ComunicacionAPIService(base_url="http://fake")

    # _make_request devuelve None para forzar el fallback
    service._make_request = AsyncMock(return_value=None)  # type: ignore[assignment]

    contenido = {
        "hormigas": [
            {"id": "H1", "capacidad_carga": 5, "tiempo_vida": 1000},
            {"id": "H2", "capacidad_carga": 6, "tiempo_vida": 1100},
        ]
    }
    mensaje = Mensaje(
        id="msg1",
        tipo=TipoMensaje.SOLICITAR_HORMIGAS_RECOLECCION,
        contenido=contenido,
        subsistema_origen="recoleccion",
        subsistema_destino="hormiga_reina",
        procesado=True,
    )

    async def fake_consultar_mensaje(mid: str):
        return mensaje

    service.consultar_mensaje = fake_consultar_mensaje  # type: ignore[assignment]

    hormigas = await service.consultar_respuesta_hormigas("msg1")
    assert len(hormigas) == 2
    assert hormigas[0].id == "H1"


@pytest.mark.asyncio
async def test_devolver_hormigas_usa_endpoint_especifico():
    """devolver_hormigas debe usar /ants/return y devolver id de la respuesta."""
    service = ComunicacionAPIService(base_url="http://fake")

    async def fake_make_request(method, endpoint, **kwargs):
        assert endpoint == "/ants/return"
        return {"mensaje_id": "dev_1"}

    service._make_request = fake_make_request  # type: ignore[assignment]

    hormigas = [
        Hormiga(id="H1", capacidad_carga=5, estado=EstadoHormiga.DISPONIBLE),
        Hormiga(id="H2", capacidad_carga=5, estado=EstadoHormiga.DISPONIBLE),
    ]

    mid = await service.devolver_hormigas(hormigas, 10)
    assert mid == "dev_1"


@pytest.mark.asyncio
async def test_devolver_hormigas_fallback_enviar_mensaje():
    """Si /ants/return no devuelve id, debe caer a enviar_mensaje."""
    service = ComunicacionAPIService(base_url="http://fake")

    async def fake_make_request(method, endpoint, **kwargs):
        return {}

    service._make_request = fake_make_request  # type: ignore[assignment]

    async def fake_enviar(mensaje: Mensaje) -> str:
        return "dev_local"

    service.enviar_mensaje = fake_enviar  # type: ignore[assignment]

    hormigas = [
        Hormiga(id="H1", capacidad_carga=5, estado=EstadoHormiga.DISPONIBLE),
    ]

    mid = await service.devolver_hormigas(hormigas, 5)
    assert mid == "dev_local"


@pytest.mark.asyncio
async def test_comunicacion_api_is_disponible():
    """is_disponible debe usar _make_request y reflejar _disponible."""
    service = ComunicacionAPIService(base_url="http://fake")
    service._make_request = AsyncMock(return_value={"status": "ok"})  # type: ignore[assignment]

    disponible = await service.is_disponible()
    assert disponible is True



