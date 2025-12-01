# 📊 Resumen de Implementación de Allure en Pruebas Automáticas

Este documento resume la implementación completa de Allure para guardar los resultados de las pruebas automáticas del sistema de lotes de hormigas.

---

## ✅ Implementación Completada

### 1. Guardado Automático en Allure

**Ubicación:** `allure-results/`

**Formato:** Cada prueba genera 3 archivos JSON:
- `{uuid}-result.json` - Resultado de la prueba (estado, descripción, attachments)
- `{uuid}-attachment-request.json` - Request completo (método, URL, body)
- `{uuid}-attachment-response.json` - Response completo (status code, body)

**Estados guardados:**
- `passed` - Prueba exitosa (status code < 400)
- `failed` - Prueba fallida (status code >= 400)
- `broken` - Error de conexión o excepción

---

### 2. Scripts Creados

#### `scripts/prueba_completa_sistema_lotes.py`
- ✅ Ejecuta 12 pruebas completas del sistema
- ✅ Guarda cada prueba en Allure automáticamente
- ✅ Verifica que el servicio esté disponible antes de ejecutar
- ✅ Intenta generar reporte HTML al finalizar

#### `scripts/iniciar_servicio.ps1` y `.bat`
- ✅ Inicia el servidor FastAPI
- ✅ Verifica que el puerto 8000 esté disponible
- ✅ Muestra instrucciones claras

#### `scripts/iniciar_servicio_y_pruebas.ps1`
- ✅ Inicia el servidor en segundo plano
- ✅ Ejecuta las pruebas automáticamente
- ✅ Detiene el servidor al finalizar

---

### 3. Documentación Creada

- ✅ `ALLURE_PRUEBAS_AUTOMATICAS.md` - Guía completa de Allure
- ✅ `GUIA_INICIO_RAPIDO.md` - Guía de inicio rápido
- ✅ `PROCESOS_PRUEBAS_SISTEMA_LOTES.md` - Documentación de todos los procesos

---

## 🚀 Cómo Usar

### Método Rápido (Todo Automático)

```powershell
.\scripts\iniciar_servicio_y_pruebas.ps1
```

### Método Manual (Dos Terminales)

**Terminal 1:**
```powershell
.\scripts\iniciar_servicio.ps1
```

**Terminal 2:**
```bash
python scripts/prueba_completa_sistema_lotes.py
```

---

## 📊 Pruebas Guardadas en Allure

Cada una de estas 12 pruebas se guarda automáticamente:

1. **Health Check** - Verificar salud del servicio
2. **Crear Alimento** - Crear un alimento para pruebas
3. **Crear Tarea** - Crear una tarea de recolección
4. **Verificar Estado Inicial** - Verificar estado inicial de la tarea
5. **Asignar Hormigas - Cantidad Insuficiente** - Intentar asignar con cantidad menor (debe fallar)
6. **Asignar Hormigas - Cantidad Suficiente** - Asignar con cantidad suficiente
7. **Verificar Estado Después de Asignación** - Verificar estado después de asignar
8. **Iniciar Tarea** - Iniciar la tarea de recolección
9. **Verificar Tiempo Restante** - Verificar tiempo restante
10. **Verificar Completado Automático** - Verificar que la tarea se completó automáticamente
11. **Verificar Todas las Tareas** - Verificar todas las tareas del sistema
12. **Verificar Estadísticas** - Verificar estadísticas del sistema

---

## 📁 Estructura de Resultados

```
allure-results/
├── 550e8400-e29b-41d4-a716-446655440000-result.json
├── 550e8400-e29b-41d4-a716-446655440000-attachment-request.json
├── 550e8400-e29b-41d4-a716-446655440000-attachment-response.json
├── 660e8400-e29b-41d4-a716-446655440001-result.json
├── 660e8400-e29b-41d4-a716-446655440001-attachment-request.json
└── 660e8400-e29b-41d4-a716-446655440001-attachment-response.json
...
```

---

## 🔍 Ver Resultados

### Opción 1: Resultados JSON (Sin Allure CLI)

Los resultados están en formato JSON legible en `allure-results/`. Puedes:
- Leerlos directamente
- Usar un visor JSON
- Procesarlos con scripts

### Opción 2: Reporte HTML (Con Allure CLI)

```bash
# Generar reporte
python scripts/generate_allure_report.py

# O manualmente
allure generate allure-results --clean -o allure-report
allure open allure-report
```

### Opción 3: Servir Reporte en Tiempo Real

```bash
allure serve allure-results
```

---

## ⚙️ Configuración

### Directorio de Resultados

Configurado en `allure.properties`:
```properties
allure.results.directory=allure-results
```

### Script de Pruebas

El script crea automáticamente el directorio si no existe:
```python
ALLURE_RESULTS_DIR = Path("allure-results")
ALLURE_RESULTS_DIR.mkdir(exist_ok=True)
```

---

## 🔄 Flujo Completo

```
1. Usuario ejecuta: python scripts/prueba_completa_sistema_lotes.py
   ↓
2. Script verifica que el servicio esté disponible
   ↓
3. Para cada prueba:
   - Ejecuta la petición HTTP
   - Guarda request en Allure
   - Guarda response en Allure
   - Guarda resultado (passed/failed/broken)
   ↓
4. Al finalizar:
   - Intenta generar reporte HTML
   - Muestra resumen de pruebas
   ↓
5. Resultados disponibles en:
   - allure-results/ (JSON)
   - allure-report/ (HTML, si se generó)
```

---

## 📝 Ejemplo de Resultado JSON

```json
{
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Crear Alimento",
  "status": "passed",
  "description": "POST http://localhost:8000/alimentos",
  "start": 1705704196000,
  "stop": 1705704196100,
  "steps": [],
  "attachments": [
    {
      "name": "Request",
      "source": "550e8400-e29b-41d4-a716-446655440000-attachment-request.json",
      "type": "application/json"
    },
    {
      "name": "Response",
      "source": "550e8400-e29b-41d4-a716-446655440000-attachment-response.json",
      "type": "application/json"
    }
  ]
}
```

---

## ✅ Validaciones Implementadas

1. ✅ **Verificación de Servicio:** El script verifica que el servicio esté disponible antes de ejecutar
2. ✅ **Manejo de Errores:** Los errores se guardan como pruebas "broken" en Allure
3. ✅ **Attachments:** Request y Response se guardan como attachments
4. ✅ **Estados Correctos:** Los estados se asignan correctamente según el resultado
5. ✅ **Generación Automática:** Intenta generar el reporte HTML automáticamente

---

## 🎯 Próximos Pasos

1. **Ejecutar el script** para verificar que todo funciona
2. **Revisar resultados** en `allure-results/`
3. **Generar reporte HTML** (si Allure CLI está instalado)
4. **Integrar en CI/CD** (opcional)

---

**Última actualización:** 2024-01-15

