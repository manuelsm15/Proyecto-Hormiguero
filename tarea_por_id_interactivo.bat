@echo off
echo ========================================
echo Consultar Tarea por ID (Interactivo)
echo ========================================
echo.
set /p tarea_id=Ingrese tarea_id (obligatorio): 

if "%tarea_id%"=="" (
    echo ERROR: tarea_id es obligatorio.
    pause
    exit /b 1
)

set "URL=http://localhost:8000/tareas/%tarea_id%"
echo.
echo Ejecutando: GET "%URL%"
echo.

curl "%URL%"
echo.
pause
