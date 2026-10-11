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
scheduler.start()                       # начинает работать


def send_lesson_function(chat_id):                                                          # Функция, которую будет вызывать планировщик каждый день
    bot.send_message(chat_id, "here is your lesson for today! Let's learn some English!")   #одно действие что сверху , но там по уникальному айди чела которому отправляется всё

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
