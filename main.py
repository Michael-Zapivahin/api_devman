import time

import requests
import os
import telebot

from datetime import datetime
from dotenv import load_dotenv
from requests.exceptions import HTTPError, ConnectionError


def send_message(bot_token, chat_id, message):

    if not message['status'] == 'found':
        return

    lesson_url = ''
    message_text = 'The tutor returned your work for revision.'
    for attempt in message['new_attempts']:
        lesson_url = attempt['lesson_url']
        if not attempt['is_negative']:
            message_text = 'Your work completed successfully.'
            break

    message_text += f'  {lesson_url}'
    bot = telebot.TeleBot(bot_token)
    bot.send_message(chat_id, message_text)


def long_polling(devman_token, bot_token, chat_id):

    timestamp_to_request = int(datetime.timestamp(datetime.now()))
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
            print(error)
            time.sleep(10)
            continue

        works_status = response.json()
        if works_status['status'] == 'found':
            timestamp_to_request = works_status['last_attempt_timestamp']
            send_message(bot_token, chat_id, works_status)


def main():
    load_dotenv()
    dvmn_token = os.environ['DVMN_TOKEN']
    bot_token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    long_polling(dvmn_token, bot_token, chat_id)


if __name__ == '__main__':
    main()
