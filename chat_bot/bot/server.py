import asyncio
import logging
import os
import sys

import aiogram

path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from settings import TOKEN, STORAGE
from handlers.initial_bot import register_handlers_initial
from handlers.user.application import register_handlers_application

logging.basicConfig(level=logging.INFO)


# async def app_notification(message: types.Message):
#     """Send notification to admin with information about user"""
#     keyboard_markup = InlineKeyboardMarkup(row_width=3)
#     text_and_data = (
#         ('New', 'new_user'),
#         ('Active', 'active'),
#     )
#
#     row_btns = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
#
#     keyboard_markup.row(*row_btns)
#
#     await bot.send_message(
#         # message['tg_login'],  # TODO: Change for admin_id
#         '305607064',
#         f"There is new student!\n"
#         f"Name: {message['name']}\n"
#         f"Surname: {message['surname']}\n"
#         f"Email: {message['email']}\n"
#         f"Phone: {message['phone']}\n"
#         f"TG_link: t.me/{message['tg_login']}",
#         reply_markup=keyboard_markup,
#         )
#
#
# @dp.callback_query_handler(text='new_user', state=AddActiveUser.lesson_length)
# async def message_new_user(query: types.CallbackQuery, state=FSMContext):
#
#     await query.answer(f"Call to user and then insert initial lesson's time")
#
#
# @dp.callback_query_handler(text='active')
# async def add_active_user(query: types.CallbackQuery, state: FSMContext):
#     user_data = query.message.text
#     user_login = get_login(user_data)
#
#     result = retrieve_user_by_login(user_login)
#     await AddActiveUser.lesson_length.set()
#
#     async with state.proxy() as user_info:
#         user_info['id'] = result.id
#         user_info['tg_login'] = result.tg_login
#
#
#     reply_keyboard = [[KeyboardButton('60 min'), KeyboardButton('90 min')]]
#     await query.message.reply(
#         f"Ok. Let's add information about this student.\n\n"
#         f"Please, choose length of lessons",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose length'
#         ),
#     )
#
#
# @dp.message_handler(state=AddActiveUser.lesson_length)
# async def add_lesson_length(message: types.Message, state: FSMContext):
#     """Last step for application. Send message to user and admin"""
#     async with state.proxy() as user_info:
#         user_info['classes'] = {}
#         user_info['classes']['lesson_length'] = message.text
#
#     reply_keyboard = [[
#         KeyboardButton('Add Schedule')
#     ]]
#     await AddActiveUser.next()
#     await message.reply(
#         f"Ok, press 'Add schedule'",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Next step'
#         ),
#     )
#
#
# @dp.message_handler(state=AddActiveUser.day)
# async def add_day(message: types.Message, state: FSMContext):
#     """First step of application. Request name"""
#
#     if message.text != 'Add Schedule':
#         async with state.proxy() as user_info:
#             length = len(user_info['classes']['schedule'])
#             user_info['classes']['schedule'][length-1]['time'] = message.text
#
#     reply_keyboard = [[
#         KeyboardButton('Monday'),
#         KeyboardButton('Tuesday'),
#         KeyboardButton('Wednesday'),
#         KeyboardButton('Thursday'),
#         KeyboardButton('Friday'),
#         KeyboardButton('Saturday'),
#         KeyboardButton("That's All")
#     ]]
#     await AddActiveUser.next()
#     await message.reply(
#         f"Choose day.\n\n"
#         f"If you check all day, choose: That's All",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose day'
#         ),
#     )
#
#
# @dp.message_handler(state=AddActiveUser.time)
# async def add_time(message: types.Message, state: FSMContext):
#     """First step of application. Request name"""
#     if message.text == "That's All":
#         reply_keyboard = [[
#             KeyboardButton('Beginner'),
#             KeyboardButton('Elementary'),
#             KeyboardButton('Intermediate'),
#             KeyboardButton('UpperIntermediate'),
#             KeyboardButton('Advanced')
#         ]]
#         await AddActiveUser.next()
#         await message.reply(
#             f"Choose student level",
#             reply_markup=ReplyKeyboardMarkup(
#                 keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose level'
#             ),
#         )
#     else:
#         async with state.proxy() as user_info:
#             schedule = {'day': message.text}
#             if 'schedule' not in user_info['classes'].keys():
#                 user_info['classes']['schedule'] = []
#             user_info['classes']['schedule'].append(schedule)
#
#
#         await AddActiveUser.previous()
#         await message.reply(
#             f"Send scheduled time in format: 00:00",
#             reply_markup=ReplyKeyboardRemove(),
#         )
#
#
# @dp.message_handler(state=AddActiveUser.level)
# async def add_level(message: types.Message, state: FSMContext):
#     """First step of application. Request name"""
#
#     async with state.proxy() as user_info:
#         user_info['classes']['level'] = message.text
#
#     await AddActiveUser.next()
#     await message.reply(
#         f"Send count of available lessons"
#         )
#
#
# @dp.message_handler(state=AddActiveUser.lesson_available)
# async def add_available_lesson(message: types.Message, state: FSMContext):
#     """First step of application. Request name"""
#
#     async with state.proxy() as user_info:
#         user_info['classes']['available_lesson'] = message.text
#
#     reply_keyboard = [[
#         KeyboardButton('Yes'),
#         KeyboardButton('No')
#     ]]
#     await AddActiveUser.next()
#     await message.reply(
#         f"Is this student have promo status?",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Is Promo?'
#         ),
#     )
#
#
# @dp.message_handler(state=AddActiveUser.is_promo)
# async def add_promo(message: types.Message, state: FSMContext):
#     """First step of application. Request name"""
#
#     async with state.proxy() as user_info:
#         if message.text == 'Yes':
#             promo = True
#         else:
#             promo = False
#         user_info['classes']['is_promo'] = promo
#
#     await message.reply(
#         f"Thank you for the information. Check the data:\n\n"
#         f"{user_info}",
#         # f"Lesson length: {user_info['classes']['lesson_length']},"
#         # f"Level: {user_info['classes']['level']},"
#         # f"Available lessons: {user_info['classes']['available_lesson']},"
#         # f"Is promo: {user_info['classes']['available_lesson']},"
#         # f"Scheduled:"
#         # f"{user_info['classes']['schedule']}",
#         reply_markup=ReplyKeyboardRemove()
#     )
#     await state.reset_state(with_data=True)
#     await state.finish()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать диалог"),
        BotCommand(command="/help", description="Получить информацию"),
        BotCommand(command="/cancel", description="Вернуться в начало")
    ]
    await bot.set_my_commands(commands)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=STORAGE)


async def main():
    # bot = Bot(token=TOKEN)
    # dp = Dispatcher(bot, storage=STORAGE)

    # Регистрация хэндлеров
    register_handlers_initial(dp)
    register_handlers_application(dp)
    # register_handlers_food(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
