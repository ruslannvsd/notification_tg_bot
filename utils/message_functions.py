import collections
import time

from classes_folder.article import Article
from utils import time_functions
from utils.time_functions import convert_to_readable_time


def article_msg(article: Article):
    article_time = convert_to_readable_time(article.article_time)
    return f"{article.channel_name}\n{article_time}\n\n{article.article}\n\n{article.article_link}"


def reply_text(text, amount, response):
    return f"Keyword: {text}\n{amount} article(s).\nThat's all I've found for now.\n{post_frequency(response)}"


def nothing_found(text):
    return f"No news with {text} found."


def counter_text(article):
    name = article.news_channel.channel_link_2
    return f"{name[1:]} " \
           f"{time_functions.convert_to_readable_time(article.news_channel.id)}\n" \
           f"{article.news_channel.channel_link_2}"


def frequency_of_class_instances(article_list):
    counter = collections.Counter()
    for article in article_list:
        counter[counter_text(article)] += 1
    return counter.most_common()


def post_frequency(article_list):
    string = ""
    articles_counted = frequency_of_class_instances(article_list)
    for item in articles_counted:
        string += f"\n\n{item[0]} : {item[1]}"
    return string


def detect_time_of_day():
    current_time = time.time()
    seconds_since_midnight = current_time % 86400
    hours_since_midnight = seconds_since_midnight // 3600
    if hours_since_midnight == 22:
        return True
    else:
        return False
