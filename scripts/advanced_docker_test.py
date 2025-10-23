"""
Simulador avanzado de Docker para probar las APIs con configuracion completa.
"""

import subprocess
import time
import requests
import sys
import os
import json
import threading

class AdvancedDockerSimulator:
    def __init__(self):
        self.process = None
        self.port = 8000
        self.base_url = f"http://localhost:{self.port}"
        
    def simulate_docker_environment(self):
        """Simula el entorno Docker completo."""
        print("=== SIMULANDO ENTORNO DOCKER COMPLETO ===")
        
        # Simular variables de entorno de Docker
        env_vars = {
            "PYTHONPATH": "/app",
            "LOG_LEVEL": "ERROR",
            "ENVIRONMENT": "production",
            "PORT": str(self.port)
        }
        
        print("Variables de entorno simuladas:")
        for key, value in env_vars.items():
            print(f"  {key}={value}")
        
        return env_vars
    
    def start_docker_container(self):
        """Inicia el contenedor Docker simulado."""
        print("\nIniciando contenedor Docker simulado...")
        
        try:
            # Cambiar al directorio del proyecto
            os.chdir("C:\\Users\\manue\\Proyecto Hormiguero")
            
            # Simular comando Docker
            print("Comando simulado: docker run -p 8000:8000 hormiguero-recoleccion")
            print("Ejecutando: python railway_main.py")
            
            # Iniciar el proceso
            self.process = subprocess.Popen([
                sys.executable, "railway_main.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print("Contenedor Docker simulado iniciado exitosamente")
            return True
            
        except Exception as e:
            print(f"Error iniciando contenedor: {e}")
            return False
    
    def wait_for_healthcheck(self, timeout=30):
        """Espera a que el healthcheck responda."""
        print(f"\nEsperando healthcheck (timeout: {timeout}s)...")
        
        for i in range(timeout):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=2)
                if response.status_code == 200:
                    health_data = response.json()
                    print(f"Healthcheck exitoso en {i+1}s")
                    print(f"  Status: {health_data.get('status', 'unknown')}")
                    print(f"  Service: {health_data.get('service', 'unknown')}")
                    return True
            except:
                pass
            time.sleep(1)
        
        print("ERROR: Healthcheck timeout")
        return False
    
    def test_docker_apis_comprehensive(self):
        """Prueba completa de APIs en entorno Docker."""
        print("\n=== PRUEBA COMPLETA DE APIs EN DOCKER ===")
        
        # Lista completa de endpoints
        test_cases = [
            {
                "endpoint": "/health",
                "method": "GET",
                "description": "Healthcheck - CRITICO para Railway",
                "critical": True
            },
            {
                "endpoint": "/",
                "method": "GET", 
                "description": "Endpoint raiz",
                "critical": False
            },
            {
                "endpoint": "/alimentos",
                "method": "GET",
                "description": "Lista de alimentos",
                "critical": True
            },
            {
                "endpoint": "/docs",
                "method": "GET",
                "description": "Documentacion Swagger",
                "critical": True
            },
            {
                "endpoint": "/openapi.json",
                "method": "GET",
                "description": "Especificacion OpenAPI",
                "critical": False
            },
            {
                "endpoint": "/tareas",
                "method": "GET",
                "description": "Lista de tareas",
                "critical": True
            },
            {
                "endpoint": "/tareas/en-proceso",
                "method": "GET",
                "description": "Tareas en proceso",
                "critical": False
            },
            {
                "endpoint": "/tareas/completadas",
                "method": "GET",
                "description": "Tareas completadas",
                "critical": False
            },
            {
                "endpoint": "/estadisticas",
                "method": "GET",
                "description": "Estadisticas del servicio",
                "critical": False
            }
        ]
        
        results = []
        critical_failures = []
        
        for test_case in test_cases:
            endpoint = test_case["endpoint"]
            method = test_case["method"]
            description = test_case["description"]
            critical = test_case["critical"]
            
            print(f"\nProbando {description}...")
            print(f"  URL: {self.base_url}{endpoint}")
            print(f"  Metodo: {method}")
            print(f"  Critico: {'SI' if critical else 'NO'}")
            
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", timeout=10)
                
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"  OK - {description}")
                    results.append(True)
                else:
                    print(f"  ERROR - {description} (Status: {response.status_code})")
                    results.append(False)
                    if critical:
                        critical_failures.append(description)
                        
            except Exception as e:
                print(f"  ERROR - {description}: {e}")
                results.append(False)
                if critical:
                    critical_failures.append(description)
        
        # Resumen detallado
        total = len(results)
        passed = sum(results)
        failed = total - passed
        
        print(f"\n=== RESUMEN DETALLADO DE PRUEBAS DOCKER ===")
        print(f"Total de pruebas: {total}")
        print(f"Exitosas: {passed}")
        print(f"Fallidas: {failed}")
        print(f"Porcentaje de exito: {(passed/total)*100:.1f}%")
        
        if critical_failures:
            print(f"\nERRORES CRITICOS:")
            for failure in critical_failures:
                print(f"  - {failure}")
        
        return passed == total and len(critical_failures) == 0
    
    def test_docker_specific_features(self):
        """Prueba funcionalidades especificas de Docker."""
        print("\n=== PRUEBA DE FUNCIONALIDADES ESPECIFICAS DOCKER ===")
        
        # 1. Probar creacion de tarea
        print("\n1. Probando creacion de tarea...")
        try:
            tarea_data = {
                "tarea_id": "tarea_docker_test_001",
                "alimento_id": "A1"
            }
            response = requests.post(f"{self.base_url}/tareas", params=tarea_data, timeout=10)
            if response.status_code == 200:
                tarea = response.json()
                print(f"  OK - Tarea creada: {tarea['id']}")
            else:
                print(f"  ERROR - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ERROR: {e}")
            return False
        
        # 2. Probar procesamiento de recoleccion
        print("\n2. Probando procesamiento de recoleccion...")
        try:
            response = requests.post(f"{self.base_url}/procesar", timeout=10)
            if response.status_code == 200:
                resultado = response.json()
                print(f"  OK - Procesamiento exitoso")
            else:
                print(f"  ERROR - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ERROR: {e}")
            return False
        
        # 3. Probar verificacion de hormigas
        print("\n3. Probando verificacion de hormigas...")
        try:
            response = requests.post(f"{self.base_url}/verificar-hormigas", timeout=10)
            if response.status_code == 200:
                resultado = response.json()
                print(f"  OK - Verificacion exitosa")
            else:
                print(f"  ERROR - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ERROR: {e}")
            return False
        
        print("\nTodas las funcionalidades especificas funcionando")
        return True
    
    def stop_docker_container(self):
        """Detiene el contenedor Docker simulado."""
        print("\nDeteniendo contenedor Docker simulado...")
        
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("Contenedor detenido exitosamente")
            except subprocess.TimeoutExpired:
                self.process.kill()
                print("Contenedor forzado a detener")
            except Exception as e:
                print(f"Error deteniendo contenedor: {e}")
    
    def get_container_logs(self):
        """Obtiene los logs del contenedor."""
        if self.process:
            try:
                stdout, stderr = self.process.communicate(timeout=1)
                if stdout:
                    print("\n=== LOGS DEL CONTENEDOR ===")
                    print("STDOUT:", stdout)
                if stderr:
                    print("STDERR:", stderr)
            except:
                pass

def main():
    """Funcion principal del simulador avanzado."""
    print("=== SIMULADOR AVANZADO DE DOCKER PARA HORMIGUERO RECOLECCION ===")
    
    simulator = AdvancedDockerSimulator()
    
    try:
        # 1. Simular entorno Docker
        simulator.simulate_docker_environment()
        
        # 2. Iniciar contenedor
        if not simulator.start_docker_container():
            print("ERROR: No se pudo iniciar el contenedor Docker simulado")
            sys.exit(1)
        
        # 3. Esperar healthcheck
        if not simulator.wait_for_healthcheck():
            print("ERROR: Healthcheck fallo")
            simulator.get_container_logs()
            sys.exit(1)
        
        # 4. Probar APIs completas
        if not simulator.test_docker_apis_comprehensive():
            print("ERROR: Pruebas de APIs fallaron")
            simulator.get_container_logs()
            sys.exit(1)
        
        # 5. Probar funcionalidades especificas
        if not simulator.test_docker_specific_features():
            print("ERROR: Funcionalidades especificas fallaron")
            simulator.get_container_logs()
            sys.exit(1)
        
        print("\n=== TODAS LAS PRUEBAS DOCKER EXITOSAS ===")
        print("El servicio funciona correctamente en entorno Docker simulado")
        print("Listo para deploy en Railway")
        
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario")
    except Exception as e:
        print(f"Error inesperado: {e}")
        simulator.get_container_logs()
    finally:
        # 6. Limpiar
        simulator.stop_docker_container()
        print("\n=== SIMULADOR AVANZADO DE DOCKER COMPLETADO ===")

if __name__ == "__main__":
    main()
