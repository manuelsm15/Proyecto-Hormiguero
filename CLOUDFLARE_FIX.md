# 🔧 Solución al Error de Build en Cloudflare Pages

## ❌ Problema

El build falla con este error:
```
TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'
Failed to build pydantic-core
```

**Causa**: Cloudflare Pages está usando Python 3.13, pero `pydantic==2.5.0` no es compatible con Python 3.13.

## ✅ Solución

### Opción 1: Actualizar Dependencias (Recomendado)

He actualizado `requirements.txt` con versiones compatibles:

```txt
fastapi==0.115.0
uvicorn[standard]==0.32.1
pydantic==2.10.0
httpx==0.27.2
```

### Opción 2: Especificar Python 3.12

He creado `runtime.txt` que especifica Python 3.12:

```txt
python-3.12.10
```

### Opción 3: Usar Cloudflare + Railway (Mejor para APIs)

En lugar de Cloudflare Pages, usa:
1. **Railway** para el backend (Python/FastAPI)
2. **Cloudflare** como proxy/CDN

Esto es más adecuado para APIs FastAPI.

---

## 🚀 Pasos para Corregir el Deployment

### Si usas Cloudflare Pages:

1. **Actualiza el código** (ya está hecho):
   ```bash
   git add requirements.txt runtime.txt
   git commit -m "Fix: Update dependencies for Python 3.13 compatibility"
   git push
   ```

2. **En Cloudflare Dashboard**:
   - Ve a **Workers & Pages** → Tu proyecto
   - **Settings** → **Builds & deployments**
   - Asegúrate de que el **Build command** sea:
     ```
     pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
     ```
   - **Python version**: Selecciona **3.12** (si está disponible)

3. **Variables de entorno**:
   - `PYTHON_VERSION=3.12`
   - `BACKEND_URL` (si usas proxy)

### Si usas Cloudflare + Railway (Recomendado):

1. **Despliega en Railway**:
   - Conecta tu repo
   - Railway detectará automáticamente la configuración
   - Obtén tu URL: `https://hormiguero-xxxx.up.railway.app`

2. **Configura Cloudflare DNS**:
   - Crea un CNAME apuntando a tu URL de Railway
   - Activa el proxy (nube naranja)

---

## 📝 Archivos Modificados

- ✅ `requirements.txt` - Actualizado con versiones compatibles
- ✅ `runtime.txt` - Especifica Python 3.12
- ✅ `cloudflare_pages.toml` - Configuración actualizada
- ✅ `package.json` - Añadido para Cloudflare Pages
- ✅ `functions/_middleware.js` - Middleware para proxy

---

## 🔍 Verificación

Después del deployment, verifica:

```bash
# Health check
curl https://tu-dominio.com/health

# Documentación
curl https://tu-dominio.com/docs
```

---

## 💡 Recomendación Final

Para una API FastAPI, **NO uses Cloudflare Pages directamente**. En su lugar:

1. **Despliega el backend en Railway/Render**
2. **Usa Cloudflare como proxy/CDN**

Esto es más eficiente y evita problemas de compatibilidad.


