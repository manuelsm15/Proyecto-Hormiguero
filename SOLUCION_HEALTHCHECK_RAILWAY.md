# 🔧 Solución: Healthcheck Falla en Railway

## ❌ Problema
El build se completa exitosamente, pero el healthcheck falla con "service unavailable".

## 🔍 Diagnóstico

El problema puede ser:
1. **El servidor no inicia correctamente** - Necesitamos ver los logs de runtime
2. **El puerto no está configurado correctamente** - Railway asigna PORT automáticamente
3. **El endpoint /health no está disponible** - Necesitamos verificar que se registre

## ✅ Soluciones Aplicadas

### 1. Mejorado Logging
- Cambiado de `ERROR` a `INFO` level para ver mensajes de startup
- Habilitado `access_log` para ver requests
- Agregados mensajes detallados de inicio

### 2. Verificación de Rutas
- Lista todas las rutas registradas al iniciar
- Verifica que `/health` esté disponible

## 📋 Pasos para Diagnosticar

### Paso 1: Ver Logs de Runtime en Railway

1. **En Railway Dashboard**:
   - Ve a tu servicio
   - Click en **"Logs"** (no solo Build logs)
   - Busca mensajes que empiecen con:
     - `🚀 Iniciando servidor`
     - `✅ Servidor configurado`
     - `✅ Iniciando servidor...`

### Paso 2: Verificar que el Servidor Inicie

En los logs deberías ver:
```
🚀 Iniciando servidor en puerto XXXX
🌐 Host: 0.0.0.0
❤️  Healthcheck: /health
📋 App routes: ['/', '/health', '/docs', ...]
✅ Servidor configurado correctamente
✅ Iniciando servidor...
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

### Paso 3: Si NO Ves Estos Mensajes

**Problema**: El servidor no está iniciando

**Posibles causas**:
1. Error al importar módulos
2. Error al crear la app
3. Error al iniciar uvicorn

**Solución**: Revisa los logs para ver el error específico

### Paso 4: Si Ves los Mensajes Pero Healthcheck Falla

**Problema**: El servidor inicia pero no responde

**Posibles causas**:
1. El puerto no coincide con el que Railway espera
2. El healthcheck está configurado incorrectamente
3. Hay un firewall o problema de red

**Solución**: 
- Verifica que Railway asigne el puerto correctamente
- Verifica que el healthcheck path sea `/health` (sin trailing slash)

## 🔧 Configuración de Railway

### Verificar Healthcheck Settings

En Railway Dashboard → Settings → Healthcheck:
- **Path**: `/health` (sin trailing slash)
- **Timeout**: 300 segundos (5 minutos)
- **Interval**: 30 segundos

### Verificar Variables de Entorno

En Railway Dashboard → Variables:
- `PORT` - NO configurar manualmente (Railway lo asigna)
- `HOST=0.0.0.0` - Opcional, pero recomendado
- `RELOAD=false` - Importante para producción

## 🚨 Errores Comunes

### "Module not found"
- Verifica que `requirements.txt` tenga todas las dependencias
- Revisa los logs del build

### "Port already in use"
- Railway asigna el puerto automáticamente
- NO configures `PORT` manualmente
- Verifica que `railway_main.py` use `os.environ.get("PORT")`

### "Application startup failed"
- Revisa los logs para el error específico
- Puede ser un problema de importación o configuración

## 📝 Próximos Pasos

1. **Espera el nuevo deployment** (ya hice push de los cambios)
2. **Revisa los logs de runtime** (no solo build logs)
3. **Comparte los logs** si el problema persiste

---

**Última actualización**: 2025-11-27


