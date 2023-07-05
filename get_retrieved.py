import requests
from bs4 import BeautifulSoup

from classes import Article
from constants import channels
from time_functions import convert_to_millis, convert_to_readable_time


def get_time(bubble):
    time = bubble.find('time', class_='time')['datetime']
    return convert_to_millis(time)


def article_making(div_text, bubble, channel):
    text = div_text.text
    link = bubble.find('a', class_='tgme_widget_message_date')['href']
    time_in_millis = get_time(bubble)
    return Article(channel, text, time_in_millis, link)


def get_retrieved(word):
    article_list = []
    word_list = []
    if '_' in word:
        word_list = word.split("_")
    for channel in channels:
        check = True
        response = requests.get(channel.channel_link_1)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for br in soup.find_all("br"):
                br.replace_with("\n")
            message_bubbles = soup.find_all('div', class_='tgme_widget_message_bubble')
            both_words_present = len(word_list) == 2 and all(word in word_list for word in word_list)
            for bubble in message_bubbles:
                div_text = bubble.find('div', class_='tgme_widget_message_text')
                if div_text is not None and check is True:
                    first_article_time = get_time(bubble)
                    print(channel.channel_name, convert_to_readable_time(first_article_time))
                    channel.id = first_article_time
                    check = False
                if div_text is not None:
                    text_lower = div_text.text.lower()
                    if (both_words_present and all(word in text_lower for word in word_list)) or \
                            (not both_words_present and word in text_lower):
                        article = article_making(div_text, bubble, channel)
                        article_list.append(article)
        else:
            return False
    if not article_list:
        return False
    else:
        return sorted(article_list, key=lambda x: x.article_time)
