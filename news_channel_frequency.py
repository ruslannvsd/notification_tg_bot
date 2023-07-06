import collections

import time_functions


def frequency_of_class_instances(article_list):
    counter = collections.Counter()
    for article in article_list:
        counter[f"{article.news_channel.channel_name} / "
                f"{time_functions.convert_to_readable_time(article.news_channel.id)}\n"
                f"{article.news_channel.channel_link_2}"] += 1
    return counter.most_common()


def post_frequency(article_list):
    string = ""
    articles_counted = frequency_of_class_instances(article_list)
    for item in articles_counted:
        string += f"\n\n{item[0]} : {item[1]}"
    return string
