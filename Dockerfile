# Use an official Python runtime as a parent image
FROM python:3.10-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /code/app

# Purani CMD line ki jagah is nayi line ko use karo
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "120", "app.main:app"]