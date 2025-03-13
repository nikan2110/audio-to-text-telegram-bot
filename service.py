import logging
import os
from faster_whisper import WhisperModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv("WHISPER_MODEL", "small")
logger.info(f"Loading Faster-Whisper model: {MODEL_NAME}...")

model = WhisperModel(MODEL_NAME, device="cpu", compute_type="int8")

logger.info(f"Faster-Whisper model {MODEL_NAME} loaded successfully.")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes speech from an audio file using Faster-Whisper.

    :param file_path: Path to the input audio file.
    :return: Transcribed text.
    """
    try:
        logger.info(f"Starting transcription for {file_path}...")

        segments, _ = model.transcribe(file_path)
        transcription = " ".join(segment.text for segment in segments)

        logger.info(f"Transcription completed for {file_path}: {transcription}")
        return transcription
    except Exception as e:
        logger.error(f"Error transcribing {file_path}: {e}")
        return "Error during transcription"