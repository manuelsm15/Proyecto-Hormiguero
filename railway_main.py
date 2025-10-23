"""
Aplicación principal optimizada para Railway.
"""

import os
import sys
import logging
import uvicorn
from pathlib import Path

# Configurar logging para Railway - Solo errores críticos
logging.basicConfig(
    level=logging.ERROR,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Agregar el directorio actual al path
current_dir = Path.cwd()
sys.path.append(str(current_dir))

try:
    from src.recoleccion.api.recoleccion_controller import create_app
    from src.recoleccion.services.mock_entorno_service import MockEntornoService
    from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService
    
    # Crear instancias de los servicios mock
    entorno_service = MockEntornoService()
    comunicacion_service = MockComunicacionService()
    
    # Crear la aplicación FastAPI
    app = create_app(entorno_service, comunicacion_service)
    
    print("Aplicacion FastAPI creada exitosamente")
    print(f"Servicios mock inicializados")
    
except Exception as e:
    print(f"Error creando aplicacion: {e}")
    sys.exit(1)

# Configuración para Railway
if __name__ == "__main__":
    try:
        # Obtener puerto de Railway o usar 8000 por defecto
        port = int(os.environ.get("PORT", 8000))
        
        print(f"Iniciando servidor en puerto {port}")
        print(f"Host: 0.0.0.0")
        print(f"Healthcheck: /health")
        
        # Configurar uvicorn para Railway - Configuración mínima
        config = uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=port,
            log_level="critical",  # Solo errores críticos
            access_log=False,
            reload=False,
            server_header=False,
            date_header=False,
            use_colors=False,  # Deshabilitar colores
            loop="asyncio"     # Loop específico
        )
        
        # Crear servidor
        server = uvicorn.Server(config)
        
        # Ejecutar servidor
        server.run()
        
    except Exception as e:
        print(f"Error iniciando servidor: {e}")
        sys.exit(1)
