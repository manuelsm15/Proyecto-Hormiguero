# 🚀 Configuración de Cloudflare Pages

## ⚠️ Importante

Cloudflare Pages **NO ejecuta aplicaciones Python directamente**. Para desplegar una API FastAPI, tienes dos opciones:

### Opción 1: Railway + Cloudflare (Recomendado) ✅

1. **Despliega el backend en Railway**:
   ```bash
   railway login
   railway init
   railway up
   ```

2. **Usa Cloudflare como proxy/CDN**:
   - Configura un Worker o Pages Function que redirija las peticiones a Railway
   - O usa Cloudflare Tunnel para conectar directamente

### Opción 2: Cloudflare Workers (Limitado)

Cloudflare Workers tiene limitaciones para aplicaciones Python:
- No puede ejecutar Python directamente
- Solo puede hacer proxy a otro backend
- Tiempo de ejecución limitado (10ms CPU time en plan gratuito)

## 📝 Configuración Actual

El proyecto está configurado para:
- ✅ Instalar dependencias Python correctamente
- ✅ Usar Python 3.12.10
- ✅ Tener `functions/_middleware.js` para proxy (si es necesario)

## 🔧 Archivos Importantes

- `cloudflare_pages.toml` - Configuración de build para Pages
- `functions/_middleware.js` - Middleware para proxy a backend
- `requirements.txt` - Dependencias Python actualizadas

## 🚨 Solución al Error "Missing entry-point"

Si ves el error:
```
✘ [ERROR] Missing entry-point to Worker script
```

**Causa**: Cloudflare Pages detectó `_worker.js` o `wrangler.toml` y está intentando desplegar como Worker.

**Solución**: 
1. Renombrar `_worker.js` a `_worker.js.bak`
2. Renombrar `wrangler.toml` a `wrangler.toml.bak`
3. Usar solo `cloudflare_pages.toml` para Pages

## 📚 Recursos

- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Railway Docs](https://docs.railway.app/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)


