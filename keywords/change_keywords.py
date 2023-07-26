from classes_folder.user import User
from constants.general_constants import PATH, BODY
from searching.handling_messages import handle_punctuation
from utils.file_functions import user_data_ordered


def change_keywords(user_id, keywords_list):
    with open(f"{PATH}/{user_id}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        keywords = list_to_string(keywords_list)
        time_period = lines[0].strip()
        status = lines[2].strip()
        print(f"{user_id} {lines}\n{time_period} {keywords} {status}")
        with open(f"{PATH}/{user_id}.txt", "w", encoding="utf-8") as f:
            user = User(user_id, keywords, time_period, status)
            f.write(user_data_ordered(user))
        message = f"You subscribed for {keywords}."
        if status == "disabled":
            message += "\nYou need to Enable the subscription to receive news."
    return message


def list_to_string(words):
    string = ""
    for word in words:
        string += word + " "
    return string.strip()


def keywords_command(user_id):
    with open(f"{PATH}/{user_id}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        keywords_line = lines[1].strip() if lines[1] != [] else []
        print(keywords_line)
        status_line = lines[2].strip()
        if status_line == "disabled":
            status = "disabled"
        else:
            status = "enabled"
        message = f"Status of subscription: {status}\n"
        if not keywords_line:
            message += f"You've got no keywords.\n" \
                       f"Enter words you want to monitor news with:"
            return message
        else:
            message += f"You've got keywords: {keywords_line}\n" \
                       f"If you enter new keywords, old ones will be overwritten:"
            return message


async def saving_keywords(update, ctx):
    keywords = update.message.text.strip().split(" ")
    checked_keywords = []
    for word in keywords:
        checked_word = handle_punctuation(word)
        checked_keywords.append(checked_word)
    message = change_keywords(update.message.chat.id, keywords)
    await update.message.reply_text(message)
    return BODY
