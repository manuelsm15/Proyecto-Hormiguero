@echo off
echo ========================================
echo Configurar entorno SQL Server y ejecutar API
echo ========================================
echo.

REM Forzar motor SQL Server
set "DB_ENGINE=sqlserver"

REM Servidor e instancia (MSSQLSERVER es la instancia por defecto)
set "DB_SERVER=SHIRORYUU"
set "DB_INSTANCE=MSSQLSERVER"
set "DB_DATABASE=Hormiguero"

REM Tu equipo tiene Driver 17 instalado; usarlo por defecto
set "ODBC_DRIVER=ODBC Driver 17 for SQL Server"

REM Variables que usa el código Python
set "SQLSERVER_SERVER=%DB_SERVER%"
if /I not "%DB_INSTANCE%"=="MSSQLSERVER" set "SQLSERVER_SERVER=%DB_SERVER%\%DB_INSTANCE%"
set "SQLSERVER_DATABASE=%DB_DATABASE%"
set "SQLSERVER_ODBC_DRIVER=%ODBC_DRIVER%"
set "SQLSERVER_ENCRYPT=no"
set "SQLSERVER_TRUST_SERVER_CERT=yes"

REM (Opcional) URLs externas desactivadas por defecto
set "ENTORNO_API_URL="
set "COMUNICACION_API_URL="
set "BASE_API_URL="

echo Variables configuradas:
echo   DB_ENGINE=%DB_ENGINE%
echo   SQLSERVER_SERVER=%SQLSERVER_SERVER%
echo   SQLSERVER_DATABASE=%SQLSERVER_DATABASE%
echo   SQLSERVER_ODBC_DRIVER=%SQLSERVER_ODBC_DRIVER%
echo.

echo Verificando conectividad ODBC...
python -c "import os,sys; import pyodbc; print('ODBC Drivers:', pyodbc.drivers()); conn=pyodbc.connect('DRIVER={'+os.environ.get('SQLSERVER_ODBC_DRIVER','ODBC Driver 17 for SQL Server')+'};SERVER='+os.environ.get('SQLSERVER_SERVER','localhost')+';DATABASE='+os.environ.get('SQLSERVER_DATABASE','Hormiguero')+';Trusted_Connection=yes;Encrypt='+os.environ.get('SQLSERVER_ENCRYPT','no')+';TrustServerCertificate='+os.environ.get('SQLSERVER_TRUST_SERVER_CERT','yes')); print('OK: conectado a SQL Server')" || (
  echo ERROR: No se pudo conectar a SQL Server con el controlador/servidor indicados.
  echo Revise el nombre del servidor/instancia o el driver ODBC instalado.
  pause
  goto :eof
)

echo.
echo Iniciando API con Python (mantener esta ventana abierta)...
python main.py
echo.
echo API detenida.
pause


