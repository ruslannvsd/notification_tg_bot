from constants.general_constants import BODY
from database.database import get_users_col
from searching.keyword_processing import handle_punctuation


async def saving_keywords(update, ctx):
    keywords = update.message.text.strip().split(" ")
    checked_keywords = []
    for word in keywords:
        checked_word = handle_punctuation(word)
        checked_keywords.append(checked_word)
    message = change_keywords(update.message.chat.id, keywords)
    await update.message.reply_text(message)
    return BODY


def change_keywords(user_id, keywords_list):
    change_kw(user_id, keywords_list)
    message = f"You subscribed for {keywords_list}."
    # if status == "disabled":
    #     message += "\nYou need to Enable the subscription to receive news."
    return message


def change_kw(user_id, keywords):
    users_col = get_users_col()
    user = users_col.find_one({"id": user_id})
    user["keywords"] = keywords
    users_col.update_one({"id": user_id}, {"$set": {"keywords": user["keywords"]}})
    return BODY
