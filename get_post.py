import requests
from bs4 import BeautifulSoup

import constants


def get_retrieved(word):
    return_text = ""
    # CHANNELS list consists of one news channel lists as
    # ["Channel name", "https://t.me/s/telegram_address", "@telegram_address"]
    for channel in constants.CHANNELS:
        response = requests.get(channel[1])
        # Parsing the HTML content using BeautifulSoup
        if response.status_code == 200:
            # Parsing the HTML content
            soup = BeautifulSoup(response.content, "html.parser")
            # Find all the posts on the page
            posts = soup.find_all("div", class_="tgme_widget_message_text")
            # Iterate over each post and check if it contains some specific word
            for post in posts:
                post_text = post.text
                if word in post_text.lower():
                    return_text += f"{channel[0]}\n{post_text.strip()}\n{channel[2]}\n\n"
        else:
            return_text = "Failed to retrieve the page"
    return return_text
