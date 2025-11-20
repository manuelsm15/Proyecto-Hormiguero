@echo off
REM Script para iniciar el servidor FastAPI del subsistema de recolección

echo ========================================
echo Iniciando Servidor de Recoleccion
echo ========================================
echo.

cd /d "%~dp0\.."

echo Verificando que el puerto 8000 este disponible...
netstat -ano | findstr :8000 >nul
if %errorlevel% == 0 (
    echo ADVERTENCIA: El puerto 8000 ya esta en uso!
    echo Por favor, cierra el proceso que esta usando el puerto 8000
    pause
    exit /b 1
)

echo Iniciando servidor en http://localhost:8000
echo.
echo Para detener el servidor, presiona Ctrl+C
echo.

python main.py

pause

