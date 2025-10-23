"""
Simulador de Docker para probar las APIs en un entorno aislado.
"""

import subprocess
import time
import requests
import sys
import os
import signal
import threading

class DockerSimulator:
    def __init__(self):
        self.process = None
        self.port = 8000
        
    def start_container(self):
        """Simula iniciar un contenedor Docker."""
        print("Simulando inicio de contenedor Docker...")
        print(f"Puerto: {self.port}")
        print("Comando: python railway_main.py")
        
        try:
            # Cambiar al directorio del proyecto
            os.chdir("C:\\Users\\manue\\Proyecto Hormiguero")
            
            # Iniciar el proceso
            self.process = subprocess.Popen([
                sys.executable, "railway_main.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print("Proceso iniciado exitosamente")
            return True
            
        except Exception as e:
            print(f"Error iniciando proceso: {e}")
            return False
    
    def wait_for_startup(self, timeout=30):
        """Espera a que el servicio se inicie."""
        print(f"Esperando {timeout} segundos para que el servicio se inicie...")
        
        for i in range(timeout):
            try:
                response = requests.get(f"http://localhost:{self.port}/health", timeout=2)
                if response.status_code == 200:
                    print(f"Servicio iniciado exitosamente en {i+1} segundos")
                    return True
            except:
                pass
            time.sleep(1)
        
        print("Timeout: El servicio no se inicio en el tiempo esperado")
        return False
    
    def test_apis(self):
        """Prueba las APIs del servicio."""
        print("Probando APIs del servicio...")
        
        base_url = f"http://localhost:{self.port}"
        
        # Lista de endpoints a probar
        endpoints = [
            ("/health", "Healthcheck"),
            ("/", "Endpoint raiz"),
            ("/alimentos", "Lista de alimentos"),
            ("/docs", "Documentacion Swagger"),
            ("/tareas", "Lista de tareas"),
            ("/tareas/en-proceso", "Tareas en proceso"),
            ("/estadisticas", "Estadisticas")
        ]
        
        results = []
        
        for endpoint, description in endpoints:
            print(f"\nProbando {description}...")
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"  OK - {description}")
                    results.append(True)
                else:
                    print(f"  ERROR - {description} (Status: {response.status_code})")
                    results.append(False)
                    
            except Exception as e:
                print(f"  ERROR - {description}: {e}")
                results.append(False)
        
        # Resumen
        total = len(results)
        passed = sum(results)
        failed = total - passed
        
        print(f"\n=== RESUMEN DE PRUEBAS ===")
        print(f"Total de pruebas: {total}")
        print(f"Exitosas: {passed}")
        print(f"Fallidas: {failed}")
        print(f"Porcentaje de exito: {(passed/total)*100:.1f}%")
        
        return passed == total
    
    def stop_container(self):
        """Simula detener el contenedor Docker."""
        print("Simulando detencion de contenedor Docker...")
        
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("Proceso detenido exitosamente")
            except subprocess.TimeoutExpired:
                self.process.kill()
                print("Proceso forzado a terminar")
            except Exception as e:
                print(f"Error deteniendo proceso: {e}")
    
    def get_logs(self):
        """Obtiene los logs del contenedor."""
        if self.process:
            try:
                stdout, stderr = self.process.communicate(timeout=1)
                if stdout:
                    print("STDOUT:", stdout)
                if stderr:
                    print("STDERR:", stderr)
            except:
                pass

def main():
    """Funcion principal del simulador."""
    print("=== SIMULADOR DE DOCKER PARA HORMIGUERO RECOLECCION ===")
    
    simulator = DockerSimulator()
    
    try:
        # 1. Iniciar contenedor simulado
        if not simulator.start_container():
            print("ERROR: No se pudo iniciar el contenedor simulado")
            sys.exit(1)
        
        # 2. Esperar a que se inicie
        if not simulator.wait_for_startup():
            print("ERROR: El servicio no se inicio correctamente")
            simulator.get_logs()
            sys.exit(1)
        
        # 3. Probar APIs
        if simulator.test_apis():
            print("\nTODAS LAS PRUEBAS EXITOSAS!")
            print("El servicio funciona correctamente en modo Docker simulado")
        else:
            print("\nALGUNAS PRUEBAS FALLARON!")
            print("Revisar logs del servicio")
        
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        # 4. Limpiar
        simulator.stop_container()
        print("\n=== SIMULADOR DE DOCKER COMPLETADO ===")

if __name__ == "__main__":
    main()
