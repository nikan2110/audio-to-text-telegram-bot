import logging
import os
import torch
import torchaudio
import numpy as np
from pydub import AudioSegment
from transformers import WhisperProcessor, WhisperForConditionalGeneration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv("WHISPER_MODEL", "openai/whisper-base")
logger.info("Loading Whisper model...")

processor = WhisperProcessor.from_pretrained(MODEL_NAME)
model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
logger.info("Whisper model loaded successfully.")


def convert_to_wav(input_path: str) -> str:
    """
    Converts an OGG audio file to WAV format.

    :param input_path: Path to the input OGG file.
    :return: Path to the converted WAV file.
    """
    try:
        logger.info(f"Converting {input_path} to WAV format...")
        audio = AudioSegment.from_file(input_path, format="ogg")
        wav_path = input_path.replace(".ogg", ".wav")
        audio.export(wav_path, format="wav")
        logger.info(f"Converted {input_path} -> {wav_path}")
        return wav_path
    except Exception as e:
        logger.error(f"Error converting {input_path} to WAV: {e}")
        raise


def resample_audio(wav_path: str, target_sample_rate: int = 16000) -> tuple:
    """
    Resamples an audio file to the target sample rate.

    :param wav_path: Path to the WAV file.
    :param target_sample_rate: Desired sample rate (default: 16000 Hz).
    :return: Tuple containing the waveform (numpy array) and sample rate.
    """
    try:
        logger.info(f"Resampling {wav_path} to {target_sample_rate} Hz...")
        waveform, sample_rate = torchaudio.load(wav_path)

        if sample_rate != target_sample_rate:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sample_rate)
            waveform = resampler(waveform)

        waveform = waveform.numpy()

        if waveform.shape[0] > 1:
            waveform = np.mean(waveform, axis=0)  # Convert stereo to mono

        logger.info(f"Resampling completed for {wav_path}")
        return waveform, target_sample_rate
    except Exception as e:
        logger.error(f"Error resampling {wav_path}: {e}")
        raise


def transcribe_audio(file_path: str) -> str:
    """
    Transcribes speech from an audio file using Whisper.

    :param file_path: Path to the input audio file.
    :return: Transcribed text.
    """
    try:
        logger.info(f"Starting transcription for {file_path}...")
        wav_path = convert_to_wav(file_path)

        waveform, sample_rate = resample_audio(wav_path)

        input_features = processor(waveform, sampling_rate=sample_rate, return_tensors="pt").input_features
        input_features = input_features.to(device)

        predicted_ids = model.generate(input_features)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        logger.info(f"Transcription completed for {file_path}: {transcription}")
        return transcription
    except Exception as e:
        logger.error(f"Error transcribing {file_path}: {e}")
        raise