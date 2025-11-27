"""
Pruebas unitarias para RecoleccionService con TimerService mock.
"""

import pytest
from unittest.mock import AsyncMock, patch
from src.recoleccion.services.recoleccion_service import RecoleccionService
from src.recoleccion.services.mock_entorno_service import MockEntornoService
from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.estado_hormiga import EstadoHormiga


class TestRecoleccionServiceWithTimer:
    """Pruebas para RecoleccionService con TimerService."""
    
    @pytest.fixture
    def recoleccion_service(self):
        """Fixture para crear servicio de recolección."""
        entorno_service = MockEntornoService()
        comunicacion_service = MockComunicacionService()
        return RecoleccionService(entorno_service, comunicacion_service)
    
    @pytest.fixture
    def alimento_ejemplo(self):
        """Fixture para crear alimento de ejemplo."""
        return Alimento(
            id="A1",
            nombre="Fruta",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=300
        )
    
    @pytest.fixture
    def hormigas_ejemplo(self):
        """Fixture para crear hormigas de ejemplo."""
        return [
            Hormiga(id="hormiga_001", capacidad_carga=5, estado=EstadoHormiga.DISPONIBLE),
            Hormiga(id="hormiga_002", capacidad_carga=5, estado=EstadoHormiga.DISPONIBLE),
            Hormiga(id="hormiga_003", capacidad_carga=5, estado=EstadoHormiga.DISPONIBLE)
        ]
    
    @pytest.mark.asyncio
    async def test_consultar_alimentos_disponibles_exitoso(self, recoleccion_service):
        """Prueba consultar alimentos disponibles exitosamente."""
        alimentos = await recoleccion_service.consultar_alimentos_disponibles()
        
        assert len(alimentos) == 3
        assert all(isinstance(alimento, Alimento) for alimento in alimentos)
        assert all(alimento.disponible for alimento in alimentos)
        
        # Verificar IDs simplificados
        ids = [alimento.id for alimento in alimentos]
        assert "A1" in ids
        assert "A2" in ids
        assert "A3" in ids
    
    @pytest.mark.asyncio
    async def test_crear_tarea_recoleccion_exitoso(self, recoleccion_service, alimento_ejemplo):
        """Prueba crear tarea de recolección exitosamente."""
        tarea = await recoleccion_service.crear_tarea_recoleccion("tarea_001", alimento_ejemplo)
        
        assert tarea.id == "tarea_001"
        assert tarea.alimento.id == "A1"
        assert tarea.alimento.nombre == "Fruta"
        assert tarea.estado.value == "pendiente"
        assert len(tarea.hormigas_asignadas) == 0
    
    @pytest.mark.asyncio
    async def test_solicitar_hormigas_exitoso(self, recoleccion_service):
        """Prueba solicitar hormigas exitosamente."""
        hormigas = await recoleccion_service.solicitar_hormigas(3)
        
        assert len(hormigas) == 3
        assert all(isinstance(hormiga, Hormiga) for hormiga in hormigas)
        assert all(hormiga.estado == EstadoHormiga.DISPONIBLE for hormiga in hormigas)
    
    @pytest.mark.asyncio
    async def test_asignar_hormigas_a_tarea_exitoso(self, recoleccion_service, alimento_ejemplo, hormigas_ejemplo):
        """Prueba asignar hormigas a tarea exitosamente."""
        tarea = TareaRecoleccion(id="tarea_001", alimento=alimento_ejemplo)
        
        await recoleccion_service.asignar_hormigas_a_tarea(tarea, hormigas_ejemplo)
        
        assert len(tarea.hormigas_asignadas) == 3
        assert tarea.tiene_suficientes_hormigas() is True
        assert all(hormiga.estado == EstadoHormiga.DISPONIBLE for hormiga in tarea.hormigas_asignadas)
    
    @pytest.mark.asyncio
    @patch('src.recoleccion.services.recoleccion_service.timer_service')
    async def test_iniciar_tarea_recoleccion_exitoso(self, mock_timer_service, recoleccion_service, alimento_ejemplo, hormigas_ejemplo):
        """Prueba iniciar tarea de recolección exitosamente."""
        # Configurar mock del timer service
        mock_timer_service.iniciar_tarea_timer = AsyncMock(return_value=True)
        
        tarea = TareaRecoleccion(id="tarea_001", alimento=alimento_ejemplo)
        tarea.agregar_hormiga(hormigas_ejemplo[0])
        tarea.agregar_hormiga(hormigas_ejemplo[1])
        tarea.agregar_hormiga(hormigas_ejemplo[2])
        
        await recoleccion_service.iniciar_tarea_recoleccion(tarea)
        
        # Verificar que se llamó al timer service
        mock_timer_service.iniciar_tarea_timer.assert_called_once_with(tarea)
        
        # Verificar que la tarea se agregó a activas
        assert tarea in recoleccion_service.tareas_activas
    
    @pytest.mark.asyncio
    @patch('src.recoleccion.services.recoleccion_service.timer_service')
    async def test_iniciar_tarea_sin_suficientes_hormigas_falla(self, mock_timer_service, recoleccion_service, alimento_ejemplo):
        """Prueba que falla iniciar tarea sin suficientes hormigas."""
        tarea = TareaRecoleccion(id="tarea_001", alimento=alimento_ejemplo)
        # No agregar hormigas
        
        with pytest.raises(ValueError, match="No se puede iniciar la tarea sin suficientes hormigas"):
            await recoleccion_service.iniciar_tarea_recoleccion(tarea)
    
    @pytest.mark.asyncio
    async def test_completar_tarea_recoleccion_exitoso(self, recoleccion_service, alimento_ejemplo, hormigas_ejemplo):
        """Prueba completar tarea de recolección exitosamente."""
        tarea = TareaRecoleccion(id="tarea_001", alimento=alimento_ejemplo)
        tarea.agregar_hormiga(hormigas_ejemplo[0])
        tarea.agregar_hormiga(hormigas_ejemplo[1])
        tarea.agregar_hormiga(hormigas_ejemplo[2])
        
        # Cambiar estado a EN_PROCESO para poder completar
        from src.recoleccion.models.estado_tarea import EstadoTarea
        tarea.estado = EstadoTarea.EN_PROCESO
        
        # Agregar tarea a activas
        recoleccion_service.tareas_activas.append(tarea)
        
        await recoleccion_service.completar_tarea_recoleccion(tarea, 10)
        
        assert tarea.estado.value == "completada"
        assert tarea.alimento_recolectado == 10
        assert tarea not in recoleccion_service.tareas_activas
        assert tarea in recoleccion_service.tareas_completadas
        
        # Verificar que las hormigas cambiaron a transportando
        for hormiga in tarea.hormigas_asignadas:
            assert hormiga.estado == EstadoHormiga.TRANSPORTANDO
    
    @pytest.mark.asyncio
    async def test_devolver_hormigas_exitoso(self, recoleccion_service, hormigas_ejemplo):
        """Prueba devolver hormigas exitosamente."""
        mensaje_id = await recoleccion_service.devolver_hormigas(hormigas_ejemplo, 10)
        
        assert mensaje_id is not None
        assert isinstance(mensaje_id, str)
    
    @pytest.mark.asyncio
    async def test_procesar_tarea_completa_exitoso(self, recoleccion_service, alimento_ejemplo, hormigas_ejemplo):
        """Prueba procesar tarea completa exitosamente."""
        from unittest.mock import patch, AsyncMock
        
        # Arrange - configurar mocks del servicio usando patch
        with patch.object(recoleccion_service.entorno_service, 'is_disponible', return_value=True), \
             patch.object(recoleccion_service.entorno_service, 'consultar_alimentos_disponibles', return_value=[alimento_ejemplo]), \
             patch.object(recoleccion_service.entorno_service, 'marcar_alimento_como_recolectado', return_value=True), \
             patch.object(recoleccion_service.comunicacion_service, 'is_disponible', return_value=True), \
             patch.object(recoleccion_service.comunicacion_service, 'solicitar_hormigas', return_value="mensaje_001"), \
             patch.object(recoleccion_service.comunicacion_service, 'consultar_respuesta_hormigas', return_value=hormigas_ejemplo), \
             patch.object(recoleccion_service.comunicacion_service, 'devolver_hormigas', return_value="mensaje_002"), \
             patch('src.recoleccion.services.persistence_service.persistence_service') as mock_persistence:
            
            mock_persistence.obtener_alimentos = AsyncMock(return_value=[])
            
            resultado = await recoleccion_service.procesar_recoleccion()
            
            assert resultado is not None
            assert isinstance(resultado, list)
            assert len(resultado) > 0
        
        # Verificar que las tareas están completadas
        for tarea in resultado:
            assert tarea.estado.value == "completada"
            assert tarea.alimento_recolectado > 0
    
    @pytest.mark.asyncio
    async def test_obtener_estadisticas(self, recoleccion_service):
        """Prueba obtener estadísticas del servicio."""
        estadisticas = recoleccion_service.obtener_estadisticas()
        
        assert "tareas_activas" in estadisticas
        assert "tareas_completadas" in estadisticas
        assert "total_alimento_recolectado" in estadisticas
        
        assert isinstance(estadisticas["tareas_activas"], int)
        assert isinstance(estadisticas["tareas_completadas"], int)
        assert isinstance(estadisticas["total_alimento_recolectado"], int)
    
    @pytest.mark.asyncio
    async def test_verificar_hormigas_muertas(self, recoleccion_service):
        """Prueba verificar hormigas muertas."""
        # Este método debería ejecutarse sin errores
        await recoleccion_service.verificar_hormigas_muertas()
        
        # No hay assertions específicos ya que es un método de limpieza
        assert True
