FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    openai \
    python-dotenv

EXPOSE 7860

CMD ["uvicorn", "env:app", "--host", "0.0.0.0", "--port", "7860"]