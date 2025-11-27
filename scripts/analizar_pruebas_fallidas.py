#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para analizar pruebas fallidas en Allure results."""

import json
from pathlib import Path
from collections import defaultdict

def main():
    results_dir = Path("allure-results")
    if not results_dir.exists():
        print("No se encontró el directorio allure-results")
        return
    
    # Cargar todos los resultados
    all_results = []
    failed_results = []
    broken_results = []
    skipped_results = []
    
    for result_file in results_dir.glob("*-result.json"):
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                all_results.append(result)
                status = result.get('status', 'unknown')
                if status == 'failed':
                    failed_results.append(result)
                elif status == 'broken':
                    broken_results.append(result)
                elif status == 'skipped':
                    skipped_results.append(result)
        except Exception as e:
            print(f"Error leyendo {result_file}: {e}")
    
    # Estadísticas
    total = len(all_results)
    passed = sum(1 for r in all_results if r.get('status') == 'passed')
    failed = len(failed_results)
    broken = len(broken_results)
    skipped = len(skipped_results)
    
    print("=" * 80)
    print("ANÁLISIS DE PRUEBAS")
    print("=" * 80)
    print(f"Total: {total}")
    print(f"Pasadas: {passed}")
    print(f"Fallidas: {failed}")
    print(f"Rotos: {broken}")
    print(f"Omitidas: {skipped}")
    print()
    
    # Mostrar pruebas fallidas
    if failed_results:
        print("=" * 80)
        print("PRUEBAS FALLIDAS:")
        print("=" * 80)
        for idx, result in enumerate(failed_results[:20], 1):
            name = result.get('name', 'N/A')
            error = result.get('error', {})
            error_msg = error.get('message', 'N/A')
            status_details = result.get('statusDetails', {})
            description = result.get('description', 'N/A')
            
            print(f"\n{idx}. {name}")
            print(f"   Descripción: {description[:100]}")
            print(f"   Error message: {error_msg[:200]}")
            if status_details:
                print(f"   Status details: {json.dumps(status_details, indent=2, ensure_ascii=False)[:300]}")
            if error.get('trace'):
                trace = error.get('trace', '')
                # Mostrar solo las primeras líneas del trace
                trace_lines = trace.split('\n')[:5]
                print(f"   Trace (primeras líneas):")
                for line in trace_lines:
                    print(f"     {line[:150]}")
            
            # Mostrar attachments si existen
            attachments = result.get('attachments', [])
            if attachments:
                print(f"   Attachments: {len(attachments)}")
    
    # Mostrar pruebas rotas
    if broken_results:
        print("\n" + "=" * 80)
        print("PRUEBAS ROTAS:")
        print("=" * 80)
        for idx, result in enumerate(broken_results[:20], 1):
            name = result.get('name', 'N/A')
            error = result.get('error', {})
            error_msg = error.get('message', 'N/A')
            print(f"\n{idx}. {name}")
            print(f"   Error: {error_msg[:200]}")
    
    # Mostrar pruebas omitidas
    if skipped_results:
        print("\n" + "=" * 80)
        print("PRUEBAS OMITIDAS:")
        print("=" * 80)
        for idx, result in enumerate(skipped_results[:20], 1):
            name = result.get('name', 'N/A')
            print(f"{idx}. {name}")
    
    # Agrupar por tipo de error
    error_types = defaultdict(list)
    for result in failed_results + broken_results:
        error = result.get('error', {})
        error_msg = error.get('message', 'N/A')
        # Extraer tipo de error (primera parte del mensaje)
        error_type = error_msg.split(':')[0] if ':' in error_msg else error_msg[:50]
        error_types[error_type].append(result.get('name', 'N/A'))
    
    if error_types:
        print("\n" + "=" * 80)
        print("TIPOS DE ERRORES MÁS COMUNES:")
        print("=" * 80)
        for error_type, tests in sorted(error_types.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"\n{error_type}: {len(tests)} pruebas")
            for test in tests[:5]:
                print(f"  - {test}")
            if len(tests) > 5:
                print(f"  ... y {len(tests) - 5} más")

if __name__ == "__main__":
    main()

