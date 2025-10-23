# 🐳 Guía de Docker - Subsistema de Recolección

## 📋 Descripción

Esta guía te permite hostear el Subsistema de Recolección usando Docker, permitiendo que tú y tu compañero puedan acceder desde diferentes ubicaciones.

## 🚀 Inicio Rápido

### 1. Verificar Prerrequisitos

```bash
# Verificar Docker
docker --version

# Verificar Docker Compose
docker-compose --version
```

### 2. Deployment Automático

```bash
# Ejecutar script de deployment
python scripts/deploy_docker.py
```

### 3. Deployment Manual

```bash
# Construir y ejecutar
docker-compose up --build -d

# Verificar estado
docker-compose ps

# Ver logs
docker-compose logs -f
```

## 🌐 URLs de Acceso

### Local (desde tu máquina)
- **API Principal**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Nginx Proxy**: http://localhost:80

### Remoto (desde otra máquina)
- **API Principal**: http://TU_IP:8000
- **Documentación**: http://TU_IP:8000/docs
- **Nginx Proxy**: http://TU_IP:80

## 🔧 Comandos Útiles

### Gestión de Contenedores
```bash
# Iniciar servicios
docker-compose up -d

# Parar servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f
```

### Ejecutar Pruebas
```bash
# Pruebas unitarias
docker-compose exec recoleccion-api python -m pytest tests/ -v

# Pruebas con cobertura
docker-compose exec recoleccion-api python -m pytest tests/ --cov=src --cov-report=html

# Pruebas BDD
docker-compose exec recoleccion-api behave features/simple_test.feature -v
```

### Acceso al Contenedor
```bash
# Entrar al contenedor
docker-compose exec recoleccion-api bash

# Ejecutar comandos específicos
docker-compose exec recoleccion-api python scripts/demo_apis.py
```

## 📊 Monitoreo

### Health Check
```bash
# Verificar salud de la API
curl http://localhost:8000/health

# Verificar desde otra máquina
curl http://TU_IP:8000/health
```

### Logs en Tiempo Real
```bash
# Logs de todos los servicios
docker-compose logs -f

# Logs solo de la API
docker-compose logs -f recoleccion-api

# Logs solo de Nginx
docker-compose logs -f nginx
```

## 🔒 Configuración de Red

### Para Acceso Remoto

1. **Obtener tu IP local**:
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. **Configurar firewall** (si es necesario):
   - Abrir puertos 8000 y 80
   - Permitir conexiones entrantes

3. **Compartir IP con tu compañero**:
   - Ejemplo: `http://192.168.1.100:8000`

## 🧪 Pruebas de Conectividad

### Desde tu máquina
```bash
# Probar API local
curl http://localhost:8000/

# Probar documentación
curl http://localhost:8000/docs
```

### Desde otra máquina
```bash
# Reemplazar TU_IP con la IP real
curl http://TU_IP:8000/
curl http://TU_IP:8000/docs
```

## 📁 Estructura de Volúmenes

```
./logs/              # Logs de la aplicación
./allure-results/    # Resultados de pruebas Allure
./htmlcov/          # Reportes de cobertura HTML
```

## 🛠️ Solución de Problemas

### Puerto ya en uso
```bash
# Ver qué está usando el puerto
netstat -ano | findstr :8000

# Parar servicios
docker-compose down

# Cambiar puerto en docker-compose.yml
```

### Contenedor no inicia
```bash
# Ver logs detallados
docker-compose logs recoleccion-api

# Reconstruir imagen
docker-compose build --no-cache
docker-compose up -d
```

### Problemas de red
```bash
# Verificar conectividad
docker-compose exec recoleccion-api curl localhost:8000/health

# Verificar configuración de red
docker network ls
docker network inspect recoleccion-network
```

## 📈 Escalabilidad

### Múltiples Instancias
```bash
# Escalar servicios
docker-compose up --scale recoleccion-api=3 -d
```

### Load Balancer
El Nginx ya está configurado como proxy reverso para distribuir carga.

## 🔄 Actualizaciones

### Actualizar Código
```bash
# Parar servicios
docker-compose down

# Reconstruir con cambios
docker-compose build --no-cache
docker-compose up -d
```

### Actualizar Dependencias
```bash
# Reconstruir después de cambiar requirements.txt
docker-compose build --no-cache
docker-compose up -d
```

## 📞 Soporte

Si tienes problemas:

1. **Verificar logs**: `docker-compose logs -f`
2. **Verificar estado**: `docker-compose ps`
3. **Reiniciar servicios**: `docker-compose restart`
4. **Reconstruir**: `docker-compose build --no-cache && docker-compose up -d`

---

**¡El subsistema está listo para ser probado por ti y tu compañero desde cualquier ubicación!** 🚀
