import os

from constants.general_constants import PATH


def create_txt_file(user):
    path = fr"{PATH}/{user.user_id}.txt"
    user_data = user_data_ordered(user)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            print(user_data)
            f.write(user_data)


def files_list():
    raw_files = os.listdir(PATH)
    return raw_files


def user_data_ordered(user):
    return f"{user.time_period}\n{user.keywords}\n{user.enable_disable}"
