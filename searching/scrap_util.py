from datetime import datetime, timedelta

from constants.data_constants import DATETIME, D_TIME, TO_BE_REPLACED, TO_BE_INSERTED
from utils.time_functions import convert_to_millis


SPACE = " "
TRIANGLE = f"{SPACE}{SPACE}{SPACE}🔺{SPACE}{SPACE}{SPACE}"


def heading_making(word, amount):
    return f"{SPACE}\n{SPACE}{word} : {amount}{SPACE}\n{SPACE}"


def get_time(section):
    article_time = section.find(DATETIME, class_=DATETIME)[D_TIME]
    return convert_to_millis(article_time)


def handle_punctuation(word_list):
    punctuation = r"""!"#$%&'()*+, -./:;<=>?@[\]^`{|}~"""
    invalid_word = None
    for item in word_list:
        if any(char in punctuation for char in item):
            invalid_word = item
            break
    if invalid_word is not None:
        return [f"Prohibited punctuation in '{invalid_word}'. Try again."]
    else:
        return word_list


def br_removing(br_soup):
    for br in br_soup.find_all(TO_BE_REPLACED):
        br.replace_with(TO_BE_INSERTED)
    return br_soup


def within_period(millis):
    now = datetime.now()
    one_day = now - timedelta(hours=12)
    milli_time = datetime.fromtimestamp(millis / 1000)
    if one_day <= milli_time <= now:
        return True
    else:
        return False
