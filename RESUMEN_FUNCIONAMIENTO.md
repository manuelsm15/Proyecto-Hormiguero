# Resumen del Funcionamiento del Subsistema

## Estado Actual

El sistema esta funcionando correctamente. A continuacion el resumen:

## Servidor

- **URL**: http://localhost:8000
- **Estado**: ✅ Funcionando
- **Version**: 1.0.0
- **Servicios**: Entorno y Comunicacion disponibles

## Funcionalidades Implementadas

### ✅ Endpoints Disponibles

#### 1. **Informacion General**
- `GET /` - Endpoint raiz
- `GET /health` - Estado del sistema
- `GET /docs` - Documentacion interactiva (Swagger UI) ⭐ **RECOMENDADO**
- `GET /openapi.json` - Esquema OpenAPI

#### 2. **Alimentos/Recursos**
- `GET /alimentos` - Listar todos los alimentos disponibles
- `GET /alimentos?zona_id=1` - Filtrar por zona
- `GET /alimentos?estado=disponible` - Filtrar por estado

#### 3. **Tareas de Recoleccion**
- `POST /tareas` - Crear tarea (con valores por defecto)
- `GET /tareas` - Listar todas las tareas
- `GET /tareas/activas` - Solo tareas activas
- `GET /tareas/completadas` - Solo tareas completadas
- `GET /tareas/en-proceso` - Tareas en proceso
- `POST /tareas/{id}/iniciar` - Iniciar una tarea
- `POST /tareas/{id}/completar` - Completar una tarea
- `GET /tareas/{id}/tiempo-restante` - Tiempo restante
- `GET /tareas/{id}/progreso` - Progreso de la tarea

#### 4. **Persistencia**
- `GET /tareas/bd` - Tareas desde base de datos
- `GET /tareas/{id}/bd` - Tarea especifica desde BD
- `GET /eventos` - Eventos del sistema (limite configurable)

#### 5. **Procesamiento**
- `POST /procesar` - Proceso automatico completo de recoleccion
- `POST /verificar-hormigas` - Verificar hormigas muertas

#### 6. **Estadisticas**
- `GET /estadisticas` - Estadisticas combinadas (memoria + BD)

## Como Probar el Sistema

### Opcion 1: Documentacion Interactiva (Recomendado) ⭐

**Abre en tu navegador:**
```
http://localhost:8000/docs
```

Desde ahí puedes:
- Ver todos los endpoints documentados
- Probar cada endpoint directamente
- Ver ejemplos de request/response
- Ver el esquema completo de la API

### Opcion 2: Scripts de Demostracion

```bash
# Ver funcionamiento completo
python scripts/ver_funcionamiento.py

# Demostracion detallada
python scripts/demo_completa_funcional.py

# Flujo completo paso a paso
python scripts/flujo_completo_demo.py
```

### Opcion 3: Usando PowerShell

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Listar alimentos
Invoke-RestMethod -Uri "http://localhost:8000/alimentos"

# Crear tarea
Invoke-RestMethod -Method POST -Uri "http://localhost:8000/tareas"

# Ver tareas
Invoke-RestMethod -Uri "http://localhost:8000/tareas"

# Estadisticas
Invoke-RestMethod -Uri "http://localhost:8000/estadisticas"
```

### Opcion 4: Usando cURL (si esta instalado)

```bash
curl http://localhost:8000/health
curl http://localhost:8000/alimentos
curl -X POST http://localhost:8000/tareas
curl http://localhost:8000/tareas
```

## Caracteristicas Principales

### ✅ Integracion con Entorno
- Servicio API para conectarse al subsistema de Entorno en Railway
- Filtros por zona y estado
- Actualizacion automatica de recursos recolectados

### ✅ Integracion con Comunicacion/Reina
- Solicitud de hormigas
- Devolucion de hormigas con alimento recolectado
- Manejo de mensajes entre subsistemas

### ✅ Persistencia
- Base de datos SQLite (recoleccion.db)
- Tareas, alimentos, hormigas, mensajes y eventos guardados
- Consultas desde memoria y BD

### ✅ APIs Versatiles
- Valores por defecto en todos los endpoints
- Parametros opcionales para personalizacion
- Filtros flexibles

### ✅ Trazabilidad
- IDs unicos para tareas, alimentos y hormigas
- Eventos registrados en BD
- Consulta de estado en cualquier momento

## Pruebas

### Estado de Pruebas
- ✅ 100 pruebas TDD pasando
- ✅ 4 pruebas de integracion (se saltan si no hay servicios reales)
- ✅ Cobertura de codigo: 62% (meta: 80%+)

### Ejecutar Pruebas

```bash
# Todas las pruebas
pytest tests/ -v --cov=src --cov-report=html

# Solo pruebas de integracion reales
python scripts/run_integration_real.py

# Ver reporte de cobertura
# Abrir: htmlcov/index.html
```

## Base de Datos

La base de datos se encuentra en:
- Archivo: `recoleccion.db`
- Tablas:
  - `alimentos` - Alimentos disponibles
  - `tareas` - Tareas de recoleccion
  - `hormigas` - Hormigas asignadas
  - `asignaciones_hormiga_tarea` - Relaciones hormiga-tarea
  - `mensajes` - Mensajes entre subsistemas
  - `eventos` - Log de actividades

## Configuracion

### Variables de Entorno (Opcional)

Para usar servicios reales en lugar de mocks:

```bash
# Opcion 1: URL base
export BASE_API_URL="https://coloniahormigastdd-production.up.railway.app"
export USE_REAL_ENTORNO="true"
export USE_REAL_COMUNICACION="true"

# Opcion 2: URLs especificas
export ENTORNO_API_URL="https://..."
export COMUNICACION_API_URL="https://..."
```

Si no se configuran, el sistema usa servicios mock automaticamente.

## Resumen

El sistema esta **100% funcional** y listo para:

1. ✅ Desarrollo local con servicios mock
2. ✅ Integracion con servicios reales en Railway
3. ✅ Pruebas automatizadas (TDD + BDD)
4. ✅ Persistencia de datos
5. ✅ Documentacion interactiva
6. ✅ APIs versatiles y flexibles

**La mejor forma de ver todo el funcionamiento es abrir:**
```
http://localhost:8000/docs
```

Alli puedes explorar y probar todos los endpoints de forma interactiva! 🚀



