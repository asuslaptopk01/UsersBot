from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_reply_buttons(buttons, size=[1], repeat=False):  # noqa
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=button) for button in buttons])
    rkb.adjust(*size, repeat=repeat)
    return rkb.as_markup(resize_keyboard=True)