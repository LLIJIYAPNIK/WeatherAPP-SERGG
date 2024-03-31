import requests
from bs4 import BeautifulSoup



def get_current_coords(cur):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    res = requests.get(
        f'https://yandex.ru/pogoda/',
        headers=headers
    )

    soup = BeautifulSoup(res.text, 'html.parser')

    city = soup.select('#main_title')[0].getText().strip()

    current_city = str(city).split(', ')[1]

    lat, lon = cur.execute("SELECT Широта, Долгота FROM city WHERE Город = ?", (current_city,)).fetchall()[0]
    return lat, lon



