import datetime

from aiogram import types
from bot.models import Weekend, Salons, Appointments, Employee, Procedures

# from django.utils.timezone import localtime


# localtime()
PROCEDURES = [
    "Мейкап",
    "Покраска волос",
    "Маникюр",
]

SET_TIME = [
    "10_00", "10_30", "11_00", "11_30",
    "12_00", "12_30", "13_00", "13_30",
    "14_00", "14_30", "15_00", "15_30",
    "16_00", "16_30", "17_00", "17_30",
    "18_00", "18_30", "19_00", "19_30",
    "20_00", "20_30"
]

USERS_DATA = {}

DATE = {}

# specialist = ['Ольга', 'Татьяна']


def get_keyboard_navigation_calendar(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="🕔 Записаться на удобное время",
            callback_data=callback_keyboard.new(action="navigation_calendar", value="")),
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_change_fab_back(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="🔙 Вернутся назад",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_none(callback_keyboard):
    buttons = []
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_fab_for_start(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="✏️Записаться к нам",
                                   callback_data=callback_keyboard.new(action="sign_up", value="")),
        types.InlineKeyboardButton(text="📅 Посмотреть свои записи",
                                   callback_data=callback_keyboard.new(action="your_recordings", value="")),
        types.InlineKeyboardButton(text="🪪 О нас",
                                   callback_data=callback_keyboard.new(action="about_us", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_select_procedures(callback_keyboard):
    procedures = Procedures.objects.all()
    buttons = []
    for procedure in procedures:
        text = procedure.name
        value = procedure.pk
        buttons.append(
            types.InlineKeyboardButton(text=text,
            callback_data=callback_keyboard.new(action="procedure", value=value))
            )
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
        callback_data=callback_keyboard.new(action="back", value=""))
        )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_choose_specialist_before_change_date(callback_keyboard):
    buttons = []
    for master in Employee.objects.filter(procedure__pk=int(USERS_DATA["procedures"])):
        buttons.append(
            types.InlineKeyboardButton(text=f"✅ Мастер {master.name}",
                                       callback_data=callback_keyboard.new(action="navigation_calendar",
                                                                           value=master.pk)),
        )
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_choose_specialist(callback_keyboard):
    buttons = []
    for master in Employee.objects.filter(procedure__pk=int(USERS_DATA["procedures"])):
        buttons.append(types.InlineKeyboardButton(text=f"✅ Мастер {master.name}",
                        callback_data=callback_keyboard.new(action="personal_data", value=master.pk)))
    buttons.append(types.InlineKeyboardButton(text="🔚 В начало",
                        callback_data=callback_keyboard.new(action="back", value="")))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_sign_up(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="🕔 Записаться на удобное время",
            callback_data=callback_keyboard.new(action="navigation_calendar", value="")),
        types.InlineKeyboardButton(text="💁‍♀️Выбрать мастера",
                                   callback_data=callback_keyboard.new(
                                       action="choose_specialist_before_change_date", value="")),
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_set_time():
    set_time = []
    if USERS_DATA["date"] == datetime.datetime.today().date():
        for slot in SET_TIME:
            print(SET_TIME)
            print(slot)
            if datetime.datetime.now().time() < datetime.time(int(slot.split("_")[0]), int(slot.split("_")[1]), 0):
                set_time.append(slot)
        return set_time
    else:
        return SET_TIME


def get_keyboard_make_an_appointment(callback_keyboard):
    buttons = []
    set_time = get_set_time()
    for my_time in set_time:
        time_strip = my_time.replace('_', ":")
        buttons.append(types.InlineKeyboardButton(
            text=f"{time_strip}",
            callback_data=callback_keyboard.new(action="choose_specialist", value=my_time)))
    buttons.append(types.InlineKeyboardButton(text="🔚 В начало",
                                              callback_data=callback_keyboard.new(action="back", value="")))
    buttons.append(types.InlineKeyboardButton(text="🔙 Изменить день",
                                              callback_data=callback_keyboard.new(
                                                  action="back_to_select_date", value="")))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_appointment_have_choose_specialist(callback_keyboard):
    buttons = []
    set_time = get_set_time()
    for my_time in set_time:
        time_strip = my_time.replace('_', ":")
        buttons.append(types.InlineKeyboardButton(
            text=f"{time_strip}",
            callback_data=callback_keyboard.new(action="personal_data", value=my_time)))
    buttons.append(types.InlineKeyboardButton(text="🔚 В начало",
                                              callback_data=callback_keyboard.new(action="back", value="")))
    buttons.append(types.InlineKeyboardButton(text="🔙 Изменить день",
                                              callback_data=callback_keyboard.new(
                                                  action="back_to_select_date", value="")))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_personal_data(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="✅ Согласен на обработку ПД",
                                   callback_data=callback_keyboard.new(action="specify_name", value="")),
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_recordings(callback_keyboard):
    user_id = USERS_DATA.get('user_id')
    recordings = Appointments.objects.filter(telegram_id=user_id)[:10]
    buttons = []
    for recording in recordings:
        text = f'{recording.procedure.name}_{recording.appointment_date.strftime("%m-%d")}_{recording.appointment_time}'
        buttons.append(
            types.InlineKeyboardButton(text=f"{text}",
                                       callback_data=callback_keyboard.new(action="to_recordings", value='')),
        )
    buttons.append(types.InlineKeyboardButton(text="🔚 В начало",
                                              callback_data=callback_keyboard.new(action="back", value="")))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


