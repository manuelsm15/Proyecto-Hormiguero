# 🚂 Guía de Deployment en Railway

## ✅ Configuración Verificada

El proyecto está listo para deployment en Railway con:
- ✅ `railway.toml` configurado
- ✅ `Dockerfile.railway` optimizado
- ✅ `railway_main.py` para producción
- ✅ Variables de entorno configuradas
- ✅ Healthcheck en `/health`

## 🚀 Opción 1: Deployment Automático desde GitHub (Recomendado)

### Paso 1: Conectar GitHub a Railway

1. Ve a [Railway Dashboard](https://railway.app)
2. Click en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Autoriza Railway a acceder a tu repositorio
5. Selecciona el repositorio: `manuelsm15/Proyecto-Hormiguero`
6. Selecciona la rama: `main`

### Paso 2: Railway detectará automáticamente

Railway detectará:
- ✅ `railway.toml` → Usará Dockerfile.railway
- ✅ `Dockerfile.railway` → Construirá la imagen
- ✅ `railway_main.py` → Comando de inicio

### Paso 3: Configurar Variables de Entorno (Opcional)

En Railway Dashboard → Variables:
```
HOST=0.0.0.0
RELOAD=false
LOG_LEVEL=info
```

**Nota**: `PORT` se asigna automáticamente por Railway.

### Paso 4: Obtener URL del Deployment

1. Railway Dashboard → Tu proyecto
2. Click en el servicio
3. **Settings** → **Generate Domain**
4. Copia la URL (ej: `hormiguero-production.up.railway.app`)

## 🛠️ Opción 2: Deployment Manual con Railway CLI

### Paso 1: Instalar Railway CLI

```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# O con npm
npm i -g @railway/cli
```

### Paso 2: Login

```bash
railway login
```

### Paso 3: Inicializar Proyecto

```bash
# En el directorio del proyecto
railway init
```

### Paso 4: Desplegar

```bash
railway up
```

### Paso 5: Obtener URL

```bash
railway domain
```

## 🔍 Verificación Post-Deployment

### 1. Health Check

```bash
curl https://tu-dominio.up.railway.app/health
```

Debería responder:
```json
{"status": "ok", "subsistema": "recoleccion"}
```

### 2. Documentación API

Abre en el navegador:
```
https://tu-dominio.up.railway.app/docs
```

### 3. Ver Logs

```bash
railway logs
```

O desde el Dashboard → Logs

## 📋 Checklist de Deployment

- [ ] Repositorio conectado a Railway
- [ ] Build completado exitosamente
- [ ] Healthcheck responde en `/health`
- [ ] API docs accesible en `/docs`
- [ ] Logs sin errores críticos
- [ ] Dominio generado y funcionando

## 🐛 Troubleshooting

### Error: "Port already in use"
- Railway asigna el puerto automáticamente
- Verifica que `railway_main.py` use `os.environ.get("PORT")`

### Error: "Module not found"
- Verifica que `requirements.txt` tenga todas las dependencias
- Revisa los logs del build

### Error: "Healthcheck failed"
- Verifica que el endpoint `/health` esté implementado
- Revisa `railway.toml` → `healthcheckPath = "/health"`

### Build muy lento
- Railway usa caché de Docker
- El primer build puede tardar más

## 📝 Notas Importantes

1. **Railway asigna PORT automáticamente** - No lo configures manualmente
2. **RELOAD debe ser false** en producción (ya configurado)
3. **Healthcheck** se ejecuta cada 30 segundos
4. **Logs** están disponibles en tiempo real en el Dashboard

## 🔗 Enlaces Útiles

- [Railway Docs](https://docs.railway.app/)
- [Railway Dashboard](https://railway.app/dashboard)
- [Railway CLI Docs](https://docs.railway.app/develop/cli)

---

**Última actualización**: 2025-11-27



