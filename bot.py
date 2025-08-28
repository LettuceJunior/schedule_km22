import requests, datetime, pytz, telebot, json
import random
import datetime, time

API_TOKEN = "6508806550:AAGfBQYBoQK51MIVVjv-tjR2zlI36AMTE5c"
bot = telebot.TeleBot(API_TOKEN)

BASE_API = "https://api.campus.kpi.ua"
GROUP_ID = "dad22b6e-560d-4f69-8f1b-72ea2710b2fa"

# Словник з посиланнями на пари
links_dict = {
    "Математичне моделювання": "посилання_ММ",
    "Розподілені і хмарні обчислення": "посилання_РХО",
    "Інформаційні системи": "посилання_ІС",
    "Основи економіки": "посилання_ОЕ",
    "Навчання з підкріпленням": "посилання_НП",
    "Геометричне моделювання": "посилання_ГМ",
    "Застосування генеративного ШІ": "посилання_ГШІ"
}

# Абревіатури практик/лаб → повна назва пари
abbrev_to_name = {
    "мм": "Математичне моделювання",
    "рхо": "Розподілені і хмарні обчислення",
    "іс": "Інформаційні системи",
    "ое": "Основи економіки",
    "нп": "Навчання з підкріпленням",
    "гм": "Геометричне моделювання",
    "гш": "Застосування генеративного ШІ"
}

# Англійські скорочення команд для слешів
eng_abbrev_to_name = {
    "mm": "Математичне моделювання",
    "rhc": "Розподілені і хмарні обчислення",
    "is": "Інформаційні системи",
    "oe": "Основи економіки",
    "np": "Навчання з підкріпленням",
    "gm": "Геометричне моделювання",
    "gai": "Застосування генеративного ШІ"
}

# Створюємо обробник команд для англійських скорочень
def make_eng_abbrev_handler(key):
    def handler(message):
        pair_name = eng_abbrev_to_name[key]
        link = links_dict.get(pair_name, "посилання")
        bot.send_message(message.chat.id, f"<b>Посилання на {pair_name}:</b> {link}", parse_mode="HTML")
    return handler

for key in eng_abbrev_to_name:
    bot.register_message_handler(make_eng_abbrev_handler(key), commands=[key])



def get_link_for_pair(pair_name):
    """Повертає посилання для пари: з links_dict або автоматично, якщо немає"""
    if pair_name in links_dict:
        return links_dict[pair_name]
    words = pair_name.split()
    abbr = ''.join(word[0].upper() for word in words if word[0].isalpha())
    return f"посилання_{abbr}" if abbr else "посилання"

def fetch_schedule():
    url = f"{BASE_API}/schedule/lessons?groupId={GROUP_ID}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_week_type():
    week_number = datetime.datetime.now(pytz.timezone("Europe/Kyiv")).isocalendar()[1]
    return "scheduleFirstWeek" if week_number % 2 != 0 else "scheduleSecondWeek"

def parse_schedule_for(day_name):
    data = fetch_schedule()
    week_type = get_week_type()
    week_schedule = data[week_type]

    for day in week_schedule:
        if day["day"] == day_name:
            if not day["pairs"]:
                return "Пар сьогодні немає."
            text_lines = []
            for pair in day["pairs"]:
                time = pair["time"][:5]
                name = pair["name"]
                teacher = pair["teacherName"]
                type_lesson = pair["type"]
                text_lines.append(f"{time} — {type_lesson} — {name} ({teacher})")
            return "\n".join(text_lines)
    return "Розклад на цей день не знайдено."

def format_schedule_text(data_text):
    """Форматує текст розкладу з виділенням часу та типу заняття"""
    if "немає" in data_text or "не знайдено" in data_text:
        return f"<i>{data_text}</i>"
    text = ""
    for line in data_text.split("\n"):
        parts = line.split(" — ")
        if len(parts) == 3:
            time, type_lesson, rest = parts
            text += f"<b>{time}</b> — <i>{type_lesson}</i> — {rest}\n"
        else:
            text += f"{line}\n"
    return text

@bot.message_handler(commands=['today'])
def today_handler(message):
    day_index = datetime.datetime.now(pytz.timezone("Europe/Kyiv")).weekday()
    day_api_list = ["Пн","Вт","Ср","Чт","Пт","Сб","Нд"]
    day_api = day_api_list[day_index]

    week_number = datetime.datetime.now(pytz.timezone("Europe/Kyiv")).isocalendar()[1]
    week_type_text = "Парний" if week_number % 2 == 0 else "Непарний"
    day_name_full = ["Понеділок","Вівторок","Середа","Четвер","П’ятниця","Субота","Неділя"][day_index]

    data_text = parse_schedule_for(day_api)
    text = f"<b>Сьогодні: {day_name_full}</b> ({week_type_text} тиждень)\n\n"
    text += format_schedule_text(data_text)

    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(commands=['tomorrow'])
def tomorrow_handler(message):
    day_index = (datetime.datetime.now(pytz.timezone("Europe/Kyiv")).weekday() + 1) % 7
    day_api_list = ["Пн","Вт","Ср","Чт","Пт","Сб","Нд"]
    day_api = day_api_list[day_index]

    week_number = datetime.datetime.now(pytz.timezone("Europe/Kyiv")).isocalendar()[1]
    if day_index == 0:
        week_number += 1
    week_type_text = "Парний" if week_number % 2 == 0 else "Непарний"
    day_name_full = ["Понеділок","Вівторок","Середа","Четвер","П’ятниця","Субота","Неділя"][day_index]

    data_text = parse_schedule_for(day_api)
    text = f"<b>Завтра: {day_name_full}</b> ({week_type_text} тиждень)\n\n"
    text += format_schedule_text(data_text)

    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(commands=['week'])
def week_handler(message):
    data = fetch_schedule()
    week_type = get_week_type()
    week_schedule = data[week_type]
    week_number = datetime.datetime.now(pytz.timezone("Europe/Kyiv")).isocalendar()[1]
    week_type_text = "Парний" if week_number % 2 == 0 else "Непарний"

    text = f"<b>Розклад на {week_type_text} тиждень:</b>\n\n"
    day_name_full_list = ["Понеділок","Вівторок","Середа","Четвер","П’ятниця","Субота","Неділя"]

    for idx, day in enumerate(week_schedule):
        day_name_full = day_name_full_list[idx]
        text += f"<b>{day_name_full}:</b>\n"
        if not day["pairs"]:
            text += "  <i>Пар немає.</i>\n"
        else:
            for pair in day["pairs"]:
                time = pair["time"][:5]
                name = pair["name"]
                teacher = pair["teacherName"]
                type_lesson = pair["type"]
                text += f"  <b>{time}</b> — <i>{type_lesson}</i> — {name} ({teacher})\n"
        text += "\n"

    bot.send_message(message.chat.id, text, parse_mode="HTML")

def get_today_schedule_with_time():
    day_index = datetime.datetime.now(pytz.timezone("Europe/Kyiv")).weekday()
    day_api_list = ["Пн","Вт","Ср","Чт","Пт","Сб","Нд"]
    day_api = day_api_list[day_index]

    data = fetch_schedule()
    week_type = get_week_type()
    week_schedule = data[week_type]

    for day in week_schedule:
        if day["day"] == day_api:
            pairs_list = []
            for pair in day["pairs"]:
                start_time = datetime.datetime.strptime(pair["time"][:5], "%H:%M").time()
                end_dt = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=90))
                end_time = end_dt.time()
                link = pair["name"]
                pairs_list.append({
                    "name": pair["name"],
                    "teacher": pair["teacherName"],
                    "type": pair["type"],
                    "start": start_time,
                    "end": end_time,
                    "link": link
                })
            return pairs_list
    return []

@bot.message_handler(commands=['now'])
def now_handler(message):
    now = datetime.datetime.now(pytz.timezone("Europe/Kyiv")).time()
    pairs = get_today_schedule_with_time()

    for pair in pairs:
        if pair["start"] <= now <= pair["end"]:
            link = get_link_for_pair(pair["name"])
            text = (
                f"<b>Зараз йде пара:</b>\n"
                f"<i>{pair['type']}</i> — <b>{pair['name']}</b> ({pair['teacher']})\n"
                f"<u>Посилання:</u> {link}"
            )
            bot.send_message(message.chat.id, text, parse_mode="HTML")
            return

    bot.send_message(message.chat.id, "<i>Зараз пари немає.</i>", parse_mode="HTML")

@bot.message_handler(commands=['next'])
def next_handler(message):
    now = datetime.datetime.now(pytz.timezone("Europe/Kyiv")).time()
    pairs = get_today_schedule_with_time()

    for pair in pairs:
        if now < pair["start"]:
            link = get_link_for_pair(pair["name"])
            text = (
                f"<b>Наступна пара:</b>\n"
                f"<i>{pair['type']}</i> — <b>{pair['name']}</b> ({pair['teacher']})\n"
                f"<u>Посилання:</u> {link}"
            )
            bot.send_message(message.chat.id, text, parse_mode="HTML")
            return

    bot.send_message(message.chat.id, "<i>На сьогодні більше пар немає.</i>", parse_mode="HTML")
    
@bot.message_handler(commands=['weektype'])
def weektype_handler(message):
    week_number = datetime.datetime.now(pytz.timezone("Europe/Kyiv")).isocalendar()[1]
    week_text = "2 тиждень" if week_number % 2 == 0 else "1 тиждень"
    bot.send_message(message.chat.id, f"<b>Зараз {week_text}.</b>", parse_mode="HTML")


# --- Обробка абревіатур ---
# Українські без слеша
@bot.message_handler(func=lambda message: message.text.lower() in abbrev_to_name)
def abbrev_handler_plain(message):
    key = message.text.lower()
    pair_name = abbrev_to_name[key]
    link = links_dict.get(pair_name, "посилання")
    bot.send_message(message.chat.id, f"<b>Посилання на {pair_name}:</b> {link}", parse_mode="HTML")

# Англійські через слеш
def handle_abbrev_command(message, key):
    pair_name = abbrev_to_name[key]
    link = links_dict.get(pair_name, "посилання")
    bot.send_message(message.chat.id, f"<b>Посилання на {pair_name}:</b> {link}", parse_mode="HTML")

for key in abbrev_to_name:
    bot.register_message_handler(
        lambda message, k=key: handle_abbrev_command(message, k),
        commands=[key]
    )


# Зберігатимемо дату останнього використання для кожного користувача
last_random_use = {}  # ключ = user_id, значення = date у форматі YYYY-MM-DD

student_gifts = [
    "Ти підключився. Вітаю",
    "Мікрофон вимкнений. Спокійно",
    "Камера вимкнена. Можеш відпочити",
    "Знову дивишся меми. Молодець",
    "Домашка? Забудь про неї",
    "Кава врятує день",
    "Zoom завис. Ти в безпеці",
    "Викладач забув лекцію. Щастя",
    "Можеш відкривати соцмережі",
    "Лекція нудна. Засинай",
    "Ти ще живий? Вітаю",
    "Пес кращий студент ніж ти",
    "Заснув? Стратегія спрацювала",
    "Камеру включати необов’язково",
    "Мозок відпочиває. Все норм",
    "Мем під час лекції? Ідея",
    "Активний у чаті? Ніхто не дивиться",
    "Твій день = виживання онлайн",
    "Лінь сьогодні твій друг",
    "Викладач забув домашку. Щастя",
    "Можеш пропустити частину лекції",
    "Кава + Wi-Fi = твоє життя",
    "Викладач говорить швидко. Ігноруй",
    "Ти підключився. Уже добре",
    "Сьогодні лекція = тест терпіння",
    "Можеш закрити вкладку. Безпечно",
    "Лекція нудна. Насолоджуйся",
    "Викладач не помітить твоєї апатії",
    "Ти прокрастинуєш правильно",
    "Мозок протестує. Вітаю",
    "Сьогодні ти герой. Просто підключився",
    "Твій день = мемофон",
    "Смійся тихо. Ніхто не почує",
    "Заснув? Це стратегія",
    "Ти онлайн. Це перемога",
    "Викладач забув питання. Щастя",
    "Можеш робити вигляд, що слухаєш",
    "Кава сильніша за оцінку",
    "Ти вижив після Zoom. Молодець",
    "Лекція коротка. Насолоджуйся",
    "Мем під час лекції = виживання",
    "Ти ледар? Чудово",
    "Викладач говорить. Ти ігноруєш",
    "Твоя лінь = суперсила",
    "Камера вимкнена. Робиш що хочеш",
    "Твій ноутбук головний союзник",
    "Ти ще тут? Вітаю",
    "Домашка втекла. Ти ні",
    "Лекція = онлайн-арена терпіння",
    "Викладач говорить без сенсу",
    "Сьогодні можна нічого не робити",
    "Твоя кава розумніша за тебе"
]

@bot.message_handler(commands=['random'])
def random_handler(message):
    user_id = message.from_user.id
    today_str = datetime.datetime.now(pytz.timezone("Europe/Kyiv")).strftime("%Y-%m-%d")

    if last_random_use.get(user_id) == today_str:
        bot.send_message(message.chat.id, "🎲 Ти вже отримав своє щоденне передбачення. Повернися завтра!")
        return

    chosen = random.choice(student_gifts)
    bot.send_message(message.chat.id, f"🎲 <b>Твоє передбачення на сьогодні:</b>\n\n<i>{chosen}</i>", parse_mode="HTML")

    # Запам'ятовуємо, що користувач отримав сьогодні
    last_random_use[user_id] = today_str


@bot.message_handler(commands=['coin'])
def coin_handler(message):
    # Можливі варіанти і саркастичні коментарі
    outcomes = [
        ("Йти на пару", "Хехе, лох"),
        ("Не йти на пару", "Повезло, повезло"),
        ("Йти на пару", "Сміливо, але дурнувато"),
        ("Не йти на пару", "Тільки не кажи викладачу"),
        ("Йти на пару", "Ну, хай буде так"),
        ("Не йти на пару", "Свобода за тобою"),
        ("Йти на пару", "Ще один герой Zoom"),
        ("Не йти на пару", "Час для мемів")
    ]

     # Перше повідомлення
    bot.send_message(message.chat.id, "🪙 Підкидання монетки...")

    # Затримка 2 секунди
    time.sleep(2)

    # Вибір результату
    decision, comment = random.choice(outcomes)

    # Друге повідомлення з результатом
    bot.send_message(
        message.chat.id,
        f"<b>Результат:</b> {decision}\n\n<i>{comment}</i>",
        parse_mode="HTML"
    )


print("Бот запущено...")
bot.infinity_polling()


