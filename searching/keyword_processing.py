import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ContextTypes

from classes_folder.article import NewArticle
from constants.data_constants import TO_BE_REPLACED, TO_BE_INSERTED, MESSAGE_DIV, TEXT_DIV, SECTION, LINK, DATETIME, \
    D_TIME
from database.database import get_all_users
from database.getting import get_user
from utils.message_functions import article_msg
from utils.time_functions import convert_to_millis


def get_time(section):
    time = section.find(DATETIME, class_=DATETIME)[D_TIME]
    return convert_to_millis(time)


def handle_punctuation(word_list):
    punctuation = r"""!"#$%&'()*+, -./:;<=>?@[\]^`{|}~"""
    invalid_word = None
    for item in word_list:
        if any(char in punctuation for char in item):
            invalid_word = item
            break
    if invalid_word is not None:
        return [f"Prohibited punctuation in '{invalid_word}'. Try again."]
    else:
        return word_list


async def find_kw_periodically(ctx: ContextTypes.DEFAULT_TYPE):
    users = get_all_users()
    for user in users:
        user_id = user.user_id
        word_list = user.keywords
        print(f"{user_id} has {word_list}.")
        articles = finding(word_list, user_id)
        if articles:
            for article in articles:
                article_reply = article_msg(article)
                await ctx.bot.send_message(chat_id=user.user_id, text=article_reply)
        print(f"Search for {user_id} has been completed")


async def find_keyword_now(update: Update, ctx):
    user_id = update.message.chat.id
    word_list = update.message.text.strip().split()
    date = update.message.date
    print(f"User {user_id} : {word_list} (date: {date})")
    articles = finding(word_list, user_id)
    for article in articles:
        article_reply = article_msg(article)
        await update.message.reply_text(article_reply)


def finding(word_list, user_id):
    user = get_user(user_id)
    keywords = word_list if word_list else user["keywords"]
    print(keywords)
    channels = get_user(user_id)["channels"]
    checked_words = handle_punctuation(keywords)
    if checked_words == keywords:
        return word_news(keywords, channels)
    else:
        return str(checked_words)


def word_news(words, channels):
    for word in words:
        return check_chs_for_news(word.lower(), channels)


def br_removing(br_soup):
    for br in br_soup.find_all(TO_BE_REPLACED):
        br.replace_with(TO_BE_INSERTED)
    return br_soup


def check_chs_for_news(word, channels):
    article_list = []
    for chn in channels:
        chn_link = chn["link_1"]
        response = requests.get(chn_link)
        if response.status_code == 200:
            soup = br_removing(BeautifulSoup(response.content, 'html.parser'))
            message_sections = soup.find_all('div', class_=MESSAGE_DIV)
            for section in message_sections:
                article_body = section.find('div', class_=TEXT_DIV)
                if article_body is not None:
                    article_body_lower = article_body.text.lower()
                    if word in article_body_lower:
                        link = section.find('a', class_=SECTION)[LINK]
                        milli_time = get_time(section)
                        chn_name = chn["name"]
                        article = NewArticle(chn_name, article_body.text, milli_time, link)
                        article_list.append(article)
        else:
            return False
    if not article_list:
        return False
    else:
        return sorted(article_list, key=lambda x: x.article_time)
