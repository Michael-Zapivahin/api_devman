
import requests
import os

from datetime import datetime
from dotenv import load_dotenv


def long_Polling(token, timestamp=datetime.timestamp()):
    # {'request_query': [], 'status': 'found', 'new_attempts': [
    #     {'submitted_at': '2023-06-07T16:41:35.237081+03:00', 'timestamp': 1686145295.237081, 'is_negative': True,
    #      'lesson_title': 'Делаем игру про космос',
    #      'lesson_url': 'https://dvmn.org/modules/async-python/lesson/async-console-game/'}],
    #  'last_attempt_timestamp': 1686145295.237081}

    # timestamp = datetime.timestamp()
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': token,
        'timestamp': timestamp,
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ReadTimeout as timeout:
        return {'timeout': timeout, 'timestamp': timestamp}
    except requests.exceptions.HTTPError as http_error:
        return http_error
    except requests.exceptions.ConnectionError as connection_error:
        return connection_error

    response.raise_for_status()
    return response.json()





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
    # print(my_works(dvmn_token))
    while True:
        response = long_Polling(dvmn_token)


if __name__ == '__main__':
    main()