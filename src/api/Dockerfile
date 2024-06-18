FROM python:3.10

# Set the working directory
WORKDIR /APPS/streamlit_revision_en_profundidad

# Install requirements
COPY  APPS/streamlit_revision_en_profundidad/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /
# Copy configuration files
COPY config.yaml /config.yaml
COPY parametros.json /parametros.json

# Copy app files
COPY APPS/streamlit_revision_en_profundidad /APPS/streamlit_revision_en_profundidad
COPY APPS/utils APPS/utils

COPY images /images
COPY .env_api /.env_api

ENV PYTHONPATH "${PYTHONPATH}:/APPS/streamlit_revision_en_profundidad:/APPS:/"

EXPOSE 8501

# ENTRYPOINT ["streamlit", "run", "/APPS/streamlit_revision_en_profundidad/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
ENTRYPOINT ["streamlit", "run", "/APPS/streamlit_revision_en_profundidad/main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]