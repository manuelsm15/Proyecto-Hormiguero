-- Script para crear tabla de lotes de hormigas en SQL Server
-- Ejecutar en la base de datos Hormiguero

-- Crear tabla de lotes de hormigas
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.lotes_hormigas') AND type in (N'U'))
BEGIN
    CREATE TABLE dbo.lotes_hormigas (
        lote_id NVARCHAR(100) PRIMARY KEY,
        tarea_id NVARCHAR(100) NOT NULL,
        cantidad_hormigas_enviadas INT NOT NULL,
        cantidad_hormigas_requeridas INT NOT NULL,
        estado NVARCHAR(20) NOT NULL DEFAULT 'pendiente',
        fecha_creacion DATETIME DEFAULT GETDATE(),
        fecha_aceptacion DATETIME,
        FOREIGN KEY (tarea_id) REFERENCES dbo.Tareas(id)
    );
    PRINT 'Tabla lotes_hormigas creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla lotes_hormigas ya existe';
END
GO

-- Modificar tabla asignaciones_hormiga_tarea para incluir lote_id
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.asignaciones_hormiga_tarea') AND type in (N'U'))
BEGIN
    -- Verificar si la columna lote_id ya existe
    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'dbo.asignaciones_hormiga_tarea') AND name = 'lote_id')
    BEGIN
        ALTER TABLE dbo.asignaciones_hormiga_tarea
        ADD lote_id NVARCHAR(100) NULL;
        
        -- Agregar foreign key si la tabla lotes_hormigas existe
        IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'dbo.lotes_hormigas') AND type in (N'U'))
        BEGIN
            ALTER TABLE dbo.asignaciones_hormiga_tarea
            ADD CONSTRAINT FK_asignaciones_lote FOREIGN KEY (lote_id) REFERENCES dbo.lotes_hormigas(lote_id);
        END
        
        PRINT 'Columna lote_id agregada a asignaciones_hormiga_tarea';
    END
    ELSE
    BEGIN
        PRINT 'Columna lote_id ya existe en asignaciones_hormiga_tarea';
    END
END
ELSE
BEGIN
    -- Crear tabla si no existe
    CREATE TABLE dbo.asignaciones_hormiga_tarea (
        id INT IDENTITY(1,1) PRIMARY KEY,
        tarea_id NVARCHAR(100) NOT NULL,
        hormiga_id NVARCHAR(100) NOT NULL,
        lote_id NVARCHAR(100) NULL,
        fecha_asignacion DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (tarea_id) REFERENCES dbo.Tareas(id),
        FOREIGN KEY (hormiga_id) REFERENCES dbo.hormigas(id),
        FOREIGN KEY (lote_id) REFERENCES dbo.lotes_hormigas(lote_id)
    );
    PRINT 'Tabla asignaciones_hormiga_tarea creada exitosamente';
END
GO

PRINT 'Script completado';

