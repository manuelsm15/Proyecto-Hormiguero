@echo off
echo ========================================
echo Obtener Estadisticas
echo ========================================
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/estadisticas' -Method GET | ConvertTo-Json -Depth 10"
pause













