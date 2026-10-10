# 🇬🇧 ShakarovEnglishBot

Personal English teacher Telegram bot built with Python, telebot, and apscheduler. Easy to run.

---

### 🚀 Features
* ⏰ **Flexible Schedule:** Interactive buttons to choose your preferred daily lesson time (from 10:00 to 21:00).
* 🤖 **Automated Dispatcher:** Background scheduler (`APScheduler`) that sends daily lessons automatically at the selected time.
* 📚 **Structured Content:** Formatted lessons with tips, examples, and interactive tasks.

---

### 🛠 Technologies
* **Python**
* **`pyTelegramBotAPI`** (`telebot`)
* **`APScheduler`**

---

### ⚙️ How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ShakarovDev/ShakarovEnglishBot.git
   cd ShakarovEnglishBot
2. **Install dependencies:**
   ```bash
   pip install pyTelegramBotAPI apscheduler
3. Create a .env file in the root directory and add your Telegram bot token:
   ```bash
   BOT_TOKEN=your_telegram_bot_token_here
4.Run the bot:
   ```bash
   python bot.py
