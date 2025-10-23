#!/usr/bin/env python3
"""
Script para probar el acceso remoto al Subsistema de Recolección.
"""

import requests
import json
import time
from typing import Dict, Any

class RemoteTester:
    """Tester para acceso remoto al subsistema."""
    
    def __init__(self, base_url: str):
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
    
    def test_connectivity(self):
        """Prueba la conectividad básica."""
        self.print_header("PRUEBA DE CONECTIVIDAD")
        
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                print("OK: Conectividad exitosa")
                self.print_response(response, "GET / - Información del subsistema")
                return True
            else:
                print(f"ERROR: Status code {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"ERROR: No se pudo conectar - {e}")
            return False
    
    def test_health_check(self):
        """Prueba el health check."""
        self.print_header("HEALTH CHECK")
        
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            self.print_response(response, "GET /health - Verificación de salud")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Health check falló - {e}")
            return False
    
    def test_alimentos(self):
        """Prueba la consulta de alimentos."""
        self.print_header("CONSULTAR ALIMENTOS")
        
        try:
            response = self.session.get(f"{self.base_url}/alimentos", timeout=10)
            self.print_response(response, "GET /alimentos - Alimentos disponibles")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Consulta de alimentos falló - {e}")
            return False
    
    def test_crear_tarea(self):
        """Prueba la creación de una tarea."""
        self.print_header("CREAR TAREA")
        
        try:
            params = {
                "tarea_id": "tarea_remota_001",
                "alimento_id": "A1"
            }
            response = self.session.post(f"{self.base_url}/tareas", params=params, timeout=10)
            self.print_response(response, "POST /tareas - Crear tarea remota")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Creación de tarea falló - {e}")
            return False
    
    def test_procesar_recoleccion(self):
        """Prueba el procesamiento de recolección."""
        self.print_header("PROCESAR RECOLECCION")
        
        try:
            response = self.session.post(f"{self.base_url}/procesar", timeout=30)
            self.print_response(response, "POST /procesar - Procesamiento completo")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Procesamiento falló - {e}")
            return False
    
    def test_estadisticas(self):
        """Prueba las estadísticas."""
        self.print_header("ESTADISTICAS")
        
        try:
            response = self.session.get(f"{self.base_url}/estadisticas", timeout=10)
            self.print_response(response, "GET /estadisticas - Estadísticas del sistema")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Estadísticas fallaron - {e}")
            return False
    
    def test_documentacion(self):
        """Prueba el acceso a la documentación."""
        self.print_header("DOCUMENTACION")
        
        try:
            # Probar Swagger UI
            response = self.session.get(f"{self.base_url}/docs", timeout=10)
            if response.status_code == 200:
                print("OK: Swagger UI accesible")
            else:
                print(f"WARNING: Swagger UI - Status {response.status_code}")
            
            # Probar ReDoc
            response = self.session.get(f"{self.base_url}/redoc", timeout=10)
            if response.status_code == 200:
                print("OK: ReDoc accesible")
            else:
                print(f"WARNING: ReDoc - Status {response.status_code}")
            
            return True
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Documentación no accesible - {e}")
            return False
    
    def run_full_test(self):
        """Ejecuta todas las pruebas."""
        print("PRUEBAS DE ACCESO REMOTO")
        print("Subsistema de Recolección - Universidad Cenfotec")
        print("="*60)
        
        print(f"Probando acceso a: {self.base_url}")
        
        tests = [
            ("Conectividad", self.test_connectivity),
            ("Health Check", self.test_health_check),
            ("Alimentos", self.test_alimentos),
            ("Crear Tarea", self.test_crear_tarea),
            ("Procesar Recolección", self.test_procesar_recoleccion),
            ("Estadísticas", self.test_estadisticas),
            ("Documentación", self.test_documentacion)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n--- Ejecutando: {test_name} ---")
            if test_func():
                print(f"OK: {test_name}: PASO")
                passed += 1
            else:
                print(f"ERROR: {test_name}: FALLO")
        
        print(f"\n{'='*60}")
        print(f"RESULTADOS: {passed}/{total} pruebas pasaron")
        
        if passed == total:
            print("TODAS LAS PRUEBAS PASARON")
            print("El subsistema esta funcionando correctamente")
        else:
            print("ALGUNAS PRUEBAS FALLARON")
            print("Revisa la conectividad y configuracion")
        
        print(f"{'='*60}")
        
        return passed == total

def main():
    """Función principal."""
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python test_remote_access.py <URL>")
        print("Ejemplo: python test_remote_access.py http://192.168.1.100:8000")
        return 1
    
    base_url = sys.argv[1]
    tester = RemoteTester(base_url)
    
    success = tester.run_full_test()
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
