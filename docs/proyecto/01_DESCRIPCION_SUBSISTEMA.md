# Descripción del Subsistema de Recolección de Alimentos

## 1. Responsabilidades del Subsistema

El subsistema de Recolección de Alimentos es responsable de:

1. **Gestión de Alimentos**: Consultar y gestionar alimentos disponibles en el entorno
2. **Creación de Tareas**: Crear tareas de recolección para alimentos específicos
3. **Asignación de Hormigas**: Solicitar y asignar hormigas al subsistema de Hormiga Reina
4. **Ejecución de Tareas**: Iniciar, monitorear y completar tareas de recolección
5. **Persistencia**: Almacenar todos los datos del dominio en base de datos

## 2. Arquitectura y Diseño

### 2.1 Estructura del Subsistema

```
src/recoleccion/
├── api/                    # Controladores REST (FastAPI)
│   └── recoleccion_controller.py
├── models/                 # Modelos de dominio
│   ├── alimento.py
│   ├── hormiga.py
│   ├── tarea_recoleccion.py
│   └── estado_hormiga.py
├── services/               # Lógica de negocio
│   ├── recoleccion_service.py
│   ├── persistence_service.py
│   └── timer_service.py
└── database/               # Capa de persistencia
    └── database_manager.py
```

### 2.2 Decisiones de Diseño

#### 2.2.1 Separación de Responsabilidades
- **API Layer**: Maneja HTTP requests/responses
- **Service Layer**: Contiene lógica de negocio
- **Persistence Layer**: Abstrae acceso a base de datos
- **Models**: Representan entidades del dominio

#### 2.2.2 Sistema de Lotes de Hormigas
- Implementación de lotes para agrupar hormigas asignadas a tareas
- Validación de cantidad: `cantidad_enviada >= cantidad_requerida`
- Estados de lote: `pendiente`, `aceptado`, `en_uso`, `completado`
- Persistencia en tabla `lotes_hormigas`

#### 2.2.3 Completado Automático por Tiempo
- Verificación automática en endpoints de status
- Completado cuando `tiempo_actual >= fecha_inicio + tiempo_recoleccion`
- Actualización automática de estado y fecha_fin

#### 2.2.4 Persistencia Dual
- Soporte para SQL Server (producción)
- Soporte para SQLite (desarrollo/testing)
- Detección automática de esquema de BD

## 3. Modelos de Datos

### 3.1 Alimento
```python
@dataclass
class Alimento:
    id: str
    nombre: str
    cantidad_hormigas_necesarias: int
    puntos_stock: int
    tiempo_recoleccion: int  # en segundos
    disponible: bool = True
```

### 3.2 Hormiga
```python
@dataclass
class Hormiga:
    id: str
    capacidad_carga: int = 5  # máximo 5 unidades
    estado: EstadoHormiga = EstadoHormiga.DISPONIBLE
    tiempo_vida: int = 3600  # 1 hora por defecto
```

**Estados de Hormiga:**
- `DISPONIBLE`: Lista para asignar
- `BUSCANDO`: Buscando alimento
- `RECOLECTANDO`: Recolectando alimento
- `TRANSPORTANDO`: Transportando al hormiguero
- `MUERTA`: Hormiga muerta

### 3.3 TareaRecoleccion
```python
@dataclass
class TareaRecoleccion:
    id: str
    alimento: Alimento
    hormigas_asignadas: List[Hormiga] = field(default_factory=list)
    hormigas_lote_id: Optional[str] = None
    estado: EstadoTarea = EstadoTarea.PENDIENTE
    fecha_inicio: datetime = None
    fecha_fin: datetime = None
    alimento_recolectado: int = 0
```

**Estados de Tarea:**
- `PENDIENTE`: Creada pero no iniciada
- `EN_PROCESO`: En ejecución
- `COMPLETADA`: Finalizada exitosamente
- `CANCELADA`: Cancelada o fallida
- `PAUSADA`: Pausada por falta de hormigas vivas

## 4. APIs Externas

### 4.1 Subsistema de Entorno
- **Consultar alimentos disponibles**: Obtener lista de alimentos
- **Consultar alimento por ID**: Obtener alimento específico
- **Marcar alimento como recolectado**: Actualizar disponibilidad

### 4.2 Subsistema de Comunicación
- **Solicitar hormigas**: Solicitar hormigas al subsistema de Hormiga Reina
- **Consultar respuesta**: Obtener hormigas asignadas
- **Devolver hormigas**: Devolver hormigas después de completar tarea

## 5. Persistencia

### 5.1 Tablas de Base de Datos

#### Alimentos
- `id` (PK)
- `nombre`
- `cantidad_hormigas_necesarias`
- `puntos_stock`
- `tiempo_recoleccion`
- `disponible`

#### Tareas
- `id` (PK)
- `alimento_id` (FK)
- `estado`
- `inicio` (fecha_inicio)
- `fin` (fecha_fin)
- `cantidad_recolectada`
- `hormigas_asignadas` (contador)

#### lotes_hormigas
- `lote_id` (PK)
- `tarea_id` (FK)
- `cantidad_hormigas_enviadas`
- `cantidad_hormigas_requeridas`
- `estado`
- `fecha_creacion`
- `fecha_aceptacion`

#### asignaciones_hormiga_tarea
- `id` (PK)
- `tarea_id` (FK)
- `hormiga_id`
- `lote_id` (FK, nullable)
- `fecha_asignacion`

### 5.2 Motores de BD Soportados
- **SQL Server**: Producción (SHIRORYUU / Hormiguero)
- **SQLite**: Desarrollo y testing

## 6. Flujos Principales

### 6.1 Flujo de Recolección Completa

1. **Consultar Alimentos**: GET /alimentos
2. **Crear Tarea**: POST /tareas
3. **Asignar Hormigas**: POST /tareas/{id}/asignar-hormigas
4. **Iniciar Tarea**: POST /tareas/{id}/iniciar
5. **Completar Tarea**: POST /tareas/{id}/completar
6. **Verificar Status**: GET /tareas/{id}/status

### 6.2 Flujo con Lotes

1. **Crear Tarea**: POST /tareas
2. **Asignar con Lote**: POST /tareas/{id}/asignar-hormigas (con lote_id)
3. **Inicio Automático**: Si cantidad suficiente, se inicia automáticamente
4. **Completado Automático**: Por tiempo transcurrido o manual

## 7. Validaciones y Reglas de Negocio

### 7.1 Validaciones de Alimento
- `cantidad_hormigas_necesarias > 0`
- `puntos_stock > 0`
- `tiempo_recoleccion > 0`
- No se puede crear tarea si `disponible = false`

### 7.2 Validaciones de Hormiga
- `capacidad_carga > 0` (default: 5)
- `tiempo_vida > 0` (default: 3600 segundos)

### 7.3 Validaciones de Tarea
- No se puede iniciar sin suficientes hormigas
- No se puede completar si no está en `EN_PROCESO`
- `alimento_recolectado >= 0`

### 7.4 Validaciones de Lotes
- `cantidad_enviada >= cantidad_requerida`
- Lote no puede estar en uso si ya está asignado
- Lote debe existir antes de aceptarlo

## 8. Integración con Otros Subsistemas

### 8.1 Subsistema de Entorno
- **Propósito**: Obtener información de alimentos disponibles
- **Método**: API REST o Mock para testing
- **Endpoints utilizados**: `/api/entorno/alimentos`

### 8.2 Subsistema de Comunicación
- **Propósito**: Solicitar y devolver hormigas
- **Método**: API REST o Mock para testing
- **Endpoints utilizados**: `/api/comunicacion/solicitar-hormigas`

### 8.3 Subsistema de Hormiga Reina
- **Propósito**: Obtener hormigas para asignar a tareas
- **Método**: A través del subsistema de Comunicación
- **Flujo**: Recolección → Comunicación → Hormiga Reina

## 9. Tecnologías Utilizadas

- **Python 3.12**: Lenguaje de programación
- **FastAPI**: Framework web para APIs REST
- **Pytest**: Framework de testing
- **Behave**: Framework BDD
- **SQL Server**: Base de datos de producción
- **SQLite**: Base de datos de desarrollo
- **Allure**: Reportes de pruebas
- **Pydantic**: Validación de datos

## 10. Referencias

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Pytest Documentation: https://docs.pytest.org/
- Behave Documentation: https://behave.readthedocs.io/




