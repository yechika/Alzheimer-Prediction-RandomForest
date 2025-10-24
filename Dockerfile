FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY alzheimer_model.pkl .
COPY alzheimer_scaler.pkl .
COPY sample_request.json .
COPY sample_request_risiko_tinggi.json .

EXPOSE 7860

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "2", "--timeout", "120", "app:app"]
