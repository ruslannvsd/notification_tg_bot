from classes_folder.user import User
from constants.general_constants import PATH, BODY
from utils.file_functions import user_data_ordered


async def set_enable_disable(update, ctx) -> int:
    # getting user_id
    user_id = update.message.chat.id
    # great to have txt-file name as user_id + .txt
    with open(f"{PATH}/{user_id}.txt", "r", encoding="utf-8") as file:
        # let's get lines of the file for further processing
        lines = file.readlines()
        # processing
        time_period = lines[0].strip()
        # since it's set_enable_disable we here change the user's status into opposite
        new_status = "disabled" if lines[2].strip() == "enabled" else "enabled"
        # just for the rewriting
        keywords = lines[1].strip()
        print(new_status)
        with open(f"{PATH}/{user_id}.txt", "w", encoding="utf-8") as f:
            # user with new status
            user = User(user_id, keywords, time_period, new_status)
            # above-mentioned rewriting
            f.write(user_data_ordered(user))
            # notifying the user of what has been done
            await update.message.reply_text(f"Your subscription is {new_status}")
    # bye to the fun
    return BODY

