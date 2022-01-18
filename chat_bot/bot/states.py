from aiogram.dispatcher.filters.state import StatesGroup, State


class AppDialog(StatesGroup):
    start = State()
    name = State()
    surname = State()
    email = State()
    phone = State()


class AddActiveUser(StatesGroup):
    lesson_length = State()
    day = State()
    time = State()
    level = State()
    lesson_available = State()
    is_promo = State()
