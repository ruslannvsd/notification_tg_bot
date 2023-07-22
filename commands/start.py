import os

from telegram import Update
from telegram.ext import ContextTypes

from classes_folder.user import User
from constants import constants


def create_txt_file(user):
    if not os.path.exists(f"{constants.PATH}/{user.user_id}.txt"):
        with open(f"{constants.PATH}/{user.user_id}.txt", "r") as f:
            f.write(f"{user.time_period}\n{user.keywords}\n{user.enable_disable}")


# commands
async def start_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    user = User(user_id, "", 0, "disabled")
    create_txt_file(user)
    await update.message.reply_text(constants.WELCOME_MESSAGE)
