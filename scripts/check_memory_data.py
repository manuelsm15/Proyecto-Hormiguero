"""
Script para verificar los datos almacenados en memoria mientras el servicio está ejecutándose.
"""

import requests
import json
from datetime import datetime

def check_memory_data():
    """Verifica los datos almacenados en memoria del servicio."""
    print("=== VERIFICANDO DATOS EN MEMORIA DEL SERVICIO ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Verificar que el servicio esté funcionando
        print("\n1. VERIFICANDO SERVICIO:")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"  OK - Servicio funcionando")
            print(f"  Status: {health_data.get('status', 'unknown')}")
            print(f"  Service: {health_data.get('service', 'unknown')}")
        else:
            print(f"  ERROR - Servicio no disponible (Status: {health_response.status_code})")
            return False
        
        # 2. Verificar alimentos en memoria
        print("\n2. ALIMENTOS EN MEMORIA:")
        alimentos_response = requests.get(f"{base_url}/alimentos", timeout=5)
        if alimentos_response.status_code == 200:
            alimentos = alimentos_response.json()
            print(f"  OK - {len(alimentos)} alimentos en memoria")
            for alimento in alimentos:
                print(f"    - {alimento['id']}: {alimento['nombre']} (Hormigas: {alimento['cantidad_hormigas_necesarias']})")
        else:
            print(f"  ERROR - No se pudieron obtener alimentos (Status: {alimentos_response.status_code})")
        
        # 3. Verificar tareas en memoria
        print("\n3. TAREAS EN MEMORIA:")
        tareas_response = requests.get(f"{base_url}/tareas", timeout=5)
        if tareas_response.status_code == 200:
            tareas = tareas_response.json()
            print(f"  OK - {len(tareas)} tareas en memoria")
            for tarea in tareas:
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento: {tarea['alimento']['id']})")
        else:
            print(f"  ERROR - No se pudieron obtener tareas (Status: {tareas_response.status_code})")
        
        # 4. Verificar tareas en proceso
        print("\n4. TAREAS EN PROCESO:")
        tareas_proceso_response = requests.get(f"{base_url}/tareas/en-proceso", timeout=5)
        if tareas_proceso_response.status_code == 200:
            tareas_proceso = tareas_proceso_response.json()
            print(f"  OK - {len(tareas_proceso)} tareas en proceso")
            for tarea in tareas_proceso:
                print(f"    - {tarea['id']}: {tarea['estado']}")
        else:
            print(f"  ERROR - No se pudieron obtener tareas en proceso (Status: {tareas_proceso_response.status_code})")
        
        # 5. Verificar tareas completadas
        print("\n5. TAREAS COMPLETADAS:")
        tareas_completadas_response = requests.get(f"{base_url}/tareas/completadas", timeout=5)
        if tareas_completadas_response.status_code == 200:
            tareas_completadas = tareas_completadas_response.json()
            print(f"  OK - {len(tareas_completadas)} tareas completadas")
            for tarea in tareas_completadas:
                print(f"    - {tarea['id']}: {tarea['estado']} (Alimento recolectado: {tarea['alimento_recolectado']})")
        else:
            print(f"  ERROR - No se pudieron obtener tareas completadas (Status: {tareas_completadas_response.status_code})")
        
        # 6. Verificar estadísticas
        print("\n6. ESTADÍSTICAS DEL SERVICIO:")
        stats_response = requests.get(f"{base_url}/estadisticas", timeout=5)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"  OK - Estadísticas obtenidas")
            print(f"    - Tareas activas: {stats.get('tareas_activas', 0)}")
            print(f"    - Tareas completadas: {stats.get('tareas_completadas', 0)}")
            print(f"    - Alimentos disponibles: {stats.get('alimentos_disponibles', 0)}")
        else:
            print(f"  ERROR - No se pudieron obtener estadísticas (Status: {stats_response.status_code})")
        
        return True
        
    except Exception as e:
        print(f"ERROR - No se pudo conectar al servicio: {e}")
        return False

def show_memory_persistence():
    """Explica la persistencia en memoria."""
    print("\n=== PERSISTENCIA EN MEMORIA ===")
    print("""
    DATOS ALMACENADOS EN MEMORIA:
    ├── Tareas activas: List[TareaRecoleccion] en RecoleccionService
    ├── Tareas completadas: List[TareaRecoleccion] en RecoleccionService  
    ├── Alimentos: List[Alimento] en MockEntornoService
    ├── Mensajes: Dict[str, Mensaje] en MockComunicacionService
    └── Hormigas: Generadas dinámicamente según necesidad
    
    DURACIÓN:
    ├── Mientras el servicio esté ejecutándose: SÍ
    ├── Al reiniciar el servicio: NO (se pierden)
    ├── Al detener el servicio: NO (se pierden)
    └── Al cambiar de sesión: NO (se pierden)
    
    VENTAJAS:
    ├── Acceso inmediato a los datos
    ├── No requiere base de datos
    ├── Rendimiento óptimo
    └── Simplicidad de implementación
    
    DESVENTAJAS:
    ├── Datos se pierden al reiniciar
    ├── No hay historial persistente
    ├── No hay backup automático
    └── No hay recuperación de datos
    """)

def main():
    """Función principal."""
    print("VERIFICACIÓN DE DATOS EN MEMORIA DEL SERVICIO")
    
    # Verificar datos en memoria
    if check_memory_data():
        print("\nOK SERVICIO FUNCIONANDO - Datos disponibles en memoria")
    else:
        print("\nERROR SERVICIO NO DISPONIBLE - No se pueden verificar datos")
    
    # Explicar persistencia en memoria
    show_memory_persistence()
    
    print("\n=== RESUMEN ===")
    print("SÍ - Los datos se mantienen mientras el servicio esté ejecutándose")
    print("NO - Los datos se pierden al reiniciar o detener el servicio")

if __name__ == "__main__":
    main()
