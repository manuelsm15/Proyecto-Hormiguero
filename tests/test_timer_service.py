"""
Pruebas unitarias para el TimerService.
"""

import pytest
import asyncio
from datetime import datetime
from src.recoleccion.services.timer_service import TimerService
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.estado_tarea import EstadoTarea
from src.recoleccion.models.estado_hormiga import EstadoHormiga


class TestTimerService:
    """Pruebas para el TimerService."""
    
    def test_creacion_servicio(self):
        """Prueba la creación del servicio de timer."""
        timer_service = TimerService()
        assert timer_service is not None
        assert len(timer_service.tareas_en_proceso) == 0
        assert len(timer_service.timer_tasks) == 0
    
    @pytest.mark.asyncio
    async def test_iniciar_tarea_timer_exitoso(self):
        """Prueba iniciar timer para una tarea."""
        timer_service = TimerService()
        
        # Crear tarea de prueba
        alimento = Alimento(
            id="A1",
            nombre="Fruta",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=1  # 1 segundo para prueba rápida
        )
        
        hormiga = Hormiga(
            id="hormiga_001",
            capacidad_carga=5,
            estado=EstadoHormiga.DISPONIBLE
        )
        
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento
        )
        tarea.agregar_hormiga(hormiga)
        tarea.agregar_hormiga(hormiga)
        tarea.agregar_hormiga(hormiga)
        
        # Iniciar timer
        success = await timer_service.iniciar_tarea_timer(tarea)
        
        assert success is True
        assert tarea.id in timer_service.tareas_en_proceso
        assert tarea.estado == EstadoTarea.EN_PROCESO
        assert tarea.fecha_inicio is not None
        
        # Verificar que las hormigas cambiaron de estado
        for hormiga in tarea.hormigas_asignadas:
            assert hormiga.estado == EstadoHormiga.RECOLECTANDO
    
    @pytest.mark.asyncio
    async def test_iniciar_tarea_timer_sin_hormigas_falla(self):
        """Prueba que falla iniciar timer sin suficientes hormigas."""
        timer_service = TimerService()
        
        # Crear tarea sin hormigas
        alimento = Alimento(
            id="A1",
            nombre="Fruta",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=1
        )
        
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento
        )
        
        # No debería poder iniciar sin hormigas
        with pytest.raises(ValueError, match="No se puede iniciar la tarea sin suficientes hormigas"):
            await timer_service.iniciar_tarea_timer(tarea)
    
    @pytest.mark.asyncio
    async def test_cancelar_tarea_exitosa(self):
        """Prueba cancelar una tarea en proceso."""
        timer_service = TimerService()
        
        # Crear y iniciar tarea
        alimento = Alimento(
            id="A1",
            nombre="Fruta",
            cantidad_hormigas_necesarias=1,
            puntos_stock=10,
            tiempo_recoleccion=10  # 10 segundos
        )
        
        hormiga = Hormiga(
            id="hormiga_001",
            capacidad_carga=5,
            estado=EstadoHormiga.DISPONIBLE
        )
        
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento
        )
        tarea.agregar_hormiga(hormiga)
        
        # Iniciar timer
        await timer_service.iniciar_tarea_timer(tarea)
        
        # Cancelar tarea
        success = await timer_service.cancelar_tarea("tarea_001")
        
        assert success is True
        assert "tarea_001" not in timer_service.tareas_en_proceso
        assert "tarea_001" not in timer_service.timer_tasks
        assert tarea.estado == EstadoTarea.PAUSADA
        
        # Verificar que las hormigas volvieron a DISPONIBLE
        for hormiga in tarea.hormigas_asignadas:
            assert hormiga.estado == EstadoHormiga.DISPONIBLE
    
    def test_get_tiempo_restante_tarea_no_en_proceso(self):
        """Prueba obtener tiempo restante de tarea no en proceso."""
        timer_service = TimerService()
        
        tiempo_restante = timer_service.get_tiempo_restante("tarea_inexistente")
        assert tiempo_restante is None
    
    def test_get_progreso_tarea_no_en_proceso(self):
        """Prueba obtener progreso de tarea no en proceso."""
        timer_service = TimerService()
        
        progreso = timer_service.get_progreso("tarea_inexistente")
        assert progreso is None
    
    @pytest.mark.asyncio
    async def test_cleanup(self):
        """Prueba el cleanup del servicio."""
        timer_service = TimerService()
        
        # Crear tarea en proceso
        alimento = Alimento(
            id="A1",
            nombre="Fruta",
            cantidad_hormigas_necesarias=1,
            puntos_stock=10,
            tiempo_recoleccion=10
        )
        
        hormiga = Hormiga(
            id="hormiga_001",
            capacidad_carga=5,
            estado=EstadoHormiga.DISPONIBLE
        )
        
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento
        )
        tarea.agregar_hormiga(hormiga)
        
        await timer_service.iniciar_tarea_timer(tarea)
        
        # Verificar que hay tareas en proceso
        assert len(timer_service.tareas_en_proceso) > 0
        assert len(timer_service.timer_tasks) > 0
        
        # Cleanup
        await timer_service.cleanup()
        
        # Verificar que se limpió todo
        assert len(timer_service.tareas_en_proceso) == 0
        assert len(timer_service.timer_tasks) == 0

