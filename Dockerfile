FROM python:3.10-slim

WORKDIR /app

# 複製程式與模型資料夾
COPY ./app /app
COPY ./models /models

RUN apt-get update && apt-get install -y ffmpeg && \
    pip install --no-cache-dir fastapi uvicorn python-multipart faster-whisper

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
