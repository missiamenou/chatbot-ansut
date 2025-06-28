# Étape 1 : image Python de base
FROM python:3.10-slim

# Étape 2 : définir le dossier de travail dans le conteneur
WORKDIR /app

# Étape 3 : copier tout le code local dans l’image
COPY . .

# Étape 4 : installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : exposer le port de l’API
EXPOSE 8000

# Étape 6 : lancer l’API FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
