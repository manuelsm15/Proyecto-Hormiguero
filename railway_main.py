"""
Aplicación principal optimizada para Railway.
"""

import os
import uvicorn
from src.recoleccion.api.recoleccion_controller import create_app
from src.recoleccion.services.mock_entorno_service import MockEntornoService
from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService

# Crear instancias de los servicios mock
entorno_service = MockEntornoService()
comunicacion_service = MockComunicacionService()

# Crear la aplicación FastAPI
app = create_app(entorno_service, comunicacion_service)

# Configuración para Railway
if __name__ == "__main__":
    # Obtener puerto de Railway o usar 8000 por defecto
    port = int(os.environ.get("PORT", 8000))
    
    # Ejecutar la aplicación
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
