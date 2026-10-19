FROM python:3.12-slim
WORKDIR /app

COPY site/database/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY site/ ./site/

WORKDIR /app/site/database
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]