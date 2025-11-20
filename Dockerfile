# Imagen base de Python
FROM python:3.9-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar aplicación
COPY . .

# Exponer puerto
EXPOSE 5001

# Comando de inicio
CMD ["python", "app.py"]
