from datetime import datetime

import requests
from bs4 import BeautifulSoup

import constants


def get_retrieved(word):
    return_list = [f"{str(word).upper()}:\n\n"]
    for channel in constants.CHANNELS:
        response = requests.get(channel[1])
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            message_bubbles = soup.find_all('div', class_='tgme_widget_message_bubble')
            for bubble in message_bubbles:
                if word in bubble.text.lower():
                    text = bubble.find('div', class_='tgme_widget_message_text').text
                    link = bubble.find('a', class_='tgme_widget_message_date')['href']
                    time = bubble.find('time', class_='time')['datetime']
                    date_time = datetime.fromisoformat(time)
                    formatted_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
                    text_to_add = f"{channel[0]}\n{link}\n{formatted_time}\n\n{text}\n{channel[2]}\n\n"
                    return_list.append(text_to_add)
        else:
            return_list = ["Failed to retrieve the page"]
    return return_list
