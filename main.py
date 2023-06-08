import time

import requests
import os

from datetime import datetime
from dotenv import load_dotenv


def long_polling(token, timestamp):
    url = 'https://dvmn.org/api/long_polling/'
    last_attempt_timestamp = timestamp
    headers = {
        'Authorization': token,
    }
    while True:
        payload = {
            'last_attempt_timestamp': last_attempt_timestamp,
        }
        try:
            response = requests.get(url, headers=headers, timeout=5, params=payload)
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
    dvmn_token = os.getenv('DVMN_TOKEN', default='DEMO_KEY')
    timestamp = datetime.timestamp(datetime.now())
    long_polling(dvmn_token, f'{int(timestamp)}')


if __name__ == '__main__':
    main()
