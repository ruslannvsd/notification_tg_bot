from constants.general_constants import BODY, keyboard
from database.database import get_users_col


async def set_time(update, ctx):
    user_id = update.message.chat.id
    time = update.message.text
    users_col = get_users_col()
    user = users_col.find_one({"id": user_id})
    user["period"] = time
    users_col.update_one({"id": user_id}, {"$set": {"period": user["period"]}})
    message = f"You've just updated news checking time period: {time}"
    await update.message.reply_text(message, reply_markup=keyboard)
    return BODY
