@echo off
echo ========================================
echo Iniciar Tarea de Recoleccion (Interactivo)
echo ========================================
echo.
set /p tarea_id=Ingrese tarea_id (obligatorio): 

if "%tarea_id%"=="" (
    echo ERROR: tarea_id es obligatorio.
    pause
    exit /b 1
)

echo.
set /p hormigas_lote_id=Ingrese ID del lote de hormigas (obligatorio): 

if "%hormigas_lote_id%"=="" (
    echo ERROR: El ID del lote de hormigas es obligatorio.
    pause
    exit /b 1
)

set "URL=http://localhost:8000/tareas/%tarea_id%/iniciar"
echo.
echo Ejecutando: POST "%URL%"
echo Con body: {"hormigas_lote_id": "%hormigas_lote_id%"}
echo.

REM Crear archivo temporal con el JSON
echo {"hormigas_lote_id": "%hormigas_lote_id%"} > temp_body.json

curl -X POST "%URL%" -H "Content-Type: application/json" -d @temp_body.json

echo.
echo.

REM Limpiar archivo temporal
del temp_body.json 2>nul

pause
