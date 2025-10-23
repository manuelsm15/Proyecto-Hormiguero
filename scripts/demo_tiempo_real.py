#!/usr/bin/env python3
"""
Script de demostración del sistema de tiempo real para recolección.
"""

import requests
import json
import time
from typing import Dict, Any

class DemoTiempoReal:
    """Demostración del sistema de tiempo real."""
    
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
    
    def test_alimentos_simplificados(self):
        """Prueba los alimentos con IDs simplificados."""
        self.print_header("ALIMENTOS CON IDs SIMPLIFICADOS")
        try:
            response = self.session.get(f"{self.base_url}/alimentos")
            self.print_response(response, "GET /alimentos - Alimentos con IDs A1, A2, A3")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_crear_tarea_tiempo_real(self):
        """Crea una tarea y la inicia con tiempo real."""
        self.print_header("CREAR TAREA CON TIEMPO REAL")
        try:
            # Crear tarea para A1 (Fruta - 5 minutos)
            params = {
                "tarea_id": "tarea_tiempo_real_001",
                "alimento_id": "A1"
            }
            response = self.session.post(f"{self.base_url}/tareas", params=params)
            self.print_response(response, "POST /tareas - Crear tarea para A1 (Fruta)")
            
            if response.status_code == 200:
                tarea_data = response.json()
                print(f"\nTarea creada: {tarea_data['id']}")
                print(f"Alimento: {tarea_data['alimento']['nombre']}")
                print(f"Hormigas necesarias: {tarea_data['alimento']['cantidad_hormigas_necesarias']}")
                print(f"Tiempo de recoleccion: {tarea_data['alimento']['tiempo_recoleccion']} segundos")
                print(f"Puntos de stock: {tarea_data['alimento']['puntos_stock']}")
                
                return tarea_data['id']
        except Exception as e:
            print(f"ERROR: {e}")
        return None
    
    def test_iniciar_tarea_tiempo_real(self, tarea_id: str):
        """Inicia una tarea con tiempo real."""
        self.print_header("INICIAR TAREA CON TIEMPO REAL")
        try:
            response = self.session.post(f"{self.base_url}/tareas/{tarea_id}/iniciar")
            self.print_response(response, f"POST /tareas/{tarea_id}/iniciar - Iniciar con timer")
            
            if response.status_code == 200:
                print(f"\nTarea {tarea_id} iniciada con timer en tiempo real!")
                print("La tarea se completara automaticamente en 5 minutos (300 segundos)")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_monitorear_tiempo_real(self, tarea_id: str):
        """Monitorea el progreso en tiempo real."""
        self.print_header("MONITOREO EN TIEMPO REAL")
        
        print(f"Monitoreando tarea {tarea_id}...")
        print("Presiona Ctrl+C para detener el monitoreo")
        
        try:
            for i in range(10):  # Monitorear por 10 iteraciones
                print(f"\n--- Iteracion {i+1} ---")
                
                # Obtener tiempo restante
                try:
                    response = self.session.get(f"{self.base_url}/tareas/{tarea_id}/tiempo-restante")
                    if response.status_code == 200:
                        tiempo_data = response.json()
                        print(f"Tiempo restante: {tiempo_data['tiempo_restante_segundos']} segundos")
                        print(f"Tiempo restante: {tiempo_data['tiempo_restante_minutos']} minutos")
                    else:
                        print("Tarea no encontrada o completada")
                        break
                except:
                    print("Error obteniendo tiempo restante")
                
                # Obtener progreso
                try:
                    response = self.session.get(f"{self.base_url}/tareas/{tarea_id}/progreso")
                    if response.status_code == 200:
                        progreso_data = response.json()
                        print(f"Progreso: {progreso_data['progreso_porcentaje']}%")
                    else:
                        print("Tarea no encontrada o completada")
                        break
                except:
                    print("Error obteniendo progreso")
                
                # Esperar 30 segundos
                print("Esperando 30 segundos...")
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\nMonitoreo detenido por el usuario")
    
    def test_tareas_en_proceso(self):
        """Lista tareas en proceso."""
        self.print_header("TAREAS EN PROCESO")
        try:
            response = self.session.get(f"{self.base_url}/tareas/en-proceso")
            self.print_response(response, "GET /tareas/en-proceso - Tareas con timer activo")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_estadisticas_tiempo_real(self):
        """Obtiene estadísticas en tiempo real."""
        self.print_header("ESTADISTICAS EN TIEMPO REAL")
        try:
            response = self.session.get(f"{self.base_url}/estadisticas")
            self.print_response(response, "GET /estadisticas - Estadisticas actualizadas")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_cancelar_tarea(self, tarea_id: str):
        """Cancela una tarea en proceso."""
        self.print_header("CANCELAR TAREA")
        try:
            response = self.session.post(f"{self.base_url}/tareas/{tarea_id}/cancelar")
            self.print_response(response, f"POST /tareas/{tarea_id}/cancelar - Cancelar tarea")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def run_demo_completa(self):
        """Ejecuta la demostración completa de tiempo real."""
        print("DEMOSTRACION DE SISTEMA DE TIEMPO REAL")
        print("Subsistema de Recoleccion - Universidad Cenfotec")
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
        
        # 1. Mostrar alimentos con IDs simplificados
        self.test_alimentos_simplificados()
        
        # 2. Crear tarea
        tarea_id = self.test_crear_tarea_tiempo_real()
        if not tarea_id:
            print("ERROR: No se pudo crear la tarea")
            return
        
        # 3. Iniciar tarea con tiempo real
        self.test_iniciar_tarea_tiempo_real(tarea_id)
        
        # 4. Mostrar tareas en proceso
        self.test_tareas_en_proceso()
        
        # 5. Monitorear progreso (opcional)
        print(f"\n¿Deseas monitorear el progreso en tiempo real? (s/n)")
        respuesta = input().lower()
        if respuesta == 's':
            self.test_monitorear_tiempo_real(tarea_id)
        
        # 6. Mostrar estadísticas
        self.test_estadisticas_tiempo_real()
        
        print(f"\n{'='*60}")
        print("DEMOSTRACION COMPLETADA")
        print("Sistema de tiempo real funcionando correctamente")
        print("Los estados cambian automaticamente segun el tiempo configurado")
        print(f"{'='*60}")

def main():
    """Función principal."""
    demo = DemoTiempoReal()
    demo.run_demo_completa()

if __name__ == "__main__":
    main()
