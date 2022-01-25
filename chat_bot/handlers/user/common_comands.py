from aiogram import Dispatcher, types
from functions.db_scripts import check_user_in_db, get_lessons_by_user


async def get_lesson(message: types.Message):
    user = check_user_in_db(user=message.from_user.id, status='Active')
    if user is None:
        pass
    else:
        data = get_lessons_by_user(user.id)
        newline = "\n\t\t"
        await message.reply(
            f"Info:\n\n"
            f"Level: {data['level']}\n"
            f"Available lessons: {data['available_lesson']}\n"
            f"Scheduled: \n\t\t"
            f"{newline.join(f'{key}: {value}' for key, value in data['schedule'].items())}", )


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(get_lesson, commands="lesson", state="*")
