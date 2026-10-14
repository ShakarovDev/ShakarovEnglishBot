# ==========================================
# PROJECT: ShakarovEnglishBot
# DESCRIPTION: Personal English teacher Telegram bot 
# CREATED WITH: Python, pyTelegramBotAPI, APScheduler
# ==========================================
 
import os          #импортирует  библиотеку пайтона что бы с системой работать
import json        # ← НОВОЕ: нужен для сохранения прогресса в файл
import telebot         #импортирует главную библиотеку pyTelegramBotAPI, которая связывает код с серверами Telegram.
from apscheduler.schedulers.background import BackgroundScheduler   #импортирует  планировщик задач
from dotenv import load_dotenv     #импортирует  функцию load_dotenv которая берёт секретные данные о моём тг токене , что бы бот мог ими воспользоваться но в гит хаб не заливался 
from telebot import types          #импортирует  клаву и наборы инструментов для создания интерфейса телеграм

from lessons import LESSONS        # ← НОВОЕ: импортируем список уроков из файла lessons.py

load_dotenv()                      # Загружает переменные из файла .env

TOKEN = os.getenv("BOT_TOKEN")      #  # берёт токен из .env

bot = telebot.TeleBot(TOKEN)      # Инициализируем бота с помощью полученного токена


bot.remove_webhook()              # Сбрасывает возможные конфликты вебхука

scheduler = BackgroundScheduler()       # Инициализируем фоновый планировщик задач (APScheduler) для отправки уроков по расписанию
scheduler.start()


# ─────────────────────────────────────────────
# ← НОВОЕ: храним, какой урок у какого пользователя идёт следующим
# ─────────────────────────────────────────────
# user_lesson_index — это словарь {chat_id: индекс_следующего_урока}
# Например: {"123456": 0} — урок 1 ещё не отправлен, следующий будет LESSONS[0]
#           {"123456": 1} — урок 1 отправлен, следующий будет LESSONS[1]

STATE_FILE = "state.json"        # файл, куда сохраняем прогресс, чтобы не потерять при перезапуске

def load_state():
    # Читает сохранённый прогресс. Если файла нет — возвращает пустой словарь.
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_state(state):
    # Сохраняет прогресс в файл.
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

user_lesson_index = load_state()   # загружаем прогресс при старте


# ─────────────────────────────────────────────
# Функция, которую вызывает планировщик каждый день в выбранное время
# ─────────────────────────────────────────────
def send_lesson_function(chat_id):
    key = str(chat_id)                       # ключи в JSON всегда строки, приводим на всякий случай

    idx = user_lesson_index.get(key, 0)      # берём индекс следующего урока (или 0, если новый юзер)

    # Если уроки закончились — поздравляем и выходим
    if idx >= len(LESSONS):
        bot.send_message(chat_id, "🎉 You have completed all the lessons! Congratulations!")
        return

    lesson_text = LESSONS[idx]               # ← достаём урок из списка по индексу
    bot.send_message(chat_id, lesson_text, parse_mode="Markdown")   # отправляем

    user_lesson_index[key] = idx + 1         # сдвигаем индекс на следующий урок
    save_state(user_lesson_index)            # сохраняем на диск

    print(f"DEBUG: отправлен урок #{idx + 1} пользователю {chat_id}")


@bot.message_handler(commands=['start'])         # Обработчик команды /start — срабатывает, когда пользователь запускает бота
def any_message(message):                        # уже словил команду старт и отвечает на неё
    bot.reply_to(message, "Hello, I am your personal English teacher. I can help you learn English, let's get started!") # Приветствуем пользователя
    marcup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создаем клавиатуру с кнопками для выбора времени урока
    btn1 = types.KeyboardButton("10:00")              #кнопка на 10 утра 
    btn2 = types.KeyboardButton("11:00")              #кнопка на 11 утра итд.
    btn3 = types.KeyboardButton("12:00")
    btn4 = types.KeyboardButton("13:00")
    btn5 = types.KeyboardButton("14:00")
    btn6 = types.KeyboardButton("15:00")
    btn7 = types.KeyboardButton("16:00")
    btn8 = types.KeyboardButton("17:00")
    btn9 = types.KeyboardButton("18:00")
    btn10 = types.KeyboardButton("19:00")
    btn11 = types.KeyboardButton("20:00")
    btn12 = types.KeyboardButton("21:00")
    marcup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12) #Добавляет все кнопки на клавиатуру
    bot.send_message(message.chat.id, "Please choose a time for our lesson:", reply_markup=marcup) #Отправляет сообщение с предложением выбрать время, прикрепляя клавиатуру


# ← НОВОЕ: список валидных времён. Нужен, чтобы не пытаться парсить "привет" как время
VALID_TIMES = [f"{h}:00" for h in range(10, 22)]


@bot.message_handler(content_types=['text'])  # Обработчик обычных текстовых сообщений (сюда попадает выбранное время от пользователя)
def catch_time(message):      # словил сообщение с текстом ( время ) которое нажал юзер в его клаве (btn = types...) 
    selected_time = message.text.strip()       # сохраняет то что скинули (strip убирает пробелы по краям)

    # ← НОВОЕ: проверяем, что это реально время из кнопок, а не случайный текст
    if selected_time not in VALID_TIMES:
        bot.reply_to(message, "Please, choose a time from the buttons below.")
        return

    bot.reply_to(message, f"Great! I have scheduled our lesson at {selected_time}. See you later!")     # отвечает на то сообщение 
    
    parts = selected_time.split(":")       # Разбивает выбранное время (например, "10:00") на часы и минуты
    hour = int(parts[0])                   # превращает первую часть ( 14 ) в целое ( час ) 
    minute = int(parts[1])                 # превращает вторую часть ( 00 ) в целое  ( минуты )
    chat_id = message.chat.id              # сохраняет айди юзера 
    
    print(f"DEBUG: Сохраненный chat_id = {chat_id}")        #скидывает в терминал сохранённый айди 

    # ← НОВОЕ: убираем старую задачу для этого юзера, если она была.
    # Без этого при повторном выборе времени будут две задачи — уроки придут дважды.
    job_id = f"lesson_{chat_id}"
    existing = scheduler.get_job(job_id)
    if existing:
        existing.remove()
        print(f"DEBUG: удалена старая задача для {chat_id}")
    
    scheduler.add_job(                     # Добавляет задачу в планировщик: каждый день в указанные hour и minute вызывать send_lesson_function
        send_lesson_function,              # какую функцию вызвать ( в нашем случае отправление урока )
        'cron',                            # режим работы расписания ( крон это повторение по расписанию , каждый день в то же время )
        hour=hour,                         # в какой час запускать ( берётся из переменной hour, которая берётся из текста клавиатуры (btn2 = types...)  )
        minute=minute,                     # тоже самое что и часы 
        args=[chat_id],                    # что передать в функцию (мы передадим чат айди что бы бот понял кому урок скидывать)
        id=job_id,                         # ← НОВОЕ: уникальный id задачи (защита от дублей)
        replace_existing=True              # ← НОВОЕ: если задача с таким id есть — заменить её
    )

    print(f"DEBUG: задача создана для {chat_id} на {selected_time} каждый день")


print("success")                  #Выводит в консоль/терминал сообщение об успешном запуске скрипта
bot.polling(none_stop=True)            #Запускаем бесконечный опрос сервера Telegram на наличие новых сообщений
