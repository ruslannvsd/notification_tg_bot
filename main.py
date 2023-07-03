import time

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import constants
import get_post
import time_functions
from send_notification import send_notification
from sensitive_constants import TOKEN, USER_ID
from time_trigger import send_message


# commands
async def start_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(constants.WELCOME_MESSAGE)


def handle_checking_news(word: str):
    news = get_post.get_retrieved(word)
    if news is False:
        return False
    else:
        return news


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # getting message type
    message_type = update.message.chat.type
    # getting words a user entered
    text = update.message.text.split(" ")
    # internal registration of the time a user made an entry
    date = update.message.date
    print(f"User {update.message.chat.id} in {message_type} : {text} (date: {date})")
    # checking if words are contained in latest news
    for txt in text:
        amount = 0
        if handle_checking_news(txt.lower()) is not False:
            response = handle_checking_news(txt.lower())
            amount = len(response)
            for item in response:
                time_ = time_functions.convert_to_readable_time(item.article_time)
                article = f"{item.news_channel.channel_name}" \
                          f"\n{item.article_link}\n{time_}\n\n{item.article}"
                await update.message.reply_text(article)
        else:
            await update.message.reply_text(f"No news with {txt} found.")
        await update.message.reply_text(f"{amount} article(s).\nThat's all I've found for now.")
        print("Processing completed")


# app body
if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("Polling ...")
    app.run_polling(3)

    send_notification(app.bot, USER_ID)



