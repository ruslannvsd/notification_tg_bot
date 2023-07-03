import requests
from bs4 import BeautifulSoup

import constants
from classes import Article
from time_functions import convert_to_millis


def get_retrieved(word):
    article_list = []
    for channel in constants.channels:
        response = requests.get(channel.channel_link_1)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            message_bubbles = soup.find_all('div', class_='tgme_widget_message_bubble')
            for bubble in message_bubbles:
                if word in bubble.text.lower():
                    text = bubble.find('div', class_='tgme_widget_message_text').text()
                    link = bubble.find('a', class_='tgme_widget_message_date')['href']
                    time = bubble.find('time', class_='time')['datetime']
                    time_in_millis = convert_to_millis(time)
                    article = Article(channel, text, time_in_millis, link)
                    article_list.append(article)
        else:
            return False
    return sorted(article_list, key=lambda x: x.article_time)

