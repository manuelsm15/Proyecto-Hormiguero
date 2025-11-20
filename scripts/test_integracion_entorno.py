"""
Script de prueba para verificar la integración con el Subsistema de Entorno.
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.recoleccion.services.entorno_api_service import EntornoAPIService
from src.recoleccion.services.mock_entorno_service import MockEntornoService


async def test_mock_service():
    """Prueba el servicio mock."""
    print("=" * 60)
    print("PRUEBA DEL SERVICIO MOCK")
    print("=" * 60)
    
    service = MockEntornoService()
    
    # Probar disponibilidad
    disponible = await service.is_disponible()
    print(f"Servicio disponible: {disponible}")
    
    # Consultar alimentos disponibles
    alimentos = await service.consultar_alimentos_disponibles()
    print(f"\nAlimentos disponibles: {len(alimentos)}")
    for alimento in alimentos:
        print(f"  - {alimento.id}: {alimento.nombre} ({alimento.cantidad_hormigas_necesarias} hormigas)")
    
    # Consultar por ID
    alimento = await service.consultar_alimento_por_id("A1")
    if alimento:
        print(f"\nAlimento A1 encontrado: {alimento.nombre}")
    
    # Marcar como recolectado
    success = await service.marcar_alimento_como_recolectado("A1")
    print(f"\nMarcar A1 como recolectado: {success}")
    
    # Verificar que ya no está disponible
    alimentos = await service.consultar_alimentos_disponibles()
    print(f"Alimentos disponibles después de recolectar A1: {len(alimentos)}")
    
    print("\n" + "=" * 60)


async def test_api_service(base_url: str):
    """Prueba el servicio real de API."""
    print("=" * 60)
    print(f"PRUEBA DEL SERVICIO REAL DE API: {base_url}")
    print("=" * 60)
    
    service = EntornoAPIService(base_url=base_url)
    
    # Probar disponibilidad
    disponible = await service.is_disponible()
    print(f"Servicio disponible: {disponible}")
    
    if not disponible:
        print("\nERROR: El servicio de entorno no está disponible.")
        print(f"Verifica que el subsistema de entorno esté corriendo en: {base_url}")
        return
    
    # Consultar recursos disponibles
    try:
        recursos = await service.consultar_alimentos_disponibles()
        print(f"\nRecursos disponibles: {len(recursos)}")
        for recurso in recursos:
            print(f"  - {recurso.id}: {recurso.nombre} ({recurso.cantidad_hormigas_necesarias} hormigas)")
    except Exception as e:
        print(f"\nERROR al consultar recursos: {e}")
    
    # Consultar por zona (si hay zonas)
    try:
        recursos_zona = await service.consultar_recursos_por_zona(1)
        print(f"\nRecursos en zona 1: {len(recursos_zona)}")
    except Exception as e:
        print(f"\nNo se pudieron consultar recursos por zona: {e}")
    
    print("\n" + "=" * 60)
    
    # Cerrar el cliente HTTP
    await service.client.aclose()


async def main():
    """Función principal."""
    import os
    
    # Probar servicio mock
    await test_mock_service()
    
    # Probar servicio real si está configurado
    entorno_url = os.getenv("ENTORNO_API_URL", "")
    if entorno_url:
        print("\n")
        await test_api_service(entorno_url)
    else:
        print("\n" + "=" * 60)
        print("SERVICIO REAL NO CONFIGURADO")
        print("=" * 60)
        print("Para probar el servicio real, configura la variable de entorno:")
        print("  export ENTORNO_API_URL='http://localhost:8001'")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())



