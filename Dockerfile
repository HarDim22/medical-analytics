FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Koyeb sets PORT automatically
ENV PORT=8000

CMD ["sh", "-c", "python create_tables.py && python seed_events.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
