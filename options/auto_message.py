import time

from constants.data_constants import KEYWORDS, USER_ID
from searching.handling_messages import auto_text
from utils.time_functions import convert_to_readable_time


def auto_news(bot, user_time_period):
    while True:
        now = time.time()
        print(convert_to_readable_time(now*1000))
        time.sleep(user_time_period[1])
        for word in KEYWORDS:
            auto_message = auto_text(word)
            for message in auto_message[0]:
                bot.send_message(chat_id=USER_ID, text=message)
            bot.send_message(chat_id=USER_ID, text=auto_message[1])


def detect_time_of_day():
    current_time = time.time()
    seconds_since_midnight = current_time % 86400
    hours_since_midnight = seconds_since_midnight // 3600
    if hours_since_midnight == 22:
        return True
    else:
        return False
