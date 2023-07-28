from telegram import Update

from classes_folder.news_channel import NewsChannel
from constants.general_constants import BODY, ENTER_CHANNELS
from database.database import get_users_col


async def adding_channels(update: Update, ctx):
    user_id = update.message.chat.id
    users_col = get_users_col()
    user = users_col.find_one({"id": user_id})
    text = update.message.text.strip().split()
    channel_list = []
    incorrect = []
    for item in text:
        if item[0] == "@":
            link = item
            news_channel = NewsChannel(link).to_dict()
            channel_list.append(news_channel)
        else:
            incorrect.append(item)

    if len(incorrect) != 0:
        await update.message.reply_text(f"Incorrectly entered channels: {incorrect}\n"
                                        f"Correct mistakes and reenter all the channels again.")
        return ENTER_CHANNELS
    else:
        user["channels"] = channel_list
        users_col.update_one({"id": user_id}, {"$set": {"channels": user["channels"]}})
        await update.message.reply_text("Your channels has been successfully updated.")
        return BODY


def get_current_channel_list(user_id):
    users_col = get_users_col()
    user = users_col.find_one({"id": user_id})
    old_channels = user["channels"]
    channel_string = "You've got no channel stored."
    if len(old_channels) > 0:
        channel_string = ""
        for channel in old_channels:
            link_2 = channel.get("link_2", "")
            channel_string += link_2 + " "
        channel_string = channel_string.strip()
    return channel_string
