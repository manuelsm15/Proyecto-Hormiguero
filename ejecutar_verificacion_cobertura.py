"""
Script para ejecutar tests y verificar cobertura, guardando resultados en archivo.
"""
import subprocess
import sys
from datetime import datetime

def ejecutar_comando(cmd, descripcion):
    """Ejecuta un comando y retorna la salida."""
    print(f"\n{'='*80}")
    print(f"{descripcion}")
    print(f"Comando: {cmd}")
    print('='*80)
    
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        salida = result.stdout + result.stderr
        return salida, result.returncode
    except Exception as e:
        return f"Error ejecutando comando: {e}", 1

# Abrir archivo para guardar resultados
archivo_resultados = "resultados_cobertura.txt"
with open(archivo_resultados, 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write(f"REPORTE DE COBERTURA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("="*80 + "\n\n")
    
    # 1. Ejecutar tests de cobertura faltante
    print("\n1. Ejecutando tests de cobertura faltante...")
    salida1, codigo1 = ejecutar_comando(
        "python -m pytest tests/test_api_cobertura_missing.py -v --tb=line -q",
        "TESTS DE COBERTURA FALTANTE"
    )
    f.write("\n" + "="*80 + "\n")
    f.write("TESTS DE COBERTURA FALTANTE\n")
    f.write("="*80 + "\n")
    f.write(salida1)
    f.write(f"\nCódigo de salida: {codigo1}\n")
    print(salida1[-500:] if len(salida1) > 500 else salida1)
    
    # 2. Verificar cobertura
    print("\n2. Verificando cobertura del controlador de API...")
    salida2, codigo2 = ejecutar_comando(
        "python -m pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py --cov=src/recoleccion/api/recoleccion_controller --cov-report=term-missing --cov-report=html -q --tb=no",
        "VERIFICACIÓN DE COBERTURA"
    )
    f.write("\n" + "="*80 + "\n")
    f.write("VERIFICACIÓN DE COBERTURA\n")
    f.write("="*80 + "\n")
    f.write(salida2)
    f.write(f"\nCódigo de salida: {codigo2}\n")
    
    # Buscar porcentaje de cobertura
    import re
    patron = r'recoleccion_controller\.py\s+\d+\s+(\d+)\s+(\d+)%'
    match = re.search(patron, salida2)
    if match:
        stmts = match.group(1)
        cover = match.group(2)
        f.write(f"\nRESUMEN:\n")
        f.write(f"  Líneas totales: {stmts}\n")
        f.write(f"  Cobertura: {cover}%\n")
        print(f"\n{'='*80}")
        print(f"COBERTURA: {cover}%")
        print(f"{'='*80}")
        if int(cover) >= 80:
            print("✅ Objetivo alcanzado (≥80%)")
        else:
            print(f"⚠️  Falta {80 - int(cover)}% para alcanzar el objetivo")
    else:
        # Buscar en formato TOTAL
        patron2 = r'TOTAL\s+\d+\s+\d+\s+(\d+)%'
        match2 = re.search(patron2, salida2)
        if match2:
            cover = match2.group(1)
            f.write(f"\nRESUMEN:\n")
            f.write(f"  Cobertura: {cover}%\n")
            print(f"\n{'='*80}")
            print(f"COBERTURA: {cover}%")
            print(f"{'='*80}")
            if int(cover) >= 80:
                print("✅ Objetivo alcanzado (≥80%)")
            else:
                print(f"⚠️  Falta {80 - int(cover)}% para alcanzar el objetivo")
    
    print(salida2[-1000:] if len(salida2) > 1000 else salida2)
    
    f.write("\n" + "="*80 + "\n")
    f.write("FIN DEL REPORTE\n")
    f.write("="*80 + "\n")

print(f"\n✅ Resultados guardados en: {archivo_resultados}")
print("📊 Revisa el reporte HTML en: htmlcov/index.html")


