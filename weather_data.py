import json

import requests


def weather_api(lat, lon):
    access_key = '28e958ab-e685-424f-bdf8-3d1c5a2536d1'

    headers = {
        'X-Yandex-Weather-Key': access_key
    }

    response = requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&lang=ru_RU', headers=headers)
    return response.json()


print(weather_api(55.7522, 37.6156)['fact']['temp'])