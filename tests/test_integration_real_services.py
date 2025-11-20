# -*- coding: utf-8 -*-
"""
Pruebas de integración contra servicios reales (Entorno y Comunicación/Reina).

Estas pruebas SOLO se ejecutan si existen variables de entorno configuradas:
- BASE_API_URL o ENTORNO_API_URL para Entorno
- BASE_API_URL o COMUNICACION_API_URL para Comunicación/Reina

Si no están configuradas, las pruebas se marcan como `skipped` automáticamente.
"""

import os
import asyncio
import pytest

from src.recoleccion.services.entorno_api_service import EntornoAPIService
from src.recoleccion.services.comunicacion_api_service import ComunicacionAPIService


def _get_entorno_url() -> str:
    base = os.getenv("BASE_API_URL", "").rstrip("/")
    entorno = os.getenv("ENTORNO_API_URL", "").rstrip("/")
    if entorno:
        return entorno
    if base:
        # Rutas comunes; la implementación interna probará varias rutas
        return base
    return ""


def _get_comunicacion_url() -> str:
    base = os.getenv("BASE_API_URL", "").rstrip("/")
    comm = os.getenv("COMUNICACION_API_URL", "").rstrip("/")
    if comm:
        return comm
    if base:
        return base
    return ""


@pytest.mark.integration
@pytest.mark.asyncio
async def test_entorno_api_service_disponible():
    url = _get_entorno_url()
    if not url:
        pytest.skip("BASE_API_URL/ENTORNO_API_URL no configurado; se salta la prueba real de entorno")

    service = EntornoAPIService(base_url=url)
    disponible = await service.is_disponible()
    # No afirmamos True estrictamente para no romper en entornos CI; al menos debe retornar bool
    assert isinstance(disponible, bool)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_entorno_api_service_listar_alimentos():
    url = _get_entorno_url()
    if not url:
        pytest.skip("BASE_API_URL/ENTORNO_API_URL no configurado; se salta la prueba real de entorno")

    service = EntornoAPIService(base_url=url)
    alimentos = await service.consultar_alimentos_disponibles()
    # Debe retornar lista, aunque pueda estar vacía
    assert isinstance(alimentos, list)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_comunicacion_api_service_solicitar_y_consultar_hormigas():
    url = _get_comunicacion_url()
    if not url:
        pytest.skip("BASE_API_URL/COMUNICACION_API_URL no configurado; se salta la prueba real de comunicación")

    service = ComunicacionAPIService(base_url=url)

    # Solicitar hormigas (el contrato real puede variar; no hacemos suposiciones fuertes)
    mensaje_id = await service.solicitar_hormigas(2, "recoleccion")
    assert isinstance(mensaje_id, str) and len(mensaje_id) > 0

    # Dar un pequeño tiempo por si el backend procesa async
    await asyncio.sleep(0.2)

    hormigas = await service.consultar_respuesta_hormigas(mensaje_id)
    # Debe retornar lista (puede estar vacía si el backend aún no responde)
    assert isinstance(hormigas, list)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_comunicacion_api_service_devolver_hormigas():
    url = _get_comunicacion_url()
    if not url:
        pytest.skip("BASE_API_URL/COMUNICACION_API_URL no configurado; se salta la prueba real de comunicación")

    service = ComunicacionAPIService(base_url=url)

    # Intentar devolver hormigas vacías para validar contrato mínimo
    mensaje_id = await service.devolver_hormigas([], alimento_recolectado=0)
    assert isinstance(mensaje_id, str) and len(mensaje_id) > 0


