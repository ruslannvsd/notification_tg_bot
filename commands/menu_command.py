from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from constants import constants


def menu_f(user_id):
    with open(f"{constants.PATH}/{user_id}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        status = "Disable" if lines[2].strip() == "enabled" else "Enable"
        menu_items = [
            [InlineKeyboardButton("Enter/change keywords", callback_data='option1')],
            [InlineKeyboardButton(status, callback_data='option2')],
            [InlineKeyboardButton("Set time", callback_data='option3')],
            [InlineKeyboardButton("Find now", callback_data='option4')]
        ]
    return InlineKeyboardMarkup(menu_items)


async def menu_command_f(update, ctx):
    await update.message.reply_text("Menu:", reply_markup=menu_f(update.message.chat.id))
