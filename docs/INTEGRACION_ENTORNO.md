# Integración con el Subsistema de Generación de Entorno

Este documento describe cómo el **Subsistema de Recolección de Alimentos** se integra con el **Subsistema de Generación de Entorno** según la especificación proporcionada.

## 📋 Cambios Realizados

### 1. Nuevo Servicio de API (`EntornoAPIService`)

Se creó un nuevo servicio `EntornoAPIService` que se conecta a la API REST del Subsistema de Generación de Entorno usando los siguientes endpoints:

- **GET /resources**: Listar recursos (con filtros opcionales por `zona_id` y `estado`)
- **GET /resources/{id}**: Obtener un recurso específico por ID
- **PUT /resources/{id}**: Actualizar el estado de un recurso (para marcar como recolectado)

### 2. Mapeo de Modelos

El servicio mapea automáticamente los recursos del entorno al modelo `Alimento` del subsistema de recolección:

| Campo Entorno | Campo Alimento | Descripción |
|--------------|----------------|-------------|
| `id` (Integer) | `id` (str) | ID único del recurso |
| `nombre` | `nombre` | Nombre del recurso |
| `cantidad_requerida_hormigas` | `cantidad_hormigas_necesarias` | Hormigas necesarias |
| `duracion_recoleccion` | `tiempo_recoleccion` | Tiempo en segundos |
| `cantidad_unitaria` | `puntos_stock` | Cantidad disponible |
| `estado` | `disponible` | `true` si estado="disponible" |

### 3. Filtrado por Zona y Estado

El servicio ahora permite filtrar recursos por:
- **Zona ID**: Obtener solo recursos de una zona específica
- **Estado**: Filtrar por `disponible`, `en_proceso`, o `recolectado`

### 4. Actualización de Estado de Recursos

Cuando se completa una recolección, el servicio actualiza automáticamente el recurso en el entorno:
- Si `cantidad_unitaria` llega a 0 → estado = `"recolectado"`
- Si `cantidad_unitaria` > 0 pero < cantidad original → estado = `"en_proceso"`
- Si no se modifica → estado = `"disponible"`

## 🔧 Configuración

### Variables de Entorno

El subsistema puede usar el servicio real de entorno o un servicio mock para desarrollo:

```bash
# Usar servicio real de entorno
export ENTORNO_API_URL="http://localhost:8001"
# o
export USE_REAL_ENTORNO="true"
export ENTORNO_API_URL="http://localhost:8001"

# Usar servicio mock (por defecto)
# No configurar ENTORNO_API_URL o configurar USE_REAL_ENTORNO="false"
```

### En Railway

Agregar la variable de entorno:
```
ENTORNO_API_URL=https://tu-subsistema-entorno.railway.app
```

## 📡 Endpoints Actualizados

### GET /alimentos

Consulta recursos del entorno con filtros opcionales:

```bash
# Todos los recursos disponibles
GET /alimentos

# Recursos de una zona específica
GET /alimentos?zona_id=1

# Recursos por estado
GET /alimentos?estado=en_proceso

# Combinación de filtros
GET /alimentos?zona_id=1&estado=disponible
```

**Parámetros de Query:**
- `zona_id` (opcional): ID de la zona
- `estado` (opcional): `disponible`, `en_proceso`, o `recolectado`

**Respuesta:**
```json
[
  {
    "id": "1",
    "nombre": "Fruta",
    "cantidad_hormigas_necesarias": 3,
    "puntos_stock": 10,
    "tiempo_recoleccion": 300,
    "disponible": true,
    "fecha_creacion": "2025-01-15T10:00:00"
  }
]
```

## 🔄 Flujo de Integración

1. **Consulta de Recursos**: El subsistema de recolección consulta recursos disponibles usando `GET /resources`
2. **Creación de Tarea**: Se crea una tarea de recolección para un recurso específico
3. **Procesamiento**: Se procesa la recolección (solicita hormigas, inicia tarea, etc.)
4. **Actualización**: Al completar, se actualiza el recurso usando `PUT /resources/{id}` con el nuevo estado y cantidad

## 🧪 Pruebas

Para probar la integración:

```python
# Ejemplo con servicio mock (por defecto)
python main.py

# Ejemplo con servicio real
export ENTORNO_API_URL="http://localhost:8001"
python main.py
```

## 📝 Notas Importantes

1. **Compatibilidad hacia atrás**: El servicio mock sigue funcionando para desarrollo local
2. **Manejo de errores**: El servicio maneja automáticamente errores de conexión y los marca como no disponible
3. **Timeout**: Las peticiones HTTP tienen un timeout configurable (por defecto 30 segundos)
4. **Estados**: El servicio mapea los estados del entorno a la lógica de disponibilidad del subsistema de recolección

## 🔗 Referencias

- Especificación del Subsistema de Generación de Entorno
- Documentación de la API del entorno: `http://localhost:8001/docs` (o la URL configurada)



