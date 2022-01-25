from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from functions.db_scripts import create_user
from functions.states import AppDialog
from handlers.admin.notifications import new_user_notification


async def app_start(message: types.Message, state: FSMContext):
    """First step of application. Request name"""
    async with state.proxy() as user_info:
        user_info['id'] = message.from_user.id
        user_info['tg_login'] = message.from_user.username

    await AppDialog.next()
    await message.reply(
        f"Good!\n"
        f"Sign up doesn't take a lot of time.\n\n"
        f"You can leave sign up with command: /cancel\n\n"
        f"Please, wright your NAME in Russian."
        f"For example, Василий",
        reply_markup=ReplyKeyboardRemove(),
    )


async def app_name(message: types.Message, state: FSMContext):
    """Second step for application. Request surname"""
    async with state.proxy() as user_info:
        user_info['name'] = message.text

    await AppDialog.next()
    await message.reply(
        f"Please, wright your SURNAME in Russian.\n"
        f"For example, Петров"
    )


async def app_surname(message: types.Message, state: FSMContext):
    """Third step for application. Request email"""
    async with state.proxy() as user_info:
        user_info['surname'] = message.text

    await AppDialog.next()
    await message.reply(
        f"There are only a couple of steps left!\n"
        f"Please, wright your EMAIL"
    )


async def app_email(message: types.Message, state: FSMContext):
    """Fourth step for application. Request phone"""
    async with state.proxy() as user_info:
        user_info['email'] = message.text

    await AppDialog.next()
    await message.reply(
        f"Write your PHONE NUMBER in the format +79999999999"
    )


async def app_phone(message: types.Message, state: FSMContext):
    """Last step for application. Send message to user and admin"""
    async with state.proxy() as user_info:
        user_info['phone'] = message.text

        create_user(user_info)

        await message.reply(
            f"Thank you for the information, {user_info['name']}!\n\n"
            f"Julia will send you a message soon.\n"
            f"Have a nice day!"
        )

        await new_user_notification(user_info)
    await state.reset_state(with_data=True)
    await state.finish()


def register_handlers_application(dp: Dispatcher):
    dp.register_message_handler(app_start, state=AppDialog.start)
    dp.register_message_handler(app_name, state=AppDialog.name)
    dp.register_message_handler(app_surname, state=AppDialog.surname)
    dp.register_message_handler(app_email, state=AppDialog.email)
    dp.register_message_handler(app_phone, state=AppDialog.phone)
