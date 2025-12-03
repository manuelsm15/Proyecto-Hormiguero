"""
Aplicación principal optimizada para Railway.
"""

import os
import sys
import logging
import uvicorn
from pathlib import Path

# Forzar que los prints se muestren inmediatamente
sys.stdout.flush()
sys.stderr.flush()

# Configurar logging para Railway - Info level para debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
    force=True  # Forzar reconfiguración
)

# Logger específico
logger = logging.getLogger(__name__)
logger.info("=" * 50)
logger.info("INICIANDO APLICACION RAILWAY")
logger.info("=" * 50)
sys.stdout.flush()

# Agregar el directorio actual al path
current_dir = Path.cwd()
sys.path.append(str(current_dir))

try:
    logger.info("Importando módulos...")
    sys.stdout.flush()
    
    from src.recoleccion.api.recoleccion_controller import create_app
    from src.recoleccion.services.mock_entorno_service import MockEntornoService
    from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService
    
    logger.info("✅ Módulos importados correctamente")
    sys.stdout.flush()
    
    # Crear instancias de los servicios mock
    logger.info("Creando servicios mock...")
    sys.stdout.flush()
    entorno_service = MockEntornoService()
    comunicacion_service = MockComunicacionService()
    
    logger.info("✅ Servicios mock creados")
    sys.stdout.flush()
    
    # Crear la aplicación FastAPI
    logger.info("Creando aplicación FastAPI...")
    sys.stdout.flush()
    app = create_app(entorno_service, comunicacion_service)
    
    logger.info("✅ Aplicacion FastAPI creada exitosamente")
    logger.info(f"✅ App title: {app.title}")
    logger.info(f"✅ App version: {app.version}")
    
    # Listar rutas disponibles
    routes = [route.path for route in app.routes if hasattr(route, 'path')]
    logger.info(f"✅ Rutas registradas: {len(routes)}")
    logger.info(f"✅ Rutas: {routes[:10]}...")  # Primeras 10 rutas
    
    sys.stdout.flush()
    
except Exception as e:
    logger.error(f"❌ Error creando aplicacion: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit(1)

# Configuración para Railway
if __name__ == "__main__":
    try:
        # Obtener puerto de Railway o usar 8000 por defecto
        port = int(os.environ.get("PORT", 8000))
        host = os.environ.get("HOST", "0.0.0.0")
        
        logger.info("=" * 50)
        logger.info("CONFIGURANDO SERVIDOR UVICORN")
        logger.info("=" * 50)
        logger.info(f"🚀 Puerto: {port}")
        logger.info(f"🌐 Host: {host}")
        logger.info(f"❤️  Healthcheck: /health")
        logger.info(f"📋 Total rutas: {len([r for r in app.routes if hasattr(r, 'path')])}")
        sys.stdout.flush()
        
        # Verificar que /health existe
        health_route_exists = any(
            hasattr(route, 'path') and route.path == '/health' 
            for route in app.routes
        )
        if health_route_exists:
            logger.info("✅ Ruta /health encontrada")
        else:
            logger.warning("⚠️  Ruta /health NO encontrada!")
        sys.stdout.flush()
        
        # Configurar uvicorn para Railway
        logger.info("Configurando uvicorn...")
        sys.stdout.flush()
        
        config = uvicorn.Config(
            app=app,
            host=host,
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
        
        logger.info("✅ Servidor configurado correctamente")
        logger.info("✅ Iniciando servidor uvicorn...")
        logger.info("=" * 50)
        sys.stdout.flush()
        sys.stderr.flush()
        
        # Ejecutar servidor (esto es bloqueante)
        server.run()
        
    except KeyboardInterrupt:
        logger.info("Servidor detenido por usuario")
        sys.stdout.flush()
    except Exception as e:
        logger.error(f"❌ Error iniciando servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(1)
