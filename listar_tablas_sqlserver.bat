@echo off
echo ========================================
echo Listar tablas de SQL Server (BD: Hormiguero)
echo ========================================
echo.
set "SERVER=SHIRORYUU"
set "INSTANCE=MSSQLSERVER"
set "DATABASE=Hormiguero"

set "SERVER_TARGET=%SERVER%"
if /I not "%INSTANCE%"=="MSSQLSERVER" set "SERVER_TARGET=%SERVER%\%INSTANCE%"

powershell -NoProfile -Command "$cn='Server=%SERVER_TARGET%;Database=%DATABASE%;Integrated Security=True;TrustServerCertificate=True';$c=New-Object System.Data.SqlClient.SqlConnection $cn;try{$c.Open();$cmd=$c.CreateCommand();$cmd.CommandText='SELECT s.name AS SchemaName,t.name AS TableName FROM sys.tables t JOIN sys.schemas s ON t.schema_id=s.schema_id ORDER BY s.name,t.name';$r=$cmd.ExecuteReader();$dt=New-Object System.Data.DataTable;$dt.Load($r);$dt | Format-Table -AutoSize}catch{Write-Host 'Error:' $_.Exception.Message}finally{$c.Close()}"
echo.
pause


