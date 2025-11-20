"""
Demostración completa y funcional del subsistema de recolección.
Crea tareas, las procesa y muestra todo el flujo completo.
"""

import requests
import json
import time
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


def print_header(title: str):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_json(data: Any, indent: int = 2):
    """Imprime datos en formato JSON legible."""
    print(json.dumps(data, indent=indent, ensure_ascii=False))


def main():
    """Demostración completa del funcionamiento."""
    print_header("DEMOSTRACION COMPLETA DEL SUBSISTEMA DE RECOLECCION")
    
    print("\nSistema corriendo en:", BASE_URL)
    print("Documentacion interactiva:", f"{BASE_URL}/docs")
    
    # 1. VERIFICAR SALUD
    print_header("1. VERIFICAR ESTADO DEL SISTEMA")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print_json(response.json())
    except Exception as e:
        print(f"ERROR: No se puede conectar al servidor: {e}")
        return
    
    # 2. PROCESAR RECOLECCION (esto crea tareas y las procesa)
    print_header("2. PROCESAR RECOLECCION AUTOMATICA")
    print("Ejecutando proceso completo de recoleccion...")
    print("Este endpoint:")
    print("  - Consulta alimentos disponibles")
    print("  - Crea tareas de recoleccion")
    print("  - Solicita hormigas")
    print("  - Inicia la recoleccion")
    print("  - Completa las tareas")
    print("  - Devuelve hormigas con alimento")
    
    try:
        response = requests.post(f"{BASE_URL}/procesar")
        print(f"\nStatus: {response.status_code}")
        data = response.json()
        print_json(data)
        
        if data.get("tareas_procesadas", 0) > 0:
            print(f"\nEXITOSO: Se procesaron {data['tareas_procesadas']} tareas")
            print(f"Tareas creadas: {len(data.get('tareas', []))}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 3. VER TAREAS CREADAS
    print_header("3. TAREAS CREADAS")
    response = requests.get(f"{BASE_URL}/tareas")
    print(f"Status: {response.status_code}")
    tareas = response.json()
    print(f"Total de tareas: {len(tareas)}")
    
    if tareas:
        print("\nDetalles de tareas:")
        for tarea in tareas[:3]:  # Mostrar maximo 3
            print(f"\n  Tarea ID: {tarea.get('id', 'N/A')}")
            print(f"  Estado: {tarea.get('estado', 'N/A')}")
            print(f"  Alimento: {tarea.get('alimento', {}).get('nombre', 'N/A')}")
            print(f"  Hormigas asignadas: {len(tarea.get('hormigas_asignadas', []))}")
            print(f"  Alimento recolectado: {tarea.get('alimento_recolectado', 0)}")
    else:
        print("No hay tareas en memoria")
    
    # 4. TAREAS POR ESTADO
    print_header("4. TAREAS POR ESTADO")
    
    print("\nTareas Activas:")
    response = requests.get(f"{BASE_URL}/tareas/activas")
    activas = response.json()
    print(f"  Cantidad: {len(activas)}")
    
    print("\nTareas Completadas:")
    response = requests.get(f"{BASE_URL}/tareas/completadas")
    completadas = response.json()
    print(f"  Cantidad: {len(completadas)}")
    
    print("\nTareas en Proceso:")
    response = requests.get(f"{BASE_URL}/tareas/en-proceso")
    en_proceso = response.json()
    print(f"  Cantidad: {len(en_proceso)}")
    
    # 5. ESTADISTICAS COMPLETAS
    print_header("5. ESTADISTICAS DEL SISTEMA")
    response = requests.get(f"{BASE_URL}/estadisticas")
    stats = response.json()
    print_json(stats)
    
    # 6. EVENTOS RECIENTES
    print_header("6. EVENTOS DEL SISTEMA (Ultimos 10)")
    response = requests.get(f"{BASE_URL}/eventos?limite=10")
    eventos_data = response.json()
    eventos = eventos_data.get("eventos", [])
    print(f"Total de eventos: {eventos_data.get('total', 0)}")
    
    if eventos:
        print("\nUltimos eventos:")
        for evento in eventos[:5]:  # Mostrar 5
            print(f"\n  [{evento.get('fecha_evento', 'N/A')}]")
            print(f"  Tipo: {evento.get('tipo_evento', 'N/A')}")
            print(f"  Descripcion: {evento.get('descripcion', 'N/A')}")
    
    # 7. TAREAS EN BASE DE DATOS
    print_header("7. TAREAS PERSISTIDAS EN BASE DE DATOS")
    try:
        response = requests.get(f"{BASE_URL}/tareas/bd")
        tareas_bd = response.json()
        print(f"Tareas en BD: {len(tareas_bd)}")
        
        if tareas_bd:
            print("\nEjemplo de tarea desde BD:")
            print_json(tareas_bd[0])
    except Exception as e:
        print(f"Error consultando BD: {e}")
    
    # 8. VERIFICAR HORMIGAS
    print_header("8. VERIFICACION DE HORMIGAS")
    try:
        response = requests.post(f"{BASE_URL}/verificar-hormigas")
        print(f"Status: {response.status_code}")
        print_json(response.json())
    except Exception as e:
        print(f"Error: {e}")
    
    # 9. RESUMEN
    print_header("RESUMEN FINAL")
    print("\nEndpoints disponibles:")
    print(f"  GET  {BASE_URL}/                          - Endpoint raiz")
    print(f"  GET  {BASE_URL}/health                     - Estado del sistema")
    print(f"  GET  {BASE_URL}/alimentos                  - Listar alimentos")
    print(f"  GET  {BASE_URL}/alimentos?zona_id=1        - Filtrar por zona")
    print(f"  GET  {BASE_URL}/alimentos?estado=disponible - Filtrar por estado")
    print(f"  POST {BASE_URL}/tareas                     - Crear tarea")
    print(f"  GET  {BASE_URL}/tareas                     - Listar todas las tareas")
    print(f"  GET  {BASE_URL}/tareas/activas             - Tareas activas")
    print(f"  GET  {BASE_URL}/tareas/completadas         - Tareas completadas")
    print(f"  GET  {BASE_URL}/tareas/en-proceso          - Tareas en proceso")
    print(f"  GET  {BASE_URL}/tareas/bd                  - Tareas desde BD")
    print(f"  GET  {BASE_URL}/tareas/{{id}}/bd            - Tarea especifica desde BD")
    print(f"  POST {BASE_URL}/tareas/{{id}}/iniciar       - Iniciar tarea")
    print(f"  POST {BASE_URL}/tareas/{{id}}/completar     - Completar tarea")
    print(f"  POST {BASE_URL}/procesar                   - Proceso automatico completo")
    print(f"  GET  {BASE_URL}/estadisticas                - Estadisticas")
    print(f"  GET  {BASE_URL}/eventos                     - Eventos del sistema")
    print(f"  GET  {BASE_URL}/docs                       - Documentacion interactiva")
    
    print("\n" + "=" * 70)
    print("DEMOSTRACION COMPLETA")
    print("=" * 70)
    print(f"\nPara ver la documentacion interactiva, abre:")
    print(f"  {BASE_URL}/docs")
    print("\nAhí puedes probar todos los endpoints de forma interactiva!")


if __name__ == "__main__":
    main()



