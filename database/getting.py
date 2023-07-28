from database.database import get_users_col


def get_user(user_id):
    users_col = get_users_col()
    user = users_col.find_one({"id": user_id})
    return user
