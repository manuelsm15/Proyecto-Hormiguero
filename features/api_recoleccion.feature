# language: es
Feature: APIs del Subsistema de Recolección de Alimentos
  Como usuario del sistema
  Necesito poder interactuar con las APIs del subsistema
  Para gestionar alimentos, tareas y hormigas

  Background:
    Given que el subsistema de recolección está configurado
    And que los servicios de entorno y comunicación están disponibles

  @api @alimentos
  Scenario: Consultar alimentos disponibles exitosamente
    Given que hay alimentos disponibles en el entorno
    When consulto los alimentos disponibles mediante GET /alimentos
    Then debo recibir un código de respuesta 200
    And la respuesta debe ser una lista de alimentos
    And cada alimento debe tener sus propiedades correctas

  @api @alimentos
  Scenario: Consultar alimentos con filtro de estado disponible
    Given que hay alimentos disponibles y no disponibles en el sistema
    When realizo una petición GET a /alimentos?estado=disponible
    Then debo recibir un código de respuesta 200
    And la respuesta debe contener solo alimentos disponibles

  @api @alimentos
  Scenario: Crear alimento exitosamente
    Given que tengo los datos de un nuevo alimento:
      | nombre                       | cantidad_hormigas_necesarias | puntos_stock | tiempo_recoleccion |
      | Nueva Fruta                  | 2                           | 5            | 180                |
    When realizo una petición POST a /alimentos con el cuerpo JSON
    Then debo recibir un código de respuesta 200
    And la respuesta debe contener el alimento creado
    And el alimento debe tener un ID generado automáticamente

  @api @tareas
  Scenario: Crear tarea de recolección exitosamente
    Given que tengo un alimento disponible con ID "A1"
    When realizo una petición POST a /tareas con:
      | parámetro  | valor      |
      | tarea_id   | T1001      |
      | alimento_id| A1         |
    Then debo recibir un código de respuesta 200
    And la respuesta debe contener la tarea creada
    And la tarea debe tener estado "pendiente"
    And la tarea debe tener el alimento asignado

  @api @tareas
  Scenario: Fallar al crear tarea con alimento no disponible
    Given que tengo un alimento que no está disponible con ID "A2"
    When intento crear una tarea de recolección para ese alimento
    Then debo recibir un código de respuesta 400
    And el mensaje de error debe indicar que el alimento no está disponible

  @api @tareas
  Scenario: Fallar al crear tarea con alimento inexistente
    Given que no existe un alimento con ID "ALIMENTO_INEXISTENTE"
    When intento crear una tarea de recolección para ese alimento
    Then debo recibir un código de respuesta 404
    And el mensaje de error debe indicar "Alimento no encontrado"

  @api @tareas
  Scenario: Listar todas las tareas
    Given que hay tareas activas y completadas en el sistema
    When realizo una petición GET a /tareas
    Then debo recibir un código de respuesta 200
    And la respuesta debe ser una lista de tareas

  @api @hormigas
  Scenario: Asignar hormigas a tarea exitosamente
    Given que tengo una tarea con ID "T1001" en estado "pendiente"
    And la tarea requiere 3 hormigas
    When realizo una petición POST a /tareas/T1001/asignar-hormigas con cantidad 3
    Then debo recibir un código de respuesta 200
    And la respuesta debe indicar que se asignaron 3 hormigas
    And la tarea debe tener 3 hormigas asignadas

  @api @hormigas
  Scenario: Asignar hormigas con lote_id e inicio automático
    Given que tengo una tarea con ID "T1001" en estado "pendiente"
    And la tarea requiere 3 hormigas
    When realizo una petición POST a /tareas/T1001/asignar-hormigas con lote_id "LOTE_001" y cantidad 3
    Then debo recibir un código de respuesta 200
    And la respuesta debe indicar que la tarea se inició automáticamente
    And la tarea debe tener estado "en_proceso"

  @api @tareas
  Scenario: Iniciar tarea exitosamente
    Given que tengo una tarea con ID "T1001" en estado "pendiente"
    And la tarea tiene 3 hormigas asignadas
    And la tarea requiere 3 hormigas
    When realizo una petición POST a /tareas/T1001/iniciar con lote_id "LOTE_001"
    Then debo recibir un código de respuesta 200
    And la respuesta debe indicar que la tarea se inició exitosamente
    And la tarea debe tener estado "en_proceso"
    And la tarea debe tener fecha_inicio establecida

  @api @tareas
  Scenario: Fallar al iniciar tarea sin suficientes hormigas
    Given que tengo una tarea con ID "T1001" en estado "pendiente"
    And la tarea requiere 3 hormigas
    And la tarea tiene 0 hormigas asignadas
    When intento iniciar la tarea
    Then debo recibir un código de respuesta 400
    And el mensaje de error debe indicar que no hay suficientes hormigas

  @api @tareas
  Scenario: Completar tarea exitosamente
    Given que tengo una tarea con ID "T1001" en estado "en_proceso"
    And la tarea tiene fecha_inicio establecida
    When realizo una petición POST a /tareas/T1001/completar con cantidad_recolectada 10
    Then debo recibir un código de respuesta 200
    And la respuesta debe indicar que la tarea se completó exitosamente
    And la tarea debe tener estado "completada"
    And la tarea debe tener fecha_fin establecida
    And el alimento asociado debe estar marcado como no disponible

  @api @status
  Scenario: Obtener status de todas las tareas
    Given que hay tareas activas y completadas en el sistema
    When realizo una petición GET a /tareas/status
    Then debo recibir un código de respuesta 200
    And la respuesta debe ser una lista de tareas con su status

  @api @status
  Scenario: Obtener status de tarea específica
    Given que tengo una tarea con ID "T1001" en estado "en_proceso"
    And la tarea tiene lote_id "LOTE_001"
    When realizo una petición GET a /tareas/T1001/status
    Then debo recibir un código de respuesta 200
    And la respuesta debe contener el status de la tarea
    And el status debe incluir el lote_id "LOTE_001"




