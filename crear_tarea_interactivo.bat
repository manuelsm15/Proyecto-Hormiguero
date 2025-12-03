@echo off
echo ========================================
echo Crear Tarea de Recoleccion (Interactivo)
echo ========================================
echo.
set /p tarea_id=Ingrese tarea_id (opcional, Enter para omitir): 
set /p alimento_id=Ingrese alimento_id (opcional, Enter para omitir): 

set "BASE_URL=http://localhost:8000/tareas"
set "URL=%BASE_URL%"

REM Construir querystring segun parametros ingresados
set "QS="
if not "%tarea_id%"=="" set "QS=tarea_id=%tarea_id%"
if not "%alimento_id%"=="" (
    if not "%QS%"=="" (
        set "QS=%QS%&alimento_id=%alimento_id%"
    ) else (
        set "QS=alimento_id=%alimento_id%"
    )
)

if not "%QS%"=="" set "URL=%URL%?%QS%"

echo.
echo Ejecutando: POST "%URL%"
echo.

curl -X POST "%URL%"
echo.
pause
