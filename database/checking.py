from classes_folder.user import User
from database.getting import get_user
from database.inserting import insert_user


def check_user_if_exists(user_id):
    user_dict = get_user(user_id)
    if user_dict is None:
        user = User(user_id, [], 0, False, []).to_dict()
        insert_user(user)
    user = User.from_dict(user_dict)
    return user.status

