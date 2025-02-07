import telebot
import time
bot = telebot.TeleBot('6508806550:AAFG0dq4AntPx7_l8kIBzRen4yMKjyCA2K0')

# Додаємо список команд
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
]

# Встановлюємо команди перед запуском бота
bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Хай біч, шукаєш розклад?")

@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, "Шо тобі курва помогти? \nЯк дурне сі вродило, то вже й Господь не поможе 🤷")
    time.sleep(3)
    bot.send_message(message.chat.id, "Та ладно, шуткую. \nПросто напиши предмет і я кину посилання. Або напиши день тижня і я кину розклад. Все просто 💁")

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
