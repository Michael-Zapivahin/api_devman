
import requests





def main():
    payload = {
        'api_key': nasa_token,
        'date': apod_day
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    




if __name__ == '__main__':
    main()