# Subsistema de Recolección de Alimentos

## 🐜 Simulación de Colonia de Hormigas - Universidad Cenfotec

### 📋 Descripción
Subsistema de recolección de alimentos para la simulación de una colonia de hormigas, desarrollado siguiendo metodologías TDD y BDD.

### 🚀 Características
- **TDD (Test-Driven Development)**: Desarrollo guiado por pruebas
- **BDD (Behavior-Driven Development)**: Desarrollo guiado por comportamiento
- **Cobertura de código**: ≥80% con reportes Allure
- **APIs REST**: FastAPI con documentación automática
- **Timer en tiempo real**: Gestión de tareas con tiempo real
- **Docker**: Containerización para despliegue

### 🛠️ Tecnologías
- **Python 3.12**
- **FastAPI** - Framework web
- **Pytest** - Testing
- **Behave** - BDD
- **Allure** - Reportes
- **Docker** - Containerización
- **Railway** - Despliegue

### 📁 Estructura del Proyecto
```
src/
├── recoleccion/
│   ├── api/           # Controladores REST
│   ├── models/        # Modelos de datos
│   └── services/       # Lógica de negocio
tests/                  # Pruebas unitarias
features/               # Pruebas BDD
scripts/                # Scripts de automatización
```

### 🚀 Instalación y Uso

#### Requisitos
- Python 3.12+
- pip

#### Instalación
```bash
# Clonar repositorio
git clone https://github.com/manuelsm15/Proyecto-Hormiguero.git
cd Proyecto-Hormiguero

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar pruebas
python scripts/run_tests.py

# Iniciar servidor
python main.py
```

#### URLs Disponibles
- **API Principal**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 🧪 Testing

#### Pruebas Unitarias
```bash
python -m pytest tests/ -v --cov=src --cov-report=html
```

#### Pruebas BDD
```bash
behave features/ -o allure-results
```

#### Reportes Allure
```bash
python scripts/generate_allure_report.py
```

### 🐳 Docker

#### Construir imagen
```bash
docker build -f Dockerfile.railway -t subsistema-recoleccion .
```

#### Ejecutar contenedor
```bash
docker run -p 8000:8000 subsistema-recoleccion
```

### 🚀 Despliegue en Railway

#### Configuración automática
```bash
# Login en Railway
railway login

# Inicializar proyecto
railway init

# Desplegar
railway up

# Obtener URL
railway domain
```

### 📊 APIs Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información del subsistema |
| `/health` | GET | Health check |
| `/alimentos` | GET | Alimentos disponibles |
| `/tareas` | POST | Crear tareas |
| `/tareas` | GET | Listar tareas |
| `/tareas/en-proceso` | GET | Tareas con timer |
| `/procesar` | POST | Procesamiento automático |
| `/estadisticas` | GET | Estadísticas |

### 🎯 Alimentos Disponibles
- **A1**: Fruta (3 hormigas, 10 puntos, 300s)
- **A2**: Semilla (2 hormigas, 5 puntos, 180s)
- **A3**: Hoja (1 hormiga, 3 puntos, 120s)

### 📈 Cobertura de Código
- **Total**: 88%
- **Servicios**: 86%
- **Modelos**: 76-100%
- **APIs**: 100%

### 👥 Autores
- **Manuel** - Universidad Cenfotec
- **Email**: manuelsm15@gmail.com

### 📄 Licencia
Este proyecto es parte del curso de Universidad Cenfotec.

### 🔗 Enlaces
- **GitHub**: https://github.com/manuelsm15/Proyecto-Hormiguero
- **Railway**: https://TU_PROYECTO-production.up.railway.app
- **Documentación**: https://TU_PROYECTO-production.up.railway.app/docs

