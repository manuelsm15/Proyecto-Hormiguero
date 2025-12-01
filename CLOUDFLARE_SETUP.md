# ⚡ Setup Rápido: Cloudflare Deployment

## 🎯 Pasos Rápidos para Deployment

### Opción 1: Cloudflare + Railway (5 minutos) ⭐ RECOMENDADO

1. **Despliega en Railway**:
   - Ve a [railway.app](https://railway.app)
   - Conecta tu repo: `manuelsm15/Proyecto-Hormiguero`
   - Railway detectará automáticamente la configuración
   - Obtén tu URL: `https://hormiguero-xxxx.up.railway.app`

2. **Configura Cloudflare**:
   - Ve a [dash.cloudflare.com](https://dash.cloudflare.com)
   - Selecciona tu dominio
   - **DNS** → **Add record**:
     - Type: `CNAME`
     - Name: `api`
     - Target: `hormiguero-xxxx.up.railway.app`
     - Proxy: 🟠 **ON** (nube naranja)
   - Guarda

3. **Espera 5 minutos** y prueba:
   ```
   https://api.tudominio.com/docs
   ```

✅ **¡Listo!** Tu API está desplegada y protegida por Cloudflare.

---

### Opción 2: Cloudflare Pages (Manual)

1. **Instala Wrangler**:
   ```bash
   npm install -g wrangler
   ```

2. **Autentícate**:
   ```bash
   wrangler login
   ```

3. **Despliega**:
   ```bash
   wrangler pages deploy . --project-name=hormiguero
   ```

---

## 🔑 Variables de Entorno

Configura en Cloudflare Dashboard → Workers & Pages → Settings → Environment Variables:

```
BACKEND_URL=https://tu-backend-url.com
ENTORNO_API_URL=https://entorno-api.com
COMUNICACION_API_URL=https://comunicacion-api.com
```

---

## 📝 Archivos Creados

- ✅ `wrangler.toml` - Configuración de Cloudflare Workers
- ✅ `cloudflare_pages.toml` - Configuración de Cloudflare Pages
- ✅ `_worker.js` - Worker proxy para API
- ✅ `cloudflare_deploy.sh` - Script de deployment (Linux/Mac)
- ✅ `cloudflare_deploy.ps1` - Script de deployment (Windows)
- ✅ `.github/workflows/cloudflare-deploy.yml` - CI/CD automático
- ✅ `DEPLOY_CLOUDFLARE.md` - Guía completa

---

## 🆘 Problemas Comunes

**502 Bad Gateway?**
- Verifica que Railway esté corriendo
- Revisa logs en Railway Dashboard

**DNS no resuelve?**
- Espera 5-10 minutos
- Verifica que el CNAME esté correcto

---

## 📞 Soporte

- **Account ID**: `719189be500e460aed972c47cd97b209`
- **GitHub**: [@manuelsm15/Proyecto-Hormiguero](https://github.com/manuelsm15/Proyecto-Hormiguero)
- **Email**: manuelsm15@gmail.com


