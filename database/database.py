import pymongo

from classes_folder.user import User
from constants.general_constants import HOST

client = pymongo.MongoClient(HOST)


def get_users_col():
    users_db = client["us_db"]
    users_col = users_db["users"]
    return users_col


def get_all_users():
    users_col = get_users_col()
    all_users = []
    for user_data in users_col.find():
        user = User(
            user_id=user_data["id"],
            keywords=user_data["keywords"],
            time_period=user_data["period"],
            status=user_data["status"],
            channels=user_data["channels"]
        )
        all_users.append(user)

    return all_users
