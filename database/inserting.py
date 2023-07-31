from database.database import get_users_col


def insert_user(user_data):
    users_col = get_users_col()
    users_col.insert_one(user_data)
