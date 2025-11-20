# 🚀 Guía de Inicio Rápido - Pruebas del Sistema

Esta guía te ayudará a iniciar el servicio y ejecutar las pruebas completas del sistema de lotes de hormigas.

---

## 📋 Pasos para Ejecutar las Pruebas

### Opción 1: Todo Automático (Recomendado)

**Inicia el servidor y ejecuta las pruebas automáticamente:**
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

#### Paso 1: Iniciar el Servidor

**Terminal 1 - Script PowerShell (Recomendado en Windows)**
```powershell
.\scripts\iniciar_servicio.ps1
```

**O Script Batch:**
```cmd
scripts\iniciar_servicio.bat
```

**O Manualmente:**
```bash
python main.py
```

**Verificar que el servidor está corriendo:**
- Abre tu navegador en: `http://localhost:8000/docs`
- O verifica con: `Invoke-RestMethod -Uri "http://localhost:8000/health"`

---

#### Paso 2: Ejecutar las Pruebas

**Terminal 2** (deja el servidor corriendo en la Terminal 1):

```bash
python scripts/prueba_completa_sistema_lotes.py
```

El script automáticamente:
- ✅ Verifica que el servicio esté disponible (si no, muestra instrucciones)
- ✅ Ejecuta todas las pruebas
- ✅ Guarda resultados en Allure
- ✅ Intenta generar el reporte HTML

---

### Paso 3: Ver los Resultados

#### Opción A: Ver Resultados JSON Directamente

Los resultados están en formato JSON legible:
```
allure-results/
├── {uuid}-result.json
├── {uuid}-attachment-request.json
└── {uuid}-attachment-response.json
```

#### Opción B: Generar Reporte HTML (Requiere Allure CLI)

**Si tienes Allure CLI instalado:**
```bash
python scripts/generate_allure_report.py
allure open allure-report
```

**Si NO tienes Allure CLI:**
- Los resultados JSON están en `allure-results/`
- Puedes leerlos directamente o instalar Allure CLI más tarde

---

## 🔧 Instalar Allure CLI (Opcional)

### Windows (con Chocolatey)
```powershell
choco install allure-commandline
```

### Windows (Manual)
1. Descargar desde: https://github.com/allure-framework/allure2/releases
2. Extraer y agregar a PATH
3. Verificar: `allure --version`

### Linux/Mac
```bash
# Linux
sudo apt-get install allure

# Mac
brew install allure
```

---

## 📊 Estructura de Pruebas

Las pruebas ejecutan el siguiente flujo:

1. ✅ Health Check
2. ✅ Crear Alimento
3. ✅ Crear Tarea
4. ✅ Verificar Estado Inicial
5. ❌ Intentar Asignar con Cantidad Insuficiente (debe fallar)
6. ✅ Asignar con Cantidad Suficiente
7. ✅ Verificar Estado Después de Asignación
8. ✅ Iniciar Tarea
9. ✅ Verificar Tiempo Restante
10. ✅ Esperar y Verificar Completado Automático
11. ✅ Verificar Todas las Tareas
12. ✅ Verificar Estadísticas

---

## 🐛 Solución de Problemas

### Error: "No se puede establecer una conexión"

**Causa:** El servidor no está corriendo.

**Solución:**
1. Inicia el servidor primero (Paso 1)
2. Verifica que esté en `http://localhost:8000`
3. Ejecuta las pruebas nuevamente

### Error: "Puerto 8000 ya está en uso"

**Solución:**
```powershell
# Ver qué proceso está usando el puerto
netstat -ano | findstr :8000

# Cerrar el proceso (reemplaza PID con el número del proceso)
taskkill /PID <PID> /F
```

### Error: "allure: command not found"

**Solución:**
- Los resultados se guardan en `allure-results/` aunque no tengas Allure CLI
- Puedes leer los JSON directamente
- O instala Allure CLI (ver arriba)

---

## 📝 Ejemplo de Ejecución Completa

```powershell
# Terminal 1: Iniciar servidor
.\scripts\iniciar_servicio.ps1

# Terminal 2: Ejecutar pruebas
python scripts/prueba_completa_sistema_lotes.py

# Terminal 2: Ver reporte (si Allure CLI está instalado)
python scripts/generate_allure_report.py
allure open allure-report
```

---

## ✅ Verificación Rápida

**¿El servidor está corriendo?**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

**¿Las pruebas se ejecutaron?**
```powershell
Test-Path "allure-results"
Get-ChildItem "allure-results" | Measure-Object
```

**¿Se generó el reporte?**
```powershell
Test-Path "allure-report/index.html"
```

---

**Última actualización:** 2024-01-15

