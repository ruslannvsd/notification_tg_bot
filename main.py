from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from constants import constants
from options.disable_enable import set_enable_disable
from options.keywords import keywords_command, enter_keywords
from commands.menu_command import menu_command_f
from commands.start import start_command
from constants.data_constants import TOKEN
from searching.handling_messages import handle_message


async def button_click(update, ctx):
    query = update.callback_query
    option = query.data
    user_id = query.message.chat.id
    text = ""

    # handling different options
    if option == "option1":
        text = "Enter/change keywords:"
        await app.bot.send_message(user_id, keywords_command(user_id))
        app.add_handler(MessageHandler(filters.TEXT, enter_keywords))
    elif option == "option2":
        with open(f"{constants.PATH}/{user_id}.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            status = "disabled" if lines[2].strip() == "enabled" else "enabled"
            text = f"Your subscription is {status}"
        set_enable_disable(user_id)
    elif option == "option3":
        text = "Set time in the following format,\n" \
               "where HH - starting hour of the day\n" \
               "x - hour-frequency:\nHH, x"
    elif option == "option4":
        text = "Enter keyword(s) to check news now:"
        app.add_handler(MessageHandler(filters.TEXT, handle_message))
    await update.effective_message.edit_reply_markup(None)
    await app.bot.send_message(user_id, text)

# app body
if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler(constants.COMMANDS[0], start_command))
    app.add_handler(CommandHandler(constants.COMMANDS[1], menu_command_f))
    app.add_handler(CallbackQueryHandler(button_click))
    print("Polling ...")
    app.run_polling(3)
