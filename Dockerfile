# Image de base
FROM ubuntu:24.04

# Configuration
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Installation de Python et FreeFem++
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    freefem++ \
    && rm -rf /var/lib/apt/lists/*

# Dossier de travail
WORKDIR /app

# Environnement Python
RUN python3.12 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copie du projet
COPY . .

# Port Streamlit
EXPOSE 8501

# Démarrage de THERMO-SMART
CMD ["sh", "-c", "streamlit run python/app.py --server.address 0.0.0.0 --server.port ${PORT:-8501} --server.headless true"]
