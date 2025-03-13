import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from service import transcribe_audio

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

@dp.message(Command("start"))
async def start_command(message: Message):
    """
    Handles the /start command.

    :param message: Telegram message object
    """
    logger.info(f"User {message.from_user.id} started the bot.")
    await message.answer("Hello! Send me a voice message or an audio file, and I will transcribe it.")


@dp.message(lambda message: message.voice)
async def handle_voice(message: Message):
    """
    Handles voice messages, downloads the file, transcribes it, and sends back the text.

    :param message: Telegram message object containing a voice message
    """
    # Notify the user that processing has started
    processing_msg = await message.answer("File received, processing...")

    voice = await bot.get_file(message.voice.file_id)
    file_path = os.path.join(AUDIO_DIR, f"{voice.file_id}.ogg")
    wav_path = os.path.join(AUDIO_DIR, f"{voice.file_id}.wav")

    await bot.download_file(voice.file_path, file_path)
    logger.info(f"Downloaded voice message from user {message.from_user.id}: {file_path}")

    text = transcribe_audio(file_path)

    # Edit the initial message with the final transcription result
    await processing_msg.edit_text(text)

    # Safe file deletion
    for path in [file_path, wav_path]:
        if os.path.exists(path):
            try:
                os.remove(path)
                logger.info(f"Deleted file: {path}")
            except Exception as e:
                logger.error(f"Error deleting {path}: {e}")

async def main():
    """
    Main function to start the bot.
    """
    logger.info("Bot is starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())