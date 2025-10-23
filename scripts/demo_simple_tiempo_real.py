#!/usr/bin/env python3
"""
Script de demostración simple del sistema de tiempo real.
"""

import requests
import json
import time

def test_alimentos_simplificados():
    """Prueba los alimentos con IDs simplificados."""
    print("\n" + "="*60)
    print(">>> ALIMENTOS CON IDs SIMPLIFICADOS")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8000/alimentos")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        # Mostrar resumen
        alimentos = response.json()
        print(f"\nResumen de Alimentos:")
        for alimento in alimentos:
            print(f"- {alimento['id']}: {alimento['nombre']} - {alimento['puntos_stock']} puntos - {alimento['tiempo_recoleccion']}s - {alimento['cantidad_hormigas_necesarias']} hormigas")
        
    except Exception as e:
        print(f"ERROR: {e}")

def test_procesar_automatico():
    """Prueba el procesamiento automático con tiempo real."""
    print("\n" + "="*60)
    print(">>> PROCESAMIENTO AUTOMATICO CON TIEMPO REAL")
    print("="*60)
    
    try:
        print("Iniciando procesamiento automatico...")
        response = requests.post("http://localhost:8000/procesar")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        # Mostrar resumen del procesamiento
        data = response.json()
        print(f"\nResumen del Procesamiento:")
        print(f"- Tareas procesadas: {data.get('tareas_procesadas', 0)}")
        print(f"- Total de tareas: {len(data.get('tareas', []))}")
        
        for tarea in data.get('tareas', []):
            print(f"  * {tarea['id']}: {tarea['alimento']['nombre']} - {tarea['alimento_recolectado']} puntos recolectados")
        
    except Exception as e:
        print(f"ERROR: {e}")

def test_estadisticas_tiempo_real():
    """Obtiene estadísticas en tiempo real."""
    print("\n" + "="*60)
    print(">>> ESTADISTICAS EN TIEMPO REAL")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8000/estadisticas")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"ERROR: {e}")

def test_tareas_en_proceso():
    """Lista tareas en proceso."""
    print("\n" + "="*60)
    print(">>> TAREAS EN PROCESO")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8000/tareas/en-proceso")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"ERROR: {e}")

def test_crear_tarea_manual():
    """Crea una tarea manualmente."""
    print("\n" + "="*60)
    print(">>> CREAR TAREA MANUAL")
    print("="*60)
    
    try:
        # Crear tarea para A2 (Semilla - 3 minutos)
        params = {
            "tarea_id": "tarea_manual_001",
            "alimento_id": "A2"
        }
        response = requests.post("http://localhost:8000/tareas", params=params)
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            tarea_data = response.json()
            print(f"\nTarea creada exitosamente:")
            print(f"- ID: {tarea_data['id']}")
            print(f"- Alimento: {tarea_data['alimento']['nombre']}")
            print(f"- Hormigas necesarias: {tarea_data['alimento']['cantidad_hormigas_necesarias']}")
            print(f"- Tiempo de recoleccion: {tarea_data['alimento']['tiempo_recoleccion']} segundos")
            print(f"- Puntos de stock: {tarea_data['alimento']['puntos_stock']}")
        
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    """Función principal."""
    print("DEMOSTRACION DE SISTEMA DE TIEMPO REAL")
    print("Subsistema de Recoleccion - Universidad Cenfotec")
    print("="*60)
    
    # Verificar conectividad
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("OK: Conexion exitosa con la API")
        else:
            print("ERROR: Error de conexion")
            return
    except Exception as e:
        print(f"ERROR: No se puede conectar a http://localhost:8000")
        print("Asegurate de que la aplicacion este ejecutandose con: python main.py")
        return
    
    # Ejecutar pruebas
    test_alimentos_simplificados()
    test_crear_tarea_manual()
    test_procesar_automatico()
    test_tareas_en_proceso()
    test_estadisticas_tiempo_real()
    
    print("\n" + "="*60)
    print("DEMOSTRACION COMPLETADA")
    print("Sistema de tiempo real funcionando correctamente")
    print("Los estados cambian automaticamente segun el tiempo configurado")
    print("IDs simplificados: A1, A2, A3")
    print("="*60)

if __name__ == "__main__":
    main()

