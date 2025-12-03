"""
Tests unitarios para PersistenceService usando una DB fake en memoria.

El objetivo es cubrir la lógica de:
- guardado/actualización de entidades
- llamadas a _registrar_evento
- manejo de excepciones
"""

import pytest
from types import SimpleNamespace

from src.recoleccion.services.persistence_service import PersistenceService
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.tarea_recoleccion import TareaRecoleccion
from src.recoleccion.models.mensaje import Mensaje
from src.recoleccion.models.tipo_mensaje import TipoMensaje
from src.recoleccion.models.estado_tarea import EstadoTarea
from src.recoleccion.models.estado_hormiga import EstadoHormiga


class FakeDB:
    """DB fake mínima que registra las llamadas."""

    def __init__(self):
        self.guardados = []
        self.eventos = []
        self.last_error = None

    # Métodos usados por PersistenceService
    def guardar_alimento(self, alimento):
        self.guardados.append(("alimento", alimento.id))
        return True

    def obtener_alimentos(self):
        return []

    def obtener_alimento_por_id(self, alimento_id):
        return {
            "id": alimento_id,
            "nombre": "Fruta",
            "cantidad_hormigas_necesarias": 3,
            "puntos_stock": 10,
            "tiempo_recoleccion": 300,
            "disponible": 1,
        }

    def actualizar_alimento_disponibilidad(self, alimento_id, disponible):
        self.guardados.append(("alimento_disponible", alimento_id, disponible))
        return True

    def guardar_tarea(self, tarea):
        self.guardados.append(("tarea", tarea.id))
        return True

    def obtener_tareas(self):
        return []

    def actualizar_estado_tarea(self, tarea_id, nuevo_estado):
        self.guardados.append(("estado_tarea", tarea_id, nuevo_estado))
        return True

    def guardar_mensaje(self, mensaje):
        self.guardados.append(("mensaje", mensaje.id))
        return True

    def obtener_mensajes(self, subsistema_origen=None):
        return []

    def obtener_estadisticas(self):
        return {"ok": True}

    def obtener_eventos(self, limite):
        return []

    def guardar_evento(self, tipo_evento, descripcion, datos_adicionales=None):
        self.eventos.append((tipo_evento, descripcion, datos_adicionales))
        return True

    # Lotes y hormigas
    def crear_lote_hormigas(self, lote_id, tarea_id, cantidad_enviada, cantidad_requerida):
        self.guardados.append(("lote", lote_id, tarea_id))
        return True

    def aceptar_lote_hormigas(self, lote_id):
        self.guardados.append(("lote_aceptado", lote_id))
        return True

    def marcar_lote_en_uso(self, lote_id):
        self.guardados.append(("lote_en_uso", lote_id))
        return True

    def verificar_lote_disponible(self, lote_id, cantidad_requerida):
        return True, None

    def guardar_hormigas_en_lote(self, lote_id, hormigas):
        self.guardados.append(("hormigas_lote", lote_id, len(hormigas)))
        return True

    def obtener_hormigas_por_lote(self, lote_id):
        return []


@pytest.fixture
def persistence_with_fake_db():
    """Instancia de PersistenceService con una DB fake inyectada."""
    ps = PersistenceService()
    ps.db = FakeDB()
    return ps


@pytest.mark.asyncio
async def test_guardar_alimento_registra_evento(persistence_with_fake_db):
    ps = persistence_with_fake_db
    alimento = Alimento(
        id="A1",
        nombre="Fruta",
        cantidad_hormigas_necesarias=3,
        puntos_stock=10,
        tiempo_recoleccion=300,
    )

    ok = await ps.guardar_alimento(alimento)
    assert ok is True
    assert ("alimento", "A1") in ps.db.guardados
    # Debe haberse registrado un evento
    assert any(ev[0] == "alimento_guardado" for ev in ps.db.eventos)


@pytest.mark.asyncio
async def test_actualizar_alimento_disponibilidad_registra_evento(persistence_with_fake_db):
    ps = persistence_with_fake_db
    ok = await ps.actualizar_alimento_disponibilidad("A1", False)
    assert ok is True
    assert ("alimento_disponible", "A1", False) in ps.db.guardados
    assert any(ev[0] == "alimento_actualizado" for ev in ps.db.eventos)


@pytest.mark.asyncio
async def test_guardar_tarea_registra_evento(persistence_with_fake_db):
    ps = persistence_with_fake_db
    alimento = Alimento(
        id="A1",
        nombre="Fruta",
        cantidad_hormigas_necesarias=1,
        puntos_stock=10,
        tiempo_recoleccion=300,
    )
    tarea = TareaRecoleccion(id="T1", alimento=alimento)

    ok = await ps.guardar_tarea(tarea)
    assert ok is True
    assert ("tarea", "T1") in ps.db.guardados
    assert any(ev[0] == "tarea_guardada" for ev in ps.db.eventos)


@pytest.mark.asyncio
async def test_actualizar_estado_tarea_registra_evento(persistence_with_fake_db):
    ps = persistence_with_fake_db
    ok = await ps.actualizar_estado_tarea("T1", EstadoTarea.EN_PROCESO)
    assert ok is True
    assert ("estado_tarea", "T1", "en_proceso") in ps.db.guardados
    assert any(ev[0] == "tarea_actualizada" for ev in ps.db.eventos)


@pytest.mark.asyncio
async def test_guardar_mensaje_registra_evento(persistence_with_fake_db):
    ps = persistence_with_fake_db
    mensaje = Mensaje(
        id="M1",
        tipo=TipoMensaje.SOLICITAR_ALIMENTOS,
        contenido={"x": 1},
        subsistema_origen="recoleccion",
        subsistema_destino="entorno",
    )
    ok = await ps.guardar_mensaje(mensaje)
    assert ok is True
    assert ("mensaje", "M1") in ps.db.guardados
    assert any(ev[0] == "mensaje_guardado" for ev in ps.db.eventos)


@pytest.mark.asyncio
async def test_crear_y_aceptar_lote_hormigas_registra_eventos(persistence_with_fake_db):
    ps = persistence_with_fake_db
    ok, err = await ps.crear_lote_hormigas("L1", "T1", 3, 3)
    assert ok is True and err is None
    assert ("lote", "L1", "T1") in ps.db.guardados
    assert any(ev[0] == "lote_creado" for ev in ps.db.eventos)

    ok, err = await ps.aceptar_lote_hormigas("L1")
    assert ok is True and err is None
    assert ("lote_aceptado", "L1") in ps.db.guardados
    assert any(ev[0] == "lote_aceptado" for ev in ps.db.eventos)


@pytest.mark.asyncio
async def test_guardar_hormigas_en_lote_registra_evento(persistence_with_fake_db):
    ps = persistence_with_fake_db
    hormigas = [
        Hormiga(id="H1", capacidad_carga=5, estado=EstadoHormiga.DISPONIBLE),
        Hormiga(id="H2", capacidad_carga=5, estado=EstadoHormiga.DISPONIBLE),
    ]
    ok = await ps.guardar_hormigas_en_lote("L1", hormigas)
    assert ok is True
    assert ("hormigas_lote", "L1", 2) in ps.db.guardados
    assert any(ev[0] == "hormigas_guardadas_en_lote" for ev in ps.db.eventos)


@pytest.mark.asyncio
async def test_obtener_info_bd_devuelve_engine_y_implementation(persistence_with_fake_db):
    ps = persistence_with_fake_db
    info = await ps.obtener_info_bd()
    assert "engine" in info
    assert "implementation" in info



