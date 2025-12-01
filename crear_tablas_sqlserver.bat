@echo off
echo ========================================
echo Crear tablas en SQL Server (BD: Hormiguero)
echo ========================================
echo.
set "SERVER=SHIRORYUU"
set "INSTANCE=MSSQLSERVER"
set "DATABASE=Hormiguero"

set "SERVER_TARGET=%SERVER%"
if /I not "%INSTANCE%"=="MSSQLSERVER" set "SERVER_TARGET=%SERVER%\%INSTANCE%"

echo Verificando y creando base de datos si no existe en %SERVER_TARGET%...
powershell -NoProfile -Command ^
  "$cn='Server=%SERVER_TARGET%;Database=master;Integrated Security=True;TrustServerCertificate=True'; ^
    $sql = @'
IF DB_ID(''${env:DATABASE}'') IS NULL
BEGIN
  DECLARE @sql NVARCHAR(MAX) = N'CREATE DATABASE [' + REPLACE('${env:DATABASE}',']',']]') + N']';
  EXEC(@sql);
END
'@; ^
    $c=New-Object System.Data.SqlClient.SqlConnection $cn; ^
    $c.Open(); ^
    $cmd=$c.CreateCommand(); ^
    $cmd.CommandText=$sql; ^
    $cmd.ExecuteNonQuery() | Out-Null; ^
    $c.Close(); ^
    Write-Host 'Base de datos verificada/creada.'"

IF %ERRORLEVEL% NEQ 0 (
  echo Error creando/verificando la base de datos. Revisa servidor/instancia y permisos.
  pause
  exit /b 1
)

echo Creando tablas si no existen en %SERVER_TARGET% - BD %DATABASE%...
powershell -NoProfile -Command ^
  "$cn='Server=%SERVER_TARGET%;Database=%DATABASE%;Integrated Security=True;TrustServerCertificate=True'; ^
    $sql = @'
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'dbo') EXEC('CREATE SCHEMA dbo');

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Alimentos' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
  CREATE TABLE dbo.Alimentos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(200) NOT NULL,
    tipo NVARCHAR(50) NOT NULL,
    zona_id INT NULL,
    cantidad_unitaria INT NOT NULL,
    peso INT NOT NULL,
    duracion_recoleccion INT NOT NULL,
    hormigas_requeridas INT NOT NULL,
    estado NVARCHAR(50) NOT NULL,
    disponible BIT NOT NULL CONSTRAINT DF_Alimentos_disponible DEFAULT(1),
    created_at DATETIME2 NOT NULL CONSTRAINT DF_Alimentos_created DEFAULT SYSUTCDATETIME()
  );
END

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Tareas' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
  CREATE TABLE dbo.Tareas (
    id NVARCHAR(100) NOT NULL PRIMARY KEY,
    alimento_id INT NULL,
    estado NVARCHAR(50) NOT NULL,
    cantidad_recolectada INT NOT NULL CONSTRAINT DF_Tareas_cant DEFAULT(0),
    hormigas_asignadas INT NULL,
    inicio DATETIME2 NULL,
    fin DATETIME2 NULL,
    created_at DATETIME2 NOT NULL CONSTRAINT DF_Tareas_created DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_Tareas_Alimentos FOREIGN KEY (alimento_id) REFERENCES dbo.Alimentos(id)
  );
END

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Eventos' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
  CREATE TABLE dbo.Eventos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tipo NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(1000) NULL,
    payload NVARCHAR(MAX) NULL,
    creado_en DATETIME2 NOT NULL CONSTRAINT DF_Eventos_creado DEFAULT SYSUTCDATETIME()
  );
END

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'Mensajes' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
  CREATE TABLE dbo.Mensajes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    origen NVARCHAR(100) NULL,
    destino NVARCHAR(100) NULL,
    contenido NVARCHAR(MAX) NULL,
    creado_en DATETIME2 NOT NULL CONSTRAINT DF_Mensajes_creado DEFAULT SYSUTCDATETIME()
  );
END
'@; ^
    $c=New-Object System.Data.SqlClient.SqlConnection $cn; ^
    $c.Open(); ^
    $cmd=$c.CreateCommand(); ^
    $cmd.CommandText=$sql; ^
    $cmd.ExecuteNonQuery() | Out-Null; ^
    $c.Close(); ^
    Write-Host 'Tablas verificadas/creadas correctamente.'"

IF %ERRORLEVEL% NEQ 0 (
  echo Hubo un error creando las tablas. Revisa el servidor e instancia configurados.
) ELSE (
  echo.
  echo Listando tablas creadas:
  call listar_tablas_sqlserver.bat
)

pause


