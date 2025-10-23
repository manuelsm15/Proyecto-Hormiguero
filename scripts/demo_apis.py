#!/usr/bin/env python3
"""
Script de demostración de las APIs del Subsistema de Recolección.
"""

import requests
import json
import time
from typing import Dict, Any

class APIDemo:
    """Demostración de las APIs del subsistema de recolección."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def print_header(self, title: str):
        """Imprime un encabezado formateado."""
        print(f"\n{'='*60}")
        print(f">>> {title}")
        print(f"{'='*60}")
    
    def print_response(self, response: requests.Response, description: str):
        """Imprime la respuesta de la API de forma formateada."""
        print(f"\nAPI: {description}")
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except:
            print(response.text)
    
    def test_root_endpoint(self):
        """Prueba el endpoint raíz."""
        self.print_header("ENDPOINT RAÍZ")
        try:
            response = self.session.get(f"{self.base_url}/")
            self.print_response(response, "GET / - Información del subsistema")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_health_check(self):
        """Prueba el health check."""
        self.print_header("HEALTH CHECK")
        try:
            response = self.session.get(f"{self.base_url}/health")
            self.print_response(response, "GET /health - Verificación de salud")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_consultar_alimentos(self):
        """Prueba la consulta de alimentos."""
        self.print_header("CONSULTAR ALIMENTOS")
        try:
            response = self.session.get(f"{self.base_url}/alimentos")
            self.print_response(response, "GET /alimentos - Consultar alimentos disponibles")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_crear_tarea(self):
        """Prueba la creación de una tarea."""
        self.print_header("CREAR TAREA")
        try:
            params = {
                "tarea_id": "tarea_demo_001",
                "alimento_id": "alimento_001"
            }
            response = self.session.post(f"{self.base_url}/tareas", params=params)
            self.print_response(response, "POST /tareas - Crear nueva tarea")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_listar_tareas(self):
        """Prueba el listado de tareas."""
        self.print_header("LISTAR TAREAS")
        try:
            response = self.session.get(f"{self.base_url}/tareas")
            self.print_response(response, "GET /tareas - Listar tareas activas")
            
            response = self.session.get(f"{self.base_url}/tareas/completadas")
            self.print_response(response, "GET /tareas/completadas - Listar tareas completadas")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_iniciar_tarea(self):
        """Prueba el inicio de una tarea."""
        self.print_header("INICIAR TAREA")
        try:
            response = self.session.post(f"{self.base_url}/tareas/tarea_demo_001/iniciar")
            self.print_response(response, "POST /tareas/{id}/iniciar - Iniciar tarea")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_completar_tarea(self):
        """Prueba la finalización de una tarea."""
        self.print_header("COMPLETAR TAREA")
        try:
            params = {"cantidad_recolectada": 10}
            response = self.session.post(f"{self.base_url}/tareas/tarea_demo_001/completar", params=params)
            self.print_response(response, "POST /tareas/{id}/completar - Completar tarea")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_procesar_recoleccion(self):
        """Prueba el procesamiento completo de recolección."""
        self.print_header("PROCESAR RECOLECCIÓN")
        try:
            response = self.session.post(f"{self.base_url}/procesar")
            self.print_response(response, "POST /procesar - Procesar recolección completa")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_estadisticas(self):
        """Prueba la obtención de estadísticas."""
        self.print_header("ESTADÍSTICAS")
        try:
            response = self.session.get(f"{self.base_url}/estadisticas")
            self.print_response(response, "GET /estadisticas - Obtener estadísticas")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_verificar_hormigas(self):
        """Prueba la verificación de hormigas."""
        self.print_header("VERIFICAR HORMIGAS")
        try:
            response = self.session.post(f"{self.base_url}/verificar-hormigas")
            self.print_response(response, "POST /verificar-hormigas - Verificar hormigas muertas")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_documentacion(self):
        """Muestra información sobre la documentación."""
        self.print_header("DOCUMENTACIÓN DE LA API")
        print("Documentacion disponible en:")
        print(f"   - Swagger UI: {self.base_url}/docs")
        print(f"   - ReDoc: {self.base_url}/redoc")
        print(f"   - OpenAPI JSON: {self.base_url}/openapi.json")
    
    def run_demo(self):
        """Ejecuta la demostración completa."""
        print("DEMOSTRACION DE APIs DEL SUBSISTEMA DE RECOLECCION")
        print("Universidad Cenfotec - Proyecto Final")
        print("=" * 60)
        
        # Verificar conectividad
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                print("OK: Conexion exitosa con la API")
            else:
                print("ERROR: Error de conexion")
                return
        except Exception as e:
            print(f"ERROR: No se puede conectar a {self.base_url}")
            print("Asegurate de que la aplicacion este ejecutandose con: python main.py")
            return
        
        # Ejecutar todas las pruebas
        self.test_root_endpoint()
        self.test_health_check()
        self.test_consultar_alimentos()
        self.test_crear_tarea()
        self.test_listar_tareas()
        self.test_iniciar_tarea()
        self.test_completar_tarea()
        self.test_procesar_recoleccion()
        self.test_estadisticas()
        self.test_verificar_hormigas()
        self.test_documentacion()
        
        print(f"\n{'='*60}")
        print("DEMOSTRACION COMPLETADA")
        print("Todas las APIs del subsistema de recoleccion han sido probadas")
        print("Para mas detalles, visita la documentacion en /docs")
        print(f"{'='*60}")

def main():
    """Función principal."""
    demo = APIDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
