"""
Script para exportar el esquema OpenAPI a un archivo JSON.
Útil para versionar el contrato de la API o compartirlo con otros equipos.
"""

import json
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.recoleccion.api.recoleccion_controller import create_app
from src.recoleccion.services.mock_entorno_service import MockEntornoService
from src.recoleccion.services.mock_comunicacion_service import MockComunicacionService


def export_openapi_schema(output_file: str = "openapi.json"):
    """
    Exporta el esquema OpenAPI a un archivo JSON.
    
    Args:
        output_file: Nombre del archivo de salida (por defecto: openapi.json)
    """
    # Crear la aplicación FastAPI
    entorno_service = MockEntornoService()
    comunicacion_service = MockComunicacionService()
    app = create_app(entorno_service, comunicacion_service)
    
    # Obtener el esquema OpenAPI
    openapi_schema = app.openapi()
    
    # Guardar en archivo
    output_path = root_dir / output_file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Esquema OpenAPI exportado exitosamente a: {output_path}")
    print(f"[INFO] Tamaño del archivo: {output_path.stat().st_size} bytes")
    return output_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Exportar esquema OpenAPI a JSON")
    parser.add_argument(
        "-o", "--output",
        default="openapi.json",
        help="Nombre del archivo de salida (por defecto: openapi.json)"
    )
    
    args = parser.parse_args()
    export_openapi_schema(args.output)

