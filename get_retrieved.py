import requests
from bs4 import BeautifulSoup

from classes import Article
from constants import channels
from time_functions import convert_to_millis


def article_making(div_text, bubble, channel):
    text = div_text.text
    link = bubble.find('a', class_='tgme_widget_message_date')['href']
    time = bubble.find('time', class_='time')['datetime']
    time_in_millis = convert_to_millis(time)
    return Article(channel, text, time_in_millis, link)


def get_retrieved(word):
    article_list = []
    word_list = []
    if '_' in word:
        word_list = word.split("_")
    for channel in channels:
        response = requests.get(channel.channel_link_1)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for br in soup.find_all("br"):
                br.replace_with("\n")
            message_bubbles = soup.find_all('div', class_='tgme_widget_message_bubble')
            for bubble in message_bubbles:
                div_text = bubble.find('div', class_='tgme_widget_message_text')
                if len(word_list) != 0:
                    if div_text is not None and word_list[0] in div_text.text.lower() and word_list[1] in div_text.text.lower():
                        article = article_making(div_text, bubble, channel)
                        article_list.append(article)
                else:
                    if div_text is not None and word in div_text.text.lower():
                        article = article_making(div_text, bubble, channel)
                        article_list.append(article)
        else:
            return False
    if not article_list:
        return False
    else:
        return sorted(article_list, key=lambda x: x.article_time)
