# Script PowerShell para ejecutar tests y verificar cobertura
Write-Host "`n=== EJECUTANDO TESTS DE COBERTURA ===" -ForegroundColor Cyan

# 1. Ejecutar tests de cobertura faltante
Write-Host "`n1. Ejecutando tests de cobertura faltante..." -ForegroundColor Yellow
python -m pytest tests/test_api_cobertura_missing.py -v --tb=line -q

# 2. Verificar cobertura
Write-Host "`n2. Verificando cobertura del controlador de API..." -ForegroundColor Yellow
python -m pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py --cov=src/recoleccion/api/recoleccion_controller --cov-report=term-missing --cov-report=html -q

# 3. Mostrar resumen
Write-Host "`n=== RESUMEN ===" -ForegroundColor Green
Write-Host "Revisa el reporte HTML en: htmlcov/index.html" -ForegroundColor White




