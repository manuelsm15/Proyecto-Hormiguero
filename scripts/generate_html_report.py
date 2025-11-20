#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de reporte HTML simple para pruebas.
Lee los archivos JSON de Allure y genera un reporte HTML sin necesidad de Allure CLI.
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def load_allure_results(results_dir: Path) -> List[Dict[str, Any]]:
    """Carga todos los resultados de Allure desde archivos JSON."""
    results = []
    
    if not results_dir.exists():
        return results
    
    # Buscar todos los archivos *-result.json
    for result_file in results_dir.glob("*-result.json"):
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                results.append(result)
        except Exception as e:
            print(f"Advertencia: No se pudo leer {result_file}: {e}")
    
    return results


def load_attachments(result_uuid: str, results_dir: Path) -> Dict[str, Any]:
    """Carga los attachments (request/response) para un resultado."""
    attachments = {}
    
    # Buscar archivos de attachments
    request_file = results_dir / f"{result_uuid}-attachment-request.json"
    response_file = results_dir / f"{result_uuid}-attachment-response.json"
    
    if request_file.exists():
        try:
            with open(request_file, 'r', encoding='utf-8') as f:
                attachments['request'] = json.load(f)
        except Exception as e:
            attachments['request'] = {"error": str(e)}
    
    if response_file.exists():
        try:
            with open(response_file, 'r', encoding='utf-8') as f:
                attachments['response'] = json.load(f)
        except Exception as e:
            attachments['response'] = {"error": str(e)}
    
    return attachments


def get_status_color(status: str) -> str:
    """Retorna el color CSS para un estado."""
    colors = {
        "passed": "#28a745",
        "failed": "#dc3545",
        "broken": "#ffc107",
        "skipped": "#6c757d"
    }
    return colors.get(status, "#6c757d")


def get_status_icon(status: str) -> str:
    """Retorna el ícono para un estado."""
    icons = {
        "passed": "✓",
        "failed": "✗",
        "broken": "⚠",
        "skipped": "⊘"
    }
    return icons.get(status, "?")


def format_duration(seconds: float) -> str:
    """Formatea una duración en segundos."""
    if seconds < 1:
        return f"{int(seconds * 1000)}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}m {secs:.1f}s"


def generate_html_report(results: List[Dict[str, Any]], output_file: Path):
    """Genera un reporte HTML a partir de los resultados."""
    
    # Calcular estadísticas
    total = len(results)
    passed = sum(1 for r in results if r.get('status') == 'passed')
    failed = sum(1 for r in results if r.get('status') == 'failed')
    broken = sum(1 for r in results if r.get('status') == 'broken')
    skipped = sum(1 for r in results if r.get('status') == 'skipped')
    
    total_duration = sum(r.get('time', {}).get('duration', 0) or 0 for r in results)
    
    # Generar HTML
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .timestamp {{
            opacity: 0.9;
            font-size: 0.9em;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        .stat-passed {{ color: #28a745; }}
        .stat-failed {{ color: #dc3545; }}
        .stat-broken {{ color: #ffc107; }}
        .stat-skipped {{ color: #6c757d; }}
        .stat-total {{ color: #667eea; }}
        .tests {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .test-item {{
            border-bottom: 1px solid #eee;
            padding: 20px;
            transition: background 0.2s;
        }}
        .test-item:hover {{
            background: #f8f9fa;
        }}
        .test-item:last-child {{
            border-bottom: none;
        }}
        .test-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }}
        .test-name {{
            font-size: 1.2em;
            font-weight: 600;
            color: #333;
        }}
        .test-status {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }}
        .test-description {{
            color: #666;
            margin: 10px 0;
            font-size: 0.95em;
        }}
        .test-details {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }}
        .detail-section {{
            margin-bottom: 15px;
        }}
        .detail-label {{
            font-weight: 600;
            color: #555;
            margin-bottom: 5px;
        }}
        .detail-content {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            overflow-x: auto;
        }}
        .detail-content pre {{
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .error-message {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px;
            margin-top: 10px;
            border-radius: 4px;
        }}
        .collapsible {{
            cursor: pointer;
            user-select: none;
        }}
        .collapsible:hover {{
            opacity: 0.8;
        }}
        .collapsible-content {{
            display: none;
            margin-top: 10px;
        }}
        .collapsible-content.active {{
            display: block;
        }}
        .json-key {{
            color: #0066cc;
        }}
        .json-string {{
            color: #008000;
        }}
        .json-number {{
            color: #ff6600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Reporte de Pruebas</h1>
            <div class="timestamp">Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value stat-total">{total}</div>
                <div class="stat-label">Total</div>
            </div>
            <div class="stat-card">
                <div class="stat-value stat-passed">{passed}</div>
                <div class="stat-label">Pasadas</div>
            </div>
            <div class="stat-card">
                <div class="stat-value stat-failed">{failed}</div>
                <div class="stat-label">Fallidas</div>
            </div>
            <div class="stat-card">
                <div class="stat-value stat-broken">{broken}</div>
                <div class="stat-label">Rotos</div>
            </div>
            <div class="stat-card">
                <div class="stat-value stat-skipped">{skipped}</div>
                <div class="stat-label">Omitidas</div>
            </div>
            <div class="stat-card">
                <div class="stat-value stat-total">{format_duration(total_duration / 1000000000)}</div>
                <div class="stat-label">Duración Total</div>
            </div>
        </div>
        
        <div class="tests">
"""
    
    # Agregar cada prueba
    for i, result in enumerate(results):
        status = result.get('status', 'unknown')
        name = result.get('name', 'Prueba sin nombre')
        description = result.get('description', '')
        error = result.get('error', {})
        time_info = result.get('time', {})
        duration = time_info.get('duration', 0) or 0
        duration_seconds = duration / 1000000000  # Convertir nanosegundos a segundos
        
        # Cargar attachments
        result_uuid = result.get('uuid', f'test-{i}')
        attachments = load_attachments(result_uuid, Path('allure-results'))
        
        status_color = get_status_color(status)
        status_icon = get_status_icon(status)
        
        html += f"""
            <div class="test-item">
                <div class="test-header">
                    <div class="test-name">{name}</div>
                    <div class="test-status" style="background: {status_color}20; color: {status_color};">
                        {status_icon} {status.upper()}
                    </div>
                </div>
                <div class="test-description">{description}</div>
                <div style="color: #666; font-size: 0.9em; margin-top: 5px;">
                    Duración: {format_duration(duration_seconds)}
                </div>
"""
        
        # Mostrar error si existe
        if error and error.get('message'):
            html += f"""
                <div class="error-message">
                    <strong>Error:</strong> {error.get('message', 'N/A')}
                </div>
"""
        
        # Mostrar detalles (request/response)
        if attachments.get('request') or attachments.get('response'):
            html += f"""
                <div class="test-details">
                    <div class="collapsible" onclick="toggleDetails({i})">
                        <strong>📋 Ver Detalles (Request/Response)</strong>
                    </div>
                    <div class="collapsible-content" id="details-{i}">
"""
            
            if attachments.get('request'):
                request_json = json.dumps(attachments['request'], indent=2, ensure_ascii=False)
                html += f"""
                        <div class="detail-section">
                            <div class="detail-label">📤 Request:</div>
                            <div class="detail-content"><pre>{request_json}</pre></div>
                        </div>
"""
            
            if attachments.get('response'):
                response_json = json.dumps(attachments['response'], indent=2, ensure_ascii=False)
                html += f"""
                        <div class="detail-section">
                            <div class="detail-label">📥 Response:</div>
                            <div class="detail-content"><pre>{response_json}</pre></div>
                        </div>
"""
            
            html += """
                    </div>
                </div>
"""
        
        html += """
            </div>
"""
    
    # Cerrar HTML
    html += """
        </div>
    </div>
    
    <script>
        function toggleDetails(index) {
            const content = document.getElementById('details-' + index);
            content.classList.toggle('active');
        }
    </script>
</body>
</html>
"""
    
    # Escribir archivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    """Función principal."""
    project_root = Path(__file__).parent.parent
    results_dir = project_root / "allure-results"
    output_file = project_root / "test-report.html"
    
    print("Generando reporte HTML...")
    
    if not results_dir.exists():
        print("[ERROR] No se encontro el directorio allure-results")
        print("Ejecuta primero las pruebas con: python scripts/prueba_completa_sistema_lotes.py")
        return 1
    
    # Cargar resultados
    results = load_allure_results(results_dir)
    
    if not results:
        print("[ERROR] No se encontraron resultados de pruebas")
        return 1
    
    print(f"[OK] Cargados {len(results)} resultados")
    
    # Generar reporte
    try:
        generate_html_report(results, output_file)
        print(f"[OK] Reporte HTML generado exitosamente")
        print(f"Ubicacion: {output_file}")
        print(f"\nPara abrir el reporte:")
        print(f"  - Abre el archivo: {output_file}")
        print(f"  - O ejecuta: start {output_file} (Windows)")
        return 0
    except Exception as e:
        print(f"[ERROR] Error al generar reporte: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

