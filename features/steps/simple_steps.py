from behave import given, when, then

@given("que tengo un sistema funcionando")
def step_impl(context):
    context.sistema = "funcionando"

@when("ejecuto una prueba")
def step_impl(context):
    context.resultado = "exitoso"

@then("debo obtener un resultado exitoso")
def step_impl(context):
    assert context.resultado == "exitoso"

