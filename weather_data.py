import requests


def weather_data(lat, lon):
    access_key = '251f5b1c-ba22-4437-a2fe-86a9428986fe'

    headers = {
        'X-Yandex-Weather-Key': access_key
    }

    response = requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}', headers=headers)