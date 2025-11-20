"""
Script de demostración del funcionamiento completo del subsistema de recolección.
"""

import requests
import json
import time
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """Imprime una sección con formato."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_response(response: requests.Response, description: str):
    """Imprime la respuesta de una petición."""
    print(f"{description}:")
    print(f"  Status: {response.status_code}")
    if response.status_code < 400:
        try:
            data = response.json()
            print(f"  Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        except:
            print(f"  Response: {response.text}")
    else:
        print(f"  Error: {response.text}")
    print()


def main():
    """Función principal de demostración."""
    print_section("DEMOSTRACION COMPLETA DEL SUBSISTEMA DE RECOLECCION")
    
    # 1. HEALTH CHECK
    print_section("1. VERIFICACION DE SALUD")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response(response, "Health Check")
    except Exception as e:
        print(f"ERROR: No se pudo conectar al servidor: {e}")
        print("Asegurate de que el servidor este corriendo: python main.py")
        return
    
    # 2. ENDPOINT RAIZ
    print_section("2. ENDPOINT RAIZ")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Endpoint Raiz")
    
    # 3. CONSULTAR ALIMENTOS
    print_section("3. CONSULTAR ALIMENTOS DISPONIBLES")
    try:
        response = requests.get(f"{BASE_URL}/alimentos")
        print_response(response, "Alimentos Disponibles")
    except Exception as e:
        print(f"Error: {e}")
    
    # 4. CREAR TAREA
    print_section("4. CREAR TAREA DE RECOLECCION")
    try:
        response = requests.post(f"{BASE_URL}/tareas")
        print_response(response, "Crear Tarea (con valores por defecto)")
    except Exception as e:
        print(f"Error: {e}")
    
    # 5. LISTAR TAREAS
    print_section("5. LISTAR TODAS LAS TAREAS")
    response = requests.get(f"{BASE_URL}/tareas")
    print_response(response, "Todas las Tareas")
    
    # 6. TAREAS ACTIVAS
    print_section("6. TAREAS ACTIVAS")
    response = requests.get(f"{BASE_URL}/tareas/activas")
    print_response(response, "Tareas Activas")
    
    # 7. TAREAS COMPLETADAS
    print_section("7. TAREAS COMPLETADAS")
    response = requests.get(f"{BASE_URL}/tareas/completadas")
    print_response(response, "Tareas Completadas")
    
    # 8. ESTADISTICAS
    print_section("8. ESTADISTICAS DEL SISTEMA")
    response = requests.get(f"{BASE_URL}/estadisticas")
    print_response(response, "Estadisticas")
    
    # 9. EVENTOS
    print_section("9. EVENTOS RECIENTES")
    response = requests.get(f"{BASE_URL}/eventos?limite=10")
    print_response(response, "Eventos Recientes (ultimos 10)")
    
    # 10. TAREAS DESDE BASE DE DATOS
    print_section("10. TAREAS DESDE BASE DE DATOS")
    try:
        response = requests.get(f"{BASE_URL}/tareas/bd")
        print_response(response, "Tareas desde BD")
    except Exception as e:
        print(f"Error: {e}")
    
    # 11. PROCESAR RECOLECCION (AUTOMATICO)
    print_section("11. PROCESAR RECOLECCION AUTOMATICA")
    print("Este endpoint ejecuta el proceso completo de recoleccion...")
    try:
        response = requests.post(f"{BASE_URL}/procesar")
        print_response(response, "Procesar Recoleccion")
        
        # Esperar un momento y ver estadisticas actualizadas
        print("\nEsperando 2 segundos para ver cambios...")
        time.sleep(2)
        
        response = requests.get(f"{BASE_URL}/estadisticas")
        print_response(response, "Estadisticas Actualizadas")
    except Exception as e:
        print(f"Error: {e}")
    
    # 12. DOCUMENTACION
    print_section("12. DOCUMENTACION INTERACTIVA")
    print(f"Para ver la documentacion completa, abre en tu navegador:")
    print(f"  {BASE_URL}/docs")
    print(f"\nPara ver el esquema OpenAPI:")
    print(f"  {BASE_URL}/openapi.json")
    
    print_section("DEMOSTRACION COMPLETA")
    print("Todos los endpoints han sido probados!")
    print(f"El servidor esta corriendo en: {BASE_URL}")
    print(f"Documentacion interactiva: {BASE_URL}/docs")


if __name__ == "__main__":
    main()



