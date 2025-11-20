"""
Script para probar todos los métodos GET y POST de la API.
Permite probar contra localhost o Railway.
"""

import requests
import json
import sys
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"  # Cambiar por tu URL de Railway si es necesario

# Colores para terminal (Windows compatible)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}[ERROR] {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}[INFO] {text}{Colors.RESET}")

def print_response(response):
    try:
        data = response.json()
        print(f"{Colors.YELLOW}Respuesta:{Colors.RESET}")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(f"{Colors.YELLOW}Respuesta (texto):{Colors.RESET}")
        print(response.text)

def test_get_endpoint(method, endpoint, description, params=None):
    """Prueba un endpoint GET."""
    print(f"\n{Colors.BOLD}GET {endpoint}{Colors.RESET}")
    print(f"  {description}")
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print_success(f"Status: {response.status_code}")
            print_response(response)
            return response
        else:
            print_error(f"Status: {response.status_code}")
            print_response(response)
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_post_endpoint(method, endpoint, description, data=None, params=None):
    """Prueba un endpoint POST."""
    print(f"\n{Colors.BOLD}POST {endpoint}{Colors.RESET}")
    print(f"  {description}")
    try:
        url = f"{BASE_URL}{endpoint}"
        if data:
            response = requests.post(url, json=data, params=params, timeout=30)
        else:
            response = requests.post(url, params=params, timeout=30)
        
        if response.status_code in [200, 201]:
            print_success(f"Status: {response.status_code}")
            print_response(response)
            return response
        else:
            print_error(f"Status: {response.status_code}")
            print_response(response)
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def main():
    # Preguntar URL si se pasa como argumento
    if len(sys.argv) > 1:
        global BASE_URL
        BASE_URL = sys.argv[1]
    
    print_header(f"PRUEBAS GET y POST - {BASE_URL}")
    print_info(f"URL Base: {BASE_URL}")
    print_info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Variables para almacenar IDs creados
    tarea_id = None
    alimento_id = None
    
    # ===========================================
    # PRUEBAS GET
    # ===========================================
    print_header("PRUEBAS GET - ENDPOINTS DE CONSULTA")
    
    # 1. Health Check
    test_get_endpoint("GET", "/health", "Verificación de salud del servicio")
    
    # 2. Root
    test_get_endpoint("GET", "/", "Información del subsistema")
    
    # 3. Alimentos disponibles
    print_info("Consulta sin filtros:")
    alimentos_response = test_get_endpoint("GET", "/alimentos", "Listar alimentos disponibles")
    
    # 3.1. Alimentos con filtro zona_id
    print_info("Consulta con filtro zona_id=1:")
    test_get_endpoint("GET", "/alimentos", "Alimentos por zona", params={"zona_id": 1})
    
    # 3.2. Alimentos con filtro estado
    print_info("Consulta con filtro estado=disponible:")
    test_get_endpoint("GET", "/alimentos", "Alimentos por estado", params={"estado": "disponible"})
    
    # 4. Listar todas las tareas
    tareas_response = test_get_endpoint("GET", "/tareas", "Listar todas las tareas (activas + completadas)")
    
    # 5. Tareas activas
    test_get_endpoint("GET", "/tareas/activas", "Listar tareas activas")
    
    # 6. Tareas completadas
    test_get_endpoint("GET", "/tareas/completadas", "Listar tareas completadas")
    
    # 7. Tareas en proceso
    test_get_endpoint("GET", "/tareas/en-proceso", "Listar tareas en proceso")
    
    # 8. Estadísticas
    test_get_endpoint("GET", "/estadisticas", "Obtener estadísticas del servicio")
    
    # 9. Tareas desde BD
    test_get_endpoint("GET", "/tareas/bd", "Obtener tareas desde base de datos")
    
    # 10. Eventos
    test_get_endpoint("GET", "/eventos", "Obtener eventos recientes", params={"limite": 10})
    
    # ===========================================
    # PRUEBAS POST - CREACIÓN Y ACCIONES
    # ===========================================
    print_header("PRUEBAS POST - CREACIÓN Y MODIFICACIÓN")
    
    # 1. Crear tarea (sin parámetros, usa defaults)
    print_info("Creando tarea con valores por defecto...")
    crear_response = test_post_endpoint("POST", "/tareas", "Crear nueva tarea de recolección")
    
    if crear_response and crear_response.status_code == 200:
        try:
            tarea_data = crear_response.json()
            tarea_id = tarea_data.get("id")
            if tarea_data.get("alimento"):
                alimento_id = tarea_data["alimento"].get("id")
            print_success(f"Tarea creada: ID = {tarea_id}, Alimento = {alimento_id}")
        except:
            pass
    
    # 2. Crear tarea con parámetros específicos
    print_info("Creando tarea con parámetros específicos...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tarea_id_custom = f"tarea_test_{timestamp}"
    crear_response2 = test_post_endpoint(
        "POST", 
        "/tareas", 
        "Crear tarea con ID y alimento específicos",
        params={"tarea_id": tarea_id_custom, "alimento_id": "A1"}
    )
    
    if crear_response2 and crear_response2.status_code == 200:
        try:
            tarea_data = crear_response2.json()
            tarea_id = tarea_data.get("id") or tarea_id_custom
            print_success(f"Tarea personalizada creada: ID = {tarea_id}")
        except:
            tarea_id = tarea_id_custom
    
    # 3. Iniciar tarea
    if tarea_id:
        test_post_endpoint("POST", f"/tareas/{tarea_id}/iniciar", f"Iniciar tarea {tarea_id}")
        
        # 3.1. Obtener tiempo restante (GET pero relacionado)
        test_get_endpoint("GET", f"/tareas/{tarea_id}/tiempo-restante", f"Tiempo restante de tarea {tarea_id}")
        
        # 3.2. Obtener progreso (GET pero relacionado)
        test_get_endpoint("GET", f"/tareas/{tarea_id}/progreso", f"Progreso de tarea {tarea_id}")
    else:
        print_error("No se pudo obtener tarea_id, saltando prueba de iniciar")
    
    # 4. Procesar recolección (proceso completo)
    print_info("Ejecutando proceso completo de recolección...")
    test_post_endpoint("POST", "/procesar", "Ejecutar proceso completo de recolección")
    
    # 5. Verificar hormigas muertas
    test_post_endpoint("POST", "/verificar-hormigas", "Verificar y manejar hormigas muertas")
    
    # 6. Completar tarea (necesita cantidad_recolectada)
    if tarea_id:
        print_info(f"Intentando completar tarea {tarea_id} con cantidad 10...")
        # Nota: Este endpoint requiere cantidad_recolectada como query param
        test_post_endpoint(
            "POST", 
            f"/tareas/{tarea_id}/completar", 
            f"Completar tarea {tarea_id}",
            params={"cantidad_recolectada": 10}
        )
    else:
        print_error("No se pudo obtener tarea_id, saltando prueba de completar")
    
    # 7. Obtener tarea específica desde BD (GET pero relacionado con POST)
    if tarea_id:
        test_get_endpoint("GET", f"/tareas/{tarea_id}/bd", f"Obtener tarea {tarea_id} desde BD")
    
    # ===========================================
    # RESUMEN FINAL
    # ===========================================
    print_header("VERIFICACIÓN FINAL")
    
    # Verificar estado final
    print_info("Consultando estado final después de todas las operaciones:")
    test_get_endpoint("GET", "/tareas", "Tareas finales")
    test_get_endpoint("GET", "/estadisticas", "Estadísticas finales")
    test_get_endpoint("GET", "/eventos", "Eventos recientes", params={"limite": 5})
    
    print_header("PRUEBAS COMPLETADAS")
    print_success("Todas las pruebas GET y POST se han ejecutado")
    print_info(f"Base URL utilizada: {BASE_URL}")
    print_info(f"Para ver la documentación interactiva: {BASE_URL}/docs")

if __name__ == "__main__":
    main()

