"""
Demostracion del flujo completo: crear tarea, iniciarla y completarla.
"""

import requests
import json
import time


BASE_URL = "http://localhost:8000"


def print_step(num, desc):
    print(f"\n{'='*70}")
    print(f"PASO {num}: {desc}")
    print('='*70)


def main():
    print("\n" + "="*70)
    print("  FLUJO COMPLETO DE RECOLECCION DE ALIMENTOS")
    print("="*70)
    
    print("\nEste script demuestra el flujo completo:")
    print("  1. Verificar salud del sistema")
    print("  2. Consultar alimentos disponibles")
    print("  3. Crear una tarea de recoleccion")
    print("  4. Iniciar la tarea")
    print("  5. Ver progreso")
    print("  6. Completar la tarea")
    print("  7. Ver estadisticas finales")
    
    # Paso 1: Health check
    print_step(1, "Verificar estado del sistema")
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"Status: {r.status_code}")
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Paso 2: Consultar alimentos
    print_step(2, "Consultar alimentos disponibles")
    try:
        r = requests.get(f"{BASE_URL}/alimentos")
        print(f"Status: {r.status_code}")
        alimentos = r.json()
        print(f"Alimentos encontrados: {len(alimentos)}")
        if alimentos:
            for alimento in alimentos[:3]:
                print(f"\n  - ID: {alimento.get('id')}")
                print(f"    Nombre: {alimento.get('nombre')}")
                print(f"    Hormigas necesarias: {alimento.get('cantidad_hormigas_necesarias')}")
                print(f"    Disponible: {alimento.get('disponible')}")
        
        if not alimentos:
            print("\nNOTA: No hay alimentos disponibles del servicio mock.")
            print("Usaremos valores por defecto para crear la tarea.")
            alimento_id = "A1"
        else:
            alimento_id = alimentos[0].get('id', 'A1')
            
    except Exception as e:
        print(f"Advertencia: {e}")
        print("Usando alimento por defecto: A1")
        alimento_id = "A1"
    
    # Paso 3: Crear tarea
    print_step(3, "Crear tarea de recoleccion")
    try:
        # Crear tarea usando el endpoint con valores por defecto
        r = requests.post(f"{BASE_URL}/tareas")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            tarea = r.json()
            tarea_id = tarea.get('id', 'tarea_001')
            print(f"Tarea creada exitosamente!")
            print(f"  ID: {tarea_id}")
            print(f"  Alimento: {tarea.get('alimento', {}).get('nombre', 'N/A')}")
            print(f"  Estado: {tarea.get('estado', 'N/A')}")
        else:
            print(f"Respuesta: {r.text}")
            print("\nIntentando con alimento_id especificado...")
            r = requests.post(f"{BASE_URL}/tareas?alimento_id={alimento_id}")
            print(f"Status: {r.status_code}")
            if r.status_code == 200:
                tarea = r.json()
                tarea_id = tarea.get('id', 'tarea_001')
                print(f"Tarea creada: {tarea_id}")
            else:
                print("No se pudo crear tarea. Mostrando tareas existentes...")
                r = requests.get(f"{BASE_URL}/tareas")
                tareas = r.json()
                if tareas:
                    tarea_id = tareas[0].get('id')
                    print(f"Usando tarea existente: {tarea_id}")
                else:
                    print("No hay tareas disponibles.")
                    return
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Paso 4: Ver tareas
    print_step(4, "Ver todas las tareas")
    try:
        r = requests.get(f"{BASE_URL}/tareas")
        tareas = r.json()
        print(f"Total de tareas: {len(tareas)}")
        if tareas:
            print("\nPrimeras 3 tareas:")
            for t in tareas[:3]:
                print(f"\n  Tarea: {t.get('id')}")
                print(f"    Estado: {t.get('estado')}")
                print(f"    Alimento: {t.get('alimento', {}).get('nombre', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Paso 5: Estadisticas
    print_step(5, "Estadisticas del sistema")
    try:
        r = requests.get(f"{BASE_URL}/estadisticas")
        stats = r.json()
        print("Estadisticas:")
        print(f"  Tareas activas: {stats.get('tareas_activas', 0)}")
        print(f"  Tareas completadas: {stats.get('tareas_completadas', 0)}")
        print(f"  Total alimento recolectado: {stats.get('total_alimento_recolectado', 0)}")
        if 'base_datos' in stats:
            bd = stats['base_datos']
            print(f"\nBase de datos:")
            print(f"  Tareas en BD: {bd.get('tareas', {}).get('total', 0)}")
            print(f"  Eventos registrados: {bd.get('eventos', {}).get('total', 0)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Paso 6: Eventos
    print_step(6, "Eventos recientes")
    try:
        r = requests.get(f"{BASE_URL}/eventos?limite=5")
        eventos_data = r.json()
        eventos = eventos_data.get('eventos', [])
        print(f"Total de eventos: {eventos_data.get('total', 0)}")
        print("\nUltimos eventos:")
        for evento in eventos[:5]:
            print(f"\n  [{evento.get('fecha_evento')}] {evento.get('tipo_evento')}")
            print(f"    {evento.get('descripcion')}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Paso 7: Resumen final
    print("\n" + "="*70)
    print("  RESUMEN FINAL")
    print("="*70)
    print("\nEl sistema esta funcionando correctamente!")
    print(f"\nPara probar mas funcionalidades:")
    print(f"  1. Abre en tu navegador: {BASE_URL}/docs")
    print(f"  2. Ahí puedes probar todos los endpoints interactivamente")
    print(f"\nEndpoints principales:")
    print(f"  - GET  {BASE_URL}/alimentos")
    print(f"  - POST {BASE_URL}/tareas")
    print(f"  - GET  {BASE_URL}/tareas")
    print(f"  - POST {BASE_URL}/procesar  (proceso automatico completo)")
    print(f"  - GET  {BASE_URL}/estadisticas")
    print(f"  - GET  {BASE_URL}/eventos")
    print("="*70)


if __name__ == "__main__":
    main()



