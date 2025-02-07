import telebot
import time
import datetime


bot = telebot.TeleBot('6508806550:AAFG0dq4AntPx7_l8kIBzRen4yMKjyCA2K0')

commands = [
    telebot.types.BotCommand("start", "запустити бота"),
    telebot.types.BotCommand("help", "а шо дєлать"),
    telebot.types.BotCommand("lec", "лекційне посилання"),
    telebot.types.BotCommand("ml", "машинне навчання"),
    telebot.types.BotCommand("bzhd", "БЖД"),
    telebot.types.BotCommand("bzhd_lec", "БЖД лекції"),
    telebot.types.BotCommand("bd", "бази даних"),
    telebot.types.BotCommand("ad", "аналіз даних"),
    telebot.types.BotCommand("ib", "інф. безпека"),
    telebot.types.BotCommand("eng", "англійська"),
    telebot.types.BotCommand("mo", "методи оптимізації"),
    telebot.types.BotCommand("frontend", "Front-end"),
    telebot.types.BotCommand("rmf", "рівняння мат. фіз."),
    telebot.types.BotCommand("now", "яка пара зараз"),
    telebot.types.BotCommand("tomorrow", "розклад на завтра"),
    telebot.types.BotCommand("day", "розклад на потрібний день")
]

week1 = {
    "Monday": {
        "08:30": "Методи оптимізації (лек)",
        "10:25": "Бази даних (лек)",
        "12:20": "Основи машинного навчання (лек)"
    },
    "Tuesday": {
        "08:30": "БЖД та цивільний захист (лек)",
        "10:25": "Практичний курс іноземної мови професійного спрямування (пр)",
        "12:20": "Front-end розробка (лаб)",
        "14:15": "Інформаційна безпекам (пр)"
    },
    "Wednesday": {
        "08:30": "Front-end розробка (лек)",
        "10:25": "Аналіз даних (лек)",
        "12:20": "Рівняння математичної фізики (лек)"
    },
    "Thursday": {
        "08:30": "Основи машинного навчання (пр)",
        "10:25": "",
        "12:20": "БЖД та цивільний захист (пр)"
    }
}

week2 = {
    "Monday": {
        "08:30": "Методи оптимізації (лек)",
        "10:25": "Бази даних (лек)",
        "12:20": "Інформаційна безпека (лек)",
        "14:15": "Методи оптимізації (пр)"
    },
    "Tuesday": {
        "10:25": "Практичний курс іноземної мови професійного спрямування (пр)",
        "12:20": "Front-end розробка (лаб)",
        "14:15": "Аналіз даних (пр)"
    },
    "Wednesday": {
        "08:30": "Front-end розробка (лек)",
        "10:25": "Аналіз даних (лек)",
        "12:20": "Рівняння математичної фізики (лек)",
        "14:15": "Рівняння математичної фізики (пр)"
    },
    "Friday": {
        "08:30": "Основи машинного навчання (пр)",
        "10:25": "",
        "12:20": "",
        "14:15": "Бази даних (лаб)"
    }
}

@bot.message_handler(func=lambda message: True)  # Обробляє всі повідомлення
def get_chat_id(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"ID цієї групи: {chat_id}")
    print(f"Group ID: {chat_id}")  # Виводимо в консоль
    
def get_week_type():
    week_number = datetime.datetime.now().isocalendar()[1]  
    return 2 if week_number % 2 != 0 else 1

now = datetime.datetime.now()
day = now.strftime("%A")  # День тижня англійською
time = now.strftime("%H:%M")  # Поточний час
week = get_week_type()  # Визначаємо тиждень
schedule = week1 if week == 1 else week2  # Вибираємо розклад
end_time = "15:55"

def get_current_lesson():
    
    if day in schedule:
        for lesson_time, lesson_link in schedule[day].items():
            if lesson_time <= time < end_time :  # Якщо вже час для заняття
                return f"🔔 Зараз: {lesson_link}"
    return f"📅 Зараз немає занять"

def get_schedule_for_day(day):
    week_type = get_week_type()  # Визначаємо тиждень
    schedule = week1 if week_type == 1 else week2  # Вибираємо розклад

    if day in schedule:
        lessons = "\n".join([f"{time} - {link}" for time, link in schedule[day].items()])
        return f"📅 Розклад на {day} ({week}-й тиждень):\n{lessons}"
    return f"❌ Немає розкладу на цей день"

# 📌 Обробник команди /now (що зараз?)
@bot.message_handler(commands=['now'])
def now_handler(message):
    bot.send_message(message.chat.id, get_current_lesson())

bot.set_my_commands(commands)

# 📌 Обробник команди /tomorrow (розклад на завтра)
@bot.message_handler(commands=['tomorrow'])
def tomorrow_handler(message):
    today = datetime.datetime.now().strftime("%A")  # Поточний день
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    tomorrow_index = (days.index(today) + 1) % 7  # Наступний день

    bot.send_message(message.chat.id, get_schedule_for_day(days[tomorrow_index]))

# 📌 Обробник команди /day (розклад на будь-який день)
@bot.message_handler(commands=['day'])
def day_handler(message):
    text = message.text.split()
    if len(text) > 1:
        day = text[1].capitalize()  # Приводимо до формату (Monday, Tuesday)
        bot.send_message(message.chat.id, get_schedule_for_day(day))
    else:
        bot.send_message(message.chat.id, "❓ Введи день: /day Monday")


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Хай біч, шукаєш розклад?")

@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, "Шо тобі курва помогти? \nЯк дурне сі вродило, то вже й Господь не поможе 🤷")
    time.sleep(3)
    bot.send_message(message.chat.id, "Та ладно, шуткую. \nНапиши <b><i>/предмет</i></b> і я кину посилання: \n" 
                     "/lec - лекційне посилання\n"
                     "/ml - машинне навчання\n"
                     "/bzhd - БЖД\n"
                     "/bzhd_lec - БЖД лекції\n"
                     "/bd - бази даних\n"
                     "/ad - аналіз даних\n"
                     "/ib - інф. безпека\n"
                     "/eng - англійська\n"
                     "/mo - методи оптимізації\n"
                     "/frontend - Front-end\n"
                     "/rmf - рівняння мат. фіз.\n"
                     "/now - яка пара зараз\n"
                     "/tomorrow - розклад на завтра\n"
                     "Або напиши <b><i>/day_день-тижня</i></b> (тіпа '/day Monday') і я кину розклад. Все просто 💁", parse_mode="HTML")

@bot.message_handler(commands=['tavrov'])
def start_handler(message):
    bot.send_message(message.chat.id, "Тавров підарас")

@bot.message_handler(commands=['lec', 'лекція'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Лекційне посилання</b> \nhttps://us02web.zoom.us/j/9189174549?pwd=bTNWY1BnVkFLRFViTXVjbUUwTVFUQT09", parse_mode="HTML") 

@bot.message_handler(commands=['ml', 'мл'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Основи машинного навчання</b> \nhttps://us06web.zoom.us/j/82625902531?pwd=xP6ogdCLRxzVoQkm1AT61Dma7rmZZI.1", parse_mode="HTML") 

@bot.message_handler(commands=['bzhd', 'бжд'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>БЖД</b> \nhttps://us04web.zoom.us/j/75247526367?pwd=TFZoc0Z3bkpTb0Q0cmVXeXUrM0RjUT09", parse_mode="HTML") 

@bot.message_handler(commands=['bzhd_lec', 'бжд_лек'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>БЖД лекції</b> \nhttps://us02web.zoom.us/j/8787295500?pwd=QVFyU2JOM2xGcHNMOTArZDlJeXZmZz09", parse_mode="HTML") 

@bot.message_handler(commands=['bd', 'бд'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Бази даних</b> \nhttps://us06web.zoom.us/j/82625902531?pwd=xP6ogdCLRxzVoQkm1AT61Dma7rmZZI.1", parse_mode="HTML")

@bot.message_handler(commands=['ad', 'ад'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Аналіз даних</b> \nhttps://us05web.zoom.us/j/3591803845?pwd=QjZoc2N2ZTV3NVZ0cjdJZjFVS0hWUT09", parse_mode="HTML") 

@bot.message_handler(commands=['ib', 'іб'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Інформаційна безпека</b> \nhttps://us04web.zoom.us/j/2045916957?pwd=RUxNcVlSVlJuUFBzUklXZDduWTNWZz09", parse_mode="HTML")

@bot.message_handler(commands=['eng', 'англ'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Англійська мова</b> \nhttps://us04web.zoom.us/j/77395391258?pwd=MGiaK3k0fUSkvJE2dTPqRoVP8bcNma.1", parse_mode="HTML") 

@bot.message_handler(commands=['mo', 'мо'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Методи оптимізації</b> \n\nНема ще. \nВ тебе є? Ділись (скажи @lettucejunior)", parse_mode="HTML") 

@bot.message_handler(commands=['frontend', 'фронтенд'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Front-end розробка</b> \n\nНема ще. \nВ тебе є? Ділись (скажи @lettucejunior)", parse_mode="HTML") 

@bot.message_handler(commands=['rmf', 'рмф'])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Рівняння мат. фізики</b> \n\nНема ще. \nВ тебе є? Ділись (скажи @lettucejunior)", parse_mode="HTML") 


bot.infinity_polling()
