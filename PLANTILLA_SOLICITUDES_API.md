# 📄 Plantilla: Ejecución de Endpoints (GET / POST)  

Guía rápida para construir solicitudes hacia la API del subsistema de recolección.  
Todos los ejemplos asumen:
- `BASE_URL = http://localhost:8000`
- Cabecera común para POST: `Content-Type: application/json`

Puedes ajustar el host o agregar cabeceras de autenticación según tu entorno.

---

## 🧱 Formato base de los comandos

### GET (consulta sin body)
```bash
curl -X GET "$BASE_URL/<ruta>?param1=valor"
```

### POST (con body JSON)
```bash
curl -X POST "$BASE_URL/<ruta>" \
  -H "Content-Type: application/json" \
  -d '{
    "campo1": "valor",
    "campo2": 123
  }'
```

Versión PowerShell (`Invoke-RestMethod`):
```powershell
Invoke-RestMethod -Uri "$BASE_URL/<ruta>" -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body (@{
    campo1 = "valor"
    campo2 = 123
  } | ConvertTo-Json)
```

---

## 🔍 Endpoints GET (consultas)

| Endpoint | Descripción | Template | Parámetros útiles |
|----------|-------------|----------|-------------------|
| `/health` | Estado del servicio | `curl -X GET "$BASE_URL/health"` | — |
| `/` | Información general | `curl -X GET "$BASE_URL/"` | — |
| `/alimentos` | Lista de alimentos | `curl -X GET "$BASE_URL/alimentos"` | `?estado=disponible`, `?zona_id=1` |
| `/tareas` | Lista de tareas | `curl -X GET "$BASE_URL/tareas"` | — |
| `/tareas/{id}/status` | Status detallado | `curl -X GET "$BASE_URL/tareas/{tarea_id}/status"` | — |
| `/tareas/status` | Status de todas las tareas | `curl -X GET "$BASE_URL/tareas/status"` | — |
| `/debug/db` | Info de BD activa | `curl -X GET "$BASE_URL/debug/db"` | — |

> Sustituye `{tarea_id}` con el identificador real (ej. `T1001`).

---

## 🛠️ Endpoints POST (creación / acciones)

### 1. Crear alimento
```bash
curl -X POST "$BASE_URL/alimentos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Manzana",
    "cantidad_hormigas_necesarias": 2,
    "puntos_stock": 30,
    "tiempo_recoleccion": 120,
    "disponible": true
  }'
```

### 2. Crear tarea de recolección
```bash
curl -X POST "$BASE_URL/tareas" \
  -H "Content-Type: application/json" \
  -d '{
    "tarea_id": "T1001",
    "alimento_id": "1"
  }'
```

### 3. Asignar hormigas (y opcionalmente iniciar)
- **Solo asignar (el lote se puede omitir):**
```bash
curl -X POST "$BASE_URL/tareas/T1001/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "cantidad": 2
  }'
```
- **Asignar e iniciar con lote (recomendado):**
```bash
curl -X POST "$BASE_URL/tareas/T1001/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_H001"
  }'
```

### 4. Iniciar tarea manualmente
```bash
curl -X POST "$BASE_URL/tareas/T1001/iniciar" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "LOTE_H001"
  }'
```

### 5. Completar tarea (fin manual)
```bash
curl -X POST "$BASE_URL/tareas/T1001/completar?cantidad_recolectada=50"
```

### 6. Procesar recolección automática
```bash
curl -X POST "$BASE_URL/procesar"
```
(Opcional: `-d '{ "zona_id": 1 }'` si se implementan filtros)

### 7. Cancelar tarea
```bash
curl -X POST "$BASE_URL/tareas/T1001/cancelar"
```

---

## 🧪 Templates listos para copiar

| Acción | Método | Ruta | Body mínimo |
|--------|--------|------|-------------|
| Crear alimento | POST | `/alimentos` | `{ "nombre": "...", "cantidad_hormigas_necesarias": 0, "puntos_stock": 0, "tiempo_recoleccion": 0, "disponible": true }` |
| Crear tarea | POST | `/tareas` | `{ "tarea_id": "TXXXX", "alimento_id": "ID_ALIMENTO" }` |
| Asignar hormigas | POST | `/tareas/{id}/asignar-hormigas` | `{ "hormigas_lote_id": "LOTE_X" }` |
| Iniciar tarea | POST | `/tareas/{id}/iniciar` | `{ "hormigas_lote_id": "LOTE_X" }` |
| Status de tarea | GET | `/tareas/{id}/status` | — |
| Status global | GET | `/tareas/status` | — |

---

## ✅ Buenas prácticas
- Verificar disponibilidad del alimento (`disponible: true`) antes de crear la tarea.
- Guardar el `tarea_id` y el `hormigas_lote_id` usados, ya que se requieren en múltiples endpoints.
- Utilizar `GET /tareas/status` después de iniciar tareas para confirmar cambios de estado.
- Ante error 400 por “alimento no disponible”, validar en `GET /alimentos` que no esté marcado como `disponible: false`.

---

## 🧾 Plantilla rápida (rellena y pega)
```bash
BASE_URL="http://localhost:8000"

# 1) Crear alimento
curl -X POST "$BASE_URL/alimentos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "<NOMBRE>",
    "cantidad_hormigas_necesarias": <ENTERO>,
    "puntos_stock": <ENTERO>,
    "tiempo_recoleccion": <SEGUNDOS>,
    "disponible": true
  }'

# 2) Crear tarea
curl -X POST "$BASE_URL/tareas" \
  -H "Content-Type: application/json" \
  -d '{
    "tarea_id": "<TAREA_ID>",
    "alimento_id": "<ID_ALIMENTO>"
  }'

# 3) Asignar e iniciar con lote
curl -X POST "$BASE_URL/tareas/<TAREA_ID>/asignar-hormigas" \
  -H "Content-Type: application/json" \
  -d '{
    "hormigas_lote_id": "<LOTE_ID>"
  }'

# 4) Consultar status
curl -X GET "$BASE_URL/tareas/<TAREA_ID>/status"
```

---

> Guarda esta plantilla junto a tus scripts o inclúyela en tu README para compartir buenas prácticas de uso de la API. Ajusta los valores entre `< >` antes de ejecutar.







