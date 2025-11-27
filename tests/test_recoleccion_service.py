"""
Pruebas unitarias para el servicio de recolección.
Siguiendo metodología TDD (Test-Driven Development).
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.recoleccion.services.recoleccion_service import RecoleccionService
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.estado_hormiga import EstadoHormiga
from src.recoleccion.models.estado_tarea import EstadoTarea
from src.recoleccion.models.tipo_mensaje import TipoMensaje


class TestRecoleccionService:
    """Pruebas para el servicio de recolección."""
    
    @pytest.fixture
    def mock_entorno_service(self):
        """Mock del servicio de entorno."""
        return AsyncMock()
    
    @pytest.fixture
    def mock_comunicacion_service(self):
        """Mock del servicio de comunicación."""
        return AsyncMock()
    
    @pytest.fixture
    def recoleccion_service(self, mock_entorno_service, mock_comunicacion_service):
        """Instancia del servicio de recolección con mocks."""
        return RecoleccionService(mock_entorno_service, mock_comunicacion_service)
    
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

    @pytest.mark.asyncio
    async def test_consultar_alimentos_disponibles_exitoso(
        self, recoleccion_service, mock_entorno_service, alimento_ejemplo
    ):
        """Prueba la consulta exitosa de alimentos disponibles."""
        # Arrange
        mock_entorno_service.is_disponible.return_value = True
        mock_entorno_service.consultar_alimentos_disponibles.return_value = [alimento_ejemplo]
        
        # Act
        resultado = await recoleccion_service.consultar_alimentos_disponibles()
        
        # Assert
        assert len(resultado) == 1
        assert resultado[0].id == "alimento_001"
        assert resultado[0].nombre == "Fruta"
        mock_entorno_service.consultar_alimentos_disponibles.assert_called_once_with(
            zona_id=None,
            estado=None
        )
    
    @pytest.mark.asyncio
    async def test_consultar_alimentos_disponibles_por_zona(
        self, recoleccion_service, mock_entorno_service, alimento_ejemplo
    ):
        """Prueba la consulta de alimentos filtrados por zona."""
        # Arrange
        mock_entorno_service.is_disponible.return_value = True
        mock_entorno_service.consultar_alimentos_disponibles.return_value = [alimento_ejemplo]
        
        # Act
        resultado = await recoleccion_service.consultar_alimentos_disponibles(zona_id=1)
        
        # Assert
        assert len(resultado) == 1
        mock_entorno_service.consultar_alimentos_disponibles.assert_called_once_with(
            zona_id=1,
            estado=None
        )
    
    @pytest.mark.asyncio
    async def test_consultar_alimentos_disponibles_por_estado(
        self, recoleccion_service, mock_entorno_service, alimento_ejemplo
    ):
        """Prueba la consulta de alimentos filtrados por estado."""
        # Arrange
        mock_entorno_service.is_disponible.return_value = True
        mock_entorno_service.consultar_alimentos_disponibles.return_value = [alimento_ejemplo]
        
        # Act
        resultado = await recoleccion_service.consultar_alimentos_disponibles(estado="disponible")
        
        # Assert
        assert len(resultado) == 1
        mock_entorno_service.consultar_alimentos_disponibles.assert_called_once_with(
            zona_id=None,
            estado="disponible"
        )

    @pytest.mark.asyncio
    async def test_consultar_alimentos_disponibles_servicio_no_disponible(
        self, recoleccion_service, mock_entorno_service
    ):
        """Prueba el manejo cuando el servicio de entorno no está disponible."""
        # Arrange
        mock_entorno_service.is_disponible.return_value = False
        
        # Act & Assert
        with pytest.raises(Exception, match="Servicio de entorno no disponible"):
            await recoleccion_service.consultar_alimentos_disponibles()

    @pytest.mark.asyncio
    async def test_crear_tarea_recoleccion_exitoso(
        self, recoleccion_service, alimento_ejemplo
    ):
        """Prueba la creación exitosa de una tarea de recolección."""
        # Act
        tarea = await recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", alimento_ejemplo
        )
        
        # Assert
        assert tarea.id == "tarea_001"
        assert tarea.alimento.id == "alimento_001"
        assert tarea.estado == EstadoTarea.PENDIENTE
        assert len(tarea.hormigas_asignadas) == 0

    @pytest.mark.asyncio
    async def test_solicitar_hormigas_exitoso(
        self, recoleccion_service, mock_comunicacion_service, hormiga_ejemplo
    ):
        """Prueba la solicitud exitosa de hormigas."""
        # Arrange
        mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
        mock_comunicacion_service.consultar_respuesta_hormigas.return_value = [hormiga_ejemplo]
        
        # Act
        hormigas = await recoleccion_service.solicitar_hormigas(3)
        
        # Assert
        assert len(hormigas) == 1
        assert hormigas[0].id == "hormiga_001"
        mock_comunicacion_service.solicitar_hormigas.assert_called_once_with(3, "recoleccion")

    @pytest.mark.asyncio
    async def test_asignar_hormigas_a_tarea_exitoso(
        self, recoleccion_service, alimento_ejemplo, hormiga_ejemplo
    ):
        """Prueba la asignación exitosa de hormigas a una tarea."""
        # Arrange
        tarea = await recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", alimento_ejemplo
        )
        
        # Act
        # Enviar suficientes hormigas (3) para que pase la validación
        await recoleccion_service.asignar_hormigas_a_tarea(tarea, [hormiga_ejemplo] * 3)
        
        # Assert
        assert len(tarea.hormigas_asignadas) == 3
        assert tarea.hormigas_asignadas[0].id == "hormiga_001"

    @pytest.mark.asyncio
    async def test_iniciar_tarea_recoleccion_exitoso(
        self, recoleccion_service, alimento_ejemplo, hormiga_ejemplo
    ):
        """Prueba el inicio exitoso de una tarea de recolección."""
        # Arrange
        tarea = await recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", alimento_ejemplo
        )
        await recoleccion_service.asignar_hormigas_a_tarea(tarea, [hormiga_ejemplo] * 3)
        
        # Act
        await recoleccion_service.iniciar_tarea_recoleccion(tarea)
        
        # Assert
        assert tarea.estado == EstadoTarea.EN_PROCESO
        assert tarea.fecha_inicio is not None

    @pytest.mark.asyncio
    async def test_iniciar_tarea_sin_suficientes_hormigas_falla(
        self, recoleccion_service, alimento_ejemplo, hormiga_ejemplo
    ):
        """Prueba que falla al iniciar una tarea sin suficientes hormigas."""
        # Arrange
        tarea = await recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", alimento_ejemplo
        )
        await recoleccion_service.asignar_hormigas_a_tarea(tarea, [hormiga_ejemplo])  # Solo 1 hormiga, necesita 3
        
        # Act & Assert
        with pytest.raises(ValueError, match="No se puede iniciar la tarea sin suficientes hormigas"):
            await recoleccion_service.iniciar_tarea_recoleccion(tarea)

    @pytest.mark.asyncio
    @patch('src.recoleccion.services.recoleccion_service.timer_service')
    async def test_completar_tarea_recoleccion_exitoso(
        self, mock_timer_service, recoleccion_service, alimento_ejemplo, hormiga_ejemplo
    ):
        """Prueba la finalización exitosa de una tarea de recolección."""
        # Configurar mock del timer service
        mock_timer_service.iniciar_tarea_timer = AsyncMock(return_value=True)
        
        # Arrange
        tarea = await recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", alimento_ejemplo
        )
        await recoleccion_service.asignar_hormigas_a_tarea(tarea, [hormiga_ejemplo] * 3)
        await recoleccion_service.iniciar_tarea_recoleccion(tarea)
        
        # Cambiar estado a EN_PROCESO para poder completar
        from src.recoleccion.models.estado_tarea import EstadoTarea
        tarea.estado = EstadoTarea.EN_PROCESO
        
        # Act
        await recoleccion_service.completar_tarea_recoleccion(tarea, 10)
        
        # Assert
        assert tarea.estado == EstadoTarea.COMPLETADA
        assert tarea.alimento_recolectado == 10
        assert tarea.fecha_fin is not None
        # Verificar que el alimento se marcó como no disponible
        assert tarea.alimento.disponible is False

    @pytest.mark.asyncio
    async def test_devolver_hormigas_exitoso(
        self, recoleccion_service, mock_comunicacion_service, hormiga_ejemplo
    ):
        """Prueba la devolución exitosa de hormigas."""
        # Arrange
        mock_comunicacion_service.devolver_hormigas.return_value = "mensaje_002"
        
        # Act
        mensaje_id = await recoleccion_service.devolver_hormigas(
            [hormiga_ejemplo], 10
        )
        
        # Assert
        assert mensaje_id == "mensaje_002"
        mock_comunicacion_service.devolver_hormigas.assert_called_once_with(
            [hormiga_ejemplo], 10
        )

    @pytest.mark.asyncio
    async def test_procesar_tarea_completa_exitoso(
        self, recoleccion_service, mock_entorno_service, mock_comunicacion_service, 
        alimento_ejemplo, hormiga_ejemplo
    ):
        """Prueba el procesamiento completo de una tarea de recolección."""
        from unittest.mock import patch, AsyncMock
        
        # Arrange
        mock_entorno_service.is_disponible.return_value = True
        mock_entorno_service.consultar_alimentos_disponibles.return_value = [alimento_ejemplo]
        mock_comunicacion_service.is_disponible.return_value = True
        mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
        mock_comunicacion_service.consultar_respuesta_hormigas.return_value = [hormiga_ejemplo] * 3
        mock_comunicacion_service.devolver_hormigas.return_value = "mensaje_002"
        mock_entorno_service.marcar_alimento_como_recolectado.return_value = True
        
        # Mockear la BD para que retorne lista vacía y use el servicio de entorno
        with patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            mock_persistence.obtener_alimentos = AsyncMock(return_value=[])
            
            # Act
            resultado = await recoleccion_service.procesar_recoleccion()
            
            # Assert
            assert resultado is not None
            assert len(resultado) > 0
        mock_entorno_service.consultar_alimentos_disponibles.assert_called_once()
        mock_comunicacion_service.solicitar_hormigas.assert_called_once()
        mock_comunicacion_service.devolver_hormigas.assert_called_once()
        mock_entorno_service.marcar_alimento_como_recolectado.assert_called_once()

    @pytest.mark.asyncio
    @patch('src.recoleccion.services.recoleccion_service.timer_service')
    async def test_iniciar_tarea_con_hormigas_lote_id(
        self, mock_timer_service, recoleccion_service, alimento_ejemplo, hormiga_ejemplo
    ):
        """Prueba el inicio de una tarea con hormigas_lote_id."""
        # Configurar mock del timer service para que inicie la tarea
        async def mock_iniciar_tarea_timer(tarea):
            tarea.iniciar_tarea()
            return True
        mock_timer_service.iniciar_tarea_timer = AsyncMock(side_effect=mock_iniciar_tarea_timer)
        
        # Arrange
        tarea = await recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", alimento_ejemplo
        )
        await recoleccion_service.asignar_hormigas_a_tarea(tarea, [hormiga_ejemplo] * 3)
        lote_id = "LOTE_001"
        
        # Act
        await recoleccion_service.iniciar_tarea_recoleccion(tarea, hormigas_lote_id=lote_id)
        
        # Assert
        assert tarea.estado == EstadoTarea.EN_PROCESO
        assert tarea.fecha_inicio is not None
        assert tarea.hormigas_lote_id == lote_id

    @pytest.mark.asyncio
    @patch('src.recoleccion.services.recoleccion_service.timer_service')
    async def test_verificar_y_completar_tarea_por_tiempo_exitoso(
        self, mock_timer_service, recoleccion_service, alimento_ejemplo, hormiga_ejemplo
    ):
        """Prueba el completado automático de una tarea por tiempo transcurrido."""
        from datetime import datetime, timedelta
        
        # Configurar mock del timer service para que inicie la tarea
        async def mock_iniciar_tarea_timer(tarea):
            tarea.iniciar_tarea()
            return True
        mock_timer_service.iniciar_tarea_timer = AsyncMock(side_effect=mock_iniciar_tarea_timer)
        
        # Arrange
        tarea = await recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", alimento_ejemplo
        )
        await recoleccion_service.asignar_hormigas_a_tarea(tarea, [hormiga_ejemplo] * 3)
        await recoleccion_service.iniciar_tarea_recoleccion(tarea, hormigas_lote_id="LOTE_001")
        
        # Simular que ha pasado el tiempo de recolección
        tarea.fecha_inicio = datetime.now() - timedelta(seconds=alimento_ejemplo.tiempo_recoleccion + 10)
        
        # Act
        completada = await recoleccion_service.verificar_y_completar_tarea_por_tiempo(tarea)
        
        # Assert
        assert completada is True
        assert tarea.estado == EstadoTarea.COMPLETADA
        assert tarea.fecha_fin is not None
        assert tarea.alimento.disponible is False
        # Verificar que fecha_fin es fecha_inicio + tiempo_recoleccion
        fecha_fin_esperada = tarea.fecha_inicio + timedelta(seconds=alimento_ejemplo.tiempo_recoleccion)
        assert abs((tarea.fecha_fin - fecha_fin_esperada).total_seconds()) < 1  # Tolerancia de 1 segundo

    @pytest.mark.asyncio
    @patch('src.recoleccion.services.recoleccion_service.timer_service')
    async def test_verificar_y_completar_tarea_por_tiempo_no_completada(
        self, mock_timer_service, recoleccion_service, alimento_ejemplo, hormiga_ejemplo
    ):
        """Prueba que una tarea no se completa si no ha pasado el tiempo suficiente."""
        from datetime import datetime, timedelta
        
        # Configurar mock del timer service para que inicie la tarea
        async def mock_iniciar_tarea_timer(tarea):
            tarea.iniciar_tarea()
            return True
        mock_timer_service.iniciar_tarea_timer = AsyncMock(side_effect=mock_iniciar_tarea_timer)
        
        # Arrange
        tarea = await recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", alimento_ejemplo
        )
        await recoleccion_service.asignar_hormigas_a_tarea(tarea, [hormiga_ejemplo] * 3)
        await recoleccion_service.iniciar_tarea_recoleccion(tarea, hormigas_lote_id="LOTE_001")
        
        # Simular que solo ha pasado la mitad del tiempo
        tarea.fecha_inicio = datetime.now() - timedelta(seconds=alimento_ejemplo.tiempo_recoleccion / 2)
        
        # Act
        completada = await recoleccion_service.verificar_y_completar_tarea_por_tiempo(tarea)
        
        # Assert
        assert completada is False
        assert tarea.estado == EstadoTarea.EN_PROCESO
        assert tarea.fecha_fin is None

    @pytest.mark.asyncio
    async def test_verificar_y_completar_tarea_por_tiempo_tarea_pendiente(
        self, recoleccion_service, alimento_ejemplo
    ):
        """Prueba que una tarea pendiente no se completa automáticamente."""
        # Arrange
        tarea = await recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", alimento_ejemplo
        )
        # Tarea en estado PENDIENTE, sin fecha_inicio
        
        # Act
        completada = await recoleccion_service.verificar_y_completar_tarea_por_tiempo(tarea)
        
        # Assert
        assert completada is False
        assert tarea.estado == EstadoTarea.PENDIENTE

    @pytest.mark.asyncio
    async def test_crear_tarea_con_alimento_no_disponible_debe_fallar(
        self, recoleccion_service
    ):
        """Prueba que no se puede crear una tarea con un alimento no disponible."""
        # Arrange
        alimento_no_disponible = Alimento(
            id="alimento_002",
            nombre="Fruta Agotada",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=300,
            disponible=False
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="no está disponible"):
            await recoleccion_service.crear_tarea_recoleccion(
                "tarea_001", alimento_no_disponible
            )
