from classes_folder.user import User
from constants.general_constants import PATH, BODY, keyboard
from utils.message_functions import user_data_ordered


async def set_time(update, ctx):
    user_id = update.message.chat.id
    time = update.message.text
    with open(f"{PATH}/{user_id}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        keywords = lines[1].strip()
        status = lines[2].strip()
        print(f"{user_id} {lines}\n{keywords} {time} {status}")
        file.close()
        with open(f"{PATH}/{user_id}.txt", "w", encoding="utf-8") as f:
            user = User(user_id, keywords, time, status)
            f.write(user_data_ordered(user))
            f.close()
        message = f"You've updated time: {time}."
        if status == "disabled":
            message += "\nYou need to Enable the subscription to receive news."
    await update.message.reply_text(message, reply_markup=keyboard)
    return BODY
