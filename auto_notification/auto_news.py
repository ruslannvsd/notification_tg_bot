import time

from telegram.ext import ContextTypes

from classes_folder.user import User
from constants.general_constants import PATH
from database.database import get_all_users
from searching.handling_messages import auto_text
from utils.file_functions import files_list
from utils.time_functions import convert_to_readable_time


async def auto_searching(context: ContextTypes.DEFAULT_TYPE):
    users = get_all_users()
    for user in users:
        print(f"run_tasks works for {user.user_id}")
        now = time.time()
        print(convert_to_readable_time(now * 1000))
        if user.keywords:
            for word in user.keywords:
                auto_message = auto_text(user.user_id, word)
                for message in auto_message:
                    await context.bot.send_message(chat_id=user.user_id, text=message)
                # await context.bot.send_message(chat_id=user.user_id, text=auto_message[1])
        else:
            await context.bot.send_message(chat_id=user.user_id, text="You've got no keywords.")


def all_users():
    # list of files where names of them are user_ids+.txt
    files = files_list()
    # getting info of users from file
    # empty list of users
    users = []
    for file_name in files:
        # get rid of ".txt"
        user_id = file_name[:-4].strip()
        with open(f"{PATH}/{file_name}", "r", encoding="utf-8") as file:
            # read lines of the file of the selected user
            lines = file.readlines()
            # making the user from lines
            user = User(user_id,
                        str(lines[1]).strip(),
                        int(lines[0].strip())*3600,
                        str(lines[2].strip()),
                        user.channels
                        )
            # adding the user to the list
            users.append(user)
    # saying bye to the fun and going right there from where we come
    return users
