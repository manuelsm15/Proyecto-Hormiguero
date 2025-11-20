@echo off
echo ========================================
echo Configurar SQL Server (Windows Auth) y arrancar servicio
echo ========================================

REM Configuracion de entorno (edita si necesitas cambiar)
set "DB_ENGINE=sqlserver"
set "SQLSERVER_SERVER=SHIRORYUU"
set "SQLSERVER_DATABASE=Hormiguero"
set "SQLSERVER_ODBC_DRIVER=ODBC Driver 18 for SQL Server"
set "SQLSERVER_ENCRYPT=no"
set "SQLSERVER_TRUST_SERVER_CERT=yes"

echo.
echo Variables de entorno configuradas:
echo   DB_ENGINE=%DB_ENGINE%
echo   SQLSERVER_SERVER=%SQLSERVER_SERVER%
echo   SQLSERVER_DATABASE=%SQLSERVER_DATABASE%
echo   SQLSERVER_ODBC_DRIVER=%SQLSERVER_ODBC_DRIVER%
echo   SQLSERVER_ENCRYPT=%SQLSERVER_ENCRYPT%
echo   SQLSERVER_TRUST_SERVER_CERT=%SQLSERVER_TRUST_SERVER_CERT%

echo.
echo Verificando pyodbc...
pip show pyodbc >NUL 2>&1
if errorlevel 1 (
    echo pyodbc no encontrado. Instalando...
    pip install pyodbc
    if errorlevel 1 (
        echo ERROR: No se pudo instalar pyodbc. Verifica tu Python/pip.
        pause
        exit /b 1
    )
) else (
    echo pyodbc OK
)

echo.
echo Probando conexion a SQL Server y creando BD si no existe...
powershell -NoProfile -Command "$server = '%SQLSERVER_SERVER%'; $db = '%SQLSERVER_DATABASE%'; $connMaster = New-Object System.Data.SqlClient.SqlConnection ('Server='+$server+';Database=master;Integrated Security=True;TrustServerCertificate=True'); try { $connMaster.Open(); $existsCmd = $connMaster.CreateCommand(); $existsCmd.CommandText = 'IF DB_ID(@db) IS NULL SELECT 0 ELSE SELECT 1'; $p = $existsCmd.Parameters.Add('@db',[System.Data.SqlDbType]::NVarChar,128); $p.Value = $db; $exists = [int]$existsCmd.ExecuteScalar(); if ($exists -eq 0) { Write-Host 'BD no existe. Creando...'; $createCmd = $connMaster.CreateCommand(); $createCmd.CommandText = 'CREATE DATABASE ['+$db+']'; $null = $createCmd.ExecuteNonQuery(); } else { Write-Host 'BD ya existe.'; } $connMaster.Close(); $connDb = New-Object System.Data.SqlClient.SqlConnection ('Server='+$server+';Database='+$db+';Integrated Security=True;TrustServerCertificate=True'); $connDb.Open(); Write-Host 'Conexion a SQL Server OK.'; $connDb.Close(); exit 0 } catch { Write-Host ('ERROR conexion SQL Server: ' + $_.Exception.Message); exit 1 }"
if errorlevel 1 (
    echo ERROR: No se pudo conectar/crear la base de datos. ^
    echo Asegurate de que el servidor "%SQLSERVER_SERVER%" este accesible y tengas permisos. ^
    echo Verifica tambien que el driver "%SQLSERVER_ODBC_DRIVER%" este instalado.
    pause
    exit /b 1
)

echo.
echo Iniciando servicio (FastAPI)...
python main.py


