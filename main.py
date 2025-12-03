"""
Aplicación principal del subsistema de recolección de alimentos.
"""

import os
import uvicorn
from src.recoleccion.api.recoleccion_controller import create_app
from src.recoleccion.services.mock_entorno_service import MockEntornoService
from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService

# Configuración: Usar servicios reales o mocks
# URLs de los subsistemas (configurables por variables de entorno)
ENTORNO_API_URL = os.getenv("ENTORNO_API_URL", "")
COMUNICACION_API_URL = os.getenv("COMUNICACION_API_URL", "")
BASE_API_URL = os.getenv("BASE_API_URL", "")

# Si BASE_API_URL está configurado, usar URLs derivadas
if BASE_API_URL and not ENTORNO_API_URL:
    # Intentar detectar endpoints del entorno y comunicación
    # Por defecto, asumir que están en el mismo dominio con rutas diferentes
    ENTORNO_API_URL = f"{BASE_API_URL}/api/entorno"  # Ajustar según la API real
    COMUNICACION_API_URL = f"{BASE_API_URL}/api/comunicacion"  # Ajustar según la API real

USE_REAL_ENTORNO = os.getenv("USE_REAL_ENTORNO", "false").lower() == "true" or bool(ENTORNO_API_URL)
USE_REAL_COMUNICACION = os.getenv("USE_REAL_COMUNICACION", "false").lower() == "true" or bool(COMUNICACION_API_URL)

# Configurar servicio de entorno
if USE_REAL_ENTORNO and ENTORNO_API_URL:
    from src.recoleccion.services.entorno_api_service import EntornoAPIService
    entorno_service = EntornoAPIService(base_url=ENTORNO_API_URL)
    print(f"Usando servicio real de entorno: {ENTORNO_API_URL}")
else:
    entorno_service = MockEntornoService()
    print("Usando servicio mock de entorno (configurar ENTORNO_API_URL o BASE_API_URL para usar servicio real)")

# Configurar servicio de comunicación
if USE_REAL_COMUNICACION and COMUNICACION_API_URL:
    from src.recoleccion.services.comunicacion_api_service import ComunicacionAPIService
    comunicacion_service = ComunicacionAPIService(base_url=COMUNICACION_API_URL)
    print(f"Usando servicio real de comunicación: {COMUNICACION_API_URL}")
else:
    comunicacion_service = MockComunicacionService()
    print("Usando servicio mock de comunicación (configurar COMUNICACION_API_URL o BASE_API_URL para usar servicio real)")

# Crear la aplicación FastAPI
app = create_app(entorno_service, comunicacion_service)


def main():
    """Función principal para ejecutar la aplicación."""
    # Obtener configuración de variables de entorno (compatible con Railway/Cloudflare)
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    # reload solo en desarrollo, nunca en producción
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    # Ejecutar la aplicación
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=os.getenv("LOG_LEVEL", "info")
    )


if __name__ == "__main__":
    main()
