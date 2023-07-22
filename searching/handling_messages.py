from telegram import Update
from telegram.ext import ContextTypes

from searching import get_retrieved
from utils import time_functions
from constants.data_constants import reply_text, nothing_found


def handle_punctuation(text):
    punctuation = r"""!"#$%&'()*+, -./:;<=>?@[\]^`{|}~"""
    for item in punctuation:
        if item in text:
            return f"Prohibited punctuation {item} was used. Try again."
    return text


def handle_checking_news(word: str):
    news = get_retrieved.get_retrieved(word)
    if news is False:
        return False
    else:
        return news


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # getting message type
    message_type = update.message.chat.type
    # getting words a user entered
    text = update.message.text
    checked_text = handle_punctuation(text)
    if checked_text == text:
        # internal registration of the time a user made an entry
        date = update.message.date
        print(f"User {update.message.chat.id} in {message_type} : {text} (date: {date})")
        # checking if words are contained in latest news
        response = []
        amount = 0
        if handle_checking_news(text.lower()) is not False:
            response = handle_checking_news(text.lower())
            amount = len(response)
            for item in response:
                time_ = time_functions.convert_to_readable_time(item.article_time)
                article = f"{item.news_channel.channel_name}" \
                          f"\n{item.article_link}\n{time_}\n\n{item.article}"
                await update.message.reply_text(article)
        else:
            await update.message.reply_text(nothing_found(text))
        await update.message.reply_text(reply_text(text, amount, response))
        print("Processing completed")
    else:
        await update.message.reply_text(str(checked_text))


def auto_text(text):
    response = []
    articles = []
    amount = 0
    if handle_checking_news(text.lower()) is not False:
        response = handle_checking_news(text.lower())
        amount = len(response)
        for item in response:
            time_ = time_functions.convert_to_readable_time(item.article_time)
            article = f"{item.news_channel.channel_name}" \
                      f"\n{item.article_link}\n{time_}\n\n{item.article}"
            articles.append(article)
    else:
        articles.append(nothing_found(text))
    final_message = reply_text(text, amount, response)
    print("Processing completed")
    return articles, final_message
