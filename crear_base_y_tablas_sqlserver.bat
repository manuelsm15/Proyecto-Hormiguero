@echo off
echo ========================================
echo Recrear Base de Datos y Tablas (SQL Server)
echo BD: Hormiguero (desde 0)
echo ========================================
echo.
set "SERVER=SHIRORYUU"
set "INSTANCE=MSSQLSERVER"
set "DATABASE=Hormiguero"

echo Paso 1/3: Eliminar base si existe en %SERVER%\\%INSTANCE% ...
powershell -NoProfile -Command ^
  "$cn='Server=%SERVER%\\%INSTANCE%;Database=master;Integrated Security=True;TrustServerCertificate=True'; ^
    $sql = @'
IF DB_ID(N''${env:DATABASE}'') IS NOT NULL
BEGIN
  DECLARE @db NVARCHAR(256) = N'[' + REPLACE('${env:DATABASE}',']',']]') + N']';
  DECLARE @sql NVARCHAR(MAX) = N'ALTER DATABASE ' + @db + N' SET SINGLE_USER WITH ROLLBACK IMMEDIATE; DROP DATABASE ' + @db + N';';
  EXEC(@sql);
END
'@; ^
    $c=New-Object System.Data.SqlClient.SqlConnection $cn; ^
    $c.Open(); ^
    $cmd=$c.CreateCommand(); ^
    $cmd.CommandText=$sql; ^
    $cmd.ExecuteNonQuery() | Out-Null; ^
    $c.Close(); ^
    Write-Host 'Base eliminada si existía.'"
IF %ERRORLEVEL% NEQ 0 (
  echo Error eliminando la base. Verifica permisos/instancia.
  pause
  exit /b 1
)

echo Paso 2/3: Crear base desde cero...
powershell -NoProfile -Command ^
  "$cn='Server=%SERVER%\\%INSTANCE%;Database=master;Integrated Security=True;TrustServerCertificate=True'; ^
    $sql = @'
DECLARE @db NVARCHAR(256) = N'[' + REPLACE('${env:DATABASE}',']',']]') + N']';
DECLARE @sql NVARCHAR(MAX) = N'CREATE DATABASE ' + @db + N'';
EXEC(@sql);
ALTER DATABASE ['+ '${env:DATABASE}' +'] SET RECOVERY SIMPLE;
'@; ^
    $c=New-Object System.Data.SqlClient.SqlConnection $cn; ^
    $c.Open(); ^
    $cmd=$c.CreateCommand(); ^
    $cmd.CommandText=$sql; ^
    $cmd.ExecuteNonQuery() | Out-Null; ^
    $c.Close(); ^
    Write-Host 'Base creada correctamente.'"
IF %ERRORLEVEL% NEQ 0 (
  echo Error creando la base. Verifica permisos/instancia.
  pause
  exit /b 1
)

echo Paso 3/3: Crear tablas y datos iniciales...
powershell -NoProfile -Command ^
  "$cn='Server=%SERVER%\\%INSTANCE%;Database=%DATABASE%;Integrated Security=True;TrustServerCertificate=True'; ^
    $sql = @'
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = ''dbo'') EXEC(''CREATE SCHEMA dbo'');

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

CREATE TABLE dbo.Eventos (
  id INT IDENTITY(1,1) PRIMARY KEY,
  tipo NVARCHAR(100) NOT NULL,
  descripcion NVARCHAR(1000) NULL,
  payload NVARCHAR(MAX) NULL,
  creado_en DATETIME2 NOT NULL CONSTRAINT DF_Eventos_creado DEFAULT SYSUTCDATETIME()
);

CREATE TABLE dbo.Mensajes (
  id INT IDENTITY(1,1) PRIMARY KEY,
  origen NVARCHAR(100) NULL,
  destino NVARCHAR(100) NULL,
  contenido NVARCHAR(MAX) NULL,
  creado_en DATETIME2 NOT NULL CONSTRAINT DF_Mensajes_creado DEFAULT SYSUTCDATETIME()
);

-- Datos iniciales (A1, A2, A3)
INSERT INTO dbo.Alimentos (nombre, tipo, zona_id, cantidad_unitaria, peso, duracion_recoleccion, hormigas_requeridas, estado, disponible)
VALUES
 (N'A1', N'FRUTA', 1, 10, 1, 5, 5, N'disponible', 1),
 (N'A2', N'SEMILLA', 1, 8, 1, 4, 4, N'disponible', 1),
 (N'A3', N'AZUCAR', 2, 12, 1, 6, 6, N'disponible', 1);
'@; ^
    $c=New-Object System.Data.SqlClient.SqlConnection $cn; ^
    $c.Open(); ^
    $cmd=$c.CreateCommand(); ^
    $cmd.CommandText=$sql; ^
    $cmd.ExecuteNonQuery() | Out-Null; ^
    $c.Close(); ^
    Write-Host 'Tablas y datos iniciales creados.'"
IF %ERRORLEVEL% NEQ 0 (
  echo Error creando tablas/datos iniciales.
  pause
  exit /b 1
)

echo.
echo Verificacion de tablas:
call listar_tablas_sqlserver.bat

echo.
echo Listado de alimentos iniciales:
powershell -NoProfile -Command ^
  "$cn='Server=%SERVER%\\%INSTANCE%;Database=%DATABASE%;Integrated Security=True;TrustServerCertificate=True'; ^
    $q='SELECT id, nombre, tipo, estado, cantidad_unitaria FROM dbo.Alimentos ORDER BY id'; ^
    $c=New-Object System.Data.SqlClient.SqlConnection $cn; ^
    $c.Open(); ^
    $cmd=$c.CreateCommand(); ^
    $cmd.CommandText=$q; ^
    $r=$cmd.ExecuteReader(); ^
    $dt=New-Object System.Data.DataTable; ^
    $dt.Load($r); ^
    $c.Close(); ^
    $dt | Format-Table -AutoSize"

echo.
echo Todo listo.
pause












