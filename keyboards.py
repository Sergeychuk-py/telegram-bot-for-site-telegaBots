from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def markup():
    keyboards = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Поддержка")],
        [KeyboardButton(text="Нишы ботов")],
        [KeyboardButton(text="Заказать разработку")],
    ], resize_keyboard=True)
    return keyboards