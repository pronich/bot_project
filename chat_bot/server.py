import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand
from config.settings import BOT, DP, LOGGER
from handlers.initial_bot import register_handlers_initial
from handlers.user.application import register_handlers_application
from handlers.admin.add_new_user import register_handlers_add_user

logging.basicConfig(level=logging.INFO)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать диалог"),
        BotCommand(command="/help", description="Получить информацию"),
        BotCommand(command="/cancel", description="Вернуться в начало")
    ]
    await bot.set_my_commands(commands)


async def main():
    LOGGER.error("Starting bot")

    # Регистрация хэндлеров
    register_handlers_initial(DP)
    register_handlers_application(DP)
    register_handlers_add_user(DP)

    # Установка общих команд бота
    await set_commands(BOT)

    # Запуск поллинга
    await DP.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await DP.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
