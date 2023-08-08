from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

from constants.general_constants import WELCOME_MESSAGE, BODY, FIND, SAVE_KEY, SAVE_TIME, keyboard, time_keyboard, \
    COMMANDS, ENTER_CHANNELS, STATUS_COMMANDS, INTERVAL
from constants.data_constants import TOKEN
from database.checking import check_user_if_exists
from database.chg_channels import adding_channels, get_current_channel_list
from database.chg_kw import saving_keywords
from database.chg_status import change_status
from database.chg_time_period import set_time
from database.database import get_users_col
from searching.scraping import repeating_scraping, now_scraping


async def start_command(update, ctx):
    user_id = update.message.chat.id
    status = STATUS_COMMANDS[0] if not check_user_if_exists(user_id) else STATUS_COMMANDS[1]
    kb = keyboard(status)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=kb)
    return BODY


async def cancel_command(update, ctx):
    await update.message.reply_text("Your last command is cancelled.")
    return BODY


async def find_now(update, ctx):
    user_id = update.message.chat.id
    text = "Enter keyword(s) to check news now:"
    await app.bot.send_message(user_id, text)
    return FIND


async def keywords_f(update, ctx):
    user_id = update.message.chat.id
    users_col = get_users_col()
    user = users_col.find_one({"id": user_id})
    current_kw = user["keywords"]
    if current_kw:
        kw_string = " ".join(current_kw).strip()
        await app.bot.send_message(user_id, "Your current list of keywords:")
        await app.bot.send_message(user_id, "`" + kw_string + "`", parse_mode="MarkdownV2")
        await app.bot.send_message(user_id, "Enter your new list of keywords:")
    else:
        text = f"You've got no keywords.\n\nEnter your list of keywords:"
        await app.bot.send_message(user_id, text)
    return SAVE_KEY


async def before_time_set(update, ctx):
    text = "Choose time :"
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
                MessageHandler(filters.Regex(f"^{STATUS_COMMANDS[0]}$"), change_status),
                MessageHandler(filters.Regex(f"^{STATUS_COMMANDS[1]}$"), change_status),
                MessageHandler(filters.Regex(f"^{COMMANDS[4]}$"), add_channel)
            ],
            FIND: [
                MessageHandler(filters.TEXT, now_scraping)
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
        fallbacks=[CommandHandler(f"{COMMANDS[5]}", cancel_command)]
    )


# app body
if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(conv_handler)
    job_queue = app.job_queue
    job_queue.run_repeating(repeating_scraping, interval=INTERVAL[0], first=1)
    app.run_polling(3)
