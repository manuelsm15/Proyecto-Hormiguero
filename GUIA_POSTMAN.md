# Guía para Usar el Proyecto desde Postman

## 📥 Importar Colección en Postman

### Opción 1: Importar Archivo JSON

1. Abre Postman
2. Haz clic en **"Import"** (botón arriba a la izquierda)
3. Selecciona **"File"**
4. Navega a la carpeta del proyecto
5. Selecciona el archivo: **`POSTMAN_COLLECTION.json`**
6. Haz clic en **"Import"**

### Opción 2: Importar desde URL (si subes el archivo)

Si subes el archivo a GitHub o algún lugar público, puedes importarlo directamente desde la URL.

---

## 🚀 Configuración Inicial

### 1. Iniciar el Servidor

Antes de probar en Postman, asegúrate de que el servidor está corriendo:

```powershell
cd "C:\Users\manue\Proyecto Hormiguero"
python main.py
```

Espera a ver:
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Configurar Variable de Entorno en Postman

1. En Postman, haz clic en el icono de **"Environments"** (manejo de entorno)
2. Crea un nuevo ambiente llamado **"Local Development"**
3. Agrega estas variables:
   - **Variable**: `base_url`
   - **Valor inicial**: `http://localhost:8000`
   - **Valor actual**: `http://localhost:8000`

4. Selecciona este ambiente en el dropdown superior

---

## 📋 Endpoints Disponibles en la Colección

### 📊 Información General

#### **GET /** - Endpoint Raíz
- **URL**: `http://localhost:8000/`
- **Descripción**: Información básica del subsistema
- **Respuesta esperada**: `{"message": "Subsistema de Recolección..."}`

#### **GET /health** - Health Check
- **URL**: `http://localhost:8000/health`
- **Descripción**: Estado del sistema y servicios
- **Respuesta esperada**: Estado de salud y disponibilidad de servicios

---

### 🍎 Alimentos

#### **GET /alimentos** - Listar Todos
- **URL**: `http://localhost:8000/alimentos`
- **Query Params** (opcionales):
  - `zona_id` (int): Filtrar por zona
  - `estado` (string): `disponible`, `en_proceso`, `recolectado`

**Ejemplo con filtros:**
```
GET http://localhost:8000/alimentos?zona_id=1&estado=disponible
```

---

### 📝 Tareas

#### **POST /tareas** - Crear Tarea
- **URL**: `http://localhost:8000/tareas`
- **Method**: POST
- **Query Params** (opcionales):
  - `tarea_id` (string): ID único (si no se proporciona, se genera automáticamente)
  - `alimento_id` (string): ID del alimento (si no se proporciona, usa "A1" por defecto)

**Ejemplos:**
```
POST http://localhost:8000/tareas
POST http://localhost:8000/tareas?tarea_id=mi_tarea&alimento_id=A1
```

#### **GET /tareas** - Listar Todas
- **URL**: `http://localhost:8000/tareas`
- **Descripción**: Retorna todas las tareas (activas + completadas)

#### **GET /tareas/activas** - Solo Activas
- **URL**: `http://localhost:8000/tareas/activas`

#### **GET /tareas/completadas** - Solo Completadas
- **URL**: `http://localhost:8000/tareas/completadas`

#### **GET /tareas/en-proceso** - En Proceso
- **URL**: `http://localhost:8000/tareas/en-proceso`

#### **POST /tareas/{id}/iniciar** - Iniciar Tarea
- **URL**: `http://localhost:8000/tareas/tarea_001/iniciar`
- **Method**: POST
- **Path Variable**: Reemplaza `tarea_001` con el ID real de tu tarea

#### **POST /tareas/{id}/completar** - Completar Tarea
- **URL**: `http://localhost:8000/tareas/tarea_001/completar?cantidad_recolectada=10`
- **Method**: POST
- **Query Param**: `cantidad_recolectada` (int): Cantidad recolectada

#### **GET /tareas/{id}/tiempo-restante** - Tiempo Restante
- **URL**: `http://localhost:8000/tareas/tarea_001/tiempo-restante`

#### **GET /tareas/{id}/progreso** - Progreso
- **URL**: `http://localhost:8000/tareas/tarea_001/progreso`

---

### 💾 Base de Datos

#### **GET /tareas/bd** - Tareas desde BD
- **URL**: `http://localhost:8000/tareas/bd`
- **Descripción**: Retorna todas las tareas desde la base de datos SQLite

#### **GET /tareas/{id}/bd** - Tarea Específica desde BD
- **URL**: `http://localhost:8000/tareas/tarea_001/bd`

---

### ⚙️ Procesamiento

#### **POST /procesar** - Proceso Automático Completo
- **URL**: `http://localhost:8000/procesar`
- **Method**: POST
- **Descripción**: Ejecuta el proceso completo:
  - Consulta alimentos disponibles
  - Crea tareas de recolección
  - Solicita hormigas
  - Inicia recolección
  - Completa tareas
  - Devuelve hormigas con alimento

**No requiere body**, ejecuta todo automáticamente.

#### **POST /verificar-hormigas** - Verificar Hormigas Muertas
- **URL**: `http://localhost:8000/verificar-hormigas`
- **Method**: POST

---

### 📈 Estadísticas

#### **GET /estadisticas** - Estadísticas del Sistema
- **URL**: `http://localhost:8000/estadisticas`
- **Descripción**: Retorna estadísticas combinadas de memoria y base de datos

#### **GET /eventos** - Eventos Recientes
- **URL**: `http://localhost:8000/eventos?limite=10`
- **Query Param**: `limite` (int, 1-1000): Cantidad de eventos a retornar

---

## 🎯 Flujo de Prueba Recomendado en Postman

### 1. Verificar Estado del Sistema
```
GET http://localhost:8000/health
```
✅ Debe retornar status `200` con `"status": "healthy"`

### 2. Consultar Alimentos Disponibles
```
GET http://localhost:8000/alimentos
```
✅ Debe retornar una lista de alimentos (puede estar vacía si no hay mock configurado)

### 3. Crear una Tarea
```
POST http://localhost:8000/tareas
```
✅ Debe crear una tarea y retornar el objeto `TareaRecoleccion`

### 4. Ver la Tarea Creada
```
GET http://localhost:8000/tareas
```
✅ Debe mostrar la tarea recién creada

### 5. Procesar Recolección Automática
```
POST http://localhost:8000/procesar
```
✅ Ejecuta el proceso completo y retorna las tareas procesadas

### 6. Ver Estadísticas
```
GET http://localhost:8000/estadisticas
```
✅ Muestra estadísticas actualizadas

### 7. Ver Eventos
```
GET http://localhost:8000/eventos?limite=10
```
✅ Muestra los últimos eventos del sistema

---

## 🔧 Configuración Avanzada en Postman

### Variables de Colección

Puedes usar estas variables en las URLs:

- `{{base_url}}` - URL base (por defecto: `http://localhost:8000`)
- `{{tarea_id}}` - ID de tarea actual (por defecto: `tarea_001`)

### Scripts Pre-request (Opcional)

Puedes agregar scripts para automatizar:

```javascript
// En el tab "Pre-request Script"
pm.environment.set("timestamp", Date.now());
```

### Tests Automáticos (Opcional)

```javascript
// En el tab "Tests"
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

---

## 📝 Ejemplos de Respuestas

### Respuesta de Health Check
```json
{
  "status": "healthy",
  "service": "subsistema-recoleccion",
  "version": "1.0.0",
  "entorno_disponible": true,
  "comunicacion_disponible": true
}
```

### Respuesta de Tarea Creada
```json
{
  "id": "tarea_20251029_104530",
  "alimento": {
    "id": "A1",
    "nombre": "Fruta",
    "cantidad_hormigas_necesarias": 3,
    "puntos_stock": 10,
    "tiempo_recoleccion": 300,
    "disponible": true
  },
  "hormigas_asignadas": [],
  "estado": "pendiente",
  "fecha_inicio": null,
  "fecha_fin": null,
  "alimento_recolectado": 0
}
```

### Respuesta de Estadísticas
```json
{
  "tareas_activas": 0,
  "tareas_completadas": 0,
  "total_alimento_recolectado": 0,
  "base_datos": {
    "tareas": {
      "total": 1,
      "activas": 1,
      "completadas": 0
    },
    "alimentos": {
      "total": 0,
      "disponibles": 0
    },
    "mensajes": {
      "total": 0
    },
    "eventos": {
      "total": 2
    },
    "fecha_consulta": "2025-10-29T10:45:18.297159"
  },
  "tareas_memoria": {
    "activas": 0,
    "completadas": 0
  }
}
```

---

## 🐛 Solución de Problemas

### Error: "Could not get response"

**Causa**: El servidor no está corriendo

**Solución**: 
1. Verifica que el servidor esté activo: `python main.py`
2. Verifica que esté en el puerto 8000
3. Verifica la URL en Postman: `http://localhost:8000`

### Error: "Connection refused"

**Causa**: Servidor no iniciado o puerto incorrecto

**Solución**: Inicia el servidor y verifica el puerto

### Error 500: "Servicio de entorno no disponible"

**Causa**: El sistema está intentando usar servicios reales que no responden

**Solución**: Limpia las variables de entorno en PowerShell:
```powershell
$env:BASE_API_URL=""
$env:USE_REAL_ENTORNO=""
```
Luego reinicia el servidor.

---

## ✅ Lista de Verificación

- [ ] Servidor iniciado (`python main.py`)
- [ ] Colección importada en Postman
- [ ] Ambiente configurado con `base_url = http://localhost:8000`
- [ ] Health check retorna 200
- [ ] Puedo ver/listar tareas
- [ ] Puedo crear tareas
- [ ] Puedo procesar recolección

---

## 📚 Recursos Adicionales

- **Documentación Interactiva**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Archivo de Colección**: `POSTMAN_COLLECTION.json`

---

**¡Ya estás listo para probar el sistema completo desde Postman!** 🚀



