from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from functions.db_scripts import check_user_in_db
from functions.states import AppDialog


async def send_welcome(message: types.Message):
    """Welcome message from functions"""
    user_id = message.from_user.id
    user_login = message.from_user.username

    result = check_user_in_db(user_id)
    if result is None:
        reply_keyboard = [[KeyboardButton('Sign up'), KeyboardButton('Cancel')]]

        await AppDialog.start.set()
        await message.answer(
            f"Hi, {user_login}!\n\n"
            f"Welcome to JuliasUchitBot.\n"
            f"You are new user, so lets sign up.\n\n"
            f"Are you ready?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Sign up, please'
            ),
        )
    else:
        await send_help(message)


async def send_help(message: types.Message):
    """Send information about functions depending on users"""
    user_id = message.from_user.id
    result = check_user_in_db(user_id)
    if result is None:
        await message.answer(
            "This functions will allow you to receive information and reminder about lessons, sign a contract\n\n"
            "You are new user, so you have limited functional.\n"
            "To get more, sign up, please.\n\n"
            "To sign up: /start"
        )
    else:
        await message.answer(
            "This functions will allow you to receive information and reminder about lessons, sign a contract\n\n"
            "Get information of lessons: /lesson"
        )


async def cancel_app(message: types.Message, state: FSMContext):
    """Canceling application process"""

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.reset_state(with_data=True)
    await state.finish()
    await message.reply(
        "Ok, maybe next time!\n"
        "Have a good day!",)


def register_handlers_initial(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands="start", state="*")
    dp.register_message_handler(send_help, commands="help", state="*")
    dp.register_message_handler(cancel_app, commands="cancel", state="*")
    dp.register_message_handler(cancel_app, Text(equals="отмена", ignore_case=True), state="*")
