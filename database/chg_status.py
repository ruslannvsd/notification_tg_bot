from telegram import Update

from constants.general_constants import BODY, STATUS_COMMANDS, keyboard
from database.checking import check_user_if_exists
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
    kb_status = STATUS_COMMANDS[0] if not check_user_if_exists(user_id) else STATUS_COMMANDS[1]
    kb = keyboard(kb_status)
    await update.message.reply_text(f"Your subscription is {new_status}.", reply_markup=kb)
    return BODY
