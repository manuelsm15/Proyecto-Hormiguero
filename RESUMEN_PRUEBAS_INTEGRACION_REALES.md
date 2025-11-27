# Resumen: Pruebas de Integración Reales

## Scripts Creados

### 1. `test_integracion_real_completo.py`
Script principal que ejecuta pruebas de integración reales:
- Conecta al servicio FastAPI real (http://localhost:8000)
- Crea datos reales (alimentos, tareas)
- Hace llamadas HTTP reales a los endpoints
- Valida los datos en la base de datos real (SQL Server)
- Muestra evidencias de lo que se guardó

### 2. `ejecutar_pruebas_integracion_reales.py`
Script maestro que:
- Inicia el servicio FastAPI automáticamente
- Ejecuta las pruebas de integración
- Detiene el servicio al finalizar

### 3. `ejecutar_pruebas_integracion_reales.ps1`
Script PowerShell alternativo para Windows

## Cómo Ejecutar

### Opción 1: Servicio ya corriendo
```bash
python test_integracion_real_completo.py
```

### Opción 2: Iniciar servicio automáticamente
```bash
python ejecutar_pruebas_integracion_reales.py
```

### Opción 3: PowerShell (Windows)
```powershell
.\ejecutar_pruebas_integracion_reales.ps1
```

## Proceso de Pruebas

1. **Verificar Salud del Servicio**: Health check
2. **Crear Alimento Real**: POST /alimentos
3. **Crear Tarea Real**: POST /tareas
4. **Asignar Hormigas con Lote**: POST /tareas/{id}/asignar-hormigas
5. **Verificar Status**: GET /tareas/{id}/status
6. **Iniciar Tarea** (si no se inició automáticamente): POST /tareas/{id}/iniciar
7. **Completar Tarea**: POST /tareas/{id}/completar
8. **Consultar Evidencias en BD Real**: Consulta directa a SQL Server

## Evidencias Generadas

- Datos guardados en SQL Server (SHIRORYUU / Hormiguero)
- Validación de columna `hormigas_asignadas`
- Verificación de lotes de hormigas
- Confirmación de asignaciones

## Notas

- Las pruebas usan el proceso real, no simulaciones
- Los datos se guardan en la base de datos real
- El servicio debe estar corriendo o se iniciará automáticamente
- Todas las evidencias se muestran en la consola



