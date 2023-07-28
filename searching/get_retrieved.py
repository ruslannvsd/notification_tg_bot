import requests
from bs4 import BeautifulSoup

from classes_folder.article import Article
from constants.data_constants import MESSAGE_DIV, TEXT_DIV, DIVIDER, TO_BE_REPLACED, TO_BE_INSERTED, SECTION, DATETIME, D_TIME, \
    LINK
from database.chg_channels import get_current_channel_list
from utils.time_functions import convert_to_millis


def get_time(section):
    time = section.find(DATETIME, class_=DATETIME)[D_TIME]
    return convert_to_millis(time)


def article_making(div_text, section, channel):
    text = div_text.text
    link = section.find('a', class_=SECTION)[LINK]
    time_in_millis = get_time(section)
    return Article(channel[1:], text, time_in_millis, link)


def get_retrieved(user_id, word):
    print(user_id)
    article_list = []
    word_list = []
    if DIVIDER in word:
        word_list = word.split(DIVIDER)
    current_chn_list = get_current_channel_list(user_id).split(" ")
    for channel in current_chn_list:
        check = True
        web_link = "https://t.me/s/" + channel[1:]
        response = requests.get(web_link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for br in soup.find_all(TO_BE_REPLACED):
                br.replace_with(TO_BE_INSERTED)
            message_sections = soup.find_all('div', class_=MESSAGE_DIV)
            both_words_present = len(word_list) == 2 and all(word in word_list for word in word_list)
            for section in message_sections:
                div_text = section.find('div', class_=TEXT_DIV)
                if div_text is not None and check is True:
                    # first_article_time = get_time(section)
                    # channel.id = first_article_time
                    check = False
                if div_text is not None:
                    text_lower = div_text.text.lower()
                    if (both_words_present and all(word in text_lower for word in word_list)) or \
                            (not both_words_present and word in text_lower):
                        article = article_making(div_text, section, channel)
                        article_list.append(article)
        else:
            return False
    if not article_list:
        return False
    else:
        return sorted(article_list, key=lambda x: x.article_time)
