"""
Aplicación principal optimizada para Railway.
"""

import os
import sys
import uvicorn
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

try:
    from src.recoleccion.api.recoleccion_controller import create_app
    from src.recoleccion.services.mock_entorno_service import MockEntornoService
    from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService
    
    # Crear instancias de los servicios mock
    entorno_service = MockEntornoService()
    comunicacion_service = MockComunicacionService()
    
    # Crear la aplicación FastAPI
    app = create_app(entorno_service, comunicacion_service)
    
    print("✅ Aplicación FastAPI creada exitosamente")
    print(f"✅ Servicios mock inicializados")
    
except Exception as e:
    print(f"❌ Error creando aplicación: {e}")
    sys.exit(1)

# Configuración para Railway
if __name__ == "__main__":
    try:
        # Obtener puerto de Railway o usar 8000 por defecto
        port = int(os.environ.get("PORT", 8000))
        
        print(f"🚀 Iniciando servidor en puerto {port}")
        print(f"🌐 Host: 0.0.0.0")
        print(f"📊 Log level: info")
        
        # Ejecutar la aplicación
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        sys.exit(1)
