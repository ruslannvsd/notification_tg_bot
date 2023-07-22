import time

from constants.data_constants import KEYWORDS, USER_ID
from searching.handling_messages import auto_text
from utils.time_functions import convert_to_readable_time


def auto_news(bot):
    while True:
        now = time.time()
        print(convert_to_readable_time(now*1000))
        time.sleep(10)
        for word in KEYWORDS:
            auto_message = auto_text(word)
            for message in auto_message[0]:
                bot.send_message(chat_id=USER_ID, text=message)
            bot.send_message(chat_id=USER_ID, text=auto_message[1])
