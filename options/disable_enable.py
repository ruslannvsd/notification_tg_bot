from classes_folder.user import User
from constants.general_constants import PATH, BODY
from utils.message_functions import user_data_ordered


async def set_enable_disable(update, ctx) -> int:
    user_id = update.message.chat.id
    with open(f"{PATH}/{user_id}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        time_period = lines[0].strip()
        new_status = "disabled" if lines[2].strip() == "enabled" else "enabled"
        keywords = lines[1].strip()
        print(new_status)
        with open(f"{PATH}/{user_id}.txt", "w", encoding="utf-8") as f:
            user = User(user_id, keywords, time_period, new_status)
            f.write(user_data_ordered(user))
            await update.message.reply_text(f"Your subscription is {new_status}")
    return BODY

