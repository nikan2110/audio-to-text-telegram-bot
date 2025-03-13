FROM python:3.11
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /app
COPY . .
ENV WHISPER_MODEL=openai/whisper-base
ENV TOKEN=YOUR_TELEGRAM_TOKEN
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]