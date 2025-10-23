FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget unzip xvfb libnss3 libxss1 libgconf-2-4 libgtk-3-0 fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY products.csv .

CMD ["xvfb-run", "-a", "python3", "src/tracker.py"]
