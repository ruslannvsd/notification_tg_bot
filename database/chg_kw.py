from constants.general_constants import BODY
from database.database import get_users_col


def change_kw(user_id, keywords):
    users_col = get_users_col()
    user = users_col.find_one({"id": user_id})
    user["keywords"] = keywords
    users_col.update_one({"id": user_id}, {"$set": {"keywords": user["keywords"]}})
    return BODY
