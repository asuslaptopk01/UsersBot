from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_inline_buttons(buttons, size=None, repeat=False):
    ikb = InlineKeyboardBuilder()

    for item in buttons:
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str):
            text, callback = item
            ikb.row(InlineKeyboardButton(text=text, callback_data=callback))

        elif isinstance(item, (list, tuple)):
            row_buttons = []
            for btn in item:
                if isinstance(btn, tuple) and len(btn) == 2:
                    text, callback = btn
                    row_buttons.append(InlineKeyboardButton(text=text, callback_data=callback))
            if row_buttons:
                ikb.row(*row_buttons)
        else:
            raise ValueError(f"Invalid button format: {item}")
    if size:
        ikb.adjust(*size, repeat=repeat)

    return ikb.as_markup()
