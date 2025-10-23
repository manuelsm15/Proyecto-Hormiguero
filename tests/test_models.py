"""
Pruebas unitarias para los modelos de datos.
"""

import pytest
from datetime import datetime, timedelta

from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga, EstadoHormiga
from src.recoleccion.models.mensaje import Mensaje, TipoMensaje
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion, EstadoTarea


class TestAlimento:
    """Pruebas para el modelo Alimento."""
    
    def test_alimento_creacion_exitosa(self):
        """Prueba la creación exitosa de un alimento."""
        alimento = Alimento(
            id="alimento_001",
            nombre="Fruta",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=300
        )
        
        assert alimento.id == "alimento_001"
        assert alimento.nombre == "Fruta"
        assert alimento.cantidad_hormigas_necesarias == 3
        assert alimento.puntos_stock == 10
        assert alimento.tiempo_recoleccion == 300
        assert alimento.disponible is True
        assert isinstance(alimento.fecha_creacion, datetime)

    def test_alimento_validaciones_error(self):
        """Prueba las validaciones de un alimento."""
        with pytest.raises(ValueError, match="La cantidad de hormigas necesarias debe ser mayor a 0"):
            Alimento(
                id="alimento_001",
                nombre="Fruta",
                cantidad_hormigas_necesarias=0,
                puntos_stock=10,
                tiempo_recoleccion=300
            )
        
        with pytest.raises(ValueError, match="Los puntos de stock deben ser mayores a 0"):
            Alimento(
                id="alimento_001",
                nombre="Fruta",
                cantidad_hormigas_necesarias=3,
                puntos_stock=0,
                tiempo_recoleccion=300
            )
        
        with pytest.raises(ValueError, match="El tiempo de recolección debe ser mayor a 0"):
            Alimento(
                id="alimento_001",
                nombre="Fruta",
                cantidad_hormigas_necesarias=3,
                puntos_stock=10,
                tiempo_recoleccion=0
            )

    def test_marcar_como_recolectado(self):
        """Prueba marcar un alimento como recolectado."""
        alimento = Alimento(
            id="alimento_001",
            nombre="Fruta",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=300
        )
        
        assert alimento.disponible is True
        alimento.marcar_como_recolectado()
        assert alimento.disponible is False

    def test_str_representation(self):
        """Prueba la representación en string del alimento."""
        alimento = Alimento(
            id="alimento_001",
            nombre="Fruta",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=300
        )
        
        str_repr = str(alimento)
        assert "alimento_001" in str_repr
        assert "Fruta" in str_repr
        assert "3" in str_repr


class TestHormiga:
    """Pruebas para el modelo Hormiga."""
    
    def test_hormiga_creacion_exitosa(self):
        """Prueba la creación exitosa de una hormiga."""
        hormiga = Hormiga(
            id="hormiga_001",
            capacidad_carga=5,
            tiempo_vida=3600,
            subsistema_origen="recoleccion"
        )
        
        assert hormiga.id == "hormiga_001"
        assert hormiga.capacidad_carga == 5
        assert hormiga.tiempo_vida == 3600
        assert hormiga.subsistema_origen == "recoleccion"
        assert hormiga.estado == EstadoHormiga.DISPONIBLE
        assert isinstance(hormiga.fecha_creacion, datetime)

    def test_hormiga_valores_por_defecto(self):
        """Prueba los valores por defecto de una hormiga."""
        hormiga = Hormiga(id="hormiga_001")
        
        assert hormiga.capacidad_carga == 5
        assert hormiga.estado == EstadoHormiga.DISPONIBLE
        assert hormiga.tiempo_vida == 3600
        assert hormiga.subsistema_origen is None

    def test_hormiga_validaciones_error(self):
        """Prueba las validaciones de una hormiga."""
        with pytest.raises(ValueError, match="La capacidad de carga debe ser mayor a 0"):
            Hormiga(
                id="hormiga_001",
                capacidad_carga=0,
                tiempo_vida=3600
            )
        
        with pytest.raises(ValueError, match="El tiempo de vida debe ser mayor a 0"):
            Hormiga(
                id="hormiga_001",
                capacidad_carga=5,
                tiempo_vida=0
            )

    def test_is_viva(self):
        """Prueba la verificación de si una hormiga está viva."""
        hormiga = Hormiga(
            id="hormiga_001",
            tiempo_vida=3600  # 1 hora
        )
        
        assert hormiga.is_viva() is True
        
        # Simular hormiga muerta
        hormiga.tiempo_vida = -1
        assert hormiga.is_viva() is False

    def test_cambiar_estado(self):
        """Prueba el cambio de estado de una hormiga."""
        hormiga = Hormiga(id="hormiga_001")
        
        assert hormiga.estado == EstadoHormiga.DISPONIBLE
        hormiga.cambiar_estado(EstadoHormiga.BUSCANDO)
        assert hormiga.estado == EstadoHormiga.BUSCANDO

    def test_str_representation(self):
        """Prueba la representación en string de la hormiga."""
        hormiga = Hormiga(id="hormiga_001")
        str_repr = str(hormiga)
        assert "hormiga_001" in str_repr
        assert "disponible" in str_repr


class TestMensaje:
    """Pruebas para el modelo Mensaje."""
    
    def test_mensaje_creacion_exitosa(self):
        """Prueba la creación exitosa de un mensaje."""
        mensaje = Mensaje(
            id="mensaje_001",
            tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
            contenido={"data": "test"},
            subsistema_origen="recoleccion",
            subsistema_destino="entorno"
        )
        
        assert mensaje.id == "mensaje_001"
        assert mensaje.tipo == TipoMensaje.SOLICITAR_ALIMENTOS
        assert mensaje.contenido == {"data": "test"}
        assert mensaje.subsistema_origen == "recoleccion"
        assert mensaje.subsistema_destino == "entorno"
        assert mensaje.ttl == 60
        assert mensaje.procesado is False
        assert isinstance(mensaje.fecha_creacion, datetime)

    def test_mensaje_valores_por_defecto(self):
        """Prueba los valores por defecto de un mensaje."""
        mensaje = Mensaje(
            id="mensaje_001",
            tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
            contenido="test",
            subsistema_origen="recoleccion",
            subsistema_destino="entorno"
        )
        
        assert mensaje.ttl == 60
        assert mensaje.procesado is False
        assert isinstance(mensaje.fecha_creacion, datetime)

    def test_mensaje_validaciones_error(self):
        """Prueba las validaciones de un mensaje."""
        with pytest.raises(ValueError, match="El TTL debe ser mayor a 0"):
            Mensaje(
                id="mensaje_001",
                tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
                contenido="test",
                subsistema_origen="recoleccion",
                subsistema_destino="entorno",
                ttl=0
            )

    def test_is_expirado(self):
        """Prueba la verificación de si un mensaje ha expirado."""
        mensaje = Mensaje(
            id="mensaje_001",
            tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
            contenido="test",
            subsistema_origen="recoleccion",
            subsistema_destino="entorno",
            ttl=1  # 1 segundo
        )
        
        assert mensaje.is_expirado() is False
        
        # Simular mensaje expirado
        mensaje.fecha_creacion = datetime.now() - timedelta(seconds=2)
        assert mensaje.is_expirado() is True

    def test_marcar_como_procesado(self):
        """Prueba marcar un mensaje como procesado."""
        mensaje = Mensaje(
            id="mensaje_001",
            tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
            contenido="test",
            subsistema_origen="recoleccion",
            subsistema_destino="entorno"
        )
        
        assert mensaje.procesado is False
        mensaje.marcar_como_procesado()
        assert mensaje.procesado is True

    def test_str_representation(self):
        """Prueba la representación en string del mensaje."""
        mensaje = Mensaje(
            id="mensaje_001",
            tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
            contenido="test",
            subsistema_origen="recoleccion",
            subsistema_destino="entorno"
        )
        
        str_repr = str(mensaje)
        assert "mensaje_001" in str_repr
        assert "solicitar_alimentos" in str_repr


class TestTareaRecoleccion:
    """Pruebas para el modelo TareaRecoleccion."""
    
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

    def test_tarea_creacion_exitosa(self, alimento_ejemplo):
        """Prueba la creación exitosa de una tarea."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        
        assert tarea.id == "tarea_001"
        assert tarea.alimento == alimento_ejemplo
        assert tarea.estado == EstadoTarea.PENDIENTE
        assert len(tarea.hormigas_asignadas) == 0
        assert tarea.alimento_recolectado == 0

    def test_tarea_valores_por_defecto(self, alimento_ejemplo):
        """Prueba los valores por defecto de una tarea."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        
        assert tarea.estado == EstadoTarea.PENDIENTE
        assert len(tarea.hormigas_asignadas) == 0
        assert tarea.alimento_recolectado == 0
        assert tarea.fecha_inicio is None
        assert tarea.fecha_fin is None

    def test_tarea_validaciones_error(self, alimento_ejemplo):
        """Prueba las validaciones de una tarea."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        
        # La validación se hace en __post_init__, no en el setter
        with pytest.raises(ValueError, match="El alimento recolectado no puede ser negativo"):
            TareaRecoleccion(
                id="tarea_001",
                alimento=alimento_ejemplo,
                alimento_recolectado=-1
            )

    def test_agregar_hormiga(self, alimento_ejemplo, hormiga_ejemplo):
        """Prueba agregar una hormiga a la tarea."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        
        assert len(tarea.hormigas_asignadas) == 0
        tarea.agregar_hormiga(hormiga_ejemplo)
        assert len(tarea.hormigas_asignadas) == 1
        assert hormiga_ejemplo in tarea.hormigas_asignadas

    def test_agregar_hormiga_none(self, alimento_ejemplo):
        """Prueba agregar una hormiga None a la tarea."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        
        tarea.agregar_hormiga(None)
        assert len(tarea.hormigas_asignadas) == 0

    def test_tiene_suficientes_hormigas(self, alimento_ejemplo, hormiga_ejemplo):
        """Prueba la verificación de suficientes hormigas."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        
        assert tarea.tiene_suficientes_hormigas() is False
        
        # Agregar 3 hormigas (necesarias)
        for i in range(3):
            hormiga = Hormiga(id=f"hormiga_{i}")
            tarea.agregar_hormiga(hormiga)
        
        assert tarea.tiene_suficientes_hormigas() is True

    def test_todas_las_hormigas_vivas(self, alimento_ejemplo, hormiga_ejemplo):
        """Prueba la verificación de hormigas vivas."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        
        tarea.agregar_hormiga(hormiga_ejemplo)
        assert tarea.todas_las_hormigas_vivas() is True
        
        # Simular hormiga muerta - usar un tiempo muy pequeño para que expire
        hormiga_muerta = Hormiga(id="hormiga_muerta", tiempo_vida=1)  # 1 segundo
        # Simular que ya pasó el tiempo
        hormiga_muerta.fecha_creacion = hormiga_muerta.fecha_creacion.replace(year=2020)
        tarea.agregar_hormiga(hormiga_muerta)
        assert tarea.todas_las_hormigas_vivas() is False

    def test_iniciar_tarea_exitoso(self, alimento_ejemplo, hormiga_ejemplo):
        """Prueba el inicio exitoso de una tarea."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        
        # Agregar suficientes hormigas
        for i in range(3):
            hormiga = Hormiga(id=f"hormiga_{i}")
            tarea.agregar_hormiga(hormiga)
        
        tarea.iniciar_tarea()
        assert tarea.estado == EstadoTarea.EN_PROCESO
        assert tarea.fecha_inicio is not None

    def test_iniciar_tarea_sin_suficientes_hormigas(self, alimento_ejemplo, hormiga_ejemplo):
        """Prueba el inicio de tarea sin suficientes hormigas."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        
        tarea.agregar_hormiga(hormiga_ejemplo)  # Solo 1 hormiga, necesita 3
        
        with pytest.raises(ValueError, match="No se puede iniciar la tarea sin suficientes hormigas"):
            tarea.iniciar_tarea()

    def test_iniciar_tarea_estado_incorrecto(self, alimento_ejemplo, hormiga_ejemplo):
        """Prueba el inicio de tarea en estado incorrecto."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        tarea.estado = EstadoTarea.EN_PROCESO
        
        with pytest.raises(ValueError, match="Solo se pueden iniciar tareas en estado PENDIENTE"):
            tarea.iniciar_tarea()

    def test_completar_tarea_exitoso(self, alimento_ejemplo, hormiga_ejemplo):
        """Prueba la finalización exitosa de una tarea."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        tarea.estado = EstadoTarea.EN_PROCESO
        
        tarea.completar_tarea(10)
        assert tarea.estado == EstadoTarea.COMPLETADA
        assert tarea.alimento_recolectado == 10
        assert tarea.fecha_fin is not None

    def test_completar_tarea_estado_incorrecto(self, alimento_ejemplo):
        """Prueba la finalización de tarea en estado incorrecto."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        tarea.estado = EstadoTarea.PENDIENTE
        
        with pytest.raises(ValueError, match="Solo se pueden completar tareas en estado EN_PROCESO"):
            tarea.completar_tarea(10)

    def test_pausar_tarea(self, alimento_ejemplo):
        """Prueba pausar una tarea."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        tarea.estado = EstadoTarea.EN_PROCESO
        
        tarea.pausar_tarea()
        assert tarea.estado == EstadoTarea.PAUSADA

    def test_pausar_tarea_estado_incorrecto(self, alimento_ejemplo):
        """Prueba pausar tarea en estado incorrecto."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        tarea.estado = EstadoTarea.PENDIENTE
        
        with pytest.raises(ValueError, match="Solo se pueden pausar tareas en estado EN_PROCESO"):
            tarea.pausar_tarea()

    def test_str_representation(self, alimento_ejemplo):
        """Prueba la representación en string de la tarea."""
        tarea = TareaRecoleccion(
            id="tarea_001",
            alimento=alimento_ejemplo
        )
        
        str_repr = str(tarea)
        assert "tarea_001" in str_repr
        assert "Fruta" in str_repr
        assert "pendiente" in str_repr
