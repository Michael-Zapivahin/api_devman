import time

import requests
import os
import telebot

from datetime import datetime
from dotenv import load_dotenv


def send_message(bot_token, chat_id, message):
    if not message['is_negative']:
        message_text = 'Your work completed successfully.'
    else:
        message_text = 'The tutor returned your work for revision.'
    message_text += f' link to work {message["lesson_url"]}'
    bot = telebot.TeleBot(bot_token)
    bot.send_message(chat_id, message_text)


def long_polling(devman_token, bot_token, chat_id):

    timestamp = datetime.timestamp(datetime.now())
    last_attempt_timestamp = f'{int(timestamp)}'

    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': devman_token,
    }
    while True:
        payload = {
            'last_attempt_timestamp': last_attempt_timestamp,
        }
        try:
            response = requests.get(url, headers=headers, timeout=60, params=payload)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.HTTPError as http_error:
            print(http_error)
            time.sleep(10)
            continue
        except requests.exceptions.ConnectionError as connection_error:
            print(connection_error)
            time.sleep(10)
            continue

        response.raise_for_status()
        works_status = response.json()
        last_attempt_timestamp = works_status['last_attempt_timestamp']
        send_message(bot_token, chat_id, works_status)


def my_works(dvmn_token):
    url = 'https://dvmn.org/api/user_reviews/'
    headers = {
        'Authorization': dvmn_token,
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    dvmn_token = os.environ['DVMN_TOKEN']
    bot_token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    long_polling(dvmn_token, bot_token, chat_id)


if __name__ == '__main__':
    main()
