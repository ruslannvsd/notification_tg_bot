import os

from constants.general_constants import PATH


def create_txt_file(user):
    # path for user data
    path = fr"{PATH}/{user.user_id}.txt"
    # user id received, only id filled, other user data are basic
    user_data = user_data_ordered(user)
    # if user previously hasn't used the bot the file with "user_id.txt"
    # is created filled with basic data. If the file already exists nothing happens
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            print(user_data)
            f.write(user_data)


def files_list():
    # getting the list of all the files names ({)used_id.txt) and returning the list
    raw_files = os.listdir(PATH)
    return raw_files


def user_data_ordered(user):
    return f"{user.time_period}\n{user.keywords}\n{user.enable_disable}"
