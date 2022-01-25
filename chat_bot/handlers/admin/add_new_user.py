from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from functions.db_scripts import get_login, retrieve_user_by_login, add_lessons_info
from functions.states import AddActiveUser


async def message_new_user(query: types.CallbackQuery):

    await query.answer(f"Call to user and then insert initial lesson's time")


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


async def add_lesson_length(message: types.Message, state: FSMContext):
    """Last step for application. Send message to user and admin"""
    async with state.proxy() as user_info:
        user_info['classes'] = {}
        user_info['classes']['lesson_length'] = message.text.split(' ')[0]

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


async def add_level(message: types.Message, state: FSMContext):
    """First step of application. Request name"""

    async with state.proxy() as user_info:
        user_info['classes']['level'] = message.text

    await AddActiveUser.next()
    await message.reply(
        f"Send count of available lessons"
        )


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


async def add_promo(message: types.Message, state: FSMContext):
    """First step of application. Request name"""

    async with state.proxy() as user_info:
        if message.text == 'Yes':
            promo = True
        else:
            promo = False
        user_info['is_promo'] = promo

    add_lessons_info(user_info)
    await message.reply(
        f"Thank you for the information. Check the data:\n\n"
        f"Lesson length: {user_info['classes']['lesson_length']},"
        f"Level: {user_info['classes']['level']},"
        f"Available lessons: {user_info['classes']['available_lesson']},"
        f"Is promo: {user_info['is_promo']},"
        f"Scheduled:"
        f"{user_info['classes']['schedule']}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.reset_state(with_data=True)
    await state.finish()


def register_handlers_add_user(dp: Dispatcher):
    dp.register_callback_query_handler(message_new_user, text='new_user')
    dp.register_callback_query_handler(add_active_user, text='active')
    dp.register_message_handler(add_lesson_length, state=AddActiveUser.lesson_length)
    dp.register_message_handler(add_day, state=AddActiveUser.day)
    dp.register_message_handler(add_time, state=AddActiveUser.time)
    dp.register_message_handler(add_level, state=AddActiveUser.level)
    dp.register_message_handler(add_available_lesson, state=AddActiveUser.lesson_available)
    dp.register_message_handler(add_promo, state=AddActiveUser.is_promo)
