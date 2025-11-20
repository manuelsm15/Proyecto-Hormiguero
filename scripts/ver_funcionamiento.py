"""
Script simple para ver el funcionamiento del sistema y abrir la documentacion.
"""

import webbrowser
import requests
import json


def main():
    BASE_URL = "http://localhost:8000"
    
    print("\n" + "=" * 70)
    print("  SUBSISTEMA DE RECOLECCION DE ALIMENTOS")
    print("=" * 70)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("\nOK Servidor funcionando correctamente!")
            print(f"  URL: {BASE_URL}")
            
            data = response.json()
            print(f"\nEstado del Sistema:")
            print(f"  Status: {data.get('status', 'N/A')}")
            print(f"  Version: {data.get('version', 'N/A')}")
            print(f"  Entorno disponible: {data.get('entorno_disponible', False)}")
            print(f"  Comunicacion disponible: {data.get('comunicacion_disponible', False)}")
            
            print("\n" + "=" * 70)
            print("  ABRIENDO DOCUMENTACION INTERACTIVA...")
            print("=" * 70)
            print(f"\nAbriendo: {BASE_URL}/docs")
            print("En tu navegador puedes:")
            print("  - Ver todos los endpoints")
            print("  - Probar cada endpoint directamente")
            print("  - Ver ejemplos de requests/responses")
            print("  - Ver el esquema OpenAPI completo")
            
            # Abrir en el navegador
            try:
                webbrowser.open(f"{BASE_URL}/docs")
                print("\nOK Documentacion abierta en tu navegador!")
            except:
                print(f"\nADVERTENCIA: No se pudo abrir automaticamente.")
                print(f"  Por favor, abre manualmente: {BASE_URL}/docs")
            
            print("\n" + "=" * 70)
            print("  ENDPOINTS PRINCIPALES")
            print("=" * 70)
            print("\nGET  /health                    - Estado del sistema")
            print("GET  /alimentos                 - Listar alimentos disponibles")
            print("GET  /alimentos?zona_id=1       - Filtrar por zona")
            print("GET  /alimentos?estado=disponible - Filtrar por estado")
            print("POST /tareas                    - Crear tarea de recoleccion")
            print("GET  /tareas                    - Listar todas las tareas")
            print("GET  /tareas/activas            - Solo tareas activas")
            print("GET  /tareas/completadas        - Solo tareas completadas")
            print("GET  /tareas/bd                 - Tareas desde base de datos")
            print("POST /procesar                  - Proceso automatico completo")
            print("GET  /estadisticas              - Estadisticas del sistema")
            print("GET  /eventos                   - Eventos recientes")
            print("GET  /docs                      - Documentacion interactiva (Swagger UI)")
            print("GET  /openapi.json              - Esquema OpenAPI")
            
            print("\n" + "=" * 70)
            
        else:
            print("\nERROR El servidor no responde correctamente")
            print(f"  Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("\nERROR No se puede conectar al servidor")
        print("\n  Por favor, inicia el servidor primero:")
        print("    python main.py")
        print("\n  Luego ejecuta este script nuevamente.")
    except Exception as e:
        print(f"\nERROR: {e}")


if __name__ == "__main__":
    main()

