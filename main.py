import time

import requests
import os
import telebot
import logging

from logging.handlers import RotatingFileHandler
from datetime import datetime
from dotenv import load_dotenv
from requests.exceptions import HTTPError, ConnectionError


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_message_text(message):

    lesson_url = ''
    message_text = 'The tutor returned your work for revision.'
    for attempt in message['new_attempts']:
        lesson_url = attempt['lesson_url']
        if not attempt['is_negative']:
            message_text = 'Your work completed successfully.'
            break

    message_text += f'  {lesson_url}'
    return message_text


def long_polling(devman_token, bot_token, chat_id):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    bot = telebot.TeleBot(bot_token)
    timestamp_to_request = int(datetime.timestamp(datetime.now()))

    file_handler = RotatingFileHandler('bot.log', maxBytes=200000, backupCount=2)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    telegram_handler = TelegramLogsHandler(bot, chat_id)
    telegram_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(telegram_handler)

    logger.info('The bot started.')

    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': devman_token,
    }
    while True:
        payload = {
            'timestamp_to_request': timestamp_to_request,
        }
        try:
            response = requests.get(url, headers=headers, timeout=60, params=payload)
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            continue
        except HTTPError or ConnectionError as error:
            logger.error(f'Network error: {error}')
            time.sleep(120)
            continue
        except Exception as error:
            logger.exception(f'The bot stopped with error: {error}')
            time.sleep(20)
            continue

        works_status = response.json()
        if works_status['status'] == 'found':
            timestamp_to_request = works_status['last_attempt_timestamp']
            bot.send_message(chat_id, get_message_text(works_status))


def main():
    load_dotenv()
    dvmn_token = os.environ['DVMN_TOKEN']
    bot_token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    long_polling(dvmn_token, bot_token, chat_id)


if __name__ == '__main__':
    main()
