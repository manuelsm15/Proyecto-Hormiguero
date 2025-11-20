"""
Script que muestra instrucciones para usar Postman con el proyecto.
"""

def main():
    print("\n" + "="*70)
    print("  COMO USAR POSTMAN CON ESTE PROYECTO")
    print("="*70)
    
    print("\n1. IMPORTAR COLECCION EN POSTMAN")
    print("-" * 70)
    print("  a) Abre Postman")
    print("  b) Haz clic en 'Import' (arriba a la izquierda)")
    print("  c) Selecciona 'File'")
    print("  d) Navega a la carpeta del proyecto")
    print("  e) Selecciona: POSTMAN_COLLECTION.json")
    print("  f) Haz clic en 'Import'")
    
    print("\n2. CONFIGURAR AMBIENTE (Opcional pero Recomendado)")
    print("-" * 70)
    print("  a) En Postman, haz clic en 'Environments'")
    print("  b) Crea un nuevo ambiente llamado 'Local Development'")
    print("  c) Agrega variable:")
    print("     - Variable: base_url")
    print("     - Initial Value: http://localhost:8000")
    print("     - Current Value: http://localhost:8000")
    print("  d) Selecciona este ambiente en el dropdown superior")
    
    print("\n3. INICIAR EL SERVIDOR")
    print("-" * 70)
    print("  En PowerShell:")
    print("    cd 'C:\\Users\\manue\\Proyecto Hormiguero'")
    print("    python main.py")
    print("\n  Espera a ver: 'Application startup complete'")
    
    print("\n4. PROBAR EN POSTMAN")
    print("-" * 70)
    print("  Orden recomendado de pruebas:")
    print("\n  1. GET /health")
    print("     - Verifica que el servidor esta funcionando")
    print("\n  2. GET /alimentos")
    print("     - Lista alimentos disponibles")
    print("\n  3. POST /tareas")
    print("     - Crea una nueva tarea")
    print("\n  4. GET /tareas")
    print("     - Lista todas las tareas creadas")
    print("\n  5. POST /procesar")
    print("     - Ejecuta proceso automatico completo")
    print("\n  6. GET /estadisticas")
    print("     - Ver estadisticas actualizadas")
    print("\n  7. GET /eventos?limite=10")
    print("     - Ver eventos recientes")
    
    print("\n5. ENDPOINTS PRINCIPALES")
    print("-" * 70)
    print("  GET  /health                    - Estado del sistema")
    print("  GET  /alimentos                 - Listar alimentos")
    print("  GET  /alimentos?zona_id=1       - Filtrar por zona")
    print("  GET  /alimentos?estado=disponible - Filtrar por estado")
    print("  POST /tareas                    - Crear tarea")
    print("  GET  /tareas                    - Listar tareas")
    print("  GET  /tareas/activas            - Solo activas")
    print("  GET  /tareas/completadas        - Solo completadas")
    print("  POST /tareas/{id}/iniciar       - Iniciar tarea")
    print("  POST /tareas/{id}/completar     - Completar tarea")
    print("  POST /procesar                  - Proceso automatico")
    print("  GET  /estadisticas              - Estadisticas")
    print("  GET  /eventos                   - Eventos")
    print("  GET  /tareas/bd                 - Tareas desde BD")
    
    print("\n6. ARCHIVO DE COLECCION")
    print("-" * 70)
    print("  Ubicacion: POSTMAN_COLLECTION.json")
    print("  Este archivo contiene todas las requests pre-configuradas")
    
    print("\n7. DOCUMENTACION ADICIONAL")
    print("-" * 70)
    print("  Ver archivo: GUIA_POSTMAN.md")
    print("  Contiene ejemplos detallados y solucion de problemas")
    
    print("\n8. DOCUMENTACION INTERACTIVA")
    print("-" * 70)
    print("  Tambien puedes probar desde el navegador:")
    print("  http://localhost:8000/docs")
    print("  (Swagger UI - similar a Postman pero en el navegador)")
    
    print("\n" + "="*70)
    print("  LISTO PARA USAR POSTMAN!")
    print("="*70)
    print("\nImporta POSTMAN_COLLECTION.json en Postman y comenzar a probar!")
    print("\n")


if __name__ == "__main__":
    main()



