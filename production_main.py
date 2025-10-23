
# Configuración de producción para el Subsistema de Recolección
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
    """Función principal para ejecutar en producción."""
    # Configuración para acceso desde cualquier IP
    uvicorn.run(
        app,
        host="0.0.0.0",  # Permitir acceso desde cualquier IP
        port=8000,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
