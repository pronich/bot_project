from sqlalchemy.orm import sessionmaker
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove

from bot.initial_db import Users
from bot.settings import TOKEN, LOGGER, ENGINE
from telegram.ext import Updater, CallbackContext, CommandHandler, ConversationHandler, MessageHandler, Filters

Session = sessionmaker(bind=ENGINE)
session = Session()

NAME, SURNAME, EMAIL, PHONE, APP_END = range(5)

user_info = {}


def get_user_info(from_user):
    user_info['id'] = from_user.id
    user_info['tg_login'] = from_user.username
    return user_info


def check_user_in_db(user):
    result = session.query(Users).filter(Users.id == user['id']).first()
    return result


def start(update: Update, context: CallbackContext) -> None:
    """Inform user about what this bot can do"""
    user = get_user_info(update.message.from_user)
    # result = check_user_in_db(user)
    # if result is None:
    #     u1 = Users(id=user['id'], tg_login=user['tg_login'], status='New')
    #     session.add(u1)
    #     session.commit()
    #     u1 = check_user_in_db(user)
    #     user_info['id'] = u1.id
    # else:
    #     user_info['id'] = result

    reply_keyboard = [['Sign up', 'Cancel']]

    update.message.reply_text(
        f"Hi, {user['tg_login']}!"
        f"Welcome to JuliasUchitBot.\n\n"
        f"You are new user, so lets sign up.\n\n"
        f"Are you ready?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Sign up, please'
        ),
    )
    return NAME
    # else:
    #     update.message.reply_text("Have a good day")



def name(update: Update, context: CallbackContext) -> None:

    update.message.reply_text(
        f"Good!\n"
        f"Sign up doesn't take a lot of time.\n\n"
        f"Please, wright your NAME in Russian."
        f"For example, Василий",
        reply_markup=ReplyKeyboardRemove(),
    )

    return SURNAME

def surname(update: Update, context: CallbackContext) -> None:

    user_info['name'] = update.message.text

    update.message.reply_text(
        f"Please, wright your SURNAME in Russian.\n"
        f"For example, Петров"
    )

    return EMAIL

def email(update: Update, context: CallbackContext) -> None:

    user_info['surname'] = update.message.text
    update.message.reply_text(
        f"There are only a couple of steps left!\n"
        f"Please, wright your EMAIL"
    )

    return PHONE


def phone(update: Update, context: CallbackContext) -> None:

    user_info['email'] = update.message.text
    update.message.reply_text(
        f"Write your PHONE NUMBER in the format +7999999999999"
    )

    return APP_END


def app_end(update: Update, context: CallbackContext) -> None:

    user_info['phone'] = update.message.text
    u1 = Users(id=user_info['id'],
               tg_login=user_info['tg_login'],
               name=user_info['name'],
               surname=user_info['surname'],
               email=user_info['email'],
               phone=user_info['phone'])
    session.add(u1)
    session.commit()
    update.message.reply_text(
        f"Thank you for the information!\n\n"
        f"Julia will send you a message soon.\n"
        f"Have a nice day!"
    )

    return ConversationHandler.END


def get_lessons(update: Update, context: CallbackContext) -> None:
    """Return leson's information to user"""
    update.message.reply_text(
        "Text here"
    )


def cancel(update: Update, context: CallbackContext) -> None:

    update.message.reply_text(
        f"Ok, maybe next time!\n"
        f"Have a good day!"
    )

    return ConversationHandler.END


def main() -> None:
    """Run bot."""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [
                MessageHandler(Filters.regex('^(Sign up)$'), name),
                MessageHandler(Filters.regex('^(Cancel)$'), cancel)
            ],
            SURNAME: [MessageHandler(Filters.text, surname)],
            EMAIL: [MessageHandler(Filters.text, email)],
            PHONE: [MessageHandler(Filters.text, phone)],
            APP_END: [MessageHandler(Filters.text, app_end)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()


{
    "id": "1312572348286544380",
    "from": {
        "id": 305607064,
        "is_bot": false,
        "first_name": "Nikolay",
        "username": "Pronich",
        "language_code": "ru"
    },
    "message": {
        "message_id": 446,
        "from": {
            "id": 5015423087,
            "is_bot": true,
            "first_name": "julia_uchit",
            "username": "JuliaUchitBot"
        },
        "chat": {
            "id": 305607064,
            "first_name": "Nikolay",
            "username": "Pronich",
            "type": "private"
        },
        "date": 1642500621,
        "text": "There is new student!\nName: Niko\nSurname: Pron\nEmail: mail@mail.ru\nPhone: +79295918007\nTG_link: t.me/Pronich",
        "entities": [
            {
                "type": "email", "offset": 54, "length": 12}, {"type": "phone_number", "offset": 74, "length": 12}, {"type": "url", "offset": 96, "length": 12}], "reply_markup": {"inline_keyboard": [[{"text": "New", "callback_data": "new_user"}, {"text": "Active", "callback_data": "active"}]]}}, "chat_instance": "8358028624234122487", "data": "active"}