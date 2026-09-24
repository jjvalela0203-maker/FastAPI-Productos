# 1. Usamos una versión oficial y ligera de Python
FROM python:3.12-slim

# 2. Definimos la carpeta de trabajo dentro del contenedor
WORKDIR /code

# 3. Instalamos 'uv' para manejar los paquetes rápidamente
RUN pip install uv

# 4. Copiamos todo tu código de la máquina local al contenedor
COPY ./app /code/app

# 5. Instalamos las dependencias globales dentro del contenedor
RUN uv pip install --system fastapi sqlmodel psycopg2-binary uvicorn

# 6. El comando que ejecutará el contenedor al encenderse
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]