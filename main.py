from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import constants
import get_post


# commands
async def start_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(constants.WELCOME_MESSAGE)


def handle_checking_news(word: str):
    news = get_post.get_retrieved(word)
    if not news:
        return [f"No news with {str(word)} are found"]
    else:
        return news


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # getting message type
    message_type = update.message.chat.type
    # getting words a user entered
    text = update.message.text.lower().split(" ")
    # internal registration of the time a user made an entry
    date = update.message.date
    print(f"User {update.message.chat.id} in {message_type} : {text} (date: {date})")
    # checking if words are contained in latest news
    for txt in text:
        response = handle_checking_news(txt)
        for item in response:
            await update.message.reply_text(item)
        print("The End")


# app body
if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(constants.TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Polling ...")
    app.run_polling(3)
