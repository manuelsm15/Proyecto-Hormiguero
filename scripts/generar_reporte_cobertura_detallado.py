"""
Script para generar reporte de cobertura detallado por módulo/clase.
"""
import subprocess
import sys
import os
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
EVIDENCIAS_DIR = BASE_DIR / "docs" / "evidencias" / "cobertura"
EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("="*80)
print("GENERANDO REPORTE DE COBERTURA DETALLADO")
print("="*80)

# 1. Cobertura por módulo
print("\n1. Generando cobertura por módulo...")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/",
     "--cov=src/recoleccion/models",
     "--cov=src/recoleccion/services/recoleccion_service",
     "--cov=src/recoleccion/services/persistence_service",
     "--cov=src/recoleccion/api/recoleccion_controller",
     "--cov-report=term-missing",
     "--cov-report=html:" + str(EVIDENCIAS_DIR / f"html_{timestamp}"),
     "-q"],
    capture_output=True,
    text=True,
    cwd=BASE_DIR
)

# Guardar reporte
reporte_file = EVIDENCIAS_DIR / f"cobertura_detallada_{timestamp}.txt"
with open(reporte_file, "w", encoding="utf-8") as f:
    f.write("=== REPORTE DE COBERTURA DETALLADO ===\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(result.stdout)
    f.write("\n\n=== STDERR ===\n")
    f.write(result.stderr)

print(f"[OK] Reporte guardado: {reporte_file}")

# 2. Extraer métricas
metricas = {}
for line in result.stdout.split("\n"):
    if "src/recoleccion" in line and "%" in line:
        parts = line.split()
        if len(parts) >= 2:
            archivo = parts[0]
            try:
                cobertura = int(parts[-1].replace("%", ""))
                metricas[archivo] = cobertura
            except:
                pass

# 3. Generar JSON con métricas
metricas_file = EVIDENCIAS_DIR / f"metricas_cobertura_{timestamp}.json"
with open(metricas_file, "w", encoding="utf-8") as f:
    json.dump({
        "fecha": datetime.now().isoformat(),
        "cobertura_por_archivo": metricas,
        "resumen": {
            "total_archivos": len(metricas),
            "archivos_80_plus": len([v for v in metricas.values() if v >= 80]),
            "archivos_60_79": len([v for v in metricas.values() if 60 <= v < 80]),
            "archivos_menos_60": len([v for v in metricas.values() if v < 60])
        }
    }, f, indent=2, ensure_ascii=False)

print(f"[OK] Métricas guardadas: {metricas_file}")
print("\n[OK] Reporte de cobertura detallado generado")



