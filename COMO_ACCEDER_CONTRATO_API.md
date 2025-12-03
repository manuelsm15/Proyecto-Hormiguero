# 📄 Cómo Acceder al Contrato de la API (OpenAPI Schema)

El contrato de la API (esquema OpenAPI) define todos los endpoints, modelos de datos, respuestas y validaciones del subsistema de recolección.

---

## 🔍 Formas de Acceder al Contrato

### 1. **Desde el Navegador (Servidor en Ejecución)**

Cuando el servidor está corriendo, puedes acceder directamente al esquema OpenAPI:

#### URL del Esquema JSON:
```
http://localhost:8000/openapi.json
```

#### Documentación Interactiva (Swagger UI):
```
http://localhost:8000/docs
```

#### Documentación Alternativa (ReDoc):
```
http://localhost:8000/redoc
```

---

### 2. **Exportar el Esquema a un Archivo JSON**

Puedes exportar el esquema OpenAPI a un archivo JSON estático para versionarlo o compartirlo:

#### Opción A: Usando el Script de Exportación

```powershell
# Desde el directorio raíz del proyecto
python scripts/export_openapi_schema.py
```

Esto creará un archivo `openapi.json` en la raíz del proyecto.

#### Opción B: Especificar un nombre de archivo personalizado

```powershell
python scripts/export_openapi_schema.py -o mi_contrato_api.json
```

#### Opción C: Descargar desde el Navegador

1. Inicia el servidor: `python main.py`
2. Abre en el navegador: `http://localhost:8000/openapi.json`
3. Guarda la página como `openapi.json` (Ctrl+S o Cmd+S)

#### Opción D: Usando cURL o PowerShell

```powershell
# Con PowerShell
Invoke-WebRequest -Uri "http://localhost:8000/openapi.json" -OutFile "openapi.json"

# Con cURL (si está instalado)
curl http://localhost:8000/openapi.json -o openapi.json
```

---

### 3. **Código Fuente de los Contratos**

Los contratos están definidos en el código fuente:

#### Archivo Principal:
```
src/recoleccion/api/recoleccion_controller.py
```

Este archivo contiene:
- ✅ Todos los endpoints (`@app.get`, `@app.post`, etc.)
- ✅ Modelos de request (`CrearTareaRequest`, `CrearAlimentoRequest`, etc.)
- ✅ Modelos de response (`Alimento`, `TareaRecoleccion`, `ErrorResponse`)
- ✅ Validaciones y respuestas de error
- ✅ Documentación de cada endpoint

#### Modelos de Datos:
```
src/recoleccion/models/alimento.py
src/recoleccion/models/tarea_recoleccion.py
src/recoleccion/models/hormiga.py
src/recoleccion/models/estado_tarea.py
```

---

## 📋 Estructura del Contrato OpenAPI

El esquema OpenAPI incluye:

### 1. **Información General**
- Título: "Subsistema de Recolección de Alimentos"
- Versión: "1.0.0"
- Descripción completa
- Información de contacto

### 2. **Servidores**
- URL base: `http://localhost:8000`
- URLs de producción (configurables)

### 3. **Endpoints (Paths)**
Cada endpoint incluye:
- Método HTTP (GET, POST, etc.)
- Ruta
- Parámetros (path, query, body)
- Respuestas (200, 400, 404, 500)
- Ejemplos de request/response
- Descripción y documentación

### 4. **Modelos (Schemas)**
- `Alimento`
- `TareaRecoleccion`
- `CrearTareaRequest`
- `CrearAlimentoRequest`
- `IniciarTareaRequest`
- `AsignarHormigasRequest`
- `ErrorResponse`
- Y más...

### 5. **Tags y Categorías**
- Salud y Estado
- Alimentos
- Tareas
- Estado y Monitoreo
- Procesamiento
- Debug

---

## 🛠️ Uso del Contrato Exportado

### Para Desarrollo Frontend
El equipo de frontend puede usar el esquema OpenAPI para:
- Generar clientes automáticamente
- Validar requests/responses
- Generar tipos TypeScript/JavaScript

### Para Testing
- Validar que las respuestas coincidan con el contrato
- Generar mocks automáticos
- Validar integración entre servicios

### Para Documentación
- Importar en herramientas como Postman
- Generar documentación adicional
- Compartir con stakeholders

### Para CI/CD
- Validar cambios en el contrato
- Detectar breaking changes
- Generar reportes de API

---

## 📝 Ejemplo de Uso del Script

```powershell
# 1. Asegúrate de estar en el directorio raíz
cd "C:\Users\manue\Proyecto Hormiguero"

# 2. Exporta el esquema
python scripts/export_openapi_schema.py

# 3. El archivo openapi.json se creará en la raíz del proyecto
```

---

## 🔗 Herramientas que Pueden Usar el Contrato

### 1. **Postman**
- Importar: `File > Import > Link` o `File > Import > File`
- URL: `http://localhost:8000/openapi.json` o el archivo exportado

### 2. **Insomnia**
- Importar: `Application > Preferences > Data > Import Data > From URL`
- URL: `http://localhost:8000/openapi.json`

### 3. **Swagger Editor**
- Abre: https://editor.swagger.io/
- Importa el archivo `openapi.json`

### 4. **OpenAPI Generator**
```bash
# Generar cliente TypeScript
openapi-generator-cli generate -i openapi.json -g typescript-axios -o ./generated-client

# Generar cliente Python
openapi-generator-cli generate -i openapi.json -g python -o ./generated-client
```

### 5. **Redoc**
- Genera documentación HTML estática
- Útil para hosting en GitHub Pages o servidor web

---

## 📍 Ubicación de Archivos

```
Proyecto Hormiguero/
├── openapi.json                    # Esquema exportado (se genera con el script)
├── scripts/
│   └── export_openapi_schema.py   # Script para exportar el esquema
├── src/
│   └── recoleccion/
│       ├── api/
│       │   └── recoleccion_controller.py  # Definición de endpoints
│       └── models/                        # Modelos de datos
└── COMO_ACCEDER_CONTRATO_API.md   # Este archivo
```

---

## ⚡ Acceso Rápido

### Si el servidor está corriendo:
```
http://localhost:8000/openapi.json
```

### Si quieres exportarlo:
```powershell
python scripts/export_openapi_schema.py
```

### Si quieres ver el código fuente:
```
src/recoleccion/api/recoleccion_controller.py
```

---

## 💡 Tips

1. **Versionar el Contrato**: Exporta el esquema antes de cada release y guárdalo en el repositorio
2. **Validar Cambios**: Compara versiones del esquema para detectar breaking changes
3. **Compartir con Equipos**: El archivo JSON es fácil de compartir y versionar
4. **Generar Clientes**: Usa herramientas como OpenAPI Generator para crear clientes automáticamente

---

**Última actualización:** 2024-01-15


