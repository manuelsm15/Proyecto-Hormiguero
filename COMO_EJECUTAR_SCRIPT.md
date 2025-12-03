# Cómo Ejecutar el Script ejecutar_todo.py

## Opción 1: Desde PowerShell (Windows)

1. Abre PowerShell
2. Navega al directorio del proyecto:
   ```powershell
   cd "C:\Users\manue\Proyecto Hormiguero"
   ```
3. Ejecuta el script:
   ```powershell
   python ejecutar_todo.py
   ```

## Opción 2: Desde CMD (Windows)

1. Abre CMD (Símbolo del sistema)
2. Navega al directorio del proyecto:
   ```cmd
   cd "C:\Users\manue\Proyecto Hormiguero"
   ```
3. Ejecuta el script:
   ```cmd
   python ejecutar_todo.py
   ```

## Opción 3: Desde el Explorador de Windows

1. Abre el Explorador de Windows
2. Navega a: `C:\Users\manue\Proyecto Hormiguero`
3. Haz clic derecho en `ejecutar_todo.py`
4. Selecciona "Abrir con" → "Python"

## Opción 4: Desde Visual Studio Code / Cursor

1. Abre el archivo `ejecutar_todo.py` en el editor
2. Haz clic derecho en el archivo
3. Selecciona "Run Python File in Terminal"
   O presiona `Ctrl + Shift + P` y busca "Python: Run Python File in Terminal"

## Opción 5: Desde la Terminal Integrada

Si estás en Cursor/VS Code:
1. Abre la terminal integrada (`Ctrl + `` ` o `View → Terminal`)
2. Asegúrate de estar en el directorio correcto:
   ```bash
   cd "C:\Users\manue\Proyecto Hormiguero"
   ```
3. Ejecuta:
   ```bash
   python ejecutar_todo.py
   ```

## Verificar que Python está instalado

Si obtienes un error, verifica que Python esté instalado:

```bash
python --version
```

Si no funciona, intenta con:
```bash
py ejecutar_todo.py
```

## Qué hace el script

El script `ejecutar_todo.py`:
1. ✅ Ejecuta todos los tests de cobertura faltante
2. ✅ Muestra cuántos tests pasaron/fallaron
3. ✅ Verifica la cobertura del código
4. ✅ Muestra el porcentaje de cobertura
5. ✅ Genera el reporte HTML en `htmlcov/index.html`

## Salida esperada

Deberías ver algo como:
```
================================================================================
EJECUTANDO TESTS Y VERIFICANDO COBERTURA
================================================================================

================================================================================
1. EJECUTANDO TESTS DE COBERTURA FALTANTE
================================================================================
[Salida de los tests...]

Resumen Tests:
  ✅ Pasados: X
  ❌ Fallidos: Y
  ⚠️  Errores: Z

================================================================================
2. VERIFICANDO COBERTURA
================================================================================
[Salida de cobertura...]

================================================================================
COBERTURA: XX%
================================================================================
✅ Objetivo alcanzado (≥80%) o ⚠️ Falta X% para alcanzar el objetivo
```

## Si hay problemas

1. **Error: "python no se reconoce"**
   - Usa `py` en lugar de `python`
   - O instala Python desde python.org

2. **Error: "No module named pytest"**
   - Instala pytest: `pip install pytest pytest-cov`

3. **Error: "No se encuentra el archivo"**
   - Asegúrate de estar en el directorio correcto
   - Verifica que el archivo `ejecutar_todo.py` existe

## Comandos alternativos si el script no funciona

Si el script no funciona, puedes ejecutar los comandos manualmente:

```bash
# 1. Ejecutar tests
pytest tests/test_api_cobertura_missing.py -v

# 2. Verificar cobertura
pytest tests/test_api_controller.py tests/test_api_cobertura_missing.py --cov=src/recoleccion/api/recoleccion_controller --cov-report=term-missing --cov-report=html
```




