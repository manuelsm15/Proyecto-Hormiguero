# Configuración para Railway - Integración con Subsistemas

Este documento explica cómo configurar el subsistema de recolección para conectarse con los subsistemas reales desplegados en Railway.

## 🔗 URLs de los Subsistemas

### Subsistema de Entorno
- **Producción**: https://coloniahormigastdd-production.up.railway.app
- **Endpoints**:
  - `GET /resources` - Listar recursos/alimentos
  - `GET /resources/{id}` - Obtener recurso por ID
  - `PUT /resources/{id}` - Actualizar recurso

### Subsistema de Comunicación/Hormiga Reina
- **Producción**: https://coloniahormigastdd-production.up.railway.app
- **Endpoints**:
  - `POST /messages` - Crear/enviar mensajes
  - `GET /messages/{id}` - Consultar mensaje
  - `POST /ants/request` - Solicitar hormigas
  - `GET /ants/response/{message_id}` - Consultar respuesta

## ⚙️ Variables de Entorno

### Opción 1: URLs Individuales

```bash
export ENTORNO_API_URL="https://coloniahormigastdd-production.up.railway.app/api/entorno"
export COMUNICACION_API_URL="https://coloniahormigastdd-production.up.railway.app/api/comunicacion"
export USE_REAL_ENTORNO="true"
export USE_REAL_COMUNICACION="true"
```

### Opción 2: URL Base (Automático)

```bash
export BASE_API_URL="https://coloniahormigastdd-production.up.railway.app"
export USE_REAL_ENTORNO="true"
export USE_REAL_COMUNICACION="true"
```

El sistema intentará detectar automáticamente los endpoints derivando las rutas.

## 🚀 Configuración en Railway

Cuando despliegues este subsistema en Railway, agrega estas variables de entorno en el dashboard:

1. Ve a tu proyecto en Railway
2. Selecciona el servicio de Recolección
3. Ve a "Variables"
4. Agrega:

```
ENTORNO_API_URL=https://coloniahormigastdd-production.up.railway.app/api/entorno
COMUNICACION_API_URL=https://coloniahormigastdd-production.up.railway.app/api/comunicacion
USE_REAL_ENTORNO=true
USE_REAL_COMUNICACION=true
```

O usa la opción simplificada:

```
BASE_API_URL=https://coloniahormigastdd-production.up.railway.app
USE_REAL_ENTORNO=true
USE_REAL_COMUNICACION=true
```

## 🔧 Ajustar Rutas de API

Si los endpoints reales tienen rutas diferentes, actualiza el archivo `main.py`:

```python
# En main.py, línea ~21-22
ENTORNO_API_URL = f"{BASE_API_URL}/resources"  # Ajustar según la API real
COMUNICACION_API_URL = f"{BASE_API_URL}/messages"  # Ajustar según la API real
```

## ✅ Verificación

Para verificar que la conexión funciona:

```bash
# Probar servicio de entorno
curl https://coloniahormigastdd-production.up.railway.app/resources

# Probar servicio de comunicación
curl https://coloniahormigastdd-production.up.railway.app/messages
```

## 📝 Notas

- **Fallback a Mocks**: Si los servicios reales no están disponibles, el sistema automáticamente usará los servicios mock para desarrollo local.
- **Timeouts**: Los servicios tienen un timeout de 30 segundos por defecto.
- **Manejo de Errores**: El sistema maneja automáticamente errores de conexión y marca los servicios como no disponibles si fallan.



