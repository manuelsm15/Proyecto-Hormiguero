"""
Simulador completo de Railway para probar el deploy.
"""

import subprocess
import time
import requests
import sys
import os
import json

class RailwaySimulator:
    def __init__(self):
        self.process = None
        self.port = 8000
        self.base_url = f"http://localhost:{self.port}"
        
    def simulate_railway_environment(self):
        """Simula el entorno completo de Railway."""
        print("=== SIMULANDO ENTORNO RAILWAY COMPLETO ===")
        
        # Variables de entorno de Railway
        railway_env = {
            "PORT": str(self.port),
            "RAILWAY_HEALTHCHECK_TIMEOUT_SEC": "300",
            "PYTHONPATH": "/app",
            "LOG_LEVEL": "ERROR",
            "ENVIRONMENT": "production",
            "RAILWAY_PROJECT_ID": "hormiguero-recoleccion",
            "RAILWAY_SERVICE_ID": "subsistema-recoleccion"
        }
        
        print("Variables de entorno Railway simuladas:")
        for key, value in railway_env.items():
            print(f"  {key}={value}")
        
        # Simular configuracion de Railway
        railway_config = {
            "healthcheck": {
                "path": "/health",
                "timeout": 300
            },
            "deploy": {
                "startCommand": "python railway_main.py",
                "healthcheckPath": "/health",
                "healthcheckTimeout": 300
            }
        }
        
        print("\nConfiguracion Railway simulada:")
        print(f"  Healthcheck Path: {railway_config['healthcheck']['path']}")
        print(f"  Healthcheck Timeout: {railway_config['healthcheck']['timeout']}s")
        print(f"  Start Command: {railway_config['deploy']['startCommand']}")
        
        return railway_env, railway_config
    
    def start_railway_service(self):
        """Inicia el servicio Railway simulado."""
        print("\nIniciando servicio Railway simulado...")
        
        try:
            # Cambiar al directorio del proyecto
            os.chdir("C:\\Users\\manue\\Proyecto Hormiguero")
            
            # Simular comando Railway
            print("Comando Railway simulado:")
            print("  railway deploy")
            print("  railway up")
            print("Ejecutando: python railway_main.py")
            
            # Iniciar el proceso
            self.process = subprocess.Popen([
                sys.executable, "railway_main.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print("Servicio Railway simulado iniciado exitosamente")
            return True
            
        except Exception as e:
            print(f"Error iniciando servicio Railway: {e}")
            return False
    
    def wait_for_railway_healthcheck(self, timeout=60):
        """Espera a que el healthcheck de Railway responda."""
        print(f"\nEsperando healthcheck Railway (timeout: {timeout}s)...")
        print("Simulando healthcheck.railway.app requests...")
        
        for i in range(timeout):
            try:
                # Simular request desde healthcheck.railway.app
                headers = {
                    "User-Agent": "Railway-Healthcheck/1.0",
                    "Host": "healthcheck.railway.app"
                }
                
                response = requests.get(
                    f"{self.base_url}/health", 
                    headers=headers,
                    timeout=5
                )
                
                if response.status_code == 200:
                    health_data = response.json()
                    print(f"Healthcheck Railway exitoso en {i+1}s")
                    print(f"  Status: {health_data.get('status', 'unknown')}")
                    print(f"  Service: {health_data.get('service', 'unknown')}")
                    print(f"  Version: {health_data.get('version', 'unknown')}")
                    return True
                    
            except Exception as e:
                if i % 10 == 0:  # Log cada 10 segundos
                    print(f"  Esperando... ({i+1}s) - {e}")
            time.sleep(1)
        
        print("ERROR: Healthcheck Railway timeout")
        return False
    
    def test_railway_deployment(self):
        """Prueba completa del deploy Railway."""
        print("\n=== PRUEBA COMPLETA DE DEPLOY RAILWAY ===")
        
        # Endpoints criticos para Railway
        critical_endpoints = [
            {
                "endpoint": "/health",
                "description": "Healthcheck - CRITICO para Railway",
                "railway_critical": True
            },
            {
                "endpoint": "/",
                "description": "Endpoint raiz",
                "railway_critical": False
            },
            {
                "endpoint": "/alimentos",
                "description": "Lista de alimentos",
                "railway_critical": True
            },
            {
                "endpoint": "/docs",
                "description": "Documentacion Swagger",
                "railway_critical": True
            },
            {
                "endpoint": "/tareas",
                "description": "Lista de tareas",
                "railway_critical": True
            }
        ]
        
        results = []
        railway_critical_failures = []
        
        for endpoint_info in critical_endpoints:
            endpoint = endpoint_info["endpoint"]
            description = endpoint_info["description"]
            railway_critical = endpoint_info["railway_critical"]
            
            print(f"\nProbando {description}...")
            print(f"  URL: {self.base_url}{endpoint}")
            print(f"  Railway Critico: {'SI' if railway_critical else 'NO'}")
            
            try:
                # Simular request desde Railway
                headers = {
                    "User-Agent": "Railway-Client/1.0",
                    "X-Railway-Source": "deployment"
                }
                
                response = requests.get(
                    f"{self.base_url}{endpoint}", 
                    headers=headers,
                    timeout=10
                )
                
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"  OK - {description}")
                    results.append(True)
                else:
                    print(f"  ERROR - {description} (Status: {response.status_code})")
                    results.append(False)
                    if railway_critical:
                        railway_critical_failures.append(description)
                        
            except Exception as e:
                print(f"  ERROR - {description}: {e}")
                results.append(False)
                if railway_critical:
                    railway_critical_failures.append(description)
        
        # Resumen Railway
        total = len(results)
        passed = sum(results)
        failed = total - passed
        
        print(f"\n=== RESUMEN DE DEPLOY RAILWAY ===")
        print(f"Total de pruebas: {total}")
        print(f"Exitosas: {passed}")
        print(f"Fallidas: {failed}")
        print(f"Porcentaje de exito: {(passed/total)*100:.1f}%")
        
        if railway_critical_failures:
            print(f"\nERRORES CRITICOS PARA RAILWAY:")
            for failure in railway_critical_failures:
                print(f"  - {failure}")
            return False
        
        return passed == total
    
    def test_railway_production_features(self):
        """Prueba funcionalidades de produccion Railway."""
        print("\n=== PRUEBA DE FUNCIONALIDADES DE PRODUCCION RAILWAY ===")
        
        # 1. Probar creacion de tarea en produccion
        print("\n1. Probando creacion de tarea en produccion...")
        try:
            tarea_data = {
                "tarea_id": "tarea_railway_prod_001",
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
        
        # 2. Probar procesamiento completo
        print("\n2. Probando procesamiento completo en produccion...")
        try:
            response = requests.post(f"{self.base_url}/procesar", timeout=15)
            if response.status_code == 200:
                resultado = response.json()
                print(f"  OK - Procesamiento completo exitoso")
            else:
                print(f"  ERROR - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ERROR: {e}")
            return False
        
        # 3. Probar estadisticas de produccion
        print("\n3. Probando estadisticas de produccion...")
        try:
            response = requests.get(f"{self.base_url}/estadisticas", timeout=10)
            if response.status_code == 200:
                stats = response.json()
                print(f"  OK - Estadisticas obtenidas")
            else:
                print(f"  ERROR - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ERROR: {e}")
            return False
        
        print("\nTodas las funcionalidades de produccion funcionando")
        return True
    
    def stop_railway_service(self):
        """Detiene el servicio Railway simulado."""
        print("\nDeteniendo servicio Railway simulado...")
        
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("Servicio Railway detenido exitosamente")
            except subprocess.TimeoutExpired:
                self.process.kill()
                print("Servicio Railway forzado a detener")
            except Exception as e:
                print(f"Error deteniendo servicio Railway: {e}")
    
    def get_railway_logs(self):
        """Obtiene los logs del servicio Railway."""
        if self.process:
            try:
                stdout, stderr = self.process.communicate(timeout=1)
                if stdout:
                    print("\n=== LOGS DEL SERVICIO RAILWAY ===")
                    print("STDOUT:", stdout)
                if stderr:
                    print("STDERR:", stderr)
            except:
                pass

def main():
    """Funcion principal del simulador Railway."""
    print("=== SIMULADOR COMPLETO DE RAILWAY PARA HORMIGUERO RECOLECCION ===")
    
    simulator = RailwaySimulator()
    
    try:
        # 1. Simular entorno Railway
        railway_env, railway_config = simulator.simulate_railway_environment()
        
        # 2. Iniciar servicio Railway
        if not simulator.start_railway_service():
            print("ERROR: No se pudo iniciar el servicio Railway simulado")
            sys.exit(1)
        
        # 3. Esperar healthcheck Railway
        if not simulator.wait_for_railway_healthcheck():
            print("ERROR: Healthcheck Railway fallo")
            simulator.get_railway_logs()
            sys.exit(1)
        
        # 4. Probar deploy Railway
        if not simulator.test_railway_deployment():
            print("ERROR: Deploy Railway fallo")
            simulator.get_railway_logs()
            sys.exit(1)
        
        # 5. Probar funcionalidades de produccion
        if not simulator.test_railway_production_features():
            print("ERROR: Funcionalidades de produccion fallaron")
            simulator.get_railway_logs()
            sys.exit(1)
        
        print("\n=== DEPLOY RAILWAY SIMULADO EXITOSO ===")
        print("El servicio funciona correctamente en entorno Railway simulado")
        print("LISTO PARA DEPLOY REAL EN RAILWAY!")
        
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario")
    except Exception as e:
        print(f"Error inesperado: {e}")
        simulator.get_railway_logs()
    finally:
        # 6. Limpiar
        simulator.stop_railway_service()
        print("\n=== SIMULADOR RAILWAY COMPLETADO ===")

if __name__ == "__main__":
    main()
