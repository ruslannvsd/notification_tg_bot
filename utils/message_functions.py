import collections

from utils import time_functions


def reply_text(text, amount, response):
    return f"Keyword: {text}\n{amount} article(s).\nThat's all I've found for now.\n{post_frequency(response)}"


def nothing_found(text):
    return f"No news with {text} found."


def counter_text(article):
    return f"{article.news_channel.channel_name} " \
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


def user_data_ordered(user):
    return f"{user.time_period}\n{user.keywords}\n{user.enable_disable}"
