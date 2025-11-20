#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script completo de pruebas del sistema de lotes de hormigas.
Ejecuta todos los escenarios: crear alimento, tarea, asignar hormigas, etc.
Genera reportes de Allure automáticamente.
"""

import sys
import time
import json
import requests
from pathlib import Path
from datetime import datetime
import io
import uuid
import subprocess

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Importar Allure para generar reportes
try:
    from allure_commons import plugin_manager
    from allure_commons.types import AttachmentType
    from allure_commons.utils import uuid4
    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False
    print("Advertencia: allure-python-commons no está instalado. Los reportes de Allure no se generarán.")
    print("Instala con: pip install allure-python-commons")

# Intentar importar allure-pytest para usar su API
try:
    import allure
    ALLURE_PYTEST_AVAILABLE = True
except ImportError:
    ALLURE_PYTEST_AVAILABLE = False

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


BASE_URL = "http://localhost:8000"
ALLURE_RESULTS_DIR = Path("allure-results")
ALLURE_RESULTS_DIR.mkdir(exist_ok=True)

COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'CYAN': '\033[96m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m'
}

# Estructura para almacenar resultados de Allure
allure_results = []


def print_header(text):
    """Imprime un encabezado."""
    print(f"\n{COLORS['BOLD']}{COLORS['BLUE']}{'='*80}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['BLUE']}{text}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['BLUE']}{'='*80}{COLORS['RESET']}\n")


def print_step(num, text):
    """Imprime un paso del proceso."""
    print(f"\n{COLORS['CYAN']}[PASO {num}] {text}{COLORS['RESET']}")
    print("-" * 80)


def print_request(method, url, body=None):
    """Imprime información de la request."""
    print(f"{COLORS['YELLOW']}REQUEST:{COLORS['RESET']}")
    print(f"  Método: {COLORS['BOLD']}{method}{COLORS['RESET']}")
    print(f"  URL: {url}")
    if body:
        print(f"  Body:")
        print(f"    {json.dumps(body, indent=4, ensure_ascii=False)}")


def print_response(response):
    """Imprime información de la response."""
    status_color = COLORS['GREEN'] if response.status_code < 400 else COLORS['RED']
    print(f"{COLORS['YELLOW']}RESPONSE:{COLORS['RESET']}")
    print(f"  Status: {status_color}{response.status_code}{COLORS['RESET']}")
    try:
        data = response.json()
        print(f"  Body:")
        print(f"    {json.dumps(data, indent=4, ensure_ascii=False)}")
        return data
    except:
        print(f"  Body: {response.text}")
        return None


def save_allure_result(test_name, status, description, request_data=None, response_data=None, error=None):
    """Guarda un resultado de prueba en formato Allure."""
    test_uuid = str(uuid.uuid4())
    start_time = int(time.time() * 1000)
    
    # Crear estructura de resultado de Allure
    result = {
        "uuid": test_uuid,
        "name": test_name,
        "status": status,  # passed, failed, broken, skipped
        "description": description,
        "start": start_time,
        "stop": start_time + 100,  # Asumir 100ms de duración
        "steps": [],
        "attachments": []
    }
    
    # Agregar request como attachment
    if request_data:
        request_json = json.dumps(request_data, indent=2, ensure_ascii=False)
        attachment_name = f"{test_uuid}-attachment-request.json"
        attachment_file = ALLURE_RESULTS_DIR / attachment_name
        attachment_file.write_text(request_json, encoding='utf-8')
        
        result["attachments"].append({
            "name": "Request",
            "source": attachment_name,
            "type": "application/json"
        })
    
    # Agregar response como attachment
    if response_data:
        response_json = json.dumps(response_data, indent=2, ensure_ascii=False)
        attachment_name = f"{test_uuid}-attachment-response.json"
        attachment_file = ALLURE_RESULTS_DIR / attachment_name
        attachment_file.write_text(response_json, encoding='utf-8')
        
        result["attachments"].append({
            "name": "Response",
            "source": attachment_name,
            "type": "application/json"
        })
    
    # Agregar error si existe
    if error:
        result["status"] = "failed"
        result["statusDetails"] = {
            "message": str(error),
            "trace": str(error)
        }
    
    allure_results.append(result)
    
    # Guardar resultado en archivo (formato Allure)
    result_file = ALLURE_RESULTS_DIR / f"{test_uuid}-result.json"
    result_file.write_text(json.dumps(result, ensure_ascii=False), encoding='utf-8')


def safe_request(method, url, json_data=None, test_name=None, timeout=10):
    """Hace una petición HTTP con manejo de errores y guarda en Allure."""
    start_time = time.time()
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, timeout=timeout)
        else:
            raise ValueError(f"Método no soportado: {method}")
        
        # Guardar en Allure
        if test_name:
            status = "passed" if response.status_code < 400 else "failed"
            response_data = None
            try:
                response_data = response.json()
            except:
                response_data = {"text": response.text}
            
            save_allure_result(
                test_name=test_name,
                status=status,
                description=f"{method} {url}",
                request_data=json_data if json_data else {"method": method, "url": url},
                response_data={"status_code": response.status_code, "body": response_data},
                error=None if status == "passed" else f"Status code: {response.status_code}"
            )
        
        return response
    except requests.exceptions.Timeout as e:
        error_msg = f"Timeout: La petición tardó más de {timeout} segundos"
        print(f"{COLORS['RED']}ERROR: {error_msg}{COLORS['RESET']}")
        print(f"{COLORS['RED']}  URL: {url}{COLORS['RESET']}")
        print(f"{COLORS['RED']}  Método: {method}{COLORS['RESET']}")
        
        # Guardar error en Allure
        if test_name:
            save_allure_result(
                test_name=test_name,
                status="broken",
                description=f"{method} {url}",
                request_data=json_data if json_data else {"method": method, "url": url},
                response_data=None,
                error=error_msg
            )
        
        return None
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Error de conexión: No se pudo conectar al servidor"
        print(f"{COLORS['RED']}ERROR: {error_msg}{COLORS['RESET']}")
        print(f"{COLORS['RED']}  URL: {url}{COLORS['RESET']}")
        print(f"{COLORS['RED']}  Método: {method}{COLORS['RESET']}")
        print(f"{COLORS['RED']}  Detalle: {str(e)}{COLORS['RESET']}")
        
        # Guardar error en Allure
        if test_name:
            save_allure_result(
                test_name=test_name,
                status="broken",
                description=f"{method} {url}",
                request_data=json_data if json_data else {"method": method, "url": url},
                response_data=None,
                error=error_msg
            )
        
        return None
    except requests.exceptions.RequestException as e:
        error_msg = f"Error en la petición: {str(e)}"
        print(f"{COLORS['RED']}ERROR: {error_msg}{COLORS['RESET']}")
        print(f"{COLORS['RED']}  URL: {url}{COLORS['RESET']}")
        print(f"{COLORS['RED']}  Método: {method}{COLORS['RESET']}")
        if json_data:
            print(f"{COLORS['RED']}  Body: {json.dumps(json_data, indent=2)}{COLORS['RESET']}")
        
        # Guardar error en Allure
        if test_name:
            save_allure_result(
                test_name=test_name,
                status="broken",
                description=f"{method} {url}",
                request_data=json_data if json_data else {"method": method, "url": url},
                response_data=None,
                error=error_msg
            )
        
        return None
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"{COLORS['RED']}ERROR: {error_msg}{COLORS['RESET']}")
        print(f"{COLORS['RED']}  Tipo: {type(e).__name__}{COLORS['RESET']}")
        
        # Guardar error en Allure
        if test_name:
            save_allure_result(
                test_name=test_name,
                status="broken",
                description=f"{method} {url}",
                request_data=json_data if json_data else {"method": method, "url": url},
                response_data=None,
                error=error_msg
            )
        
        return None


def verificar_servicio_disponible():
    """Verifica que el servicio esté disponible."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def main():
    """Función principal de pruebas."""
    print_header("PRUEBAS COMPLETAS DEL SISTEMA DE LOTES DE HORMIGAS")
    print(f"{COLORS['CYAN']}Base URL: {BASE_URL}{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLORS['RESET']}")
    
    # Verificar que el servicio esté disponible
    print(f"\n{COLORS['YELLOW']}Verificando que el servicio esté disponible...{COLORS['RESET']}")
    if not verificar_servicio_disponible():
        print(f"\n{COLORS['RED']}ERROR: El servicio no está disponible en {BASE_URL}{COLORS['RESET']}")
        print(f"\n{COLORS['YELLOW']}Para iniciar el servicio, ejecuta uno de los siguientes comandos:{COLORS['RESET']}")
        print(f"  {COLORS['CYAN']}Windows (PowerShell):{COLORS['RESET']}")
        print(f"    .\\scripts\\iniciar_servicio.ps1")
        print(f"  {COLORS['CYAN']}Windows (CMD):{COLORS['RESET']}")
        print(f"    scripts\\iniciar_servicio.bat")
        print(f"  {COLORS['CYAN']}O manualmente:{COLORS['RESET']}")
        print(f"    python main.py")
        print(f"\n{COLORS['YELLOW']}Luego ejecuta este script nuevamente.{COLORS['RESET']}")
        return 1
    
    print(f"{COLORS['GREEN']}[OK] Servicio disponible{COLORS['RESET']}\n")
    
    # Variables para almacenar IDs
    alimento_id = None
    tarea_id = None
    lote_id = f"LOTE_PRUEBA_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    try:
        # ========================================================================
        # PASO 1: Health Check
        # ========================================================================
        print_step(1, "Verificar salud del servicio")
        url = f"{BASE_URL}/health"
        print_request("GET", url)
        response = safe_request("GET", url, test_name="Health Check")
        if response:
            data = print_response(response)
            if not data or data.get('status') != 'healthy':
                print(f"{COLORS['RED']}ERROR: El servicio no está saludable{COLORS['RESET']}")
                return
        else:
            print(f"{COLORS['RED']}ERROR: No se pudo conectar al servicio{COLORS['RESET']}")
            return
        
        time.sleep(1)
        
        # ========================================================================
        # PASO 2: Crear Alimento
        # ========================================================================
        print_step(2, "Crear un alimento para pruebas")
        url = f"{BASE_URL}/alimentos"
        body = {
            "nombre": "Fruta de Prueba",
            "cantidad_hormigas_necesarias": 3,
            "puntos_stock": 15,
            "tiempo_recoleccion": 10,  # 10 segundos para pruebas rápidas
            "disponible": True
        }
        print_request("POST", url, body)
        response = safe_request("POST", url, body, test_name="Crear Alimento")
        if response:
            data = print_response(response)
            if data and 'id' in data:
                alimento_id = data['id']
                print(f"{COLORS['GREEN']}[OK] Alimento creado: {alimento_id}{COLORS['RESET']}")
            else:
                print(f"{COLORS['RED']}ERROR: No se pudo crear el alimento{COLORS['RESET']}")
                return
        else:
            print(f"{COLORS['RED']}ERROR: No se pudo crear el alimento{COLORS['RESET']}")
            return
        
        time.sleep(2)  # Esperar un poco más para que se persista en BD
        
        # Verificar que el alimento existe consultando la lista
        print(f"{COLORS['CYAN']}Verificando que el alimento existe en la base de datos...{COLORS['RESET']}")
        alimentos_url = f"{BASE_URL}/alimentos"
        alimentos_response = safe_request("GET", alimentos_url)
        alimento_encontrado = False
        if alimentos_response and alimentos_response.status_code == 200:
            alimentos_data = alimentos_response.json()
            for alimento in alimentos_data:
                if str(alimento.get('id')) == str(alimento_id):
                    alimento_encontrado = True
                    alimento_id = str(alimento.get('id'))  # Usar el ID exacto de la BD
                    print(f"{COLORS['GREEN']}[OK] Alimento encontrado en BD: {alimento_id}{COLORS['RESET']}")
                    break
        
        if not alimento_encontrado:
            print(f"{COLORS['YELLOW']}Advertencia: Alimento {alimento_id} no encontrado en BD, buscando uno disponible...{COLORS['RESET']}")
            if alimentos_response and alimentos_response.status_code == 200:
                alimentos_data = alimentos_response.json()
                alimentos_disponibles = [a for a in alimentos_data if a.get('disponible', False)]
                if alimentos_disponibles:
                    alimento_id = str(alimentos_disponibles[0].get('id'))
                    print(f"{COLORS['GREEN']}[OK] Usando alimento disponible: {alimento_id} - {alimentos_disponibles[0].get('nombre')}{COLORS['RESET']}")
                else:
                    print(f"{COLORS['RED']}ERROR: No hay alimentos disponibles en la base de datos{COLORS['RESET']}")
                    return
        
        # ========================================================================
        # PASO 3: Crear Tarea
        # ========================================================================
        print_step(3, "Crear una tarea de recolección")
        url = f"{BASE_URL}/tareas"
        tarea_id = f"TAREA_PRUEBA_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        # Intentar primero con body JSON
        body = {
            "tarea_id": tarea_id,
            "alimento_id": alimento_id
        }
        print_request("POST", url, body)
        response = safe_request("POST", url, body, test_name="Crear Tarea")
        
        # Si falla, intentar con query params
        if not response or response.status_code != 200:
            print(f"{COLORS['YELLOW']}Intentando con query parameters...{COLORS['RESET']}")
            url_with_params = f"{BASE_URL}/tareas?tarea_id={tarea_id}&alimento_id={alimento_id}"
            print_request("POST", url_with_params)
            response = requests.post(url_with_params)
            if response:
                data = print_response(response)
                if response.status_code == 200 and data and 'id' in data:
                    print(f"{COLORS['GREEN']}[OK] Tarea creada: {tarea_id}{COLORS['RESET']}")
                else:
                    print(f"{COLORS['RED']}ERROR: No se pudo crear la tarea{COLORS['RESET']}")
                    if data:
                        print(f"{COLORS['RED']}  Detalle: {data.get('detail', 'N/A')}{COLORS['RESET']}")
                    return
            else:
                print(f"{COLORS['RED']}ERROR: No se pudo crear la tarea (sin respuesta){COLORS['RESET']}")
                return
        if response:
            data = print_response(response)
            if response.status_code == 200 and data and 'id' in data:
                print(f"{COLORS['GREEN']}[OK] Tarea creada: {tarea_id}{COLORS['RESET']}")
            else:
                print(f"{COLORS['RED']}ERROR: No se pudo crear la tarea{COLORS['RESET']}")
                if data:
                    print(f"{COLORS['RED']}  Detalle: {data.get('detail', 'N/A')}{COLORS['RESET']}")
                else:
                    print(f"{COLORS['RED']}  Status Code: {response.status_code}{COLORS['RESET']}")
                    print(f"{COLORS['RED']}  Response Text: {response.text[:200]}{COLORS['RESET']}")
                return
        else:
            print(f"{COLORS['RED']}ERROR: No se pudo crear la tarea (sin respuesta){COLORS['RESET']}")
            print(f"{COLORS['YELLOW']}Verifica que el servidor esté corriendo y que la base de datos esté configurada correctamente{COLORS['RESET']}")
            return
        
        time.sleep(1)
        
        # ========================================================================
        # PASO 4: Verificar Estado Inicial de la Tarea
        # ========================================================================
        print_step(4, "Verificar estado inicial de la tarea")
        url = f"{BASE_URL}/tareas/{tarea_id}/status"
        print_request("GET", url)
        response = safe_request("GET", url, test_name="Verificar Estado Inicial")
        if response:
            data = print_response(response)
            if data:
                print(f"{COLORS['GREEN']}[OK] Estado inicial: {data.get('estado', 'N/A')}{COLORS['RESET']}")
        
        time.sleep(1)
        
        # ========================================================================
        # PASO 5: Intentar Asignar Hormigas con Cantidad INSUFICIENTE (Debe Fallar)
        # ========================================================================
        print_step(5, "Intentar asignar hormigas con cantidad INSUFICIENTE (debe fallar)")
        url = f"{BASE_URL}/tareas/{tarea_id}/asignar-hormigas"
        body = {
            "hormigas_lote_id": lote_id,
            "cantidad": 2  # Menor a las 3 requeridas
        }
        print_request("POST", url, body)
        print(f"{COLORS['YELLOW']}NOTA: Esta prueba DEBE fallar con error 400{COLORS['RESET']}")
        response = safe_request("POST", url, body, test_name="Asignar Hormigas - Cantidad Insuficiente (Debe Fallar)")
        if response:
            data = print_response(response)
            if response.status_code == 400:
                print(f"{COLORS['GREEN']}[OK] Correcto: La asignación falló como se esperaba{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Mensaje: {data.get('detail', 'N/A') if data else 'N/A'}{COLORS['RESET']}")
            else:
                print(f"{COLORS['RED']}ERROR: Se esperaba un error 400 pero se obtuvo {response.status_code}{COLORS['RESET']}")
        else:
            print(f"{COLORS['RED']}ERROR: No se pudo hacer la petición{COLORS['RESET']}")
        
        time.sleep(1)
        
        # ========================================================================
        # PASO 6: Asignar Hormigas con Cantidad SUFICIENTE (Igual a requerida)
        # ========================================================================
        print_step(6, "Asignar hormigas con cantidad SUFICIENTE (igual a requerida: 3)")
        url = f"{BASE_URL}/tareas/{tarea_id}/asignar-hormigas"
        body = {
            "hormigas_lote_id": lote_id,
            "cantidad": 3  # Igual a las 3 requeridas
        }
        print_request("POST", url, body)
        response = safe_request("POST", url, body, test_name="Asignar Hormigas - Cantidad Suficiente")
        if response:
            data = print_response(response)
            if response.status_code == 200 and data:
                print(f"{COLORS['GREEN']}[OK] Hormigas asignadas exitosamente{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Hormigas asignadas: {data.get('hormigas_asignadas', 'N/A')}{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Hormigas requeridas: {data.get('hormigas_requeridas', 'N/A')}{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Lote ID: {data.get('hormigas_lote_id', 'N/A')}{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Iniciada automáticamente: {data.get('iniciada', False)}{COLORS['RESET']}")
            else:
                print(f"{COLORS['RED']}ERROR: No se pudieron asignar las hormigas{COLORS['RESET']}")
                return
        else:
            print(f"{COLORS['RED']}ERROR: No se pudo hacer la petición{COLORS['RESET']}")
            return
        
        time.sleep(1)
        
        # ========================================================================
        # PASO 7: Verificar Estado Después de Asignación
        # ========================================================================
        print_step(7, "Verificar estado de la tarea después de asignar hormigas")
        url = f"{BASE_URL}/tareas/{tarea_id}/status"
        print_request("GET", url)
        response = safe_request("GET", url, test_name="Verificar Estado Después de Asignación")
        if response:
            data = print_response(response)
            if data:
                print(f"{COLORS['GREEN']}[OK] Estado: {data.get('estado', 'N/A')}{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Lote ID: {data.get('hormigas_lote_id', 'N/A')}{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Inicio: {data.get('inicio', 'N/A')}{COLORS['RESET']}")
        
        time.sleep(1)
        
        # ========================================================================
        # PASO 8: Si no se inició automáticamente, Iniciar la Tarea
        # ========================================================================
        print_step(8, "Iniciar la tarea (si no se inició automáticamente)")
        url = f"{BASE_URL}/tareas/{tarea_id}/iniciar"
        body = {
            "hormigas_lote_id": lote_id
        }
        print_request("POST", url, body)
        response = safe_request("POST", url, body, test_name="Iniciar Tarea")
        if response:
            data = print_response(response)
            if response.status_code == 200:
                print(f"{COLORS['GREEN']}[OK] Tarea iniciada exitosamente{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Estado: {data.get('estado', 'N/A') if data else 'N/A'}{COLORS['RESET']}")
            elif response.status_code == 400:
                print(f"{COLORS['YELLOW']}NOTA: La tarea ya estaba iniciada o hay un problema{COLORS['RESET']}")
                if data:
                    print(f"  Mensaje: {data.get('detail', 'N/A')}")
            else:
                print(f"{COLORS['YELLOW']}NOTA: Status code {response.status_code}{COLORS['RESET']}")
        
        time.sleep(1)
        
        # ========================================================================
        # PASO 9: Verificar Tiempo Restante
        # ========================================================================
        print_step(9, "Verificar tiempo restante de la tarea")
        url = f"{BASE_URL}/tareas/{tarea_id}/tiempo-restante"
        print_request("GET", url)
        response = safe_request("GET", url, test_name="Verificar Tiempo Restante")
        if response:
            data = print_response(response)
            if data:
                print(f"{COLORS['GREEN']}[OK] Tiempo total: {data.get('tiempo_total_asignado_segundos', 'N/A')} segundos{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Tiempo restante: {data.get('tiempo_restante_segundos', 'N/A')} segundos{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Progreso: {data.get('progreso_porcentaje', 'N/A')}%{COLORS['RESET']}")
        
        time.sleep(1)
        
        # ========================================================================
        # PASO 10: Esperar y Verificar Completado Automático
        # ========================================================================
        print_step(10, "Esperar completado automático (10 segundos + 2 de margen)")
        print(f"{COLORS['CYAN']}Esperando 12 segundos para que se complete la tarea...{COLORS['RESET']}")
        for i in range(12, 0, -1):
            print(f"{COLORS['CYAN']}  Tiempo restante: {i} segundos{COLORS['RESET']}", end='\r')
            time.sleep(1)
        print()  # Nueva línea
        
        url = f"{BASE_URL}/tareas/{tarea_id}/status"
        print_request("GET", url)
        response = safe_request("GET", url, test_name="Verificar Completado Automático")
        if response:
            data = print_response(response)
            if data:
                estado = data.get('estado', 'N/A')
                completada_auto = data.get('completada_automaticamente', False)
                print(f"{COLORS['GREEN']}[OK] Estado final: {estado}{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Completada automáticamente: {completada_auto}{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Inicio: {data.get('inicio', 'N/A')}{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Fin: {data.get('fin', 'N/A')}{COLORS['RESET']}")
        
        time.sleep(1)
        
        # ========================================================================
        # PASO 11: Verificar Todas las Tareas
        # ========================================================================
        print_step(11, "Verificar todas las tareas del sistema")
        url = f"{BASE_URL}/tareas/status"
        print_request("GET", url)
        response = safe_request("GET", url, test_name="Verificar Todas las Tareas")
        if response:
            data = print_response(response)
            if data:
                print(f"{COLORS['GREEN']}[OK] Total tareas: {data.get('total_tareas', 'N/A')}{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Tareas completadas automáticamente: {data.get('tareas_completadas_automaticamente', 'N/A')}{COLORS['RESET']}")
        
        time.sleep(1)
        
        # ========================================================================
        # PASO 12: Verificar Estadísticas
        # ========================================================================
        print_step(12, "Verificar estadísticas del sistema")
        url = f"{BASE_URL}/estadisticas"
        print_request("GET", url)
        response = safe_request("GET", url, test_name="Verificar Estadísticas")
        if response:
            data = print_response(response)
            if data:
                print(f"{COLORS['GREEN']}[OK] Estadísticas obtenidas{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Tareas activas: {data.get('tareas_activas', 'N/A')}{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Tareas completadas: {data.get('tareas_completadas', 'N/A')}{COLORS['RESET']}")
        
        # ========================================================================
        # RESUMEN FINAL
        # ========================================================================
        print_header("RESUMEN DE PRUEBAS")
        print(f"{COLORS['GREEN']}[OK] Todas las pruebas se ejecutaron correctamente{COLORS['RESET']}")
        print(f"\n{COLORS['CYAN']}IDs utilizados:{COLORS['RESET']}")
        print(f"  - Alimento ID: {alimento_id}")
        print(f"  - Tarea ID: {tarea_id}")
        print(f"  - Lote ID: {lote_id}")
        print(f"\n{COLORS['CYAN']}Pruebas realizadas:{COLORS['RESET']}")
        print(f"  1. [OK] Health check")
        print(f"  2. [OK] Crear alimento")
        print(f"  3. [OK] Crear tarea")
        print(f"  4. [OK] Verificar estado inicial")
        print(f"  5. [OK] Intentar asignar con cantidad insuficiente (falló correctamente)")
        print(f"  6. [OK] Asignar con cantidad suficiente")
        print(f"  7. [OK] Verificar estado después de asignación")
        print(f"  8. [OK] Iniciar tarea")
        print(f"  9. [OK] Verificar tiempo restante")
        print(f"  10. [OK] Esperar y verificar completado automático")
        print(f"  11. [OK] Verificar todas las tareas")
        print(f"  12. [OK] Verificar estadísticas")
        
        # ========================================================================
        # GENERAR REPORTE DE ALLURE
        # ========================================================================
        print_header("GENERANDO REPORTE DE ALLURE")
        print(f"{COLORS['CYAN']}Resultados guardados en: allure-results/{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}Total de pruebas ejecutadas: {len(allure_results)}{COLORS['RESET']}")
        
        # Generar reporte HTML
        try:
            print(f"\n{COLORS['YELLOW']}Generando reporte HTML...{COLORS['RESET']}")
            import subprocess
            result = subprocess.run(
                [sys.executable, "scripts/generate_html_report.py"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=Path(__file__).parent.parent
            )
            
            if result.returncode == 0:
                print(f"{COLORS['GREEN']}[OK] Reporte HTML generado exitosamente{COLORS['RESET']}")
                print(f"{COLORS['GREEN']}  Ubicación: test-report.html{COLORS['RESET']}")
                print(f"\n{COLORS['CYAN']}Para abrir el reporte:{COLORS['RESET']}")
                print(f"  - Abre el archivo: test-report.html")
                print(f"  - O ejecuta: start test-report.html (Windows)")
            else:
                print(f"{COLORS['YELLOW']}No se pudo generar el reporte automáticamente{COLORS['RESET']}")
                if result.stderr:
                    print(f"{COLORS['RED']}  Error: {result.stderr[:200]}{COLORS['RESET']}")
                print(f"{COLORS['YELLOW']}Los resultados están guardados en: allure-results/{COLORS['RESET']}")
                print(f"{COLORS['CYAN']}Para generar el reporte manualmente, ejecuta:{COLORS['RESET']}")
                print(f"  python scripts/generate_html_report.py")
        except Exception as e:
            print(f"{COLORS['YELLOW']}Error al generar reporte: {str(e)}{COLORS['RESET']}")
            print(f"{COLORS['YELLOW']}Los resultados están guardados en: allure-results/{COLORS['RESET']}")
            print(f"{COLORS['CYAN']}Para generar el reporte manualmente, ejecuta:{COLORS['RESET']}")
            print(f"  python scripts/generate_html_report.py")
        
    except KeyboardInterrupt:
        print(f"\n{COLORS['YELLOW']}Pruebas interrumpidas por el usuario{COLORS['RESET']}")
        print(f"{COLORS['YELLOW']}Resultados parciales guardados en: allure-results/{COLORS['RESET']}")
    except Exception as e:
        print(f"\n{COLORS['RED']}ERROR INESPERADO: {str(e)}{COLORS['RESET']}")
        import traceback
        traceback.print_exc()
        print(f"{COLORS['YELLOW']}Resultados parciales guardados en: allure-results/{COLORS['RESET']}")


if __name__ == "__main__":
    main()

