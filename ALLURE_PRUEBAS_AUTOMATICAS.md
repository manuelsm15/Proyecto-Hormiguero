# 📊 Integración de Allure con Pruebas Automáticas

Este documento explica cómo las pruebas automáticas del sistema de lotes de hormigas se guardan en Allure como respaldo.

---

## 🔧 Configuración

### Requisitos

1. **Allure CLI** (opcional, para generar reportes HTML):
   ```bash
   # Windows (con Chocolatey)
   choco install allure-commandline
   
   # O descargar desde: https://github.com/allure-framework/allure2/releases
   ```

2. **Dependencias Python** (ya incluidas en `requirements.txt`):
   - `allure-pytest==2.13.2`
   - `allure-behave==2.13.2`

---

## 📁 Estructura de Archivos

```
Proyecto Hormiguero/
├── allure-results/          # Resultados de pruebas (generado automáticamente)
│   ├── {uuid}-result.json   # Resultado de cada prueba
│   ├── {uuid}-attachment-request.json  # Request de cada prueba
│   └── {uuid}-attachment-response.json  # Response de cada prueba
├── allure-report/           # Reporte HTML (generado con Allure CLI)
│   └── index.html
├── allure.properties        # Configuración de Allure
└── scripts/
    └── prueba_completa_sistema_lotes.py  # Script de pruebas con Allure
```

---

## 🚀 Uso del Script de Pruebas

### Ejecutar Pruebas con Allure

```bash
python scripts/prueba_completa_sistema_lotes.py
```

**El script automáticamente:**
1. ✅ Ejecuta todas las pruebas
2. ✅ Guarda cada prueba en `allure-results/` con:
   - Request (método, URL, body)
   - Response (status code, body)
   - Estado (passed, failed, broken)
   - Descripción
3. ✅ Intenta generar el reporte HTML automáticamente

---

## 📋 Pruebas Guardadas en Allure

Cada paso de las pruebas se guarda como un caso de prueba separado:

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

## 📊 Formato de Resultados

Cada prueba se guarda en formato JSON con la siguiente estructura:

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

### Estados Posibles

- **`passed`**: Prueba exitosa (status code < 400)
- **`failed`**: Prueba fallida (status code >= 400)
- **`broken`**: Error de conexión o excepción

---

## 📄 Attachments (Archivos Adjuntos)

Cada prueba incluye dos attachments:

### 1. Request Attachment
Contiene el método, URL y body de la petición:
```json
{
  "nombre": "Fruta de Prueba",
  "cantidad_hormigas_necesarias": 3,
  "puntos_stock": 15,
  "tiempo_recoleccion": 10,
  "disponible": true
}
```

### 2. Response Attachment
Contiene el status code y body de la respuesta:
```json
{
  "status_code": 200,
  "body": {
    "id": "A20251119210356",
    "nombre": "Fruta de Prueba",
    ...
  }
}
```

---

## 🔍 Ver Reportes de Allure

### Opción 1: Generar Reporte HTML (Recomendado)

```bash
# Generar reporte
python scripts/generate_allure_report.py

# O manualmente
allure generate allure-results --clean -o allure-report

# Abrir reporte
allure open allure-report
```

### Opción 2: Servir Reporte en Tiempo Real

```bash
allure serve allure-results
```

Esto:
- Genera el reporte temporalmente
- Abre el navegador automáticamente
- Actualiza el reporte cuando hay nuevos resultados

### Opción 3: Ver Resultados JSON Directamente

Los resultados están en formato JSON legible en:
```
allure-results/
├── {uuid}-result.json
├── {uuid}-attachment-request.json
└── {uuid}-attachment-response.json
```

---

## 📈 Información en el Reporte

El reporte de Allure muestra:

1. **Resumen General:**
   - Total de pruebas ejecutadas
   - Pruebas pasadas
   - Pruebas fallidas
   - Pruebas rotas

2. **Detalles de Cada Prueba:**
   - Nombre de la prueba
   - Estado (passed/failed/broken)
   - Descripción
   - Tiempo de ejecución
   - Request completo (método, URL, body)
   - Response completo (status code, body)
   - Errores (si los hay)

3. **Gráficos:**
   - Distribución de estados
   - Tiempo de ejecución
   - Tendencias históricas (si se ejecuta múltiples veces)

---

## 🔄 Integración con CI/CD

Los resultados de Allure se pueden integrar en pipelines de CI/CD:

```yaml
# Ejemplo para GitHub Actions
- name: Generate Allure Report
  run: |
    allure generate allure-results --clean -o allure-report
    
- name: Upload Allure Report
  uses: actions/upload-artifact@v2
  with:
    name: allure-report
    path: allure-report/
```

---

## 📝 Ejemplo de Uso Completo

```bash
# 1. Ejecutar pruebas
python scripts/prueba_completa_sistema_lotes.py

# 2. Verificar que se generaron resultados
ls allure-results/

# 3. Generar reporte HTML
python scripts/generate_allure_report.py

# 4. Abrir reporte
allure open allure-report
```

---

## ⚙️ Configuración Avanzada

### Personalizar Directorio de Resultados

Editar `allure.properties`:
```properties
allure.results.directory=allure-results
```

### Agregar Información Adicional

El script puede ser extendido para agregar:
- Tags a las pruebas
- Links a issues
- Screenshots (si se usa Selenium)
- Logs adicionales

---

## 🐛 Solución de Problemas

### Allure CLI no encontrado

**Error:** `allure: command not found`

**Solución:**
1. Instalar Allure CLI (ver requisitos arriba)
2. O usar solo los resultados JSON sin generar HTML:
   ```bash
   # Los resultados están en allure-results/
   # Puedes leerlos directamente o usar un visor JSON
   ```

### No se generan resultados

**Verificar:**
1. Que el directorio `allure-results/` existe
2. Que el script tiene permisos de escritura
3. Que no hay errores en la ejecución del script

### Reporte no se genera

**Solución:**
```bash
# Verificar que Allure CLI está instalado
allure --version

# Generar reporte manualmente
allure generate allure-results --clean -o allure-report
```

---

## 📚 Referencias

- [Documentación de Allure](https://docs.qameta.io/allure/)
- [Allure Python Commons](https://github.com/allure-framework/allure-python-commons)
- [Allure Pytest](https://github.com/allure-framework/allure-python/tree/master/allure-pytest)

---

**Última actualización:** 2024-01-15

