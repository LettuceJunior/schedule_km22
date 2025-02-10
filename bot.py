import telebot
import time
import datetime
import threading

bot = telebot.TeleBot('6508806550:AAFG0dq4AntPx7_l8kIBzRen4yMKjyCA2K0')
CHAT_ID = '-1001535245484'

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
    telebot.types.BotCommand("today", "розклад на сьогодні"),
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

START_WEEK_NUMBER = 5

def get_week_type():
    week_number = datetime.datetime.now().isocalendar()[1]  
    return 1 if (week_number - START_WEEK_NUMBER) % 2 == 0 else 2

now = datetime.datetime.now()
day = now.strftime("%A")  # День тижня англійською
time = now.strftime("%H:%M")  # Поточний час
week = get_week_type()  # Визначаємо тиждень
schedule = week1 if week == 1 else week2  # Вибираємо розклад
end_time = "15:55"

def get_current_lesson():
    now = datetime.datetime.now()
    day = now.strftime("%A")  # Оновлюємо день
    current_time = now.strftime("%H:%M")  # Оновлюємо час
    
    if day in schedule:
        for lesson_time, lesson_link in schedule[day].items():
            if lesson_time <= current_time:  # Перевіряємо, чи урок вже почався
                return f"🔔 Зараз: {lesson_link}"
    return f"📅 Зараз немає занять"


def get_schedule_for_day(day):
    week_type = get_week_type()  # Визначаємо тиждень
    schedule = week1 if week_type == 1 else week2  # Вибираємо розклад

    if day in schedule:
        lessons = "\n".join([f"{time} - {link}" for time, link in schedule[day].items()])
        return f"📅 Розклад на {day} ({week}-й тиждень):\n{lessons}"
    return f"❌ Немає розкладу на цей день"

pinned_messages = {}

# 📌 Функція, яка надсилає та закріплює повідомлення з посиланням
def send_and_pin_lesson(chat_id, lesson_link):
    global pinned_messages
    
    message = bot.send_message(chat_id, lesson_link)  # Відправляємо повідомлення
    bot.pin_chat_message(chat_id, message.message_id)  # Закріплюємо його
    
    pinned_messages[chat_id] = message.message_id  # Зберігаємо ID

    # ⏳ Запускаємо таймер для відкріплення через 1 год 40 хв (6000 сек)
    threading.Timer(6000, unpin_message, args=[chat_id]).start()

# 📌 Функція відкріплення повідомлення
def unpin_message(chat_id):
    global pinned_messages

    if chat_id in pinned_messages:
        try:
            bot.unpin_chat_message(chat_id, pinned_messages[chat_id])
            del pinned_messages[chat_id]  # Видаляємо ID після відкріплення
        except Exception as e:
            print(f"⚠️ Помилка при відкрипленні: {e}")

# 📌 Функція перевірки часу і запуску надсилання
def check_schedule():
    while True:
        now = datetime.datetime.now()
        day = now.strftime("%A")
        current_time = now.strftime("%H:%M")
        
        if day in schedule and current_time in schedule[day]:
            lesson_link = schedule[day][current_time]
            send_and_pin_lesson(CHAT_ID, f"🔔 Час пари!\n{lesson_link}")

        time.sleep(30)  # Перевіряємо кожні 30 секунд

# 📌 Запускаємо перевірку часу у фоновому потоці
thread = threading.Thread(target=check_schedule)
thread.daemon = True  # Потік завершується разом із головною програмою
thread.start()

# 📌 Обробник команди /now (що зараз?)
@bot.message_handler(commands=['now'])
def now_handler(message):
    bot.send_message(message.chat.id, get_current_lesson())

bot.set_my_commands(commands)

# 📌 Обробник команди /today (розклад на сьогодні)
@bot.message_handler(commands=['today'])
def today_handler(message):
    today = datetime.datetime.now().strftime("%A")  # Поточний день
    bot.send_message(message.chat.id, get_schedule_for_day(today))

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
    bot.send_message(message.chat.id, "Напиши <b><i>/предмет</i></b> і я кину посилання: \n" 
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
                     "/today - розклад на сьогодні\n"
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
