@echo off
echo ========================================
echo Crear e Iniciar Tarea de Recoleccion (Interactivo)
echo ========================================
echo.
echo Primero listaremos los alimentos disponibles para elegir un ID valido...
powershell -Command "try { Invoke-RestMethod -Uri 'http://localhost:8000/alimentos' -Method GET | ConvertTo-Json -Depth 10 } catch { Write-Host 'ERROR al consultar /alimentos' -ForegroundColor Red }"
echo.
set /p alimento_id=Ingrese alimento_id (obligatorio, copie uno de la lista): 
if "%alimento_id%"=="" (
    echo ERROR: alimento_id es obligatorio.
    pause
    exit /b 1
)
set /p tarea_id=Ingrese tarea_id (opcional, Enter para omitir): 

set "BASE_URL=http://localhost:8000/tareas"
set "URL=%BASE_URL%"

REM Construir querystring segun parametros ingresados
set "QS=alimento_id=%alimento_id%"
if not "%tarea_id%"=="" set "QS=tarea_id=%tarea_id%&%QS%"

if not "%QS%"=="" set "URL=%URL%?%QS%"

echo.
echo Ejecutando: POST "%URL%"
echo.
curl -s -X POST "%URL%"
echo.

REM Determinar ID de tarea para iniciar
set "tid=%tarea_id%"
if "%tid%"=="" set "tid=%alimento_id%"

if "%tid%"=="" (
    echo No se pudo determinar tarea_id para iniciar.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Iniciar Tarea (requiere ID del lote de hormigas)
echo ========================================
echo.
set /p hormigas_lote_id=Ingrese ID del lote de hormigas (obligatorio): 

if "%hormigas_lote_id%"=="" (
    echo ERROR: El ID del lote de hormigas es obligatorio.
    pause
    exit /b 1
)

echo.
set "START_URL=http://localhost:8000/tareas/%tid%/iniciar"
echo Ejecutando: POST "%START_URL%"
echo Con body: {"hormigas_lote_id": "%hormigas_lote_id%"}
echo.

REM Crear archivo temporal con el JSON
echo {"hormigas_lote_id": "%hormigas_lote_id%"} > temp_body_iniciar.json

curl -s -X POST "%START_URL%" -H "Content-Type: application/json" -d @temp_body_iniciar.json

echo.
echo.

REM Limpiar archivo temporal
del temp_body_iniciar.json 2>nul

pause



