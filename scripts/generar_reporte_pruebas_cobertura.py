"""
Script para generar reporte completo de pruebas y cobertura.
"""
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REPORTES_DIR = BASE_DIR / "docs" / "evidencias" / "reportes"
REPORTES_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("="*80)
print("GENERANDO REPORTE DE PRUEBAS Y COBERTURA")
print("="*80)

# 1. Ejecutar pruebas con cobertura
print("\n1. Ejecutando pruebas con cobertura...")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/",
     "--cov=src/recoleccion",
     "--cov-report=term-missing",
     "--cov-report=html:htmlcov",
     "--cov-report=json:coverage.json",
     "-v"],
    capture_output=True,
    text=True,
    cwd=BASE_DIR
)

# 2. Guardar salida de pruebas
reporte_pruebas = REPORTES_DIR / f"reporte_pruebas_{timestamp}.txt"
with open(reporte_pruebas, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("REPORTE DE PRUEBAS Y COBERTURA\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("="*80 + "\n\n")
    f.write(result.stdout)
    if result.stderr:
        f.write("\n\nERRORES:\n")
        f.write(result.stderr)

print(f"[OK] Reporte de pruebas guardado: {reporte_pruebas}")

# 3. Analizar resultados
print("\n2. Analizando resultados...")
cobertura_por_modulo = {}
cobertura_total = 0

for line in result.stdout.split("\n"):
    if "TOTAL" in line and "%" in line:
        parts = line.split()
        for i, part in enumerate(parts):
            if part == "TOTAL":
                try:
                    cobertura_total = float(parts[i+2].replace("%", ""))
                except:
                    pass
    elif "src\\recoleccion" in line or "src/recoleccion" in line:
        parts = line.split()
        if len(parts) >= 3:
            try:
                modulo = parts[0]
                cobertura = float(parts[-1].replace("%", ""))
                cobertura_por_modulo[modulo] = cobertura
            except:
                pass

# 4. Generar reporte resumido
reporte_resumen = REPORTES_DIR / f"resumen_cobertura_{timestamp}.md"
with open(reporte_resumen, "w", encoding="utf-8") as f:
    f.write("# Resumen de Cobertura de Código\n\n")
    f.write(f"**Fecha de Generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("## Cobertura Total\n\n")
    f.write(f"- **Cobertura General**: {cobertura_total:.1f}%\n")
    f.write(f"- **Objetivo**: ≥ 80%\n")
    f.write(f"- **Estado**: {'✅ CUMPLE' if cobertura_total >= 80 else '⚠️ MEJORABLE'}\n\n")
    
    f.write("## Cobertura por Módulo\n\n")
    f.write("| Módulo | Cobertura | Estado |\n")
    f.write("|--------|-----------|--------|\n")
    
    for modulo, cobertura in sorted(cobertura_por_modulo.items(), key=lambda x: x[1], reverse=True):
        estado = "✅" if cobertura >= 80 else "⚠️" if cobertura >= 50 else "❌"
        f.write(f"| {modulo} | {cobertura:.1f}% | {estado} |\n")
    
    f.write("\n## Módulos Críticos\n\n")
    f.write("### Modelos\n")
    modelos_cov = cobertura_por_modulo.get("src\\recoleccion\\models", 0)
    f.write(f"- **Cobertura**: {modelos_cov:.1f}%\n")
    f.write(f"- **Estado**: {'✅ Excelente' if modelos_cov >= 100 else '⚠️ Mejorable'}\n\n")
    
    f.write("### Servicios\n")
    servicios_cov = cobertura_por_modulo.get("src\\recoleccion\\services\\recoleccion_service", 0)
    f.write(f"- **Cobertura**: {servicios_cov:.1f}%\n")
    f.write(f"- **Estado**: {'✅ Excelente' if servicios_cov >= 80 else '⚠️ Mejorable'}\n\n")
    
    f.write("### APIs\n")
    apis_cov = cobertura_por_modulo.get("src\\recoleccion\\api", 0)
    f.write(f"- **Cobertura**: {apis_cov:.1f}%\n")
    f.write(f"- **Estado**: {'✅ Excelente' if apis_cov >= 80 else '⚠️ Mejorable'}\n")
    if apis_cov < 80:
        f.write(f"- **Acción Requerida**: Agregar más tests para endpoints faltantes\n\n")

print(f"[OK] Resumen de cobertura guardado: {reporte_resumen}")

# 5. Información de reportes HTML
print("\n3. Reportes HTML generados:")
print(f"   - Cobertura general: htmlcov/index.html")
print(f"   - Cobertura APIs: htmlcov/api/index.html (si existe)")

print("\n" + "="*80)
print("REPORTE COMPLETADO")
print("="*80)
print(f"\nCobertura Total: {cobertura_total:.1f}%")
print(f"Objetivo: ≥ 80%")
print(f"Estado: {'✅ CUMPLE' if cobertura_total >= 80 else '⚠️ MEJORABLE'}")



