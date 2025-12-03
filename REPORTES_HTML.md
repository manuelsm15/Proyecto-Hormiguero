# Sistema de Reportes HTML

## ✅ Problema Resuelto

El sistema ahora genera reportes HTML automáticamente **sin necesidad de instalar Allure CLI**.

## 🚀 Uso Automático

Cuando ejecutas las pruebas, el reporte se genera automáticamente:

```bash
python scripts/prueba_completa_sistema_lotes.py
```

Al finalizar, verás:
```
[OK] Reporte HTML generado exitosamente
Ubicacion: test-report.html

Para abrir el reporte:
  - Abre el archivo: test-report.html
  - O ejecuta: start test-report.html (Windows)
```

## 📊 Generar Reporte Manualmente

Si quieres generar el reporte después de ejecutar las pruebas:

```bash
python scripts/generate_html_report.py
```

## 📄 Ubicación del Reporte

El reporte se guarda en:
- **Archivo**: `test-report.html` (en la raíz del proyecto)
- **Resultados JSON**: `allure-results/` (datos brutos)

## 🎨 Características del Reporte

El reporte HTML incluye:

1. **Estadísticas Generales**:
   - Total de pruebas
   - Pruebas pasadas
   - Pruebas fallidas
   - Pruebas rotas
   - Pruebas omitidas
   - Duración total

2. **Detalles de Cada Prueba**:
   - Nombre y descripción
   - Estado (passed/failed/broken/skipped)
   - Duración
   - Mensajes de error (si aplica)
   - **Request completo** (método, URL, body)
   - **Response completo** (status code, body)

3. **Interfaz Interactiva**:
   - Diseño moderno y responsivo
   - Secciones colapsables para ver detalles
   - Código JSON formateado y legible
   - Colores según el estado de cada prueba

## 🔍 Ver Request/Response

Cada prueba tiene una sección "Ver Detalles" que muestra:
- **Request**: Método HTTP, URL, y body completo
- **Response**: Status code y body completo

Esto te permite ver exactamente qué se envió y qué se recibió en cada prueba.

## 📦 Resultados JSON (Allure)

Los resultados también se guardan en formato Allure JSON en `allure-results/`:
- `{uuid}-result.json` - Resultado de la prueba
- `{uuid}-attachment-request.json` - Request completo
- `{uuid}-attachment-response.json` - Response completo

Estos archivos son compatibles con Allure Framework si decides instalar Allure CLI más adelante.

## 🆚 Comparación: HTML vs Allure CLI

| Característica | Reporte HTML | Allure CLI |
|---------------|--------------|------------|
| Instalación | ✅ No requiere | ❌ Requiere instalación |
| Generación | ✅ Automática | ⚠️ Manual |
| Request/Response | ✅ Incluido | ✅ Incluido |
| Estadísticas | ✅ Básicas | ✅ Avanzadas |
| Historial | ❌ No | ✅ Sí |
| Gráficos | ❌ No | ✅ Sí |

## 💡 Recomendación

- **Para uso diario**: Usa el reporte HTML (automático, sin instalación)
- **Para análisis avanzado**: Instala Allure CLI si necesitas gráficos e historial

## 🔧 Instalar Allure CLI (Opcional)

Si quieres usar Allure CLI para reportes más avanzados:

**Windows (con Chocolatey):**
```bash
choco install allure-commandline
```

**O descargar desde:**
https://github.com/allure-framework/allure2/releases

Luego generar reporte:
```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

## 📝 Notas

- El reporte HTML se regenera cada vez que ejecutas las pruebas
- Los resultados JSON se acumulan en `allure-results/`
- Puedes abrir `test-report.html` directamente en cualquier navegador

