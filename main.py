from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

import constants
from commands.disable_enable import set_enable_disable
from commands.keywords import keywords_command
from commands.menu_command import menu_command_f
from commands.start import start_command
from data_constants import TOKEN
from handling_messages import handle_message


async def button_click(update, ctx):
    query = update.callback_query
    option = query.data
    user_id = query.message.chat.id

    # handling different options
    if option == "option1":
        await query.answer(text="Enter/change keywords")
        await keywords_command(user_id)
    elif option == "option2":
        with open(f"{constants.PATH}/{user_id}.txt") as file:
            lines = file.readlines()
            status = "disabled" if lines[3].strip() == "enabled" else "enabled"
            await query.answer(text=status)
        set_enable_disable(user_id)
    elif option == "option3":
        await query.answer(text="Set time")
    elif option == "option4":
        await query.answer(text="Enter keyword to find news now")
        app.add_handler(MessageHandler(filters.TEXT, handle_message))


# app body
if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler(constants.COMMANDS[0], start_command))
    app.add_handler(CommandHandler(constants.COMMANDS[1], menu_command_f))
    app.add_handler(CallbackQueryHandler(button_click))
    print("Polling ...")
    app.run_polling(3)
