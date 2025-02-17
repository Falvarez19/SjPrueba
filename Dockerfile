# Dockerfile para desplegar en Fly.io

# Usar la imagen base oficial de Python
FROM python:3.12

# Establecer el directorio de trabajo en el contenedor
WORKDIR /code

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar migraciones antes de iniciar la aplicación
RUN python manage.py migrate --noinput

# Exponer el puerto 8000 para la aplicación
EXPOSE 8000

# Comando para iniciar Gunicorn con la aplicación Django
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "ShortyShop.wsgi"]
