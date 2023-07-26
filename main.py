import time

from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, \
    ContextTypes

from classes_folder.user import User
from commands.create_txt import create_txt_file, cancel_command
from constants.general_constants import WELCOME_MESSAGE, BODY, FIND, SAVE_KEY, SAVE_TIME, keyboard, time_keyboard, \
    COMMANDS
from constants.data_constants import TOKEN
from keywords.change_keywords import saving_keywords, keywords_command
from open_files.auto_news import auto_searching, all_users
from options.disable_enable import set_enable_disable
from searching.handling_messages import handle_message, auto_text
from time_mng.time_setting import set_time
from utils.time_functions import convert_to_readable_time


async def start_command(update, ctx):
    user_id = update.message.chat.id
    user = User(user_id, "", 0, "disabled")
    create_txt_file(user)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=keyboard)
    return BODY


async def find_now(update, ctx):
    user_id = update.message.chat.id
    text = "Enter keyword(s) to check news now:"
    await app.bot.send_message(user_id, text)
    return FIND


async def keywords_f(update, ctx):
    user_id = update.message.chat.id
    text = "Enter/change keywords:"
    await app.bot.send_message(user_id, keywords_command(user_id))
    await app.bot.send_message(user_id, text)
    return SAVE_KEY


async def before_time_set(update, ctx):
    text = "Choose a period of time of monitoring:"
    await update.message.reply_text(text, reply_markup=time_keyboard)
    return SAVE_TIME


conv_handler = ConversationHandler(
        entry_points=[CommandHandler(COMMANDS[0], start_command)],
        states={
            BODY: [
                MessageHandler(filters.Regex(f"^{COMMANDS[1]}$"), find_now),
                MessageHandler(filters.Regex(f"^{COMMANDS[2]}$"), keywords_f),
                MessageHandler(filters.Regex(f"^{COMMANDS[3]}$"), before_time_set),
                MessageHandler(filters.Regex(f"^{COMMANDS[4]}$"), set_enable_disable),
            ],
            FIND: [
                MessageHandler(filters.TEXT, handle_message)
            ],
            SAVE_KEY: [
                MessageHandler(filters.TEXT, saving_keywords)
            ],
            SAVE_TIME: [
                MessageHandler(filters.TEXT, set_time)
            ]
        },
        fallbacks=[CommandHandler(f"{COMMANDS[5]}", cancel_command)]
    )


# app body
if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(conv_handler)
    job_queue = app.job_queue

    job_minute = job_queue.run_repeating(auto_searching, interval=3600, first=5)
    app.run_polling(3)
