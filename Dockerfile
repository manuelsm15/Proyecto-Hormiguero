# Dockerfile para el subsistema de recolección
FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p allure-results allure-report htmlcov

# Exponer puerto
EXPOSE 8000

# Comando para iniciar la aplicación
# Usa railway_main.py para producción (mejor optimizado)
# O main.py para desarrollo local
CMD ["python", "railway_main.py"]