from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import constants
from handling_messages import handle_message
from data_constants import TOKEN


# commands
async def start_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(constants.WELCOME_MESSAGE)


# app body
if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Polling ...")
    app.run_polling(3)
