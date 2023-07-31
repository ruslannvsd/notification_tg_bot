import time

from telegram import Update
from telegram.ext import ContextTypes

from constants.general_constants import BODY
from searching import get_retrieved
from utils import time_functions
from utils.message_functions import nothing_found, reply_text


def handle_punctuation(text):
    punctuation = r"""!"#$%&'()*+, -./:;<=>?@[\]^`{|}~"""
    for item in punctuation:
        if item in text:
            return f"Prohibited punctuation {item} was used. Try again."
    return text
