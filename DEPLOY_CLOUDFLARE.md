# 🚀 Guía de Deployment en Cloudflare

Esta guía te ayudará a desplegar el proyecto **Hormiguero** en Cloudflare.

## 📋 Opciones de Deployment

### ⚠️ IMPORTANTE: Cloudflare Pages y Python 3.13

**Problema conocido**: Cloudflare Pages usa Python 3.13 por defecto, pero algunas versiones de `pydantic` no son compatibles.

**Solución**: 
- ✅ He actualizado `requirements.txt` con versiones compatibles
- ✅ He creado `runtime.txt` para especificar Python 3.12
- ✅ **Recomendación**: Usa la Opción 2 (Cloudflare + Railway) para APIs

### Opción 1: Cloudflare Pages (Solo si es necesario)
**Nota**: Cloudflare Pages está optimizado para sitios estáticos. Para una API FastAPI completa, se recomienda la **Opción 2**.

### Opción 2: Cloudflare como Proxy/CDN (Recomendado para APIs)
Despliega el backend en Railway/Render y usa Cloudflare como proxy/CDN.

### Opción 3: Cloudflare Tunnel
Conecta tu backend local o servidor privado a Cloudflare.

---

## 🎯 Opción Recomendada: Cloudflare + Railway

### Paso 1: Desplegar Backend en Railway

1. Ve a [Railway](https://railway.app) y crea una cuenta
2. Crea un nuevo proyecto → **Deploy from GitHub repo**
3. Selecciona tu repositorio: `manuelsm15/Proyecto-Hormiguero`
4. Railway detectará automáticamente la configuración:
   - Usará `railway.toml` si existe
   - O el `Dockerfile.railway`
5. Configura las variables de entorno (si las necesitas):
   ```
   ENTORNO_API_URL=
   COMUNICACION_API_URL=
   BASE_API_URL=
   ```
6. Railway te dará una URL como: `https://hormiguero.up.railway.app`

### Paso 2: Configurar Cloudflare como Proxy

1. **Accede a Cloudflare Dashboard**
   - Ve a [dash.cloudflare.com](https://dash.cloudflare.com)
   - Selecciona tu dominio (o crea uno si no tienes)

2. **Configurar DNS**
   - Ve a **DNS** → **Records**
   - Crea un nuevo registro:
     - **Type**: `CNAME`
     - **Name**: `api` (o el subdominio que prefieras)
     - **Target**: `hormiguero.up.railway.app` (tu URL de Railway)
     - **Proxy status**: 🟠 **Proxied** (nube naranja activada)
   - Guarda el registro

3. **Configurar SSL/TLS**
   - Ve a **SSL/TLS** → **Overview**
   - Asegúrate de que está en modo **Full** o **Full (strict)**

4. **Configurar Reglas de Firewall (Opcional)**
   - Ve a **Security** → **WAF**
   - Puedes crear reglas personalizadas para proteger tu API

### Paso 3: Verificar Deployment

Después de unos minutos (propagación DNS), tu API estará disponible en:
```
https://api.tudominio.com
```

Prueba los endpoints:
- `https://api.tudominio.com/docs` - Documentación Swagger
- `https://api.tudominio.com/health` - Health check
- `https://api.tudominio.com/` - Endpoint raíz

---

## 🔧 Opción Alternativa: Cloudflare Pages (Solo si necesitas)

Si quieres intentar desplegar directamente en Cloudflare Pages:

### Requisitos Previos

1. **Instalar Wrangler CLI**:
   ```bash
   npm install -g wrangler
   ```

2. **Autenticarse en Cloudflare**:
   ```bash
   wrangler login
   ```

3. **Configurar Account ID** (ya está en `wrangler.toml`):
   ```toml
   account_id = "719189be500e460aed972c47cd97b209"
   ```

### Deployment Manual

#### Windows (PowerShell):
```powershell
.\cloudflare_deploy.ps1
```

#### Linux/Mac:
```bash
chmod +x cloudflare_deploy.sh
./cloudflare_deploy.sh
```

#### Manual con Wrangler:
```bash
wrangler pages deploy . --project-name=hormiguero
```

### Configurar Variables de Entorno en Cloudflare

1. Ve a **Cloudflare Dashboard** → **Workers & Pages** → Tu proyecto
2. Ve a **Settings** → **Environment Variables**
3. Agrega las variables necesarias:
   - `BACKEND_URL`: URL de tu backend (si usas proxy)
   - `ENTORNO_API_URL`: URL del servicio de entorno
   - `COMUNICACION_API_URL`: URL del servicio de comunicación

---

## 🌐 Cloudflare Tunnel (Para Backend Local/Privado)

Si quieres exponer un backend que corre localmente o en un servidor privado:

1. **Instalar cloudflared**:
   ```bash
   # Windows
   winget install --id Cloudflare.cloudflared
   
   # Linux
   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
   sudo dpkg -i cloudflared-linux-amd64.deb
   ```

2. **Autenticarse**:
   ```bash
   cloudflared tunnel login
   ```

3. **Crear un tunnel**:
   ```bash
   cloudflared tunnel create hormiguero
   ```

4. **Configurar el tunnel**:
   ```bash
   cloudflared tunnel route dns hormiguero api.tudominio.com
   ```

5. **Ejecutar el tunnel**:
   ```bash
   cloudflared tunnel run hormiguero
   ```

---

## 📝 Configuración de Variables de Entorno

Crea un archivo `.env` o configura en Cloudflare Dashboard:

```env
# URLs de servicios externos
ENTORNO_API_URL=https://entorno-api.example.com
COMUNICACION_API_URL=https://comunicacion-api.example.com
BASE_API_URL=https://api.example.com

# Configuración de servicios
USE_REAL_ENTORNO=false
USE_REAL_COMUNICACION=false

# Base de datos (si usas SQL Server)
DB_SERVER=your-server.database.windows.net
DB_NAME=Hormiguero
DB_USER=your-user
DB_PASSWORD=your-password
```

---

## ✅ Verificación Post-Deployment

1. **Health Check**:
   ```bash
   curl https://api.tudominio.com/health
   ```

2. **Documentación**:
   Abre en navegador: `https://api.tudominio.com/docs`

3. **Endpoints principales**:
   - `GET /` - Información del subsistema
   - `GET /health` - Health check
   - `GET /alimentos` - Listar alimentos
   - `POST /tareas` - Crear tarea
   - `GET /tareas` - Listar tareas

---

## 🔒 Seguridad

### Recomendaciones:

1. **Habilitar WAF** en Cloudflare Dashboard
2. **Configurar Rate Limiting** para proteger contra abuso
3. **Usar Cloudflare Access** para endpoints administrativos
4. **Configurar CORS** correctamente en tu API
5. **Usar HTTPS** siempre (Cloudflare lo proporciona automáticamente)

---

## 🐛 Troubleshooting

### Problema: "502 Bad Gateway"
- Verifica que tu backend en Railway esté corriendo
- Revisa los logs en Railway Dashboard
- Verifica que el CNAME apunte correctamente

### Problema: "DNS no resuelve"
- Espera 5-10 minutos para propagación DNS
- Verifica que el registro CNAME esté correcto
- Asegúrate de que el proxy esté activado (nube naranja)

### Problema: "CORS Error"
- Configura CORS en tu API FastAPI
- Verifica que los headers estén correctos

---

## 📚 Recursos

- [Cloudflare Dashboard](https://dash.cloudflare.com)
- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Cloudflare Tunnel Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

---

## 👤 Contacto

- **Autor**: Manuel
- **Email**: manuelsm15@gmail.com
- **GitHub**: [@manuelsm15/Proyecto-Hormiguero](https://github.com/manuelsm15/Proyecto-Hormiguero)

---

**Account ID de Cloudflare**: `719189be500e460aed972c47cd97b209`

