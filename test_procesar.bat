@echo off
echo ========================================
echo Procesar Recoleccion Completa
echo ========================================
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/procesar' -Method POST | ConvertTo-Json -Depth 10"
pause













