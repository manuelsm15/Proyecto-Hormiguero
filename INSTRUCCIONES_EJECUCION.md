# Instrucciones para Ejecutar y Ver el Funcionamiento

## Opcion 1: Ejecutar con Servicios Mock (Recomendado para Desarrollo Local)

### Paso 1: Asegurate de que no hay variables de entorno configuradas

```powershell
# Limpiar variables si estan configuradas
$env:BASE_API_URL=""
$env:ENTORNO_API_URL=""
$env:COMUNICACION_API_URL=""
$env:USE_REAL_ENTORNO=""
$env:USE_REAL_COMUNICACION=""
```

### Paso 2: Iniciar el servidor

```powershell
cd "C:\Users\manue\Proyecto Hormiguero"
python main.py
```

Veras:
```
Usando servicio mock de entorno (configurar ENTORNO_API_URL para usar servicio real)
Usando servicio mock de comunicacion (configurar COMUNICACION_API_URL para usar servicio real)
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Paso 3: Ver el Funcionamiento

**A. Abrir Documentacion Interactiva (MEJOR OPCION):**

En tu navegador, abre:
```
http://localhost:8000/docs
```

Desde ahi puedes:
- Ver todos los endpoints
- Probar cada uno directamente
- Ver ejemplos y respuestas

**B. Usar Scripts de Demostracion:**

En otra terminal (mientras el servidor esta corriendo):

```powershell
# Ver estado y abrir docs
python scripts/ver_funcionamiento.py

# Demostracion completa
python scripts/demo_completa_funcional.py

# Flujo paso a paso
python scripts/flujo_completo_demo.py
```

**C. Probar Manualmente con PowerShell:**

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Ver alimentos disponibles
Invoke-RestMethod -Uri "http://localhost:8000/alimentos"

# Crear tarea
Invoke-RestMethod -Method POST -Uri "http://localhost:8000/tareas"

# Ver todas las tareas
Invoke-RestMethod -Uri "http://localhost:8000/tareas"

# Procesar recoleccion automatica
Invoke-RestMethod -Method POST -Uri "http://localhost:8000/procesar"

# Ver estadisticas
Invoke-RestMethod -Uri "http://localhost:8000/estadisticas"

# Ver eventos
Invoke-RestMethod -Uri "http://localhost:8000/eventos?limite=10"
```

---

## Opcion 2: Ejecutar con Servicios Reales (Railway)

### Paso 1: Configurar Variables de Entorno

```powershell
# Configurar URL base de Railway
$env:BASE_API_URL="https://coloniahormigastdd-production.up.railway.app"
$env:USE_REAL_ENTORNO="true"
$env:USE_REAL_COMUNICACION="true"
```

O si conoces las URLs especificas:

```powershell
$env:ENTORNO_API_URL="https://coloniahormigastdd-production.up.railway.app/api/entorno"
$env:COMUNICACION_API_URL="https://coloniahormigastdd-production.up.railway.app/api/comunicacion"
```

### Paso 2: Iniciar el servidor

```powershell
python main.py
```

---

## Ver Reportes y Resultados

### Reporte de Cobertura (HTML)

Despues de ejecutar las pruebas, abre en tu navegador:
```
C:\Users\manue\Proyecto Hormiguero\htmlcov\index.html
```

### Resultados de Allure

```powershell
# Generar reporte (si tienes Allure CLI instalado)
allure generate allure-results --clean -o allure-report
allure open allure-report
```

O usar el script:
```powershell
python scripts/generate_allure_report.py
```

---

## Ejecutar Pruebas

### Todas las Pruebas

```powershell
pytest tests/ -v --cov=src --cov-report=html
```

### Solo Pruebas de Integracion Real

```powershell
# Primero configurar URL
$env:BASE_API_URL="https://coloniahormigastdd-production.up.railway.app"
python scripts/run_integration_real.py
```

---

## Solucion de Problemas

### Error: "Servicio de entorno no disponible"

**Causa**: Los servicios reales de Railway no responden o las URLs son incorrectas.

**Solucion**: Usar servicios mock eliminando las variables de entorno:

```powershell
$env:BASE_API_URL=""
$env:ENTORNO_API_URL=""
$env:COMUNICACION_API_URL=""
$env:USE_REAL_ENTORNO=""
$env:USE_REAL_COMUNICACION=""
```

Luego reiniciar el servidor.

### Error: Puerto 8000 en uso

```powershell
# Cambiar puerto en main.py o matar el proceso
# O usar:
python -m uvicorn main:app --port 8001
```

---

## Resumen Rapido

1. **Iniciar servidor**: `python main.py`
2. **Abrir docs**: http://localhost:8000/docs
3. **Probar endpoints**: Desde la documentacion interactiva o scripts

**¡La mejor forma de ver todo es abrir `/docs` en tu navegador!**



