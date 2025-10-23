"""
Steps para las pruebas BDD del subsistema de recolección.
"""

import asyncio
from behave import given, when, then, step
from unittest.mock import AsyncMock, MagicMock
import pytest

from src.recoleccion.services.recoleccion_service import RecoleccionService
from src.recoleccion.models.alimento import Alimento
from src.recoleccion.models.hormiga import Hormiga
from src.recoleccion.models.estado_hormiga import EstadoHormiga
from src.recoleccion.models.estado_tarea import EstadoTarea


# Contexto global para mantener estado entre steps
context = {}


@given("que el subsistema de recolección está configurado")
def step_impl(context):
    """Configura el subsistema de recolección con mocks."""
    context.mock_entorno_service = AsyncMock()
    context.mock_comunicacion_service = AsyncMock()
    context.recoleccion_service = RecoleccionService(
        context.mock_entorno_service, 
        context.mock_comunicacion_service
    )


@given("que los servicios de entorno y comunicación están disponibles")
def step_impl(context):
    """Configura los servicios como disponibles."""
    context.mock_entorno_service.is_disponible.return_value = True
    context.mock_comunicacion_service.is_disponible.return_value = True


@given("que hay alimentos disponibles en el entorno")
def step_impl(context):
    """Configura alimentos disponibles en el entorno."""
    context.alimentos = [
        Alimento(
            id="alimento_001",
            nombre="Fruta",
            cantidad_hormigas_necesarias=3,
            puntos_stock=10,
            tiempo_recoleccion=300
        ),
        Alimento(
            id="alimento_002",
            nombre="Semilla",
            cantidad_hormigas_necesarias=2,
            puntos_stock=5,
            tiempo_recoleccion=180
        )
    ]
    context.mock_entorno_service.consultar_alimentos_disponibles.return_value = context.alimentos


@given("que tengo un alimento disponible")
def step_impl(context):
    """Configura un alimento específico."""
    context.alimento = Alimento(
        id="alimento_001",
        nombre="Fruta",
        cantidad_hormigas_necesarias=3,
        puntos_stock=10,
        tiempo_recoleccion=300
    )


@given("que necesito {cantidad:d} hormigas para una tarea")
def step_impl(context, cantidad):
    """Configura la cantidad de hormigas necesarias."""
    context.cantidad_hormigas = cantidad


@given("que tengo una tarea de recolección")
def step_impl(context):
    """Crea una tarea de recolección."""
    context.tarea = context.recoleccion_service.tareas_activas[0] if context.recoleccion_service.tareas_activas else None


@given("que tengo hormigas disponibles")
def step_impl(context):
    """Configura hormigas disponibles."""
    context.hormigas = [
        Hormiga(
            id=f"hormiga_{i:03d}",
            capacidad_carga=5,
            tiempo_vida=3600,
            subsistema_origen="recoleccion"
        ) for i in range(1, 4)
    ]


@given("que tengo una tarea con suficientes hormigas asignadas")
def step_impl(context):
    """Configura una tarea con suficientes hormigas."""
    context.tarea = context.recoleccion_service.tareas_activas[0] if context.recoleccion_service.tareas_activas else None
    if context.tarea:
        for hormiga in context.hormigas:
            context.tarea.agregar_hormiga(hormiga)


@given("que tengo una tarea con hormigas insuficientes")
def step_impl(context):
    """Configura una tarea con hormigas insuficientes."""
    context.tarea = context.recoleccion_service.tareas_activas[0] if context.recoleccion_service.tareas_activas else None
    if context.tarea:
        # Solo agregar 1 hormiga cuando necesita 3
        context.tarea.agregar_hormiga(context.hormigas[0])


@given("que tengo una tarea en estado EN_PROCESO")
def step_impl(context):
    """Configura una tarea en proceso."""
    context.tarea = context.recoleccion_service.tareas_activas[0] if context.recoleccion_service.tareas_activas else None
    if context.tarea:
        context.tarea.estado = EstadoTarea.EN_PROCESO


@given("que el servicio de entorno no está disponible")
def step_impl(context):
    """Configura el servicio de entorno como no disponible."""
    context.mock_entorno_service.is_disponible.return_value = False


@given("que el servicio de comunicación no está disponible")
def step_impl(context):
    """Configura el servicio de comunicación como no disponible."""
    context.mock_comunicacion_service.is_disponible.return_value = False


@given("que hay {cantidad:d} alimentos disponibles en el entorno")
def step_impl(context, cantidad):
    """Configura múltiples alimentos disponibles."""
    context.alimentos = [
        Alimento(
            id=f"alimento_{i:03d}",
            nombre=f"Alimento_{i}",
            cantidad_hormigas_necesarias=2,
            puntos_stock=5,
            tiempo_recoleccion=180
        ) for i in range(1, cantidad + 1)
    ]
    context.mock_entorno_service.consultar_alimentos_disponibles.return_value = context.alimentos


@given("que tengo una tarea en proceso con hormigas")
def step_impl(context):
    """Configura una tarea en proceso con hormigas."""
    context.tarea = context.recoleccion_service.tareas_activas[0] if context.recoleccion_service.tareas_activas else None
    if context.tarea:
        context.tarea.estado = EstadoTarea.EN_PROCESO
        for hormiga in context.hormigas:
            context.tarea.agregar_hormiga(hormiga)


@given("que algunas hormigas mueren durante la recolección")
def step_impl(context):
    """Simula la muerte de algunas hormigas."""
    if context.tarea and context.tarea.hormigas_asignadas:
        # Simular muerte de la primera hormiga
        context.tarea.hormigas_asignadas[0].tiempo_vida = -1


@when("consulto los alimentos disponibles")
def step_impl(context):
    """Ejecuta la consulta de alimentos."""
    context.resultado_alimentos = asyncio.run(
        context.recoleccion_service.consultar_alimentos_disponibles()
    )


@when("creo una tarea de recolección para ese alimento")
def step_impl(context):
    """Crea una tarea de recolección."""
    context.tarea = asyncio.run(
        context.recoleccion_service.crear_tarea_recoleccion(
            "tarea_001", context.alimento
        )
    )


@when("solicito las hormigas al subsistema de comunicación")
def step_impl(context):
    """Solicita hormigas."""
    context.mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
    context.mock_comunicacion_service.consultar_respuesta_hormigas.return_value = context.hormigas
    context.hormigas_recibidas = asyncio.run(
        context.recoleccion_service.solicitar_hormigas(context.cantidad_hormigas)
    )


@when("asigno las hormigas a la tarea")
def step_impl(context):
    """Asigna hormigas a la tarea."""
    asyncio.run(
        context.recoleccion_service.asignar_hormigas_a_tarea(context.tarea, context.hormigas)
    )


@when("inicio la tarea de recolección")
def step_impl(context):
    """Inicia la tarea de recolección."""
    try:
        asyncio.run(
            context.recoleccion_service.iniciar_tarea_recoleccion(context.tarea)
        )
        context.error = None
    except Exception as e:
        context.error = e


@when("intento iniciar la tarea de recolección")
def step_impl(context):
    """Intenta iniciar la tarea de recolección."""
    try:
        asyncio.run(
            context.recoleccion_service.iniciar_tarea_recoleccion(context.tarea)
        )
        context.error = None
    except Exception as e:
        context.error = e


@when("completo la tarea con {cantidad:d} unidades de alimento")
def step_impl(context, cantidad):
    """Completa la tarea de recolección."""
    asyncio.run(
        context.recoleccion_service.completar_tarea_recoleccion(context.tarea, cantidad)
    )


@when("ejecuto el proceso completo de recolección")
def step_impl(context):
    """Ejecuta el proceso completo."""
    context.mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
    context.mock_comunicacion_service.consultar_respuesta_hormigas.return_value = context.hormigas
    context.mock_comunicacion_service.devolver_hormigas.return_value = "mensaje_002"
    context.mock_entorno_service.marcar_alimento_como_recolectado.return_value = True
    
    context.tareas_procesadas = asyncio.run(
        context.recoleccion_service.procesar_recoleccion()
    )


@when("intento consultar alimentos disponibles")
def step_impl(context):
    """Intenta consultar alimentos."""
    try:
        context.resultado_alimentos = asyncio.run(
            context.recoleccion_service.consultar_alimentos_disponibles()
        )
        context.error = None
    except Exception as e:
        context.error = e


@when("intento solicitar hormigas")
def step_impl(context):
    """Intenta solicitar hormigas."""
    try:
        context.hormigas_recibidas = asyncio.run(
            context.recoleccion_service.solicitar_hormigas(3)
        )
        context.error = None
    except Exception as e:
        context.error = e


@when("ejecuto el proceso de recolección")
def step_impl(context):
    """Ejecuta el proceso de recolección."""
    context.mock_comunicacion_service.solicitar_hormigas.return_value = "mensaje_001"
    context.mock_comunicacion_service.consultar_respuesta_hormigas.return_value = context.hormigas
    context.mock_comunicacion_service.devolver_hormigas.return_value = "mensaje_002"
    context.mock_entorno_service.marcar_alimento_como_recolectado.return_value = True
    
    context.tareas_procesadas = asyncio.run(
        context.recoleccion_service.procesar_recoleccion()
    )


@when("verifico el estado de las hormigas")
def step_impl(context):
    """Verifica el estado de las hormigas."""
    asyncio.run(
        context.recoleccion_service.verificar_hormigas_muertas()
    )


@then("debo recibir una lista de alimentos")
def step_impl(context):
    """Verifica que se recibió una lista de alimentos."""
    assert context.resultado_alimentos is not None
    assert isinstance(context.resultado_alimentos, list)
    assert len(context.resultado_alimentos) > 0


@then("cada alimento debe tener sus propiedades correctas")
def step_impl(context):
    """Verifica las propiedades de los alimentos."""
    for alimento in context.resultado_alimentos:
        assert alimento.id is not None
        assert alimento.nombre is not None
        assert alimento.cantidad_hormigas_necesarias > 0
        assert alimento.puntos_stock > 0
        assert alimento.tiempo_recoleccion > 0


@then("la tarea debe estar en estado PENDIENTE")
def step_impl(context):
    """Verifica el estado de la tarea."""
    assert context.tarea.estado == EstadoTarea.PENDIENTE


@then("la tarea debe tener el alimento asignado")
def step_impl(context):
    """Verifica que la tarea tiene el alimento asignado."""
    assert context.tarea.alimento == context.alimento


@then("debo recibir las hormigas solicitadas")
def step_impl(context):
    """Verifica que se recibieron las hormigas."""
    assert context.hormigas_recibidas is not None
    assert len(context.hormigas_recibidas) == context.cantidad_hormigas


@then("las hormigas deben estar disponibles")
def step_impl(context):
    """Verifica el estado de las hormigas."""
    for hormiga in context.hormigas_recibidas:
        assert hormiga.estado == EstadoHormiga.DISPONIBLE


@then("la tarea debe tener las hormigas asignadas")
def step_impl(context):
    """Verifica que la tarea tiene las hormigas asignadas."""
    assert len(context.tarea.hormigas_asignadas) == len(context.hormigas)


@then("las hormigas deben estar en estado DISPONIBLE")
def step_impl(context):
    """Verifica el estado de las hormigas."""
    for hormiga in context.tarea.hormigas_asignadas:
        assert hormiga.estado == EstadoHormiga.DISPONIBLE


@then("la tarea debe estar en estado EN_PROCESO")
def step_impl(context):
    """Verifica el estado de la tarea."""
    assert context.tarea.estado == EstadoTarea.EN_PROCESO


@then("las hormigas deben estar en estado BUSCANDO")
def step_impl(context):
    """Verifica el estado de las hormigas."""
    for hormiga in context.tarea.hormigas_asignadas:
        assert hormiga.estado == EstadoHormiga.BUSCANDO


@then("la tarea debe tener fecha de inicio")
def step_impl(context):
    """Verifica la fecha de inicio."""
    assert context.tarea.fecha_inicio is not None


@then("debe lanzar una excepción")
def step_impl(context):
    """Verifica que se lanzó una excepción."""
    assert context.error is not None


@then("la tarea debe permanecer en estado PENDIENTE")
def step_impl(context):
    """Verifica el estado de la tarea."""
    assert context.tarea.estado == EstadoTarea.PENDIENTE


@then("la tarea debe estar en estado COMPLETADA")
def step_impl(context):
    """Verifica el estado de la tarea."""
    assert context.tarea.estado == EstadoTarea.COMPLETADA


@then("la tarea debe tener {cantidad:d} unidades de alimento recolectado")
def step_impl(context, cantidad):
    """Verifica la cantidad de alimento recolectado."""
    assert context.tarea.alimento_recolectado == cantidad


@then("las hormigas deben estar en estado TRANSPORTANDO")
def step_impl(context):
    """Verifica el estado de las hormigas."""
    for hormiga in context.tarea.hormigas_asignadas:
        assert hormiga.estado == EstadoHormiga.TRANSPORTANDO


@then("la tarea debe tener fecha de finalización")
def step_impl(context):
    """Verifica la fecha de finalización."""
    assert context.tarea.fecha_fin is not None


@then("debo tener tareas completadas")
def step_impl(context):
    """Verifica que hay tareas completadas."""
    assert context.tareas_procesadas is not None
    assert len(context.tareas_procesadas) > 0


@then("el alimento debe estar marcado como recolectado en el entorno")
def step_impl(context):
    """Verifica que el alimento fue marcado como recolectado."""
    context.mock_entorno_service.marcar_alimento_como_recolectado.assert_called()


@then("las hormigas deben ser devueltas al subsistema de comunicación")
def step_impl(context):
    """Verifica que las hormigas fueron devueltas."""
    context.mock_comunicacion_service.devolver_hormigas.assert_called()


@then("debe lanzar una excepción indicando que el servicio no está disponible")
def step_impl(context):
    """Verifica la excepción de servicio no disponible."""
    assert context.error is not None
    assert "no disponible" in str(context.error)


@then("debo procesar los {cantidad:d} alimentos")
def step_impl(context, cantidad):
    """Verifica que se procesaron todos los alimentos."""
    assert len(context.tareas_procesadas) == cantidad


@then("cada alimento debe tener su tarea correspondiente")
def step_impl(context):
    """Verifica que cada alimento tiene su tarea."""
    assert len(context.tareas_procesadas) == len(context.alimentos)


@then("todas las tareas deben completarse exitosamente")
def step_impl(context):
    """Verifica que todas las tareas se completaron."""
    for tarea in context.tareas_procesadas:
        assert tarea.estado == EstadoTarea.COMPLETADA


@then("la tarea debe pausarse")
def step_impl(context):
    """Verifica que la tarea se pausó."""
    assert context.tarea.estado == EstadoTarea.PAUSADA


@then("la tarea debe estar en estado PAUSADA")
def step_impl(context):
    """Verifica el estado de la tarea."""
    assert context.tarea.estado == EstadoTarea.PAUSADA

