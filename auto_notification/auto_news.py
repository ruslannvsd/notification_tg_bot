import time

from telegram.ext import ContextTypes

from classes_folder.user import User
from constants.general_constants import PATH
from searching.handling_messages import auto_text
from utils.file_functions import files_list
from utils.time_functions import convert_to_readable_time


async def auto_searching(context: ContextTypes.DEFAULT_TYPE):
    users = all_users()
    for user in users:
        user_id = user.user_id
        if user.enable_disable == "enabled":
            print(f"run_tasks works for {user.user_id}")
            now = time.time()
            print(convert_to_readable_time(now * 1000))
            words = user.keywords.split()
            for word in words:
                auto_message = auto_text(word)
                for message in auto_message[0]:
                    await context.bot.send_message(chat_id=user_id, text=message)
                await context.bot.send_message(chat_id=user_id, text=auto_message[1])


def all_users():
    files = files_list()
    users = []
    for file_name in files:
        user_id = file_name[:-4].strip()
        with open(f"{PATH}/{file_name}", "r", encoding="utf-8") as file:
            lines = file.readlines()
            user = User(user_id, str(lines[1]).strip(), int(lines[0].strip())*3600, str(lines[2].strip()))
            users.append(user)
    return users
