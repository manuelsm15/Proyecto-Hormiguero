# language: es
Feature: Subsistema de Recoleccion de Alimentos
  Como encargado de recoleccion
  Necesito poder gestionar el proceso de recoleccion de alimentos
  Para mantener el suministro de alimento de la colonia

  Background:
    Given que el subsistema de recoleccion esta configurado
    And que los servicios de entorno y comunicacion estan disponibles

  Scenario: Consultar alimentos disponibles exitosamente
    Given que hay alimentos disponibles en el entorno
    When consulto los alimentos disponibles
    Then debo recibir una lista de alimentos

  Scenario: Crear tarea de recoleccion
    Given que tengo un alimento disponible
    When creo una tarea de recoleccion para ese alimento
    Then la tarea debe estar en estado PENDIENTE

  Scenario: Solicitar hormigas para recoleccion
    Given que necesito 3 hormigas para una tarea
    When solicito las hormigas al subsistema de comunicacion
    Then debo recibir las hormigas solicitadas

