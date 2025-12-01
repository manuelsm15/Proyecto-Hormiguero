# Resumen: Por qué las tareas no se procesan automáticamente

## Problema Identificado

La tarea `TEST_DIRECT_13372` tenía:
- ✅ Lote de hormigas creado y aceptado
- ✅ 3 hormigas asignadas (cantidad suficiente)
- ✅ Asignaciones guardadas en BD
- ❌ **Estado: `pendiente` (no iniciada)**
- ❌ **Sin `fecha_inicio`**

## Qué Faltaba

Para que una tarea se procese automáticamente, necesita:

1. **Estado `en_proceso`** (no `pendiente`)
2. **`fecha_inicio` establecida**
3. **Lote en estado `en_uso`** (no solo `aceptado`)
4. **Hormigas asignadas** (esto ya estaba correcto)

## Solución Aplicada

Se ejecutó `iniciar_tarea_manual.py` que:
1. Inició la tarea (cambió estado a `en_proceso`)
2. Estableció `fecha_inicio`
3. Marcó el lote como `en_uso`
4. Luego se completó la tarea

## Estado Final

La tarea `TEST_DIRECT_13372` ahora está:
- ✅ Estado: `completada`
- ✅ Fecha inicio: 2025-11-20 13:58:43
- ✅ Fecha fin: 2025-11-20 13:59:16
- ✅ Cantidad recolectada: 10
- ✅ Hormigas asignadas: 3 (se mantiene)
- ✅ Lote: `en_uso`

## Por qué no se procesaba automáticamente

El problema es que cuando se asignan hormigas con `lote_id` a través del API:
1. El lote se crea y acepta ✅
2. Las hormigas se asignan ✅
3. **PERO la tarea NO se inicia automáticamente** ❌

El código tiene lógica para iniciar automáticamente cuando se asigna con `lote_id`, pero parece que no se está ejecutando correctamente o el servicio no tiene el código actualizado.

## Solución Permanente

Para que las tareas se procesen automáticamente después de asignar hormigas:

1. **Reiniciar el servicio** para usar el código actualizado que:
   - Inicia automáticamente cuando se asigna con `lote_id`
   - Guarda correctamente en BD
   - Marca el lote como `en_uso`

2. **O iniciar manualmente** después de asignar:
   ```bash
   POST /tareas/{tarea_id}/iniciar
   Body: {"hormigas_lote_id": "LOTE_ID"}
   ```

## Scripts Disponibles

- `iniciar_tarea_manual.py` - Inicia una tarea específica
- `procesar_tarea_completa.py` - Inicia y completa una tarea
- `verificar_tarea_especifica.py` - Verifica el estado completo de una tarea



