import re

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ContextTypes

from classes_folder.article import Article
from constants.data_constants import MESSAGE_DIV, TEXT_DIV, SECTION, LINK
from constants.general_constants import BODY
from database.database import get_all_users, get_one_user, get_users_col
from searching.scrap_util import br_removing, get_time, within_period, handle_punctuation, heading_making, TRIANGLE
from utils.message_functions import article_msg


async def now_scraping(update: Update, ctx):
    user_id = update.message.chat.id
    word_list = update.message.text.strip().split()
    date = update.message.date
    print(f"User {user_id} : {word_list} (date: {date})")
    checked_words = handle_punctuation(word_list)
    if checked_words == word_list:
        user_data = get_users_col().find_one({"id": user_id})
        user = get_one_user(user_data)
        articles_dict = get_articles_list(user, word_list)
        if articles_dict:
            mess_id_list = []
            for word, articles in articles_dict.items():
                heading = heading_making(word, len(articles))
                key_message = await update.message.reply_text(text=heading)
                message_id = key_message.message_id
                mess_id_list.append(message_id)
                articles.sort(key=lambda ar: ar.article_time)
                for art in articles:
                    article_reply = article_msg(art)
                    await update.message.reply_text(article_reply)
            for mess_id in mess_id_list:
                await update.message.reply_text(
                    text=TRIANGLE,
                    reply_to_message_id=mess_id
                )
        else:
            await update.message.reply_text("Nothing has been found.")
        print("Searching has been completed.")
        return BODY
    else:
        await update.message.reply_text(checked_words)
        return BODY


async def repeating_scraping(ctx: ContextTypes.DEFAULT_TYPE):
    users = get_all_users()
    for user in users:
        user_id = user.user_id
        status = user.status
        if status is True:
            print(status)
            word_list = user.keywords
            print(word_list)
            articles_dict = get_articles_list(user, word_list)
            if articles_dict:
                mess_id_list = []
                for word, articles in articles_dict.items():
                    heading = heading_making(word, len(articles))
                    key_message = await ctx.bot.send_message(chat_id=user_id, text=heading)
                    message_id = key_message.message_id
                    mess_id_list.append(message_id)
                    articles.sort(key=lambda ar: ar.article_time)
                    for art in articles:
                        article_reply = article_msg(art)
                        await ctx.bot.send_message(chat_id=user_id, text=article_reply)
                for mess_id in mess_id_list:
                    await ctx.bot.send_message(
                        chat_id=user_id,
                        text=TRIANGLE,
                        reply_to_message_id=mess_id
                    )
    return BODY


def get_articles_list(user, word_list):
    articles_dict = {word: [] for word in word_list}
    channels = user.channels
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
                    for word in word_list:
                        if "_" not in word:
                            if re.search(word.lower(), article_body_lower):
                                milli_time = get_time(section)
                                if within_period(milli_time):
                                    link = section.find('a', class_=SECTION)[LINK]
                                    chn_name = chn["link_2"]
                                    article = Article(chn_name, article_body.text, milli_time, link)
                                    articles_dict[word].append(article)
                        else:
                            phrase = word.lower().split("_")
                            if phrase[0] in article_body_lower and phrase[1] in article_body_lower:
                                milli_time = get_time(section)
                                if within_period(milli_time):
                                    link = section.find('a', class_=SECTION)[LINK]
                                    chn_name = chn["link_2"]
                                    article = Article(chn_name, article_body.text, milli_time, link)
                                    articles_dict[word].append(article)
    articles_dict = {word: articles_list for word, articles_list in articles_dict.items() if articles_list}
    articles_dict_sorted = dict(sorted(articles_dict.items(), key=lambda item: len(item[1]), reverse=True))
    return articles_dict_sorted
