import json

import requests


def weather_api(lat, lon):
    access_key = '251f5b1c-ba22-4437-a2fe-86a9428986fe'

    headers = {
        'X-Yandex-Weather-Key': access_key
    }

    response = requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}', headers=headers)
    return response.json()


print(weather_api(55.7522, 37.6156)['fact']['temp'])