#!/usr/bin/env python3
"""
Script para ejecutar el Happy Path completo de las APIs.
Ejecuta todo el flujo desde crear alimento hasta verificar estadísticas.
"""

import sys
import time
import json
import requests
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


def print_step(num: int, message: str):
    """Imprime un paso del flujo."""
    print(f"\n{num}. {message}")
    print("-" * 50)


def print_success(message: str):
    """Imprime un mensaje de éxito."""
    print(f"   ✓ {message}")


def print_info(message: str):
    """Imprime información."""
    print(f"   ℹ {message}")


def print_error(message: str):
    """Imprime un error."""
    print(f"   ✗ ERROR: {message}")


def safe_request(method: str, url: str, json_data: dict = None):
    """Hace una petición HTTP con manejo de errores."""
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data)
        else:
            raise ValueError(f"Método no soportado: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print_error(f"Error en petición: {str(e)}")
        if hasattr(e.response, 'text'):
            print_error(f"Response: {e.response.text}")
        raise


def main():
    """Función principal."""
    base_url = "http://localhost:8000"
    tiempo_recoleccion = 10  # Tiempo en segundos para pruebas rápidas
    
    print("=" * 60)
    print("Happy Path - Flujo Completo de APIs")
    print("=" * 60)
    print(f"Base URL: {base_url}")
    print(f"Tiempo de recolección: {tiempo_recoleccion} segundos")
    
    try:
        # 1. Health Check
        print_step(1, "Verificando salud del servicio")
        health = safe_request("GET", f"{base_url}/health")
        print_success(f"Status: {health.get('status')}")
        
        # 2. Crear Alimento
        print_step(2, "Creando alimento")
        alimento_data = {
            "nombre": "Fruta Tropical",
            "cantidad_hormigas_necesarias": 2,
            "puntos_stock": 15,
            "tiempo_recoleccion": tiempo_recoleccion,
            "disponible": True
        }
        alimento = safe_request("POST", f"{base_url}/alimentos", alimento_data)
        alimento_id = alimento.get("id")
        print_success(f"Alimento creado: {alimento_id} - {alimento.get('nombre')}")
        print_info(f"Requiere {alimento.get('cantidad_hormigas_necesarias')} hormigas")
        print_info(f"Tiempo de recolección: {alimento.get('tiempo_recoleccion')} segundos")
        
        # 3. Consultar Alimentos
        print_step(3, "Consultando alimentos disponibles")
        alimentos = safe_request("GET", f"{base_url}/alimentos?estado=disponible")
        print_success(f"Total alimentos disponibles: {len(alimentos)}")
        
        # 4. Crear Tarea
        print_step(4, "Creando tarea de recolección")
        tarea_data = {
            "tarea_id": "T1001",
            "alimento_id": alimento_id
        }
        tarea = safe_request("POST", f"{base_url}/tareas", tarea_data)
        tarea_id = tarea.get("id")
        print_success(f"Tarea creada: {tarea_id}")
        print_info(f"Estado inicial: {tarea.get('estado')}")
        
        # 5. Asignar Hormigas
        print_step(5, "Asignando hormigas a la tarea")
        asignar_data = {
            "hormigas_lote_id": "LOTE_001",
            "cantidad": 2
        }
        asignacion = safe_request("POST", f"{base_url}/tareas/{tarea_id}/asignar-hormigas", asignar_data)
        print_success(f"Hormigas asignadas: {asignacion.get('hormigas_asignadas')}")
        print_info(f"Hormigas requeridas: {asignacion.get('hormigas_requeridas')}")
        print_success(f"Estado: {asignacion.get('estado')}")
        iniciada = asignacion.get('iniciada', False)
        print_success(f"Iniciada automáticamente: {iniciada}")
        
        # 6. Iniciar Tarea (solo si no se inició automáticamente)
        if not iniciada:
            print_step(6, "Iniciando la tarea")
            iniciar_data = {
                "hormigas_lote_id": "LOTE_001"
            }
            inicio = safe_request("POST", f"{base_url}/tareas/{tarea_id}/iniciar", iniciar_data)
            print_success("Tarea iniciada exitosamente")
            print_success(f"Estado: {inicio.get('estado')}")
        else:
            print_step(6, "Tarea ya iniciada automáticamente, saltando paso de inicio")
        
        # 7. Verificar Estado
        print_step(7, "Verificando estado de la tarea")
        status = safe_request("GET", f"{base_url}/tareas/{tarea_id}/status")
        print_success(f"Estado: {status.get('estado')}")
        print_info(f"Hormigas lote ID: {status.get('hormigas_lote_id')}")
        print_info(f"Inicio: {status.get('inicio')}")
        print_info(f"Fin: {status.get('fin')}")
        
        # 8. Monitorear Tiempo Restante
        print_step(8, "Monitoreando tiempo restante")
        try:
            tiempo = safe_request("GET", f"{base_url}/tareas/{tarea_id}/tiempo-restante")
            print_info(f"Tiempo total: {tiempo.get('tiempo_total_asignado_segundos')} segundos")
            print_success(f"Tiempo restante: {tiempo.get('tiempo_restante_segundos')} segundos")
            print_success(f"Progreso: {tiempo.get('progreso_porcentaje')}%")
        except Exception as e:
            print_info("No se pudo obtener tiempo restante (puede que la tarea ya esté completada)")
        
        # 9. Esperar y verificar estado final
        print_step(9, "Esperando completado automático")
        wait_time = tiempo_recoleccion + 2
        print_info(f"Esperando {wait_time} segundos para que se complete la tarea...")
        time.sleep(wait_time)
        
        print_info("Verificando estado final...")
        status_final = safe_request("GET", f"{base_url}/tareas/{tarea_id}/status")
        print_success(f"Estado final: {status_final.get('estado')}")
        completada_auto = status_final.get('completada_automaticamente', False)
        print_success(f"Completada automáticamente: {completada_auto}")
        print_info(f"Inicio: {status_final.get('inicio')}")
        print_info(f"Fin: {status_final.get('fin')}")
        
        # 10. Consultar Todas las Tareas
        print_step(10, "Consultando todas las tareas")
        todas_tareas = safe_request("GET", f"{base_url}/tareas/status")
        print_success(f"Total tareas: {todas_tareas.get('total_tareas')}")
        print_success(f"Tareas completadas automáticamente: {todas_tareas.get('tareas_completadas_automaticamente')}")
        
        # 11. Estadísticas
        print_step(11, "Consultando estadísticas")
        stats = safe_request("GET", f"{base_url}/estadisticas")
        print_success(f"Tareas activas: {stats.get('tareas_activas')}")
        print_success(f"Tareas completadas: {stats.get('tareas_completadas')}")
        
        # Resumen
        print("\n" + "=" * 60)
        print("Happy Path Completado Exitosamente")
        print("=" * 60)
        print("\nResumen:")
        print(f"  - Alimento creado: {alimento_id}")
        print(f"  - Tarea creada: {tarea_id}")
        print(f"  - Estado final: {status_final.get('estado')}")
        print()
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR EN EL FLUJO")
        print("=" * 60)
        print_error(str(e))
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()


