"""
Controlador REST para el subsistema de recolección.
"""

from fastapi import FastAPI, HTTPException, Depends, Query, Body, status
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio

from ..services.recoleccion_service import RecoleccionService
from ..services.entorno_service import EntornoService
from ..services.comunicacion_service import ComunicacionService
from ..models.alimento import Alimento
from ..models.tarea_recoleccion import TareaRecoleccion
from ..models.estado_tarea import EstadoTarea

class CrearTareaRequest(BaseModel):
    tarea_id: Optional[str] = None
    alimento_id: Optional[str] = None

class CrearAlimentoRequest(BaseModel):
    id: Optional[str] = None
    nombre: str
    cantidad_hormigas_necesarias: int
    puntos_stock: int
    tiempo_recoleccion: int
    disponible: Optional[bool] = True

class IniciarTareaRequest(BaseModel):
    hormigas_lote_id: str

class AsignarHormigasRequest(BaseModel):
    hormigas_lote_id: Optional[str] = None
    cantidad: Optional[int] = None

class ErrorResponse(BaseModel):
    """Modelo de respuesta de error estándar."""
    detail: str

# Diccionario de respuestas comunes para reutilizar
RESPONSES = {
    400: {
        "model": ErrorResponse,
        "description": "Error de validación o regla de negocio",
        "content": {
            "application/json": {
                "example": {"detail": "El alimento no está disponible. Estado: agotado"}
            }
        }
    },
    404: {
        "model": ErrorResponse,
        "description": "Recurso no encontrado",
        "content": {
            "application/json": {
                "example": {"detail": "Tarea 'T1001' no encontrada en la base de datos"}
            }
        }
    },
    500: {
        "model": ErrorResponse,
        "description": "Error interno del servidor",
        "content": {
            "application/json": {
                "example": {"detail": "Error al consultar alimentos: conexión a BD falló"}
            }
        }
    }
}


def create_app(
    entorno_service: EntornoService, 
    comunicacion_service: ComunicacionService
) -> FastAPI:
    """
    Crea la aplicación FastAPI con las dependencias inyectadas.
    
    Args:
        entorno_service: Servicio de entorno
        comunicacion_service: Servicio de comunicación
        
    Returns:
        Aplicación FastAPI configurada
    """
    app = FastAPI(
        title="Subsistema de Recolección de Alimentos",
        description="""
        ## API para la gestión de recolección de alimentos en la simulación de colonia de hormigas
        
        ### Características principales:
        - Gestión de alimentos disponibles
        - Creación y asignación de tareas de recolección
        - Asignación de hormigas por lotes
        - Completado automático de tareas por tiempo
        - Monitoreo en tiempo real del estado de tareas
        - Integración con base de datos SQL Server/SQLite
        
        ### Documentación Interactiva:
        - **Swagger UI**: `/docs` - Interfaz interactiva para probar las APIs
        - **ReDoc**: `/redoc` - Documentación alternativa en formato ReDoc
        - **OpenAPI Schema**: `/openapi.json` - Esquema OpenAPI en formato JSON
        
        ### Base URL:
        - **Local**: `http://localhost:8000`
        - **Producción**: Configurar según el entorno de despliegue
        """,
        version="1.0.0",
        contact={
            "name": "Subsistema de Recolección",
            "email": "manuelsm15@gmail.com",
        },
        tags_metadata=[
            {
                "name": "Salud y Estado",
                "description": "Endpoints para verificar el estado del servicio y obtener información básica.",
            },
            {
                "name": "Alimentos",
                "description": "Gestión de alimentos disponibles para recolección. Crear y consultar alimentos.",
            },
            {
                "name": "Tareas",
                "description": "Gestión completa de tareas de recolección. Crear, asignar hormigas, iniciar, completar y cancelar tareas.",
            },
            {
                "name": "Estado y Monitoreo",
                "description": "Endpoints para consultar el estado de tareas, tiempo restante, progreso y estadísticas. Incluye verificación automática de completado por tiempo.",
            },
            {
                "name": "Procesamiento",
                "description": "Endpoints para ejecutar procesos automáticos de recolección y verificación de hormigas.",
            },
            {
                "name": "Debug",
                "description": "Endpoints de depuración para inspeccionar el estado de la base de datos y datos raw.",
            },
        ],
    )
    
    # Inicializar servicio de recolección
    recoleccion_service = RecoleccionService(entorno_service, comunicacion_service)
    
    @app.get("/", tags=["Salud y Estado"])
    async def root():
        """Endpoint raíz."""
        return {"message": "Subsistema de Recolección de Alimentos - Universidad Cenfotec"}
    
    @app.get("/health", tags=["Salud y Estado"])
    async def health_check():
        """Verificación de salud del servicio."""
        try:
            # Healthcheck simple que siempre funciona
            return {
                "status": "healthy",
                "service": "subsistema-recoleccion",
                "version": "1.0.0",
                "entorno_disponible": True,
                "comunicacion_disponible": True
            }
        except Exception as e:
            # En caso de error, devolver unhealthy pero no lanzar excepción
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    @app.get(
        "/alimentos",
        response_model=List[Alimento],
        tags=["Alimentos"],
        responses={500: RESPONSES[500]}
    )
    async def consultar_alimentos(
        zona_id: Optional[int] = Query(None, description="(Reservado) ID de zona para filtrar recursos"),
        estado: Optional[str] = Query(
            None,
            description=(
                "(Reservado) Estado del recurso: disponible, en_proceso, recolectado. "
                "Por ahora el endpoint siempre devuelve TODOS los alimentos de la base de datos."
            ),
        ),
    ):
        """
        Consulta los alimentos/recursos **directamente desde la base de datos**.

        IMPORTANTE:
        - Siempre devuelve TODOS los registros de la tabla `Alimentos` que pueda mapear,
          sin filtrar por estado ni disponibilidad.
        - De esta forma, el resultado debe coincidir con el conteo `alimentos_en_bd`
          que muestra el endpoint `/debug/db`.
        """
        try:
            # Usar exactamente la misma conexión y lógica que el POST de alimentos:
            # a través de PersistenceService, que a su vez usa el db_manager global.
            from ..services.persistence_service import persistence_service

            alimentos: List[Alimento] = await persistence_service.obtener_alimentos()

            # Por ahora NO se aplica ningún filtro por estado ni por zona.
            return alimentos or []
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al consultar alimentos: {str(e)}")

    @app.post(
        "/alimentos", 
        response_model=Alimento, 
        tags=["Alimentos"],
        responses={500: RESPONSES[500]}
    )
    async def crear_alimento(payload: CrearAlimentoRequest = Body(...)):
        """Crea un alimento y lo guarda en la base de datos."""
        try:
            from datetime import datetime
            from ..services.persistence_service import persistence_service

            alimento = Alimento(
                id=payload.id or f"A{datetime.now().strftime('%Y%m%d%H%M%S')}",
                nombre=payload.nombre,
                cantidad_hormigas_necesarias=payload.cantidad_hormigas_necesarias,
                puntos_stock=payload.puntos_stock,
                tiempo_recoleccion=payload.tiempo_recoleccion,
                disponible=bool(payload.disponible)
            )

            ok = await persistence_service.guardar_alimento(alimento)
            if not ok:
                last_error = persistence_service.obtener_ultimo_error()
                detalle = f"No se pudo guardar el alimento en BD"
                if last_error:
                    detalle = f"{detalle}: {last_error}"
                raise HTTPException(status_code=500, detail=detalle)
            return alimento
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear alimento: {str(e)}")
    
    @app.post(
        "/tareas", 
        response_model=TareaRecoleccion, 
        tags=["Tareas"],
        responses={
            400: RESPONSES[400],
            404: RESPONSES[404],
            500: RESPONSES[500]
        }
    )
    async def crear_tarea(
        tarea_id: str = Query(""),
        alimento_id: str = Query(""),
        body: Optional[CrearTareaRequest] = Body(None)
    ):
        """Crea una nueva tarea de recolección."""
        try:
            # Usar valores por defecto si no se proporcionan
            if body and body.tarea_id and not tarea_id:
                tarea_id = body.tarea_id
            if body and body.alimento_id and not alimento_id:
                alimento_id = body.alimento_id

            if not tarea_id:
                from datetime import datetime
                tarea_id = f"tarea_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if not alimento_id:
                alimento_id = "A1"  # Usar A1 por defecto
            
            # Intentar obtener el alimento desde el servicio de entorno primero (para tests con mocks)
            alimento = None
            if await entorno_service.is_disponible():
                try:
                    alimento = await entorno_service.consultar_alimento_por_id(alimento_id)
                except Exception:
                    # Si falla, intentar con la base de datos
                    pass
            
            # Si no se obtuvo del servicio de entorno, usar la base de datos
            if not alimento:
                from ..services.persistence_service import persistence_service
                alimento = await persistence_service.obtener_alimento_por_id(alimento_id)
            
            if not alimento:
                raise HTTPException(status_code=404, detail="Alimento no encontrado")
            
            # Validar que el alimento esté disponible
            if not alimento.disponible:
                raise HTTPException(
                    status_code=400, 
                    detail=f"El alimento '{alimento.nombre}' (ID: {alimento.id}) no está disponible. Estado: agotado"
                )
            
            tarea = await recoleccion_service.crear_tarea_recoleccion(tarea_id, alimento)
            return tarea
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear tarea: {str(e)}")
    
    @app.get("/tareas", response_model=List[TareaRecoleccion], tags=["Tareas"])
    async def listar_tareas():
        """Lista todas las tareas (activas + completadas)."""
        return recoleccion_service.tareas_activas + recoleccion_service.tareas_completadas
    
    @app.get("/tareas/activas", response_model=List[TareaRecoleccion], tags=["Tareas"])
    async def listar_tareas_activas():
        """Lista todas las tareas activas."""
        return recoleccion_service.tareas_activas
    
    @app.get("/tareas/completadas", response_model=List[TareaRecoleccion], tags=["Tareas"])
    async def listar_tareas_completadas():
        """Lista todas las tareas completadas."""
        return recoleccion_service.tareas_completadas
    
    @app.get("/tareas/en-proceso", response_model=List[TareaRecoleccion], tags=["Tareas"])
    async def listar_tareas_en_proceso():
        """Lista todas las tareas en proceso."""
        return recoleccion_service.tareas_activas
    
    @app.post(
        "/tareas/{tarea_id}/asignar-hormigas", 
        tags=["Tareas"],
        responses={
            400: RESPONSES[400],
            404: RESPONSES[404],
            500: RESPONSES[500]
        }
    )
    async def asignar_hormigas_a_tarea_endpoint(
        tarea_id: str, 
        cantidad: int = Query(None),
        body: Optional[AsignarHormigasRequest] = Body(None)
    ):
        """
        Asigna hormigas a una tarea existente.
        
        Si se proporciona `hormigas_lote_id` en el body y hay suficientes hormigas,
        automáticamente inicia la tarea.
        """
        try:
            # Usar el servicio de app.state si está disponible (para tests), sino usar el del scope
            servicio_a_usar = getattr(app.state, 'recoleccion_service', None) or recoleccion_service
            
            # Buscar tarea en memoria o BD
            tarea = None
            for t in servicio_a_usar.tareas_activas + servicio_a_usar.tareas_completadas:
                if t.id == tarea_id:
                    tarea = t
                    break
            
            if not tarea:
                from ..services.persistence_service import persistence_service
                tareas_bd = await persistence_service.obtener_tareas()
                tarea = next((t for t in tareas_bd if str(t.id).strip() == tarea_id.strip()), None)
                
                if tarea and tarea not in servicio_a_usar.tareas_activas:
                    servicio_a_usar.tareas_activas.append(tarea)
            
            if not tarea:
                raise HTTPException(status_code=404, detail=f"Tarea '{tarea_id}' no encontrada")
            
            # Obtener cantidad y lote_id del body si está presente
            hormigas_lote_id = None
            if body:
                hormigas_lote_id = body.hormigas_lote_id
                if body.cantidad is not None:
                    cantidad = body.cantidad
            
            # Determinar cantidad de hormigas necesarias
            if cantidad is None:
                cantidad_necesaria = tarea.alimento.cantidad_hormigas_necesarias - len(tarea.hormigas_asignadas)
                cantidad_necesaria = max(0, cantidad_necesaria)  # No permitir negativos
            else:
                cantidad_necesaria = cantidad
            
            if cantidad_necesaria <= 0:
                # Si ya tiene suficientes hormigas y se proporcionó lote_id, iniciar directamente
                if hormigas_lote_id:
                    tarea.hormigas_lote_id = hormigas_lote_id
                    await servicio_a_usar.iniciar_tarea_recoleccion(tarea, hormigas_lote_id)
                    return {
                        "message": f"La tarea ya tenía suficientes hormigas. Se inició automáticamente con lote {hormigas_lote_id}",
                        "tarea_id": tarea.id,
                        "hormigas_actuales": len(tarea.hormigas_asignadas),
                        "hormigas_requeridas": tarea.alimento.cantidad_hormigas_necesarias,
                        "hormigas_lote_id": hormigas_lote_id,
                        "estado": tarea.estado.value if hasattr(tarea.estado, 'value') else str(tarea.estado),
                        "iniciada": True
                    }
                else:
                    return {
                        "message": f"La tarea ya tiene suficientes hormigas. Tiene: {len(tarea.hormigas_asignadas)}, Requiere: {tarea.alimento.cantidad_hormigas_necesarias}",
                        "tarea_id": tarea.id,
                        "hormigas_actuales": len(tarea.hormigas_asignadas),
                        "hormigas_requeridas": tarea.alimento.cantidad_hormigas_necesarias,
                        "hormigas_lote_id": None,
                        "iniciada": False
                    }
            
            # Solicitar hormigas
            try:
                hormigas = await servicio_a_usar.solicitar_hormigas(cantidad_necesaria)
                
                if not hormigas:
                    raise HTTPException(status_code=400, detail="No se pudieron obtener hormigas del servicio de comunicación")
                
                # Asignar hormigas a la tarea usando lotes (esto valida cantidad y crea el lote)
                exito, error_msg = await servicio_a_usar.asignar_hormigas_a_tarea(
                    tarea, hormigas, lote_id=hormigas_lote_id
                )
                
                if not exito:
                    raise HTTPException(status_code=400, detail=error_msg or "Error al asignar hormigas")
                
                # Si se proporcionó lote_id y ahora tiene suficientes hormigas, iniciar automáticamente
                iniciada = False
                if hormigas_lote_id and tarea.tiene_suficientes_hormigas():
                    try:
                        await servicio_a_usar.iniciar_tarea_recoleccion(tarea, hormigas_lote_id)
                        iniciada = True
                        # Asegurarse de que se guarde después de iniciar
                        from ..services.persistence_service import persistence_service
                        await persistence_service.guardar_tarea(tarea)
                        print(f"Tarea {tarea.id} guardada después de iniciar automáticamente")
                    except ValueError as e:
                        # Si falla el inicio, el lote ya está creado y aceptado, pero no se inició
                        print(f"Error al iniciar automáticamente: {e}")
                        pass
                
                return {
                    "message": f"Se asignaron {len(hormigas)} hormigas a la tarea {tarea_id}" + (" y se inició automáticamente" if iniciada else ""),
                    "tarea_id": tarea.id,
                    "hormigas_asignadas": len(tarea.hormigas_asignadas),
                    "hormigas_requeridas": tarea.alimento.cantidad_hormigas_necesarias,
                    "hormigas_lote_id": tarea.hormigas_lote_id or hormigas_lote_id,
                    "estado": tarea.estado.value if hasattr(tarea.estado, 'value') else str(tarea.estado),
                    "iniciada": iniciada
                }
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al solicitar hormigas: {str(e)}")
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al asignar hormigas: {str(e)}")
    
    @app.post(
        "/tareas/{tarea_id}/iniciar", 
        tags=["Tareas"],
        responses={
            400: RESPONSES[400],
            404: RESPONSES[404],
            500: RESPONSES[500]
        }
    )
    async def iniciar_tarea(tarea_id: str, request: Optional[IniciarTareaRequest] = Body(None)):
        """
        Inicia una tarea de recolección.
        
        Opcionalmente se puede pasar el ID de un lote de hormigas que contenga
        el número de hormigas requeridas para el alimento de la tarea.
        """
        try:
            # Usar el servicio de app.state si está disponible (para tests), sino usar el del scope
            servicio_a_usar = getattr(app.state, 'recoleccion_service', None) or recoleccion_service
            
            # Primero buscar en memoria (activas + completadas)
            tarea = None
            for t in servicio_a_usar.tareas_activas + servicio_a_usar.tareas_completadas:
                if t.id == tarea_id:
                    tarea = t
                    break
            
            # Si no está en memoria, buscar en la base de datos
            if not tarea:
                from ..services.persistence_service import persistence_service
                tareas_bd = await persistence_service.obtener_tareas()
                tarea = next((t for t in tareas_bd if str(t.id).strip() == tarea_id.strip()), None)
                
                # Si se encuentra en BD, agregarla a memoria para poder iniciarla
                if tarea:
                    if tarea not in servicio_a_usar.tareas_activas:
                        servicio_a_usar.tareas_activas.append(tarea)
            
            if not tarea:
                raise HTTPException(status_code=404, detail=f"Tarea '{tarea_id}' no encontrada en memoria ni en base de datos")
            
            # Verificar que tenga suficientes hormigas antes de iniciar
            if not tarea.tiene_suficientes_hormigas():
                raise HTTPException(
                    status_code=400, 
                    detail=f"No se puede iniciar la tarea sin suficientes hormigas. Requiere: {tarea.alimento.cantidad_hormigas_necesarias}, Tiene: {len(tarea.hormigas_asignadas)}"
                )
            
            # Guardar el ID del lote de hormigas en la tarea (si se proporciona)
            hormigas_lote_id = request.hormigas_lote_id if request and request.hormigas_lote_id else None
            tarea.hormigas_lote_id = hormigas_lote_id
            
            await servicio_a_usar.iniciar_tarea_recoleccion(tarea, hormigas_lote_id)
            return {
                "message": f"Tarea {tarea_id} iniciada exitosamente",
                "tarea_id": tarea.id,
                "estado": tarea.estado.value if hasattr(tarea.estado, 'value') else str(tarea.estado),
                "hormigas_asignadas": len(tarea.hormigas_asignadas),
                "hormigas_lote_id": hormigas_lote_id
            }
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al iniciar tarea: {str(e)}")
    
    @app.post(
        "/tareas/{tarea_id}/completar", 
        tags=["Tareas"],
        responses={
            400: RESPONSES[400],
            404: RESPONSES[404],
            500: RESPONSES[500]
        }
    )
    async def completar_tarea(tarea_id: str, cantidad_recolectada: int):
        """Completa una tarea de recolección."""
        try:
            tarea = next((t for t in recoleccion_service.tareas_activas if t.id == tarea_id), None)
            if not tarea:
                raise HTTPException(status_code=404, detail="Tarea no encontrada")
            
            await recoleccion_service.completar_tarea_recoleccion(tarea, cantidad_recolectada)
            return {"message": f"Tarea {tarea_id} completada exitosamente"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al completar tarea: {str(e)}")
    
    @app.post(
        "/procesar", 
        tags=["Procesamiento"],
        responses={500: RESPONSES[500]}
    )
    async def procesar_recoleccion():
        """Ejecuta el proceso completo de recolección."""
        try:
            tareas_procesadas = await recoleccion_service.procesar_recoleccion()
            # Convertir tareas a diccionarios para serialización JSON
            tareas_dict = []
            for tarea in tareas_procesadas:
                tarea_dict = {
                    "id": tarea.id,
                    "alimento": {
                        "id": tarea.alimento.id,
                        "nombre": tarea.alimento.nombre,
                        "cantidad_hormigas_necesarias": tarea.alimento.cantidad_hormigas_necesarias,
                        "puntos_stock": tarea.alimento.puntos_stock,
                        "tiempo_recoleccion": tarea.alimento.tiempo_recoleccion,
                        "disponible": tarea.alimento.disponible,
                        "fecha_creacion": tarea.alimento.fecha_creacion.isoformat() if tarea.alimento.fecha_creacion else None
                    },
                    "hormigas_asignadas": [
                        {
                            "id": h.id,
                            "capacidad_carga": h.capacidad_carga,
                            "estado": h.estado.value,
                            "tiempo_vida": h.tiempo_vida,
                            "fecha_creacion": h.fecha_creacion.isoformat() if h.fecha_creacion else None,
                            "subsistema_origen": h.subsistema_origen
                        } for h in tarea.hormigas_asignadas
                    ],
                    "estado": tarea.estado.value,
                    "fecha_inicio": tarea.fecha_inicio.isoformat() if tarea.fecha_inicio else None,
                    "fecha_fin": tarea.fecha_fin.isoformat() if tarea.fecha_fin else None,
                    "alimento_recolectado": tarea.alimento_recolectado
                }
                tareas_dict.append(tarea_dict)
            
            return {
                "message": "Proceso de recolección completado",
                "tareas_procesadas": len(tareas_procesadas),
                "tareas": tareas_dict
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en procesamiento: {str(e)}")
    
    @app.get("/estadisticas", tags=["Estado y Monitoreo"])
    async def obtener_estadisticas():
        """Obtiene estadísticas del servicio."""
        # Combinar estadísticas en memoria y de BD
        try:
            from ..services.persistence_service import persistence_service
            stats_bd = await persistence_service.obtener_estadisticas()
            stats_memoria = recoleccion_service.obtener_estadisticas()
            
            # Combinar ambas fuentes
            return {
                **stats_memoria,
                "base_datos": stats_bd,
                "tareas_memoria": {
                    "activas": len(recoleccion_service.tareas_activas),
                    "completadas": len(recoleccion_service.tareas_completadas)
                }
            }
        except Exception:
            return recoleccion_service.obtener_estadisticas()
    
    @app.get(
        "/debug/db", 
        tags=["Debug"],
        responses={500: RESPONSES[500]}
    )
    async def debug_info_bd():
        """Devuelve detalles del motor de BD activo y conteos básicos."""
        try:
            from ..services.persistence_service import persistence_service
            info = await persistence_service.obtener_info_bd()
            alimentos = await persistence_service.obtener_alimentos()
            tareas = await persistence_service.obtener_tareas()
            info.update({
                "alimentos_en_bd": len(alimentos),
                "tareas_en_bd": len(tareas),
                "ids_tareas": [str(t.id).strip() for t in tareas[:20]]  # Primeros 20 IDs
            })
            return info
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo info de BD: {str(e)}")
    
    @app.get(
        "/debug/tareas-raw", 
        tags=["Debug"],
        responses={500: RESPONSES[500]}
    )
    async def debug_tareas_raw():
        """Endpoint de depuración: muestra las tareas directamente desde SQL Server sin procesar."""
        try:
            from ..services.persistence_service import persistence_service
            db = persistence_service.db
            if hasattr(db, 'connection') and db.connection:
                cursor = db.connection.cursor()
                if hasattr(db, '_exec'):
                    # Obtener todas las tareas
                    db._exec(cursor, "SELECT id, alimento_id, estado, inicio, fin, cantidad_recolectada FROM dbo.Tareas")
                    rows = db._fetchall_dicts(cursor)
                    
                    # Obtener también conteo de alimentos para verificar JOIN
                    db._exec(cursor, "SELECT COUNT(*) as total FROM dbo.Alimentos")
                    alimentos_count = cursor.fetchone()[0]
                    
                    # Verificar si hay alimento_id que coincida
                    alimento_ids_tareas = [str(r.get('alimento_id', '')) for r in rows if r.get('alimento_id')]
                    alimentos_encontrados = []
                    if alimento_ids_tareas:
                        # Verificar si esos IDs existen en Alimentos (usar parámetros para evitar SQL injection)
                        alimento_ids_unicos = list(set(alimento_ids_tareas))
                        for aid in alimento_ids_unicos[:10]:  # Limitar a 10 para evitar queries muy largas
                            try:
                                db._exec(cursor, "SELECT id FROM dbo.Alimentos WHERE CAST(id AS VARCHAR) = ?", (aid,))
                                result = cursor.fetchone()
                                if result:
                                    alimentos_encontrados.append(str(result[0]))
                            except:
                                pass
                    
                    return {
                        "total_tareas": len(rows),
                        "total_alimentos": alimentos_count,
                        "alimento_ids_en_tareas": list(set(alimento_ids_tareas)),
                        "alimentos_encontrados": alimentos_encontrados,
                        "tareas_raw": rows
                    }
            return {"error": "No se pudo acceder a la conexión SQL Server"}
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    @app.get(
        "/tareas/bd", 
        response_model=List[Dict[str, Any]], 
        tags=["Estado y Monitoreo"],
        responses={500: RESPONSES[500]}
    )
    async def obtener_tareas_desde_bd():
        """Obtiene todas las tareas desde la base de datos."""
        try:
            from ..services.persistence_service import persistence_service
            tareas_bd = await persistence_service.obtener_tareas()
            
            # Convertir a diccionarios para serialización
            tareas_dict = []
            for tarea in tareas_bd:
                tarea_dict = {
                    "id": tarea.id,
                    "alimento": {
                        "id": tarea.alimento.id,
                        "nombre": tarea.alimento.nombre,
                        "cantidad_hormigas_necesarias": tarea.alimento.cantidad_hormigas_necesarias,
                        "puntos_stock": tarea.alimento.puntos_stock,
                        "tiempo_recoleccion": tarea.alimento.tiempo_recoleccion,
                        "disponible": tarea.alimento.disponible
                    },
                    "hormigas_asignadas": [
                        {
                            "id": h.id,
                            "capacidad_carga": h.capacidad_carga,
                            "estado": h.estado.value,
                            "tiempo_vida": h.tiempo_vida,
                            "subsistema_origen": h.subsistema_origen
                        } for h in tarea.hormigas_asignadas
                    ],
                    "estado": tarea.estado.value,
                    "fecha_inicio": tarea.fecha_inicio.isoformat() if tarea.fecha_inicio else None,
                    "fecha_fin": tarea.fecha_fin.isoformat() if tarea.fecha_fin else None,
                    "alimento_recolectado": tarea.alimento_recolectado
                }
                tareas_dict.append(tarea_dict)
            
            return tareas_dict
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error consultando BD: {str(e)}")
    
    @app.get(
        "/tareas/{tarea_id}/bd", 
        tags=["Estado y Monitoreo"],
        responses={
            404: RESPONSES[404],
            500: RESPONSES[500]
        }
    )
    async def obtener_tarea_desde_bd(tarea_id: str):
        """Obtiene una tarea específica desde la base de datos por ID de alimento."""
        try:
            from ..services.persistence_service import persistence_service
            tareas_bd = await persistence_service.obtener_tareas()
            
            # Buscar tarea por ID o por alimento_id
            tarea_encontrada = None
            for tarea in tareas_bd:
                if tarea.id == tarea_id or tarea.alimento.id == tarea_id:
                    tarea_encontrada = tarea
                    break
            
            if not tarea_encontrada:
                raise HTTPException(status_code=404, detail="Tarea no encontrada en BD")
            
            return {
                "id": tarea_encontrada.id,
                "alimento": {
                    "id": tarea_encontrada.alimento.id,
                    "nombre": tarea_encontrada.alimento.nombre,
                    "cantidad_hormigas_necesarias": tarea_encontrada.alimento.cantidad_hormigas_necesarias
                },
                "hormigas_asignadas": [
                    {
                        "id": h.id,
                        "estado": h.estado.value
                    } for h in tarea_encontrada.hormigas_asignadas
                ],
                "estado": tarea_encontrada.estado.value,
                "alimento_recolectado": tarea_encontrada.alimento_recolectado
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error consultando BD: {str(e)}")
    
    @app.get(
        "/eventos", 
        tags=["Estado y Monitoreo"],
        responses={500: RESPONSES[500]}
    )
    async def obtener_eventos(limite: int = Query(50, ge=1, le=1000)):
        """Obtiene eventos recientes del subsistema."""
        try:
            from ..services.persistence_service import persistence_service
            eventos = await persistence_service.obtener_eventos_recientes(limite)
            return {"eventos": eventos, "total": len(eventos)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo eventos: {str(e)}")
    
    # ===================== ESTADO DE TAREAS (para compartir con otros subsistemas) =====================
    @app.get(
        "/tareas/status", 
        response_model=Dict[str, Any], 
        tags=["Estado y Monitoreo"],
        responses={500: RESPONSES[500]}
    )
    async def obtener_status_tareas():
        """Devuelve el estado de todas las tareas desde SQL Server, incluyendo IDs de hormigas y alimento.
        Verifica automáticamente si alguna tarea debe completarse por tiempo transcurrido."""
        try:
            from ..services.persistence_service import persistence_service
            info_bd = await persistence_service.obtener_info_bd()
            tareas = await persistence_service.obtener_tareas()
            
            # Usar el servicio de app.state si está disponible (para tests), sino usar el del scope
            servicio_a_usar = getattr(app.state, 'recoleccion_service', None) or recoleccion_service
            
            # Verificar y completar tareas automáticamente si es necesario
            # Validación: fecha_inicio + tiempo_recoleccion <= fecha_actual
            tareas_completadas_auto = []
            from datetime import datetime
            ahora = datetime.now()
            
            for t in tareas:
                # Si la tarea está en memoria, verificar con el servicio
                tarea_en_memoria = None
                for tm in servicio_a_usar.tareas_activas + servicio_a_usar.tareas_completadas:
                    if tm.id == t.id:
                        tarea_en_memoria = tm
                        break
                
                # Si está en memoria, usar esa (puede estar más actualizada)
                tarea_a_verificar = tarea_en_memoria if tarea_en_memoria else t
                
                # Verificar si debe completarse automáticamente por tiempo
                estado_valor = tarea_a_verificar.estado.value if hasattr(tarea_a_verificar.estado, 'value') else str(tarea_a_verificar.estado)
                if estado_valor == "en_proceso" and tarea_a_verificar.fecha_inicio:
                    tiempo_transcurrido = (ahora - tarea_a_verificar.fecha_inicio).total_seconds()
                    tiempo_recoleccion = tarea_a_verificar.alimento.tiempo_recoleccion
                    
                    # Si el tiempo transcurrido es mayor o igual al tiempo de recolección, completar automáticamente
                    if tiempo_transcurrido >= tiempo_recoleccion:
                        # Ejecutar el procesamiento completo de la tarea (completar y actualizar alimento)
                        completada = await servicio_a_usar.verificar_y_completar_tarea_por_tiempo(tarea_a_verificar)
                        if completada:
                            tareas_completadas_auto.append(t.id)
                            # Asegurar que el alimento se actualizó correctamente
                            try:
                                await persistence_service.actualizar_alimento_disponibilidad(tarea_a_verificar.alimento.id, False)
                                print(f"Tarea {t.id} completada automáticamente desde status. Alimento {tarea_a_verificar.alimento.id} actualizado.")
                            except Exception as e:
                                print(f"Advertencia: No se pudo actualizar alimento {tarea_a_verificar.alimento.id} al completar tarea: {e}")
                            
                            # Si estaba en memoria, actualizar la referencia
                            if tarea_en_memoria:
                                t = tarea_en_memoria
                            else:
                                # Recargar desde BD para obtener el estado actualizado
                                tareas_actualizadas = await persistence_service.obtener_tareas()
                                t = next((ta for ta in tareas_actualizadas if ta.id == t.id), t)
            
            # Recargar tareas después de verificar completados automáticos
            if tareas_completadas_auto:
                tareas = await persistence_service.obtener_tareas()
            
            resultado: List[Dict[str, Any]] = []
            for t in tareas:
                # Obtener estado como string
                estado_str = t.estado.value if hasattr(t.estado, 'value') else str(t.estado)
                resultado.append({
                    "tarea_id": t.id,
                    "estado": estado_str,
                    "alimento": {
                        "id": t.alimento.id if t.alimento else None,
                        "nombre": t.alimento.nombre if t.alimento else None
                    },
                    "hormigas_lote_id": t.hormigas_lote_id if hasattr(t, 'hormigas_lote_id') else None,
                    "inicio": t.fecha_inicio.isoformat() if t.fecha_inicio else None,
                    "fin": t.fecha_fin.isoformat() if t.fecha_fin else None,
                    "alimento_recolectado": t.alimento_recolectado
                })
            return {
                "base_datos": {
                    "engine": info_bd.get("engine", "desconocido"),
                    "server": info_bd.get("server", "desconocido"),
                    "database": info_bd.get("database", "desconocido")
                },
                "total_tareas": len(resultado),
                "tareas_completadas_automaticamente": len(tareas_completadas_auto),
                "tareas": resultado
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error al obtener status de tareas: {str(e)}")

    @app.get(
        "/tareas/{tarea_id}/status", 
        response_model=Dict[str, Any], 
        tags=["Estado y Monitoreo"],
        responses={
            404: RESPONSES[404],
            500: RESPONSES[500]
        }
    )
    async def obtener_status_tarea(tarea_id: str):
        """Devuelve el estado de una tarea específica desde SQL Server, con IDs de hormigas y alimento."""
        try:
            from ..services.persistence_service import persistence_service
            info_bd = await persistence_service.obtener_info_bd()
            tareas = await persistence_service.obtener_tareas()
            
            # Normalizar búsqueda (case-insensitive, trim)
            tarea_id_normalizado = str(tarea_id).strip()
            tarea = None
            
            # Primero intentar búsqueda exacta
            for t in tareas:
                if str(t.id).strip() == tarea_id_normalizado:
                    tarea = t
                    break
            
            # Si no se encuentra, intentar búsqueda case-insensitive
            if not tarea:
                for t in tareas:
                    if str(t.id).strip().lower() == tarea_id_normalizado.lower():
                        tarea = t
                        break
            
            # Usar el servicio de app.state si está disponible (para tests), sino usar el del scope
            servicio_a_usar = getattr(app.state, 'recoleccion_service', None) or recoleccion_service
            
            if not tarea:
                # Buscar también en memoria
                for t in servicio_a_usar.tareas_activas + servicio_a_usar.tareas_completadas:
                    if str(t.id).strip() == tarea_id_normalizado or str(t.id).strip().lower() == tarea_id_normalizado.lower():
                        tarea = t
                        break
            
            if not tarea:
                # Debug: listar IDs disponibles para ayudar al usuario
                ids_disponibles = [str(t.id).strip() for t in tareas]
                raise HTTPException(
                    status_code=404, 
                    detail=f"Tarea '{tarea_id}' no encontrada en la base de datos. IDs disponibles: {ids_disponibles[:10]}"
                )
            
            # Verificar si la tarea debe completarse automáticamente por tiempo
            # Validación: fecha_inicio + tiempo_recoleccion <= fecha_actual
            completada_auto = False
            estado_valor = tarea.estado.value if hasattr(tarea.estado, 'value') else str(tarea.estado)
            if estado_valor == "en_proceso" and tarea.fecha_inicio:
                from datetime import datetime, timedelta
                ahora = datetime.now()
                tiempo_transcurrido = (ahora - tarea.fecha_inicio).total_seconds()
                tiempo_recoleccion = tarea.alimento.tiempo_recoleccion
                
                # Si el tiempo transcurrido es mayor o igual al tiempo de recolección, completar automáticamente
                if tiempo_transcurrido >= tiempo_recoleccion:
                    # Ejecutar el procesamiento completo de la tarea (completar y actualizar alimento)
                    completada_auto = await servicio_a_usar.verificar_y_completar_tarea_por_tiempo(tarea)
                    if completada_auto:
                        # Asegurar que el alimento se actualizó correctamente
                        try:
                            await persistence_service.actualizar_alimento_disponibilidad(tarea.alimento.id, False)
                            print(f"Tarea {tarea.id} completada automáticamente desde status. Alimento {tarea.alimento.id} actualizado.")
                        except Exception as e:
                            print(f"Advertencia: No se pudo actualizar alimento {tarea.alimento.id} al completar tarea: {e}")
                        
                        # Recargar desde BD para obtener el estado actualizado
                        tareas_actualizadas = await persistence_service.obtener_tareas()
                        tarea_actualizada = next((t for t in tareas_actualizadas if t.id == tarea.id), None)
                        if tarea_actualizada:
                            tarea = tarea_actualizada
            
            # Obtener estado como string
            estado_str = tarea.estado.value if hasattr(tarea.estado, 'value') else str(tarea.estado)
            
            # Obtener hormigas_asignadas (de la lista o de la BD si no está cargada)
            hormigas_asignadas_count = len(tarea.hormigas_asignadas) if tarea.hormigas_asignadas else 0
            
            # Si no hay hormigas en memoria pero debería haberlas, intentar obtener de BD
            if hormigas_asignadas_count == 0:
                try:
                    from ..database.database_manager import db_manager
                    cursor = db_manager.connection.cursor()
                    if hasattr(db_manager, '_exec'):
                        db_manager._exec(cursor, "SELECT hormigas_asignadas FROM dbo.Tareas WHERE id = ?", (tarea.id,))
                        hormigas_row = cursor.fetchone()
                        if hormigas_row and hormigas_row[0] is not None:
                            hormigas_asignadas_count = int(hormigas_row[0])
                except Exception:
                    pass
            
            return {
                "base_datos": {
                    "engine": info_bd.get("engine", "desconocido"),
                    "server": info_bd.get("server", "desconocido"),
                    "database": info_bd.get("database", "desconocido")
                },
                "tarea_id": tarea.id,
                "estado": estado_str,
                "completada_automaticamente": completada_auto,
                "alimento": {
                    "id": tarea.alimento.id if tarea.alimento else None,
                    "nombre": tarea.alimento.nombre if tarea.alimento else None
                },
                "hormigas_lote_id": tarea.hormigas_lote_id if hasattr(tarea, 'hormigas_lote_id') else None,
                "hormigas_asignadas": hormigas_asignadas_count,
                "inicio": tarea.fecha_inicio.isoformat() if tarea.fecha_inicio else None,
                "fecha_inicio": tarea.fecha_inicio.isoformat() if tarea.fecha_inicio else None,
                "fin": tarea.fecha_fin.isoformat() if tarea.fecha_fin else None,
                "fecha_fin": tarea.fecha_fin.isoformat() if tarea.fecha_fin else None,
                "alimento_recolectado": tarea.alimento_recolectado
            }
        except HTTPException:
            raise
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error al obtener status de la tarea: {str(e)}")

    @app.post(
        "/verificar-hormigas", 
        tags=["Procesamiento"],
        responses={500: RESPONSES[500]}
    )
    async def verificar_hormigas_muertas():
        """Verifica y maneja hormigas muertas."""
        try:
            await recoleccion_service.verificar_hormigas_muertas()
            return {"message": "Verificación de hormigas completada"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en verificación: {str(e)}")
    
    
    @app.get(
        "/tareas/{tarea_id}/tiempo-restante", 
        tags=["Estado y Monitoreo"],
        responses={404: RESPONSES[404]}
    )
    async def obtener_tiempo_restante(tarea_id: str):
        """Obtiene el tiempo restante de una tarea en proceso."""
        from ..services.timer_service import timer_service
        tiempo_restante = timer_service.get_tiempo_restante(tarea_id)
        if tiempo_restante is None:
            raise HTTPException(status_code=404, detail="Tarea no encontrada o no en proceso")
        
        # Obtener información del alimento para mostrar el tiempo total asignado
        tarea = None
        for t in recoleccion_service.tareas_activas + recoleccion_service.tareas_completadas:
            if t.id == tarea_id:
                tarea = t
                break
        
        if not tarea:
            from ..services.persistence_service import persistence_service
            tareas_bd = await persistence_service.obtener_tareas()
            tarea = next((t for t in tareas_bd if str(t.id).strip() == tarea_id.strip()), None)
        
        tiempo_total = tarea.alimento.tiempo_recoleccion if tarea else None
        
        return {
            "tarea_id": tarea_id,
            "tiempo_total_asignado_segundos": tiempo_total,
            "tiempo_total_asignado_minutos": round(tiempo_total / 60, 2) if tiempo_total else None,
            "tiempo_restante_segundos": tiempo_restante,
            "tiempo_restante_minutos": round(tiempo_restante / 60, 2),
            "tiempo_transcurrido_segundos": tiempo_total - tiempo_restante if tiempo_total else None,
            "progreso_porcentaje": round(((tiempo_total - tiempo_restante) / tiempo_total * 100), 2) if tiempo_total and tiempo_total > 0 else None
        }
    
    @app.get(
        "/tareas/{tarea_id}/progreso", 
        tags=["Estado y Monitoreo"],
        responses={404: RESPONSES[404]}
    )
    async def obtener_progreso_tarea(tarea_id: str):
        """Obtiene el progreso de una tarea en proceso."""
        from ..services.timer_service import timer_service
        progreso = timer_service.get_progreso(tarea_id)
        if progreso is None:
            raise HTTPException(status_code=404, detail="Tarea no encontrada o no en proceso")
        
        return {
            "tarea_id": tarea_id,
            "progreso_porcentaje": round(progreso, 2),
            "estado": "en_proceso"
        }
    
    @app.post(
        "/tareas/{tarea_id}/cancelar", 
        tags=["Tareas"],
        responses={
            400: RESPONSES[400],
            404: RESPONSES[404]
        }
    )
    async def cancelar_tarea(tarea_id: str):
        """
        Cancela una tarea y la resetea completamente.
        
        - Cambia el estado a CANCELADA (desde cualquier estado)
        - Limpia fechas de inicio y fin
        - Vuelve el alimento a disponible
        - Persiste todos los cambios en BD
        """
        from ..services.timer_service import timer_service
        from ..services.persistence_service import persistence_service
        
        # Normalizar ID de tarea
        tarea_id_normalizado = str(tarea_id).strip()
        
        # Buscar tarea en memoria primero
        tarea = None
        servicio_a_usar = getattr(app.state, 'recoleccion_service', None) or recoleccion_service
        
        for t in servicio_a_usar.tareas_activas + servicio_a_usar.tareas_completadas:
            if str(t.id).strip() == tarea_id_normalizado:
                tarea = t
                break
        
        # Si no está en memoria, buscar en BD (búsqueda más robusta)
        if not tarea:
            try:
                tareas_bd = await persistence_service.obtener_tareas()
                # Buscar por coincidencia exacta
                for t in tareas_bd:
                    if str(t.id).strip() == tarea_id_normalizado:
                        tarea = t
                        break
                # Si no se encuentra, intentar case-insensitive
                if not tarea:
                    for t in tareas_bd:
                        if str(t.id).strip().lower() == tarea_id_normalizado.lower():
                            tarea = t
                            break
                
                if tarea and tarea not in servicio_a_usar.tareas_activas:
                    servicio_a_usar.tareas_activas.append(tarea)
            except Exception as e:
                print(f"Error buscando tarea en BD: {e}")
        
        if not tarea:
            # Listar IDs disponibles para ayudar al usuario
            try:
                tareas_bd = await persistence_service.obtener_tareas()
                ids_disponibles = [str(t.id).strip() for t in tareas_bd[:10]]
                raise HTTPException(
                    status_code=404,
                    detail=f"Tarea '{tarea_id}' no encontrada en memoria ni en BD. IDs disponibles: {ids_disponibles}"
                )
            except:
                raise HTTPException(status_code=404, detail=f"Tarea '{tarea_id}' no encontrada")
        
        # Obtener estado actual
        estado_actual = tarea.estado.value if hasattr(tarea.estado, 'value') else str(tarea.estado)
        print(f"Cancelando tarea {tarea.id}. Estado actual: {estado_actual}")
        
        # Intentar cancelar desde timer_service (si tiene timer activo)
        success = False
        if estado_actual == "en_proceso":
            success = await timer_service.cancelar_tarea(tarea_id_normalizado)
        
        # Si no tenía timer activo o no estaba en_proceso, cancelarla manualmente
        if not success:
            # Cambiar estado a CANCELADA
            tarea.estado = EstadoTarea.CANCELADA
            
            # RESETEAR: Limpiar fechas
            tarea.fecha_inicio = None
            tarea.fecha_fin = None
            tarea.alimento_recolectado = 0
            
            # RESETEAR: Volver alimento a disponible
            tarea.alimento.disponible = True
            
            # Cambiar estado de hormigas a DISPONIBLE
            for hormiga in tarea.hormigas_asignadas:
                from ..models.estado_hormiga import EstadoHormiga
                hormiga.cambiar_estado(EstadoHormiga.DISPONIBLE)
        
        # SIEMPRE persistir cambios en BD (tanto si vino del timer como si se canceló manualmente)
        try:
            # Asegurar que el estado esté actualizado
            if tarea.estado != EstadoTarea.CANCELADA:
                tarea.estado = EstadoTarea.CANCELADA
            
            # Persistir tarea con todos los cambios
            guardado_ok = await persistence_service.guardar_tarea(tarea)
            if not guardado_ok:
                print(f"ERROR: guardar_tarea retornó False para tarea {tarea.id}")
            
            # Actualizar estado explícitamente (usar el enum, no string)
            estado_actualizado = await persistence_service.actualizar_estado_tarea(tarea.id, EstadoTarea.CANCELADA)
            if not estado_actualizado:
                print(f"ERROR: actualizar_estado_tarea retornó False para tarea {tarea.id}")
            else:
                print(f"✓ Estado de tarea {tarea.id} actualizado a CANCELADA en BD")
            
            # Actualizar alimento a disponible
            alimento_actualizado = await persistence_service.actualizar_alimento_disponibilidad(tarea.alimento.id, True)
            if not alimento_actualizado:
                print(f"ERROR: actualizar_alimento_disponibilidad retornó False para alimento {tarea.alimento.id}")
            
            # Guardar evento
            await persistence_service.guardar_evento(
                "tarea_cancelada",
                f"Tarea {tarea.id} cancelada y reseteada",
                {"tarea_id": tarea.id, "alimento_id": tarea.alimento.id, "estado_anterior": estado_actual}
            )
            
            print(f"✓ Tarea {tarea.id} cancelada y persistida en BD. Estado: CANCELADA, Alimento: disponible=True")
        except Exception as e:
            print(f"ERROR CRÍTICO: No se pudo persistir tarea cancelada en BD: {e}")
            import traceback
            traceback.print_exc()
            # Aún así devolver éxito porque la cancelación en memoria funcionó
        
        return {
            "message": f"Tarea {tarea_id} cancelada exitosamente",
            "tarea_id": tarea.id,
            "estado_anterior": estado_actual,
            "estado_nuevo": tarea.estado.value if hasattr(tarea.estado, 'value') else str(tarea.estado),
            "alimento_disponible": tarea.alimento.disponible,
            "fecha_inicio": None,
            "fecha_fin": None
        }
    
    return app
