# 🎙️ Telegram Audio-to-Text Bot (Faster-Whisper Version)  
A lightweight **Telegram bot** that transcribes voice messages and audio files into text using **Faster-Whisper**. Optimized for low-resource servers.

## ✨ Features  
✅ Supports **voice messages** and **audio files**  
✅ Uses **Faster-Whisper** for **fast and efficient transcription**
✅ Choose **different models** (`tiny`, `base`, `small`, etc.)  
✅ Runs in **Docker** for easy deployment  
✅ Works on **Linux, macOS, Raspberry Pi, VPS**  

---

## 🚀 Deployment  

### **1️⃣ Set up environment variables**  
Create a `.env` file (or pass variables in Docker):  
```ini
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
WHISPER_MODEL=small
```

### **2️⃣ Build and run the bot with Docker**  
```bash
docker build -t audio-to-text-bot .
docker run -d --restart always \
    -e TELEGRAM_BOT_TOKEN="your-token" \
    -e WHISPER_MODEL="small" \
    --name audio-to-text-bot audio-to-text-bot
```

### **3️⃣ Run without Docker**  
1. Install dependencies:  
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```
2. Start the bot:  
   ```bash
   python main.py
   ```

---

## 🛠️ Supported Models  
By default, the bot uses **`small`**. You can change it using the `WHISPER_MODEL` environment variable:  

| Model | Speed | Accuracy | RAM Required |
|--------|--------|----------|-------------|
| `tiny` | 🚀 Fast | ❌ Lower | ~0.5GB |
| `base` | ⚡ Medium | 🟡 Decent | ~1GB |
| `small` | 🐢 Slower | ✅ Good | ~2GB |
| `medium` | 🐌 Very Slow | 🔥 Excellent | ~4GB |

To change the model, **update your environment variable**:  
```bash
export WHISPER_MODEL="base"
```

---

## 📜 Logging  
The bot writes logs to both the **console** and a **log file (`bot.log`)**.  
To view logs in real time:  
```bash
docker logs -f audio-to-text-bot
```
