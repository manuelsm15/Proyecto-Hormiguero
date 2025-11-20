@echo off
echo ========================================
echo Crear Tarea de Recoleccion
echo ========================================
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/tareas' -Method POST | ConvertTo-Json -Depth 10"
pause













