FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY funcion.py .
COPY tests/ tests/

ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["uvicorn", "funcion:app", "--host", "0.0.0.0", "--port", "5000"]