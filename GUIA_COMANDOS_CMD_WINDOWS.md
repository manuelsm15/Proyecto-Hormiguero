# Guía de Comandos para Probar la API desde CMD (Command Prompt)

## Opción 1: Usar PowerShell desde CMD

Desde CMD puedes ejecutar comandos de PowerShell usando `powershell -Command`:

### Configurar URL base:
```cmd
powershell -Command "$baseUrl = 'http://localhost:8000'"
```

### Ejemplos GET:
```cmd
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/health' -Method GET"

powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/alimentos' -Method GET"

powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/tareas' -Method GET"
```

### Ejemplos POST:
```cmd
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/tareas' -Method POST"

powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/procesar' -Method POST"
```

---

## Opción 2: Usar curl (Windows 10/11)

Si tu Windows tiene `curl` instalado (Windows 10/11 lo trae por defecto):

### GET:
```cmd
curl http://localhost:8000/health

curl http://localhost:8000/alimentos

curl http://localhost:8000/tareas

curl http://localhost:8000/estadisticas
```

### POST:
```cmd
curl -X POST http://localhost:8000/tareas

curl -X POST "http://localhost:8000/tareas?tarea_id=test001&alimento_id=A1"

curl -X POST http://localhost:8000/procesar
```

---

## Opción 3: Ejecutar PowerShell en modo interactivo

Abre PowerShell desde CMD y luego usa los comandos:

```cmd
powershell
```

Dentro de PowerShell:
```powershell
$baseUrl = "http://localhost:8000"
Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
```

---

## Opción 4: Usar archivos .bat (más fácil)

Crea archivos .bat que ejecuten los comandos automáticamente (ver archivos .bat incluidos en el proyecto).













