"""
Aplicación principal optimizada para Railway.
"""

import os
import sys
import logging
import uvicorn
from pathlib import Path

# Configurar logging para Railway - Info level para debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
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
    
    print("✅ Aplicacion FastAPI creada exitosamente")
    print("✅ Servicios mock inicializados")
    print(f"✅ App object: {app}")
    print(f"✅ App title: {app.title}")
    
except Exception as e:
    print(f"❌ Error creando aplicacion: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Configuración para Railway
if __name__ == "__main__":
    try:
        # Obtener puerto de Railway o usar 8000 por defecto
        port = int(os.environ.get("PORT", 8000))
        
        print(f"🚀 Iniciando servidor en puerto {port}")
        print(f"🌐 Host: 0.0.0.0")
        print(f"❤️  Healthcheck: /health")
        print(f"📋 App routes: {[route.path for route in app.routes]}")
        
        # Configurar uvicorn para Railway
        config = uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=port,
            log_level="info",  # Info level para ver qué está pasando
            access_log=True,   # Habilitar access log para debugging
            reload=False,
            server_header=False,
            date_header=False,
            use_colors=False,  # Deshabilitar colores
            loop="asyncio"     # Loop específico
        )
        
        # Crear servidor
        server = uvicorn.Server(config)
        
        print(f"✅ Servidor configurado correctamente")
        print(f"✅ Iniciando servidor...")
        
        # Ejecutar servidor
        server.run()
        
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
