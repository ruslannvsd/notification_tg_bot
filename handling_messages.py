from telegram import Update
from telegram.ext import ContextTypes

import get_retrieved
import time_functions
from news_channel_frequency import post_frequency


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
    text = update.message.text.split("*")
    # internal registration of the time a user made an entry
    date = update.message.date
    print(f"User {update.message.chat.id} in {message_type} : {text} (date: {date})")
    # checking if words are contained in latest news
    for txt in text:
        response = []
        amount = 0
        if handle_checking_news(txt.lower()) is not False:
            response = handle_checking_news(txt.lower())
            amount = len(response)
            for item in response:
                time_ = time_functions.convert_to_readable_time(item.article_time)
                article = f"{item.news_channel.channel_name}" \
                          f"\n{item.article_link}\n{time_}\n\n{item.article}"
                await update.message.reply_text(article)
        else:
            await update.message.reply_text(f"No news with {txt} found.")
        await update.message.reply_text(f"Keyword: {txt}\n{amount} article(s)."
                                        f"\nThat's all I've found for now."
                                        f"\n{post_frequency(response)}")
    print("Processing completed")
