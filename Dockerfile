FROM python:3.14.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --no-create-home appuser

COPY . .
RUN chown -R appuser:appgroup /app

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]