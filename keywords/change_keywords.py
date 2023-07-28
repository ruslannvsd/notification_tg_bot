from constants.general_constants import BODY
from database.chg_kw import change_kw
from searching.handling_messages import handle_punctuation


def change_keywords(user_id, keywords_list):
    change_kw(user_id, keywords_list)
    message = f"You subscribed for {keywords_list}."
    # if status == "disabled":
    #     message += "\nYou need to Enable the subscription to receive news."
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
