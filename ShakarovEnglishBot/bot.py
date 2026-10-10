import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from telebot import types

TOKEN = '8692232074:AAGmfRphNlsx9mtwvLvBl_Wd3onWVwn4V-o'

bot = telebot.TeleBot(TOKEN)

# Сбрасывает возможные конфликты вебхука
bot.remove_webhook()

scheduler = BackgroundScheduler()
scheduler.start()

# Функция, которую будет вызывать планировщик каждый день
def send_lesson_function(chat_id):
    bot.send_message(chat_id, "here is your lesson for today! Let's learn some English!")

@bot.message_handler(commands=['start'])
def any_message(message):
    bot.reply_to(message, "Hello, I am your personal English teacher. I can help you learn English, let's get started!")
    marcup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("10:00")
    btn2 = types.KeyboardButton("11:00")
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
    marcup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)
    bot.send_message(message.chat.id, "Please choose a time for our lesson:", reply_markup=marcup)

@bot.message_handler(content_types=['text'])
def catch_time(message):
    selected_time = message.text
    bot.reply_to(message, f"Great! I have scheduled our lesson at {selected_time}. See you later!")
    
    parts = selected_time.split(":") 
    hour = int(parts[0])     
    minute = int(parts[1]) 
    chat_id = message.chat.id
    
    print(f"DEBUG: Сохраненный chat_id = {chat_id}")
    
    scheduler.add_job(
        send_lesson_function,
        'cron',
        hour=hour, 
        minute=minute,
        args=[chat_id]
    )

print("success")
bot.polling(none_stop=True)