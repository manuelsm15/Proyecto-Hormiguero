@echo off
echo ========================================
echo Listar Alimentos Disponibles
echo ========================================
echo.
powershell -Command "try { Invoke-RestMethod -Uri 'http://localhost:8000/alimentos' -Method GET | ConvertTo-Json -Depth 10 } catch { Write-Host 'ERROR al consultar /alimentos' -ForegroundColor Red }"
echo.
pause










