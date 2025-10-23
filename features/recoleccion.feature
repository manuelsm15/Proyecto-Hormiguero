# language: es
Feature: Subsistema de Recoleccion de Alimentos
  Como encargado de recoleccion
  Necesito poder gestionar el proceso de recoleccion de alimentos
  Para mantener el suministro de alimento de la colonia

  Background:
    Given que el subsistema de recolección está configurado
    And que los servicios de entorno y comunicación están disponibles

  @unitario
  Scenario: Consultar alimentos disponibles exitosamente
    Given que hay alimentos disponibles en el entorno
    When consulto los alimentos disponibles
    Then debo recibir una lista de alimentos
    And cada alimento debe tener sus propiedades correctas

  @unitario
  Scenario: Crear tarea de recolección
    Given que tengo un alimento disponible
    When creo una tarea de recolección para ese alimento
    Then la tarea debe estar en estado PENDIENTE
    And la tarea debe tener el alimento asignado

  @unitario
  Scenario: Solicitar hormigas para recolección
    Given que necesito 3 hormigas para una tarea
    When solicito las hormigas al subsistema de comunicación
    Then debo recibir las hormigas solicitadas
    And las hormigas deben estar disponibles

  @unitario
  Scenario: Asignar hormigas a una tarea
    Given que tengo una tarea de recolección
    And tengo hormigas disponibles
    When asigno las hormigas a la tarea
    Then la tarea debe tener las hormigas asignadas
    And las hormigas deben estar en estado DISPONIBLE

  @unitario
  Scenario: Iniciar tarea de recolección exitosamente
    Given que tengo una tarea con suficientes hormigas asignadas
    When inicio la tarea de recolección
    Then la tarea debe estar en estado EN_PROCESO
    And las hormigas deben estar en estado BUSCANDO
    And la tarea debe tener fecha de inicio

  @unitario
  Scenario: Fallar al iniciar tarea sin suficientes hormigas
    Given que tengo una tarea con hormigas insuficientes
    When intento iniciar la tarea de recolección
    Then debe lanzar una excepción
    And la tarea debe permanecer en estado PENDIENTE

  @unitario
  Scenario: Completar tarea de recolección
    Given que tengo una tarea en estado EN_PROCESO
    When completo la tarea con 10 unidades de alimento
    Then la tarea debe estar en estado COMPLETADA
    And la tarea debe tener 10 unidades de alimento recolectado
    And las hormigas deben estar en estado TRANSPORTANDO
    And la tarea debe tener fecha de finalización

  @integracion
  Scenario: Procesar recolección completa
    Given que hay alimentos disponibles en el entorno
    When ejecuto el proceso completo de recolección
    Then debo tener tareas completadas
    And el alimento debe estar marcado como recolectado en el entorno
    And las hormigas deben ser devueltas al subsistema de comunicación

  @integracion
  Scenario: Manejar fallo en servicio de entorno
    Given que el servicio de entorno no está disponible
    When intento consultar alimentos disponibles
    Then debe lanzar una excepción indicando que el servicio no está disponible

  @integracion
  Scenario: Manejar fallo en servicio de comunicación
    Given que el servicio de comunicación no está disponible
    When intento solicitar hormigas
    Then debe lanzar una excepción indicando que el servicio no está disponible

  @límite
  Scenario: Procesar múltiples alimentos simultáneamente
    Given que hay 5 alimentos disponibles en el entorno
    When ejecuto el proceso de recolección
    Then debo procesar los 5 alimentos
    And cada alimento debe tener su tarea correspondiente
    And todas las tareas deben completarse exitosamente

  @límite
  Scenario: Manejar hormigas muertas durante la recolección
    Given que tengo una tarea en proceso con hormigas
    And algunas hormigas mueren durante la recolección
    When verifico el estado de las hormigas
    Then la tarea debe pausarse
    And la tarea debe estar en estado PAUSADA
