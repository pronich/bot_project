import logging
import os
import aiohttp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import \
    ReplyKeyboardMarkup, \
    KeyboardButton, \
    ReplyKeyboardRemove, \
    InlineKeyboardMarkup, \
    InlineKeyboardButton
from pprint import pprint
import exceptions
from settings import TOKEN, STORAGE, ADMIN_ID
from check_func import create_user, check_user_in_db, retrieve_user_by_login, get_login

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=STORAGE)


class AppDialog(StatesGroup):
    start = State()
    name = State()
    surname = State()
    email = State()
    phone = State()
    notification = State()


class AddActiveUser(StatesGroup):
    lesson_length = State()
    day = State()
    time = State()
    level = State()
    lesson_available = State()
    is_promo = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Welcome message from bot"""
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


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """Send information about bot depending on users"""
    user_id = message.from_user.id
    result = check_user_in_db(user_id)
    if result is None:
        await message.answer(
            f"This bot will allow you to receive information and reminder about lessons, sign a contract\n\n"
            f"You are new user, so you have limited functional.\n"
            f"To get more, sign up, please.\n\n"
            f"To sign up: /start"
        )
    else:
        await message.answer(
            f"This bot will allow you to receive information and reminder about lessons, sign a contract\n\n"
            f"Get information of lessons: /lesson"
        )


@dp.message_handler(state='*', commands='cancel')
async def cancel_app(message: types.Message, state: FSMContext):
    """Canceling application process"""

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.reset_state(with_data=True)
    await state.finish()
    await message.reply(
        f"Ok, maybe next time!\n"
        f"Have a good day!",)


@dp.message_handler(state=AppDialog.start)
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


@dp.message_handler(state=AppDialog.name)
async def app_name(message: types.Message, state: FSMContext):
    """Second step for application. Request surname"""
    async with state.proxy() as user_info:
        user_info['name'] = message.text

    await AppDialog.next()
    await message.reply(
        f"Please, wright your SURNAME in Russian.\n"
        f"For example, Петров"
    )


@dp.message_handler(state=AppDialog.surname)
async def app_surname(message: types.Message, state: FSMContext):
    """Third step for application. Request email"""
    async with state.proxy() as user_info:
        user_info['surname'] = message.text

    await AppDialog.next()
    await message.reply(
        f"There are only a couple of steps left!\n"
        f"Please, wright your EMAIL"
    )


@dp.message_handler(state=AppDialog.email)
async def app_email(message: types.Message, state: FSMContext):
    """Fourth step for application. Request phone"""
    async with state.proxy() as user_info:
        user_info['email'] = message.text

    await AppDialog.next()
    await message.reply(
        f"Write your PHONE NUMBER in the format +7999999999999"
    )


@dp.message_handler(state=AppDialog.phone)
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

        await app_notification(user_info)
    await state.reset_state(with_data=True)
    await state.finish()


async def app_notification(message: types.Message):
    """Send notification to admin with information about user"""
    keyboard_markup = InlineKeyboardMarkup(row_width=3)
    text_and_data = (
        ('New', 'new_user'),
        ('Active', 'active'),
    )

    row_btns = (InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup.row(*row_btns)

    await bot.send_message(
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


@dp.callback_query_handler(text='new_user', state=AddActiveUser.lesson_length)
async def message_new_user(query: types.CallbackQuery, state=FSMContext):

    await query.answer(f"Call to user and then insert initial lesson's time")


@dp.callback_query_handler(text='active')
async def add_active_user(query: types.CallbackQuery, state: FSMContext):
    user_data = query.message.text
    user_login = get_login(user_data)

    result = retrieve_user_by_login(user_login)
    await AddActiveUser.lesson_length.set()

    async with state.proxy() as user_info:
        user_info['id'] = result.id
        user_info['tg_login'] = result.tg_login


    reply_keyboard = [[KeyboardButton('60 min'), KeyboardButton('90 min')]]
    await query.message.reply(
        f"Ok. Let's add information about this student.\n\n"
        f"Please, choose length of lessons",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose length'
        ),
    )


@dp.message_handler(state=AddActiveUser.lesson_length)
async def add_lesson_length(message: types.Message, state: FSMContext):
    """Last step for application. Send message to user and admin"""
    async with state.proxy() as user_info:
        user_info['classes'] = {}
        user_info['classes']['lesson_length'] = message.text

    reply_keyboard = [[
        KeyboardButton('Add Schedule')
    ]]
    await AddActiveUser.next()
    await message.reply(
        f"Ok, press 'Add schedule'",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Next step'
        ),
    )


@dp.message_handler(state=AddActiveUser.day)
async def add_day(message: types.Message, state: FSMContext):
    """First step of application. Request name"""

    if message.text != 'Add Schedule':
        async with state.proxy() as user_info:
            length = len(user_info['classes']['schedule'])
            user_info['classes']['schedule'][length-1]['time'] = message.text

    reply_keyboard = [[
        KeyboardButton('Monday'),
        KeyboardButton('Tuesday'),
        KeyboardButton('Wednesday'),
        KeyboardButton('Thursday'),
        KeyboardButton('Friday'),
        KeyboardButton('Saturday'),
        KeyboardButton("That's All")
    ]]
    await AddActiveUser.next()
    await message.reply(
        f"Choose day.\n\n"
        f"If you check all day, choose: That's All",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose day'
        ),
    )


@dp.message_handler(state=AddActiveUser.time)
async def add_time(message: types.Message, state: FSMContext):
    """First step of application. Request name"""
    if message.text == "That's All":
        reply_keyboard = [[
            KeyboardButton('Beginner'),
            KeyboardButton('Elementary'),
            KeyboardButton('Intermediate'),
            KeyboardButton('UpperIntermediate'),
            KeyboardButton('Advanced')
        ]]
        await AddActiveUser.next()
        await message.reply(
            f"Choose student level",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose level'
            ),
        )
    else:
        async with state.proxy() as user_info:
            schedule = {'day': message.text}
            if 'schedule' not in user_info['classes'].keys():
                user_info['classes']['schedule'] = []
            user_info['classes']['schedule'].append(schedule)


        await AddActiveUser.previous()
        await message.reply(
            f"Send scheduled time in format: 00:00",
            reply_markup=ReplyKeyboardRemove(),
        )


@dp.message_handler(state=AddActiveUser.level)
async def add_level(message: types.Message, state: FSMContext):
    """First step of application. Request name"""

    async with state.proxy() as user_info:
        user_info['classes']['level'] = message.text

    await AddActiveUser.next()
    await message.reply(
        f"Send count of available lessons"
        )


@dp.message_handler(state=AddActiveUser.lesson_available)
async def add_available_lesson(message: types.Message, state: FSMContext):
    """First step of application. Request name"""

    async with state.proxy() as user_info:
        user_info['classes']['available_lesson'] = message.text

    reply_keyboard = [[
        KeyboardButton('Yes'),
        KeyboardButton('No')
    ]]
    await AddActiveUser.next()
    await message.reply(
        f"Is this student have promo status?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=reply_keyboard, one_time_keyboard=True, input_field_placeholder='Is Promo?'
        ),
    )


@dp.message_handler(state=AddActiveUser.is_promo)
async def add_promo(message: types.Message, state: FSMContext):
    """First step of application. Request name"""

    async with state.proxy() as user_info:
        if message.text == 'Yes':
            promo = True
        else:
            promo = False
        user_info['classes']['is_promo'] = promo

    await message.reply(
        f"Thank you for the information. Check the data:\n\n"
        f"{user_info}",
        # f"Lesson length: {user_info['classes']['lesson_length']},"
        # f"Level: {user_info['classes']['level']},"
        # f"Available lessons: {user_info['classes']['available_lesson']},"
        # f"Is promo: {user_info['classes']['available_lesson']},"
        # f"Scheduled:"
        # f"{user_info['classes']['schedule']}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.reset_state(with_data=True)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
