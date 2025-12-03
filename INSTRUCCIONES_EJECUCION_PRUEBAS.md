# 🚀 Instrucciones para Ejecutar las Pruebas Completas

Esta guía te muestra cómo ejecutar las pruebas completas del sistema de lotes de hormigas con guardado automático en Allure.

---

## ⚡ Inicio Rápido

### Opción 1: Todo Automático (Recomendado)

```powershell
.\scripts\iniciar_servicio_y_pruebas.ps1
```

Este script:
- ✅ Inicia el servidor en segundo plano
- ✅ Espera a que esté disponible
- ✅ Ejecuta todas las pruebas
- ✅ Guarda resultados en Allure
- ✅ Detiene el servidor al finalizar

---

### Opción 2: Manual (Dos Terminales)

**Terminal 1 - Iniciar Servidor:**
```powershell
.\scripts\iniciar_servicio.ps1
```

**Terminal 2 - Ejecutar Pruebas:**
```bash
python scripts/prueba_completa_sistema_lotes.py
```

---

## 📋 Pruebas que se Ejecutan

El script ejecuta **12 pruebas completas**:

1. ✅ **Health Check** - Verificar salud del servicio
2. ✅ **Crear Alimento** - Crear un alimento para pruebas
3. ✅ **Crear Tarea** - Crear una tarea de recolección
4. ✅ **Verificar Estado Inicial** - Verificar estado inicial de la tarea
5. ❌ **Asignar Hormigas - Cantidad Insuficiente** - Intentar asignar con cantidad menor (debe fallar)
6. ✅ **Asignar Hormigas - Cantidad Suficiente** - Asignar con cantidad suficiente
7. ✅ **Verificar Estado Después de Asignación** - Verificar estado después de asignar
8. ✅ **Iniciar Tarea** - Iniciar la tarea de recolección
9. ✅ **Verificar Tiempo Restante** - Verificar tiempo restante
10. ✅ **Verificar Completado Automático** - Esperar y verificar que la tarea se completó automáticamente
11. ✅ **Verificar Todas las Tareas** - Verificar todas las tareas del sistema
12. ✅ **Verificar Estadísticas** - Verificar estadísticas del sistema

---

## 📊 Resultados Guardados en Allure

### Ubicación
```
allure-results/
├── {uuid}-result.json              # Resultado de cada prueba
├── {uuid}-attachment-request.json  # Request completo
└── {uuid}-attachment-response.json  # Response completo
```

### Información Guardada

Cada prueba guarda:
- ✅ **Nombre de la prueba**
- ✅ **Estado** (passed/failed/broken)
- ✅ **Request completo** (método, URL, body)
- ✅ **Response completo** (status code, body)
- ✅ **Tiempo de ejecución**
- ✅ **Errores** (si los hay)

---

## 🔍 Ver Resultados

### Opción 1: Resultados JSON (Sin Allure CLI)

Los resultados están en formato JSON legible:
```powershell
Get-ChildItem allure-results\*.json | Select-Object Name
```

Puedes leerlos directamente o usar un visor JSON.

### Opción 2: Reporte HTML (Con Allure CLI)

```bash
# Generar reporte
python scripts/generate_allure_report.py

# Abrir reporte
allure open allure-report
```

**Nota:** Si Allure CLI no está instalado, los resultados JSON están disponibles en `allure-results/`.

---

## 📝 Ejemplo de Ejecución Completa

```powershell
# Paso 1: Iniciar servidor (Terminal 1)
.\scripts\iniciar_servicio.ps1

# Paso 2: Ejecutar pruebas (Terminal 2)
python scripts/prueba_completa_sistema_lotes.py

# Paso 3: Ver resultados
# Opción A: Leer JSON directamente
Get-Content allure-results\*.json

# Opción B: Generar reporte HTML (si Allure CLI está instalado)
python scripts/generate_allure_report.py
allure open allure-report
```

---

## 🐛 Solución de Problemas

### Error: "El servicio no está disponible"

**Solución:**
1. Inicia el servidor primero: `.\scripts\iniciar_servicio.ps1`
2. Verifica que esté en `http://localhost:8000`
3. Ejecuta las pruebas nuevamente

### Error: "No se pudo crear la tarea"

**Posibles causas:**
- El alimento no existe en la base de datos
- El alimento no está disponible

**Solución:**
- El script automáticamente busca un alimento disponible si el creado no se encuentra
- Verifica que haya alimentos disponibles: `Invoke-RestMethod -Uri "http://localhost:8000/alimentos"`

### Error: "Puerto 8000 ya está en uso"

**Solución:**
```powershell
# Ver qué proceso está usando el puerto
netstat -ano | findstr :8000

# Cerrar el proceso (reemplaza PID)
taskkill /PID <PID> /F
```

---

## ✅ Validaciones Incluidas

El script valida:
- ✅ Cantidad de hormigas suficiente vs requerida
- ✅ Lote no en uso
- ✅ Lote existe antes de usarlo
- ✅ Alimento disponible antes de crear tarea
- ✅ Completado automático por tiempo

---

## 📈 Información en Allure

Cada prueba en Allure incluye:

1. **Request completo:**
   - Método HTTP
   - URL
   - Body (si aplica)

2. **Response completo:**
   - Status code
   - Body completo

3. **Estado:**
   - `passed` - Prueba exitosa
   - `failed` - Prueba fallida (status >= 400)
   - `broken` - Error de conexión

---

## 🎯 Próximos Pasos

1. **Ejecutar las pruebas:**
   ```powershell
   python scripts/prueba_completa_sistema_lotes.py
   ```

2. **Revisar resultados:**
   - JSON: `allure-results/`
   - HTML: `allure-report/index.html` (si se generó)

3. **Integrar en CI/CD** (opcional):
   - Los resultados JSON se pueden procesar automáticamente
   - El reporte HTML se puede publicar como artifact

---

**Última actualización:** 2024-01-15

