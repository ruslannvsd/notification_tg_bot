from telegram import Update

from constants.general_constants import BODY
from database.database import get_users_col


async def change_status(update: Update, ctx):
    user_id = update.message.chat.id
    users_col = get_users_col()
    user = users_col.find_one({"id": user_id})
    status = user["status"]
    new_status = not status
    user["status"] = new_status
    users_col.update_one({"id": user_id}, {"$set": {"status": user["status"]}})
    new_status = "enabled" if new_status is True else "disabled"
    await update.message.reply_text(f"Your subscription is {new_status}.")
    return BODY
