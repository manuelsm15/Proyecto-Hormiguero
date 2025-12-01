# 📦 Guía para Subir Cambios a Git

Esta guía te muestra cómo subir los cambios del proyecto a Git paso a paso.

---

## 🚀 Comandos Rápidos

### Opción 1: Subir TODOS los cambios (recomendado para primera vez)

```powershell
# 1. Agregar todos los archivos nuevos y modificados
git add .

# 2. Hacer commit con un mensaje descriptivo
git commit -m "Agregar Happy Path completo y documentación de APIs"

# 3. Subir los cambios al repositorio remoto
git push origin main
```

---

### Opción 2: Subir solo los archivos del Happy Path (más específico)

```powershell
# 1. Agregar solo los archivos del Happy Path
git add HAPPY_PATH_API.md
git add scripts/ejecutar_happy_path.ps1
git add scripts/ejecutar_happy_path.py

# 2. Agregar también los archivos modificados relacionados
git add src/recoleccion/api/recoleccion_controller.py
git add src/recoleccion/services/recoleccion_service.py
git add src/recoleccion/models/tarea_recoleccion.py
git add features/recoleccion.feature
git add features/steps/recoleccion_steps.py
git add tests/test_api_controller.py
git add tests/test_recoleccion_service.py

# 3. Hacer commit
git commit -m "Agregar Happy Path completo y documentación de APIs"

# 4. Subir los cambios
git push origin main
```

---

## 📝 Pasos Detallados

### Paso 1: Verificar el estado actual

```powershell
git status
```

Esto te mostrará:
- Archivos modificados (en rojo)
- Archivos nuevos sin rastrear (en rojo)
- Archivos listos para commit (en verde)

---

### Paso 2: Agregar archivos al staging area

**Agregar todos los archivos:**
```powershell
git add .
```

**O agregar archivos específicos:**
```powershell
git add HAPPY_PATH_API.md
git add scripts/ejecutar_happy_path.ps1
git add scripts/ejecutar_happy_path.py
```

**Verificar qué se agregó:**
```powershell
git status
```

Los archivos agregados aparecerán en verde bajo "Changes to be committed".

---

### Paso 3: Hacer commit (guardar los cambios localmente)

```powershell
git commit -m "Agregar Happy Path completo y documentación de APIs"
```

**Mensajes de commit recomendados:**
- `"Agregar Happy Path completo y documentación de APIs"`
- `"feat: Agregar scripts de Happy Path y documentación completa"`
- `"docs: Agregar guía de Happy Path para pruebas de APIs"`

---

### Paso 4: Verificar el remoto

```powershell
git remote -v
```

Esto te mostrará la URL del repositorio remoto (origin).

---

### Paso 5: Subir los cambios al repositorio remoto

```powershell
git push origin main
```

Si es la primera vez y necesitas configurar el upstream:
```powershell
git push -u origin main
```

---

## 🔍 Verificar Cambios Antes de Subir

### Ver qué cambios se van a subir:

```powershell
# Ver diferencias en archivos modificados
git diff

# Ver qué archivos se agregaron
git status
```

---

## ⚠️ Si hay conflictos o errores

### Si el push falla porque hay cambios remotos:

```powershell
# 1. Primero traer los cambios remotos
git pull origin main

# 2. Resolver conflictos si los hay
# (editar los archivos con conflictos)

# 3. Agregar los archivos resueltos
git add .

# 4. Hacer commit de la resolución
git commit -m "Resolver conflictos con cambios remotos"

# 5. Intentar push nuevamente
git push origin main
```

---

## 📋 Script Completo (Copia y Pega)

```powershell
# Cambiar al directorio del proyecto
cd "C:\Users\manue\Proyecto Hormiguero"

# Ver estado actual
git status

# Agregar todos los cambios
git add .

# Hacer commit
git commit -m "Agregar Happy Path completo y documentación de APIs"

# Subir cambios
git push origin main
```

---

## 🎯 Comandos Útiles Adicionales

### Ver historial de commits:
```powershell
git log --oneline
```

### Ver cambios en un archivo específico:
```powershell
git diff nombre_archivo.py
```

### Deshacer cambios no guardados:
```powershell
# Descartar cambios en un archivo específico
git restore nombre_archivo.py

# Descartar todos los cambios
git restore .
```

### Ver qué archivos están siendo rastreados:
```powershell
git ls-files
```

---

## 📌 Notas Importantes

1. **`.gitignore`**: Asegúrate de que archivos sensibles (como `.env`, `*.db`, `__pycache__/`) estén en `.gitignore`.

2. **Commits frecuentes**: Es mejor hacer commits pequeños y frecuentes que uno grande con muchos cambios.

3. **Mensajes descriptivos**: Usa mensajes de commit claros que expliquen qué cambió y por qué.

4. **Verificar antes de push**: Siempre revisa `git status` y `git diff` antes de hacer push.

---

**Última actualización:** 2024-01-15

