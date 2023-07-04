import collections


def frequency_of_class_instances(article_list):
    counter = collections.Counter()
    for article in article_list:
        counter[article.news_channel.channel_name] += 1
    return counter.most_common()


def post_frequency(article_list):
    string = ""
    articles_counted = frequency_of_class_instances(article_list)
    for item in articles_counted:
        string += f"\n{item[0]} - {item[1]}"
    return string
