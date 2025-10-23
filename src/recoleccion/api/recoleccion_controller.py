"""
Controlador REST para el subsistema de recolección.
"""

from fastapi import FastAPI, HTTPException, Depends
from typing import List, Dict, Any
import asyncio

from ..services.recoleccion_service import RecoleccionService
from ..services.entorno_service import EntornoService
from ..services.comunicacion_service import ComunicacionService
from ..models.alimento import Alimento
from ..models.tarea_recoleccion import TareaRecoleccion


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
        description="API para la gestión de recolección de alimentos en la simulación de colonia de hormigas",
        version="1.0.0"
    )
    
    # Inicializar servicio de recolección
    recoleccion_service = RecoleccionService(entorno_service, comunicacion_service)
    
    @app.get("/")
    async def root():
        """Endpoint raíz."""
        return {"message": "Subsistema de Recolección de Alimentos - Universidad Cenfotec"}
    
    @app.get("/health")
    async def health_check():
        """Verificación de salud del servicio."""
        try:
            entorno_disponible = await entorno_service.is_disponible()
            comunicacion_disponible = await comunicacion_service.is_disponible()
            
            return {
                "status": "healthy" if entorno_disponible and comunicacion_disponible else "unhealthy",
                "entorno_disponible": entorno_disponible,
                "comunicacion_disponible": comunicacion_disponible
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en verificación de salud: {str(e)}")
    
    @app.get("/alimentos", response_model=List[Alimento])
    async def consultar_alimentos():
        """Consulta los alimentos disponibles en el entorno."""
        try:
            alimentos = await recoleccion_service.consultar_alimentos_disponibles()
            return alimentos
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al consultar alimentos: {str(e)}")
    
    @app.post("/tareas", response_model=TareaRecoleccion)
    async def crear_tarea(tarea_id: str, alimento_id: str):
        """Crea una nueva tarea de recolección."""
        try:
            # Primero obtener el alimento
            alimento = await entorno_service.consultar_alimento_por_id(alimento_id)
            if not alimento:
                raise HTTPException(status_code=404, detail="Alimento no encontrado")
            
            tarea = await recoleccion_service.crear_tarea_recoleccion(tarea_id, alimento)
            return tarea
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear tarea: {str(e)}")
    
    @app.get("/tareas", response_model=List[TareaRecoleccion])
    async def listar_tareas():
        """Lista todas las tareas activas."""
        return recoleccion_service.tareas_activas
    
    @app.get("/tareas/completadas", response_model=List[TareaRecoleccion])
    async def listar_tareas_completadas():
        """Lista todas las tareas completadas."""
        return recoleccion_service.tareas_completadas
    
    @app.post("/tareas/{tarea_id}/iniciar")
    async def iniciar_tarea(tarea_id: str):
        """Inicia una tarea de recolección."""
        try:
            tarea = next((t for t in recoleccion_service.tareas_activas if t.id == tarea_id), None)
            if not tarea:
                raise HTTPException(status_code=404, detail="Tarea no encontrada")
            
            await recoleccion_service.iniciar_tarea_recoleccion(tarea)
            return {"message": f"Tarea {tarea_id} iniciada exitosamente"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al iniciar tarea: {str(e)}")
    
    @app.post("/tareas/{tarea_id}/completar")
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
    
    @app.post("/procesar")
    async def procesar_recoleccion():
        """Ejecuta el proceso completo de recolección."""
        try:
            tareas_procesadas = await recoleccion_service.procesar_recoleccion()
            return {
                "message": "Proceso de recolección completado",
                "tareas_procesadas": len(tareas_procesadas),
                "tareas": tareas_procesadas
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en procesamiento: {str(e)}")
    
    @app.get("/estadisticas")
    async def obtener_estadisticas():
        """Obtiene estadísticas del servicio."""
        return recoleccion_service.obtener_estadisticas()
    
    @app.post("/verificar-hormigas")
    async def verificar_hormigas_muertas():
        """Verifica y maneja hormigas muertas."""
        try:
            await recoleccion_service.verificar_hormigas_muertas()
            return {"message": "Verificación de hormigas completada"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en verificación: {str(e)}")
    
    @app.get("/tareas/en-proceso")
    async def listar_tareas_en_proceso():
        """Lista tareas que están en proceso con tiempo real."""
        from ..services.timer_service import timer_service
        tareas = timer_service.get_tareas_en_proceso()
        return [tarea.to_dict() for tarea in tareas]
    
    @app.get("/tareas/{tarea_id}/tiempo-restante")
    async def obtener_tiempo_restante(tarea_id: str):
        """Obtiene el tiempo restante de una tarea en proceso."""
        from ..services.timer_service import timer_service
        tiempo_restante = timer_service.get_tiempo_restante(tarea_id)
        if tiempo_restante is None:
            raise HTTPException(status_code=404, detail="Tarea no encontrada o no en proceso")
        
        return {
            "tarea_id": tarea_id,
            "tiempo_restante_segundos": tiempo_restante,
            "tiempo_restante_minutos": round(tiempo_restante / 60, 2)
        }
    
    @app.get("/tareas/{tarea_id}/progreso")
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
    
    @app.post("/tareas/{tarea_id}/cancelar")
    async def cancelar_tarea(tarea_id: str):
        """Cancela una tarea en proceso."""
        from ..services.timer_service import timer_service
        success = await timer_service.cancelar_tarea(tarea_id)
        if not success:
            raise HTTPException(status_code=404, detail="Tarea no encontrada o no en proceso")
        
        return {"message": f"Tarea {tarea_id} cancelada exitosamente"}
    
    return app
