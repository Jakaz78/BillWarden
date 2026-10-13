# Używamy oficjalnego obrazu Pythona
FROM python:3.10-slim

# Wyłączamy buforowanie wyjścia, żeby logi pojawiały się na bieżąco
ENV PYTHONUNBUFFERED=1

# Instalujemy wymagane biblioteki systemowe dla PaddleOCR i OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Tworzymy folder roboczy w kontenerze
WORKDIR /app

# Kopiujemy plik z wymaganiami i instalujemy zależności
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę kodu projektu
COPY . /app/

# Otwieramy port, na którym będzie działać Django
EXPOSE 8000

# Komenda uruchamiająca serwer produkcyjny Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "BillWarden.wsgi:application"]