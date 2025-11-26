# image légère
FROM python:3.10-slim

# dossier de travail
WORKDIR /app

# copie des dépendances
COPY requirements_prod.txt .
RUN pip install --no-cache-dir -r requirements_prod.txt

# copie du code & modèles
COPY app_api.py .
COPY src/ ./src/
COPY models/ ./models/
ENV PYTHONUNBUFFERED=1

# expose le port HF standard
EXPOSE 7860

# lancement
CMD ["uvicorn", "app_api:app", "--host", "0.0.0.0", "--port", "7860"]
