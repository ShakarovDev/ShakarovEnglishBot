# ==========================================
# PROJECT: ShakarovEnglishBot
# DESCRIPTION: Personal English teacher Telegram bot 
# CREATED WITH: Python, pyTelegramBotAPI, APScheduler
# ==========================================
 
import os          #импортирует  библиотеку пайтона что бы с системой работать
import telebot         #импортирует главную библиотеку pyTelegramBotAPI, которая связывает код с серверами Telegram.
from apscheduler.schedulers.background import BackgroundScheduler   #импортирует  планировщик задач
from dotenv import load_dotenv     #импортирует  функцию load_dotenv которая берёт секретные данные о моём тг токене , что бы бот мог ими воспользоваться но в гит хаб не заливался 
from telebot import types          #импортирует  клаву и наборы инструментов для создания интерфейса телеграм

load_dotenv()                      # Загружает переменные из файла .env

TOKEN = os.getenv("BOT_TOKEN")      # Читаем токен из окружения

bot = telebot.TeleBot(TOKEN)      # Инициализируем бота с помощью полученного токена


bot.remove_webhook()              # Сбрасывает возможные конфликты вебхука

scheduler = BackgroundScheduler()       # Инициализируем фоновый планировщик задач (APScheduler) для отправки уроков по расписанию
scheduler.start()


def send_lesson_function(chat_id):
    lesson_text = (
        "📘 *Тема урока: Present Simple (простое настоящее время)*\n\n"
        "Present Simple — простое настоящее время. Оно описывает регулярные, "
        "повторяющиеся действия, факты, постоянные состояния, а не то, что "
        "происходит прямо сейчас (для «сейчас» есть Present Continuous).\n\n"
        "А что же тогда относится к Present Simple? Давайте разберём по пунктам.\n\n"

        "*1. Регулярные/повторяющиеся действия (привычки, рутина):*\n"
        "I go to school every day. — Я хожу в школу каждый день.\n"
        "She drinks coffee in the morning.\n\n"

        "*2. Факты, общеизвестные истины:*\n"
        "The Earth goes around the Sun.\n"
        "Water boils at 100°C.\n\n"

        "*3. Постоянные состояния, чувства, мнения:*\n"
        "I like ice cream.\n"
        "He hates loud music.\n\n"

        "*4. Расписания и графики (поезда, самолёты, кино):*\n"
        "The train leaves at 7:30.\n"
        "The film starts at 9 p.m.\n\n"

        "*5. Инструкции, указания, рецепты:*\n"
        "You take the metro and get off at the third stop.\n\n"

        "*6. Комментарии (спорт, действия в реальном времени — репортаж):*\n"
        "Messi passes the ball… and scores!\n\n"

        "━━━━━━━━━━━━━━━\n"
        "📐 *Грамматика*\n\n"

        "*Формула утверждения:*\n"
        "I / You / We / They + V1\n"
        "He / She / It + V1 + s/es\n\n"

        "*Формула отрицания:*\n"
        "I / You / We / They + do not (don't) + V1\n"
        "He / She / It + does not (doesn't) + V1\n\n"
        "*Примеры:*\n"
        "I don't like tea.\n"
        "She doesn't work here.\n"
        "They don't go to the gym.\n\n"

        "*Вопрос:*\n"
        "Формула: Do / Does + Subject + V1?\n\n"
        "Do you speak English?\n"
        "Does he live in London?\n"
        "Do they like pizza?\n"
    )

    # отправка сообщения (пример для aiogram / telebot — подставьте свой метод)
    bot.send_message(chat_id, lesson_text, parse_mode="Markdown")
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

@bot.message_handler(content_types=['text'])  # Обработчик обычных текстовых сообщений (сюда попадает выбранное время от пользователя)
def catch_time(message):      # словил сообщение с текстом ( время ) которое нажал юзер в его клаве (btn = types...) 
    selected_time = message.text                # сохраняет то что скинули 
    bot.reply_to(message, f"Great! I have scheduled our lesson at {selected_time}. See you later!")     # отвечает на то сообщение 
    
    parts = selected_time.split(":")       # Разбивает выбранное время (например, "10:00") на часы и минуты
    hour = int(parts[0])                   # превращает первую часть ( 14 ) в целое ( час ) 
    minute = int(parts[1])                 # превращает вторую часть ( 00 ) в целое  ( минуты )
    chat_id = message.chat.id              # сохраняет айди юзера 
    
    print(f"DEBUG: Сохраненный chat_id = {chat_id}")        #скидывает в терминал сохранённый айди 
    
    scheduler.add_job(                     # Добавляет задачу в планировщик: каждый день в указанные hour и minute вызывать send_lesson_function
        send_lesson_function,              # какую функцию вызвать ( в нашем случае отправление урока )
        'cron',                            # режим работы расписания ( крон это повторение по расписанию , каждый день в то же время )
        hour=hour,                         # в какой час запускать ( берётся из переменной hour, которая берётся из текста клавиатуры (btn2 = types...)  )
        minute=minute,                     # тоже самое что и часы 
        args=[chat_id]                     # что передать в функцию (мы передадим чат айди что бы бот понял кому урок скидывать)
    )

print("success")                  #Выводит в консоль/терминал сообщение об успешном запуске скрипта
bot.polling(none_stop=True)            #Запускаем бесконечный опрос сервера Telegram на наличие новых сообщений 
