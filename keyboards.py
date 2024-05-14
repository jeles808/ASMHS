from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_administrator_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Результаты')],
            [KeyboardButton(text='Все ответы XLSX')],
            [KeyboardButton(text='Анализ ответов PDF')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def keyboard_start():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Старт')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


Keyboard_q3 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1'),
                                           KeyboardButton(text='2')],
                                           [KeyboardButton(text='3'),
                                           KeyboardButton(text='4')]])


Keyboard_q4 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='ИД 23.1/Б1-20'),
                                           KeyboardButton(text='ИД 23.2/Б2-20')],
                                           [KeyboardButton(text='ИД 23.1/Б2-20'),
                                           KeyboardButton(text='о.ИДc 23.1/Б3-21')]])


Keyboard_q5 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Не занимаюсь'),
                                           KeyboardButton(text='1-2 раза в неделю')],
                                           [KeyboardButton(text='3-5 раз в неделю'),
                                           KeyboardButton(text='Каждый день')]])


Keyboard_q6_q9 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Хорошо'),
                                           KeyboardButton(text='Нормально')],
                                           [KeyboardButton(text='Плохо'),
                                           KeyboardButton(text='Ужасно')]])


Keyboard_q7_q8_q11_q12_q13_q15 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да')],
                                           [KeyboardButton(text='Нет')]])


Keyboard_q10 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1-2 раза'),
                                           KeyboardButton(text='3 раза')],
                                           [KeyboardButton(text='4 раза'),
                                           KeyboardButton(text='5 или более раз')]])


Keyboard_q14 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Не употребляю'),
                                           KeyboardButton(text='Редко')],
                                           [KeyboardButton(text='Часто'),
                                           KeyboardButton(text='Постоянно')]])


Keyboard_q16 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1-2 часа'),
                                           KeyboardButton(text='3 часа')],
                                           [KeyboardButton(text='4 часа'),
                                           KeyboardButton(text='5 или более часов')]])


Keyboard_q17 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Никогда'),
                                           KeyboardButton(text='Редко')],
                                           [KeyboardButton(text='Часто'),
                                           KeyboardButton(text='Постоянно')]])
