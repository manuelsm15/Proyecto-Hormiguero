@echo off
echo ========================================
echo Verificar contenido en SQL Server (Hormiguero)
echo ========================================
echo.
set "SERVER=SHIRORYUU"
set "INSTANCE=MSSQLSERVER"
set "DATABASE=Hormiguero"

REM Normalizar destino del servidor: si es instancia por defecto, no usar "\\MSSQLSERVER"
set "SERVER_TARGET=%SERVER%"
if /I not "%INSTANCE%"=="MSSQLSERVER" set "SERVER_TARGET=%SERVER%\%INSTANCE%"

echo Probando conexion a %SERVER_TARGET% ...
powershell -NoProfile -Command "$cn='Server=%SERVER_TARGET%;Database=master;Integrated Security=True;TrustServerCertificate=True';$c=New-Object System.Data.SqlClient.SqlConnection $cn;try{$c.Open();Write-Host 'Conexion OK';}catch{Write-Host 'Fallo de conexion:' $_.Exception.Message}finally{$c.Close()}"
echo.
echo Tablas existentes:
powershell -NoProfile -Command "$cn='Server=%SERVER_TARGET%;Database=%DATABASE%;Integrated Security=True;TrustServerCertificate=True';$c=New-Object System.Data.SqlClient.SqlConnection $cn;try{$c.Open();$r=($c.CreateCommand());$r.CommandText='SELECT s.name AS SchemaName,t.name AS TableName FROM sys.tables t JOIN sys.schemas s ON t.schema_id=s.schema_id ORDER BY s.name,t.name';$dr=$r.ExecuteReader();$dt=New-Object System.Data.DataTable;$dt.Load($dr);$dt | Format-Table -AutoSize}catch{Write-Host 'Error:' $_.Exception.Message}finally{$c.Close()}"
echo.
echo Contenido de dbo.Alimentos (top 50):
powershell -NoProfile -Command "$cn='Server=%SERVER_TARGET%;Database=%DATABASE%;Integrated Security=True;TrustServerCertificate=True';$q='SELECT TOP 50 id,nombre,tipo,estado,cantidad_unitaria,created_at FROM dbo.Alimentos ORDER BY id DESC';$c=New-Object System.Data.SqlClient.SqlConnection $cn;try{$c.Open();$cmd=$c.CreateCommand();$cmd.CommandText=$q;$dr=$cmd.ExecuteReader();$dt=New-Object System.Data.DataTable;$dt.Load($dr);$dt | Format-Table -AutoSize}catch{Write-Host 'Error:' $_.Exception.Message}finally{$c.Close()}"
echo.
echo Contenido de dbo.Tareas (top 50):
powershell -NoProfile -Command "$cn='Server=%SERVER_TARGET%;Database=%DATABASE%;Integrated Security=True;TrustServerCertificate=True';$q='SELECT TOP 50 id,alimento_id,estado,cantidad_recolectada,hormigas_asignadas,inicio,fin,created_at FROM dbo.Tareas ORDER BY created_at DESC';$c=New-Object System.Data.SqlClient.SqlConnection $cn;try{$c.Open();$cmd=$c.CreateCommand();$cmd.CommandText=$q;$dr=$cmd.ExecuteReader();$dt=New-Object System.Data.DataTable;$dt.Load($dr);$dt | Format-Table -AutoSize}catch{Write-Host 'Error:' $_.Exception.Message}finally{$c.Close()}"
echo.
echo Contenido de dbo.Eventos (top 50):
powershell -NoProfile -Command "$cn='Server=%SERVER_TARGET%;Database=%DATABASE%;Integrated Security=True;TrustServerCertificate=True';$q='SELECT TOP 50 id,tipo,descripcion,creado_en FROM dbo.Eventos ORDER BY id DESC';$c=New-Object System.Data.SqlClient.SqlConnection $cn;try{$c.Open();$cmd=$c.CreateCommand();$cmd.CommandText=$q;$dr=$cmd.ExecuteReader();$dt=New-Object System.Data.DataTable;$dt.Load($dr);$dt | Format-Table -AutoSize}catch{Write-Host 'Error:' $_.Exception.Message}finally{$c.Close()}"
echo.
echo Contenido de dbo.Mensajes (top 50):
powershell -NoProfile -Command "$cn='Server=%SERVER_TARGET%;Database=%DATABASE%;Integrated Security=True;TrustServerCertificate=True';$q='SELECT TOP 50 id,origen,destino,LEFT(CONVERT(NVARCHAR(MAX),contenido),120) AS contenido,creado_en FROM dbo.Mensajes ORDER BY id DESC';$c=New-Object System.Data.SqlClient.SqlConnection $cn;try{$c.Open();$cmd=$c.CreateCommand();$cmd.CommandText=$q;$dr=$cmd.ExecuteReader();$dt=New-Object System.Data.DataTable;$dt.Load($dr);$dt | Format-Table -AutoSize}catch{Write-Host 'Error:' $_.Exception.Message}finally{$c.Close()}"
echo.
pause


