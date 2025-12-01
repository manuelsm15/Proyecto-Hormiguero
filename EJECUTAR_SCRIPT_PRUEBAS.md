# Cómo Ejecutar el Script de Pruebas

## Problema de Política de Ejecución

Si recibes el error:
```
No se puede cargar el archivo... El archivo no está firmado digitalmente.
```

Es porque PowerShell tiene una política de ejecución restrictiva.

## Soluciones

### Opción 1: Ejecutar con Bypass (Recomendado)

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\iniciar_servicio_y_pruebas.ps1"
```

### Opción 2: Cambiar Política Temporalmente (Solo para esta sesión)

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\scripts\iniciar_servicio_y_pruebas.ps1
```

### Opción 3: Ejecutar Pruebas Directamente (Si el servicio ya está corriendo)

```powershell
python scripts/prueba_completa_sistema_lotes.py
```

## Funcionalidades del Script

El script `iniciar_servicio_y_pruebas.ps1` ahora:

1. ✅ **Detecta si el servicio ya está corriendo**
   - Si el puerto 8000 está en uso, verifica si el servicio responde
   - Si el servicio está disponible, lo usa sin iniciar uno nuevo
   - Si no está disponible, inicia un nuevo servidor

2. ✅ **Ejecuta todas las pruebas automáticamente**
   - Crea alimento
   - Crea tarea
   - Asigna hormigas (prueba cantidad insuficiente y suficiente)
   - Inicia tarea
   - Verifica estados
   - Guarda resultados en Allure

3. ✅ **Limpia recursos solo si los inició**
   - Solo detiene el servidor si lo inició el script
   - Si el servicio ya estaba corriendo, no lo detiene

## Resultados

Todos los resultados se guardan automáticamente en:
- `allure-results/` - Resultados JSON de cada prueba

Para generar el reporte HTML:
```bash
python scripts/generate_allure_report.py
allure open allure-report
```

