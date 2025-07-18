# Dockerfile
FROM python:3.10-slim

# Evita archivos .pyc y buffer de salida sin envolver
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia sólo requirements y lo instala primero (cache de dependencias)
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto de la app
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]