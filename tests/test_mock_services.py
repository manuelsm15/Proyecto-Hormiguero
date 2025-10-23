"""
Pruebas unitarias para los servicios mock.
"""

import pytest
from unittest.mock import AsyncMock

from src.recoleccion.services.mock_entorno_service import MockEntornoService
from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.mensaje import Mensaje, TipoMensaje


class TestMockEntornoService:
    """Pruebas para el servicio mock de entorno."""
    
    def test_creacion_servicio(self):
        """Prueba la creación del servicio mock."""
        servicio = MockEntornoService()
        assert servicio is not None
        assert len(servicio.alimentos) == 3  # Datos iniciales
        assert servicio.disponible is True

    @pytest.mark.asyncio
    async def test_consultar_alimentos_disponibles(self):
        """Prueba la consulta de alimentos disponibles."""
        servicio = MockEntornoService()
        alimentos = await servicio.consultar_alimentos_disponibles()
        
        assert len(alimentos) == 3
        assert all(isinstance(alimento, Alimento) for alimento in alimentos)
        assert all(alimento.disponible for alimento in alimentos)

    @pytest.mark.asyncio
    async def test_consultar_alimento_por_id_existente(self):
        """Prueba la consulta de alimento por ID existente."""
        servicio = MockEntornoService()
        alimento = await servicio.consultar_alimento_por_id("A1")
        
        assert alimento is not None
        assert alimento.id == "A1"
        assert alimento.nombre == "Fruta"

    @pytest.mark.asyncio
    async def test_consultar_alimento_por_id_inexistente(self):
        """Prueba la consulta de alimento por ID inexistente."""
        servicio = MockEntornoService()
        alimento = await servicio.consultar_alimento_por_id("alimento_inexistente")
        
        assert alimento is None

    @pytest.mark.asyncio
    async def test_marcar_alimento_como_recolectado_existente(self):
        """Prueba marcar alimento como recolectado existente."""
        servicio = MockEntornoService()
        resultado = await servicio.marcar_alimento_como_recolectado("A1")
        
        assert resultado is True
        alimento = await servicio.consultar_alimento_por_id("A1")
        assert alimento.disponible is False

    @pytest.mark.asyncio
    async def test_marcar_alimento_como_recolectado_inexistente(self):
        """Prueba marcar alimento como recolectado inexistente."""
        servicio = MockEntornoService()
        resultado = await servicio.marcar_alimento_como_recolectado("alimento_inexistente")
        
        assert resultado is False

    @pytest.mark.asyncio
    async def test_is_disponible(self):
        """Prueba la verificación de disponibilidad."""
        servicio = MockEntornoService()
        assert await servicio.is_disponible() is True
        
        servicio.set_disponible(False)
        assert await servicio.is_disponible() is False

    @pytest.mark.asyncio
    async def test_agregar_alimento(self):
        """Prueba agregar un alimento al servicio."""
        servicio = MockEntornoService()
        nuevo_alimento = Alimento(
            id="alimento_nuevo",
            nombre="Nuevo Alimento",
            cantidad_hormigas_necesarias=2,
            puntos_stock=5,
            tiempo_recoleccion=180
        )
        
        servicio.agregar_alimento(nuevo_alimento)
        alimento = await servicio.consultar_alimento_por_id("alimento_nuevo")
        assert alimento is not None
        assert alimento.nombre == "Nuevo Alimento"

    def test_limpiar_alimentos(self):
        """Prueba limpiar todos los alimentos."""
        servicio = MockEntornoService()
        assert len(servicio.alimentos) == 3
        
        servicio.limpiar_alimentos()
        assert len(servicio.alimentos) == 3  # Se recargan los datos iniciales


class TestMockComunicacionService:
    """Pruebas para el servicio mock de comunicación."""
    
    def test_creacion_servicio(self):
        """Prueba la creación del servicio mock."""
        servicio = MockComunicacionService()
        assert servicio is not None
        assert len(servicio.mensajes) == 0
        assert len(servicio.respuestas_hormigas) == 0
        assert servicio.disponible is True
        assert servicio.contador_mensajes == 0

    @pytest.mark.asyncio
    async def test_enviar_mensaje(self):
        """Prueba el envío de un mensaje."""
        servicio = MockComunicacionService()
        mensaje = Mensaje(
            id="",
            tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
            contenido={"data": "test"},
            subsistema_origen="recoleccion",
            subsistema_destino="entorno"
        )
        
        mensaje_id = await servicio.enviar_mensaje(mensaje)
        
        assert mensaje_id == "mensaje_001"
        assert mensaje.id == "mensaje_001"
        assert mensaje_id in servicio.mensajes

    @pytest.mark.asyncio
    async def test_consultar_mensaje_existente(self):
        """Prueba la consulta de mensaje existente."""
        servicio = MockComunicacionService()
        mensaje = Mensaje(
            id="",
            tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
            contenido={"data": "test"},
            subsistema_origen="recoleccion",
            subsistema_destino="entorno"
        )
        
        mensaje_id = await servicio.enviar_mensaje(mensaje)
        mensaje_consultado = await servicio.consultar_mensaje(mensaje_id)
        
        assert mensaje_consultado is not None
        assert mensaje_consultado.id == mensaje_id

    @pytest.mark.asyncio
    async def test_consultar_mensaje_inexistente(self):
        """Prueba la consulta de mensaje inexistente."""
        servicio = MockComunicacionService()
        mensaje = await servicio.consultar_mensaje("mensaje_inexistente")
        
        assert mensaje is None

    @pytest.mark.asyncio
    async def test_solicitar_hormigas(self):
        """Prueba la solicitud de hormigas."""
        servicio = MockComunicacionService()
        mensaje_id = await servicio.solicitar_hormigas(3, "recoleccion")
        
        assert mensaje_id == "mensaje_001"
        mensaje = await servicio.consultar_mensaje(mensaje_id)
        assert mensaje.tipo == TipoMensaje.SOLICITAR_HORMIGAS_RECOLECCION
        assert mensaje.contenido["cantidad"] == 3
        assert mensaje.contenido["subsistema"] == "recoleccion"

    @pytest.mark.asyncio
    async def test_consultar_respuesta_hormigas_sin_respuesta_predefinida(self):
        """Prueba la consulta de respuesta de hormigas sin respuesta predefinida."""
        servicio = MockComunicacionService()
        mensaje_id = await servicio.solicitar_hormigas(3, "recoleccion")
        hormigas = await servicio.consultar_respuesta_hormigas(mensaje_id)
        
        assert len(hormigas) == 3
        assert all(isinstance(hormiga, Hormiga) for hormiga in hormigas)
        assert all(hormiga.subsistema_origen == "hormiga_reina" for hormiga in hormigas)

    @pytest.mark.asyncio
    async def test_consultar_respuesta_hormigas_con_respuesta_predefinida(self):
        """Prueba la consulta de respuesta de hormigas con respuesta predefinida."""
        servicio = MockComunicacionService()
        hormigas_predefinidas = [
            Hormiga(id="hormiga_001", subsistema_origen="hormiga_reina"),
            Hormiga(id="hormiga_002", subsistema_origen="hormiga_reina")
        ]
        
        servicio.configurar_respuesta_hormigas("mensaje_001", hormigas_predefinidas)
        hormigas = await servicio.consultar_respuesta_hormigas("mensaje_001")
        
        assert len(hormigas) == 2
        assert hormigas == hormigas_predefinidas

    @pytest.mark.asyncio
    async def test_devolver_hormigas(self):
        """Prueba la devolución de hormigas."""
        servicio = MockComunicacionService()
        hormigas = [
            Hormiga(id="hormiga_001", capacidad_carga=5),
            Hormiga(id="hormiga_002", capacidad_carga=5)
        ]
        
        mensaje_id = await servicio.devolver_hormigas(hormigas, 10)
        
        assert mensaje_id == "mensaje_001"
        mensaje = await servicio.consultar_mensaje(mensaje_id)
        assert mensaje.tipo == TipoMensaje.DEVOLVER_HORMIGAS_RECOLECCION
        assert mensaje.contenido["alimento_recolectado"] == 10
        assert len(mensaje.contenido["hormigas"]) == 2

    @pytest.mark.asyncio
    async def test_is_disponible(self):
        """Prueba la verificación de disponibilidad."""
        servicio = MockComunicacionService()
        assert await servicio.is_disponible() is True
        
        servicio.set_disponible(False)
        assert await servicio.is_disponible() is False

    def test_generar_hormigas_mock(self):
        """Prueba la generación de hormigas mock."""
        servicio = MockComunicacionService()
        hormigas = servicio._generar_hormigas_mock(3)
        
        assert len(hormigas) == 3
        assert all(isinstance(hormiga, Hormiga) for hormiga in hormigas)
        assert all(hormiga.subsistema_origen == "hormiga_reina" for hormiga in hormigas)

    def test_limpiar_mensajes(self):
        """Prueba limpiar todos los mensajes."""
        servicio = MockComunicacionService()
        # Simular que se han enviado mensajes
        servicio.contador_mensajes = 5
        servicio.mensajes = {"mensaje_001": "test"}
        servicio.respuestas_hormigas = {"mensaje_001": []}
        
        servicio.limpiar_mensajes()
        assert len(servicio.mensajes) == 0
        assert len(servicio.respuestas_hormigas) == 0
        assert servicio.contador_mensajes == 0
