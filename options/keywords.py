from constants import constants
from options.change_keywords import change_keywords


def keywords_command(user_id):
    with open(f"{constants.PATH}/{user_id}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        #         status = "Disable" if lines[1].strip() == "enabled" else "Enable"
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
                       f"Enter words you want to monitor:"
            return message
        else:
            message += f"You've got keywords: {keywords_line}\n" \
                       f"Notifications are {status_line}"
            return message


async def enter_keywords(update, ctx):
    keywords = update.message.text.strip().split(" ")
    # checked_keywords = []
    # for word in keywords:
    # checked_word = handle_punctuation(word)
    # checked_keywords.append(checked_word)
    message = change_keywords(update.message.chat.id, keywords)
    await update.message.reply_text(message)
