from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

from classes_folder.user import User
from commands.start import create_txt_file
from constants.general_constants import COMMANDS, WELCOME_MESSAGE, BODY, FIND, TIME, SAVE_KEY, SAVE_TIME, keyboard, \
    time_keyboard
from constants.data_constants import TOKEN
from keywords.change_keywords import saving_keywords, keywords_command
from options.disable_enable import set_enable_disable
from searching.handling_messages import handle_message
from time_mng.time_setting import set_time


async def start_command(update, ctx):
    user_id = update.message.chat.id
    user = User(user_id, "", 0, "disabled")
    create_txt_file(user)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=keyboard)
    return BODY


async def find_now(update, ctx) -> int:
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


# app body
if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            BODY: [
                MessageHandler(filters.Regex("^findnow$"), find_now),
                MessageHandler(filters.Regex("^keywords$"), keywords_f),
                MessageHandler(filters.Regex("^timeset$"), before_time_set),
                MessageHandler(filters.Regex("^enabling$"), set_enable_disable)
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
        fallbacks=[CommandHandler("start", start_command)]
    )
    app.add_handler(conv_handler)
    print("Polling ...")
    app.run_polling(3)
