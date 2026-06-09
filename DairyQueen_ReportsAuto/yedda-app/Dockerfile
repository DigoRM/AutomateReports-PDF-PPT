FROM python:3.9-slim

# Instala bibliotecas do sistema necessárias para o Chromium rodar de forma invisível (headless)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    procps \
    libgbm1 \
    libxss1 \
    libasound2 \
    libnspr4 \
    libnss3 \
    libxtst6 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala o navegador Chromium do Playwright e suas dependências de sistema
RUN playwright install chromium
RUN playwright install-deps chromium

# Copia o restante do código do aplicativo
COPY . .

# O Hugging Face Spaces escuta obrigatoriamente na porta 7860
EXPOSE 7860

# Executa o aplicativo usando o servidor de produção Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
