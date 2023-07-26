import os

from constants.general_constants import PATH, BODY, keyboard
from utils.message_functions import user_data_ordered


def create_txt_file(user):
    path = fr"{PATH}/{user.user_id}.txt"
    user_data = user_data_ordered(user)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            print(user_data)
            f.write(user_data)
