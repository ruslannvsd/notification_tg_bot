from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

from auto_notification.auto_news import auto_searching
from constants.general_constants import WELCOME_MESSAGE, BODY, FIND, SAVE_KEY, SAVE_TIME, keyboard, time_keyboard, \
    COMMANDS, ENTER_CHANNELS
from constants.data_constants import TOKEN
from database.checking import get_or_create_user
from database.chg_channels import adding_channels, get_current_channel_list
from database.chg_status import change_status
from keywords.change_keywords import saving_keywords
from searching.handling_messages import handle_message
from database.chg_time_period import set_time


async def start_command(update, ctx):
    get_or_create_user(update.message.chat.id)
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
    await app.bot.send_message(user_id, text)
    return SAVE_KEY


async def before_time_set(update, ctx):
    text = "Choose a period of time of monitoring:"
    await update.message.reply_text(text, reply_markup=time_keyboard)
    return SAVE_TIME


async def add_channel(update, ctx):
    user_id = update.message.chat.id
    current_list = get_current_channel_list(user_id)
    if current_list:
        await update.message.reply_text("Here's your current channel list:")
        await update.message.reply_text(current_list)
    text = "Enter a channel(e.g.: @channel)\n" \
           "or a list of channels divided by space (e.g.: @channel_1 @channel_2)"
    await update.message.reply_text(text)
    return ENTER_CHANNELS


conv_handler = ConversationHandler(
        entry_points=[CommandHandler(COMMANDS[0], start_command)],
        states={
            BODY: [
                MessageHandler(filters.Regex(f"^{COMMANDS[1]}$"), find_now),
                MessageHandler(filters.Regex(f"^{COMMANDS[2]}$"), keywords_f),
                MessageHandler(filters.Regex(f"^{COMMANDS[3]}$"), before_time_set),
                MessageHandler(filters.Regex(f"^{COMMANDS[4]}$"), change_status),
                MessageHandler(filters.Regex(f"^{COMMANDS[5]}$"), add_channel)
            ],
            FIND: [
                MessageHandler(filters.TEXT, handle_message)
            ],
            SAVE_KEY: [
                MessageHandler(filters.TEXT, saving_keywords)
            ],
            SAVE_TIME: [
                MessageHandler(filters.TEXT, set_time)
            ],
            ENTER_CHANNELS: [
                MessageHandler(filters.TEXT, adding_channels)
            ]
        },
        fallbacks=[CommandHandler(f"{COMMANDS[0]}", start_command)]
    )


# app body
if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(conv_handler)
    job_queue = app.job_queue
    job_queue.run_repeating(auto_searching, interval=14400, first=5)
    app.run_polling(3)
