from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.settings import BOT


async def new_user_notification(message: types.Message):
    """Send notification to admin with information about user"""
    keyboard_markup = InlineKeyboardMarkup(row_width=3)
    text_and_data = (
        ('New', 'new_user'),
        ('Active', 'active'),
    )

    row_btns = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup.row(*row_btns)

    await BOT.send_message(
        # message['tg_login'],  # TODO: Change for admin_id
        '305607064',
        f"There is new student!\n"
        f"Name: {message['name']}\n"
        f"Surname: {message['surname']}\n"
        f"Email: {message['email']}\n"
        f"Phone: {message['phone']}\n"
        f"TG_link: t.me/{message['tg_login']}",
        reply_markup=keyboard_markup,
        )
