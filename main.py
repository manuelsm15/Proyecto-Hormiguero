"""
Aplicación principal del subsistema de recolección de alimentos.
"""

import uvicorn
from src.recoleccion.api.recoleccion_controller import create_app
from src.recoleccion.services.mock_entorno_service import MockEntornoService
from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService

# Crear instancias de los servicios mock
entorno_service = MockEntornoService()
comunicacion_service = MockComunicacionService()

# Crear la aplicación FastAPI
app = create_app(entorno_service, comunicacion_service)


def main():
    """Función principal para ejecutar la aplicación."""
    # Ejecutar la aplicación
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
