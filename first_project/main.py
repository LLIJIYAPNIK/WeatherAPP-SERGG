import sys
from PyQt5 import QtCore, uic
from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from bs4 import BeautifulSoup
import requests

weather_to_img = {
    "Облачно": ["256/day_partial_cloud.png", "100/day_partial_cloud.png"],
    "Ветер": ["256/tornado.png", "100/tornado.png"],
    "Дождь": ["256/rain.png", "100/rain.png"],
    "Ясно": ["256/day_clear.png", "100/day_clear.png"],
    "Гроза": ["256/rain_thunder.png", "100/rain_thunder.png"],
    "Град": ["256/day_sleet.png", "100/day_sleet.png"],
    "Снег": ["256/day_snow.png", "100/day_snow.png"],
    "Мокрый снег": ["256/day_sleet.png", "100/day_sleet.png"],
    "Ливень": ["256/day_rain.png", "100/day_rain.png"],
    "Туман": ["256/fog.png", "100/fog.png"],
    "Дымка": ["256/mist.png", "100/mist.png"],
    "Пасмурно": ["256/angry_clouds.png", "100/angry_clouds.png"],
    "Прояснения": ["256/wind.png", "100/wind.png"],
    "Переменная облачность": ["256/day_partial_cloud.png", "100/day_partial_cloud.png"],
    "Небольшой снег": ["256/day_snow.png", "100/day_snow.png"],
    "Небольшой дождь": ["256/rain.png", "100/rain.png"],
    "Ясно, переменная облачность": ["256/day_clear.png", "100/day_clear.png"],
    "Снегопад": ["256/day_snow.png", "100/day_snow.png"]
}


def time_check(city):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    res = requests.get(
        f'https://www.google.com/search?q=дата+{city}&sca_esv=598645516&sxsrf=ACQVn0-vpscoS55d-9z0Mwuy9RvOtRbFWw%3A1705354103000&ei=dqOlZd_SPNqF1fIPj6-6GA&udm=&ved=0ahUKEwjf5ZmMq-CDAxXaQlUIHY-XDgMQ4dUDCBA&uact=5&oq=дата+{city}&gs_lp=Egxnd3Mtd2l6LXNlcnAiF9C00LDRgtCwINGB0LDRgNCw0YLQvtCyMgYQABgWGB4yBhAAGBYYHkjqJFAAWIchcAZ4AZABAJgBXKABtgaqAQIxMrgBA8gBAPgBAagCEcICBBAjGCfCAgoQIxiABBiKBRgnwgILEAAYgAQYsQMYgwHCAhEQLhiABBixAxiDARjHARjRA8ICDhAAGIAEGIoFGLEDGIMBwgIIEAAYgAQYsQPCAgoQABiABBiKBRhDwgIQEC4YgAQYigUYQxixAxiDAcICBRAAGIAEwgIOEC4YgAQYigUYsQMYgwHCAg0QLhiABBiKBRhDGLEDwgIQEAAYgAQYigUYQxixAxiDAcICERAuGIAEGLEDGIMBGMcBGK8BwgIHECMY6gIYJ8ICExAAGIAEGIoFGEMY6gIYtALYAQHCAhwQLhiABBiKBRhDGMcBGNEDGMgDGOoCGLQC2AECwgINEAAYgAQYigUYQxixA8ICDhAuGIAEGMcBGK8BGI4FwgIIEAAYFhgeGA_CAg4QLhgWGB4YxwEYrwEYCuIDBBgAIEG6BgYIARABGAG6BgYIAhABGAg&sclient=gws-wiz-serp',
        headers=headers
    )

    soup = BeautifulSoup(res.text, 'html.parser')

    days = []  # Дни для temperature_in_future, 1 - сегодня
    example_tags = soup.find_all(class_='vk_bk dDoNo FzvWSb')
    [days.append(tag.text) for tag in example_tags]

    return str(days[0]).strip().split(',')[1].strip()


# print(time_check(f"масква"))
def weather_check(city):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
        headers=headers
    )

    soup = BeautifulSoup(res.text, 'html.parser')

    precipitation = soup.select('#wob_dc')[0].getText().strip()  # Погода сейчас
    weather = soup.select('#wob_tm')[0].getText().strip()  # Температура сейчас
    ifashka = soup.select('#wob_pp')[0].getText().strip()  # Вероятность осадков
    vlaga = soup.select('#wob_hm')[0].getText().strip()  # Вложность
    veter = soup.select('#wob_ws')[0].getText().strip()  # Скорость ветра

    temperature_in_future = []  # Температура которая будет в будущем [min, max], 1 - сегодня

    count = 1
    count_for_all = 0
    example_tags = soup.find_all(class_='wNE31c', style_='')

    for _ in example_tags:
        data = str(example_tags[count_for_all]).split('</span>')
        for_now = []
        for _ in data:
            if count % 2 == 1:
                new = data[count - 1][::-1]
                s = ''
                for symbol in new:
                    if symbol == '>':
                        break
                    else:
                        s += symbol
                for_now.append(s[::-1])
            count += 1
        count = 1
        count_for_all += 1
        temperature_in_future.append(for_now[0:2])

    days = []  # Дни для temperature_in_future, 1 - сегодня
    example_tags = soup.find_all(class_='Z1VzSb')
    [days.append(tag.text) for tag in example_tags]

    info_for_sprites = []  # Погода для temperature_in_future, 1 - сегодня
    count_for_all = 0
    example_tags = soup.find_all(class_='DxhUm')

    for _ in example_tags:
        new = str(example_tags[count_for_all]).split("alt=")
        count = 0
        s = ''
        for symbol in str(new[1]):
            if symbol == '"':
                count += 1
            else:
                s += symbol
            if count == 2:
                info_for_sprites.append(s)
                break
        count_for_all += 1

    name = ''  # Название города
    town = soup.find_all(class_='eKPi4 BUSxSd')
    for symbol in str(town[0]).split('class="BBwThe">')[1]:
        if symbol == '<':
            break
        else:
            name += symbol

    return precipitation, weather, ifashka, vlaga, veter, temperature_in_future, days, info_for_sprites, name


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.is_burger = False
        self.initUI()

    def initUI(self):
        self.burger_btn.clicked.connect(self.do_burger)
        self.add_city.clicked.connect(self.open_add_city)
        self.edit_city.clicked.connect(self.open_edit_city)
        self.update_btn.clicked.connect(self.update)

        self.update()

    def do_burger(self):
        if self.is_burger == False:

            self.animation = QPropertyAnimation(self, b"size")
            self.animation.setDuration(1000)
            self.animation.setEndValue(QtCore.QSize(1138, 748))
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
            self.animation.start()

            self.animation_weather = QPropertyAnimation(self.weather_frame, b"geometry")
            self.animation_weather.setDuration(1000)
            self.animation_weather.setStartValue(QRect(99, 9, 902, 718))
            self.animation_weather.setEndValue(QRect(215, 9, 902, 718))
            self.animation_weather.start()

            self.animation_burger_frame = QPropertyAnimation(self.burger_frame, b"geometry")
            self.animation_burger_frame.setDuration(1000)
            self.animation_burger_frame.setStartValue(QRect(9, 9, 84, 718))
            self.animation_burger_frame.setEndValue(QRect(9, 9, 200, 718))
            self.animation_burger_frame.start()

            self.is_burger = True

            self.add_city.setMaximumSize(160, 60)
            self.edit_city.setMaximumSize(170, 60)
            self.update_btn.setMaximumSize(170, 60)

            self.add_city.setText("Добавить")
            self.edit_city.setText(" Изменить")
            self.update_btn.setText(" Обновить")

        else:
            self.add_city.setMaximumSize(60, 60)
            self.edit_city.setMaximumSize(60, 60)
            self.update_btn.setMaximumSize(60, 60)

            self.add_city.setText("")
            self.edit_city.setText("")
            self.update_btn.setText("")

            self.animation = QPropertyAnimation(self, b"size")
            self.animation.setDuration(1000)
            self.animation.setEndValue(QtCore.QSize(1004, 748))
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
            self.animation.start()

            self.animation_weather = QPropertyAnimation(self.weather_frame, b"geometry")
            self.animation_weather.setDuration(1000)
            self.animation_weather.setStartValue(QRect(215, 9, 902, 718))
            self.animation_weather.setEndValue(QRect(99, 9, 902, 718))
            self.animation_weather.start()

            self.animation_burger_frame = QPropertyAnimation(self.burger_frame, b"geometry")
            self.animation_burger_frame.setDuration(1000)
            self.animation_burger_frame.setStartValue(QRect(9, 9, 200, 718))
            self.animation_burger_frame.setEndValue(QRect(9, 9, 84, 718))
            self.animation_burger_frame.start()

            self.is_burger = False

    def update(self):
        data = open('cityes.txt', 'r', encoding='utf-8').readlines()

        if len(data) >= 1:
            data_for_weather = weather_check(f'{open("current_city.txt", encoding="utf-8").readline()} погода')

            # Верх
            self.weather_today.setPixmap(QPixmap(f'{weather_to_img[data_for_weather[0]][0]}'))
            self.temperature_today.setText(f'{str(data_for_weather[1])}°')
            self.city_lbl.setText(data_for_weather[-1])
            self.text_weather.setText(str(data_for_weather[7][0]))
            self.min_max_tmperature_today.setText(
                f'{str(data_for_weather[5][0][0])}°/{str(data_for_weather[5][0][1])}°')
            self.date_today.setText(str(time_check(open('current_city.txt', encoding='utf-8').readline())))

            # Будущее
            self.name_first_day.setText(data_for_weather[6][0])
            self.name_second_day.setText(data_for_weather[6][1])
            self.name_third_day.setText(data_for_weather[6][2])
            self.name_for_day.setText(data_for_weather[6][3])
            self.name_five_day.setText(data_for_weather[6][4])
            self.name_six_day.setText(data_for_weather[6][5])
            self.name_seven_day.setText(data_for_weather[6][6])
            self.name_eight_day.setText(data_for_weather[6][7])

            # Максимальная/минимальная температура в будущем
            self.max_first_day.setText(f'{data_for_weather[5][0][0]}°')
            self.min_first_day.setText(f'{data_for_weather[5][0][1]}°')
            self.max_second_day.setText(f'{data_for_weather[5][1][0]}°')
            self.min_second_day.setText(f'{data_for_weather[5][1][1]}°')
            self.max_third_day.setText(f'{data_for_weather[5][2][0]}°')
            self.min_third_day.setText(f'{data_for_weather[5][2][1]}°')
            self.max_for_day.setText(f'{data_for_weather[5][3][0]}°')
            self.min_for_day.setText(f'{data_for_weather[5][3][1]}°')
            self.max_five_day.setText(f'{data_for_weather[5][4][0]}°')
            self.min_five_day.setText(f'{data_for_weather[5][4][1]}°')
            self.max_six_day.setText(f'{data_for_weather[5][5][0]}°')
            self.min_six_day.setText(f'{data_for_weather[5][5][1]}°')
            self.max_seven_day.setText(f'{data_for_weather[5][6][0]}°')
            self.min_seven_day.setText(f'{data_for_weather[5][6][1]}°')
            self.max_eight_day.setText(f'{data_for_weather[5][7][0]}°')
            self.min_eight_day.setText(f'{data_for_weather[5][7][1]}°')

            # Картинки будущего
            self.weather_first_day.setPixmap(QPixmap(f'{weather_to_img[data_for_weather[-2][0]][1]}'))
            self.weather_second_day.setPixmap(QPixmap(f'{weather_to_img[data_for_weather[-2][1]][1]}'))
            self.weather_third_day.setPixmap(QPixmap(f'{weather_to_img[data_for_weather[-2][2]][1]}'))
            self.weather_for_day.setPixmap(QPixmap(f'{weather_to_img[data_for_weather[-2][3]][1]}'))
            self.weather_five_day.setPixmap(QPixmap(f'{weather_to_img[data_for_weather[-2][4]][1]}'))
            self.weather_six_day.setPixmap(QPixmap(f'{weather_to_img[data_for_weather[-2][5]][1]}'))
            self.weather_seven_day.setPixmap(QPixmap(f'{weather_to_img[data_for_weather[-2][6]][1]}'))
            self.weather_eight_day.setPixmap(QPixmap(f'{weather_to_img[data_for_weather[-2][7]][1]}'))
        else:
            self.temperature_today.setText("Добавьте город")

    def open_edit_city(self):
        self.edit_form = EditCity()
        self.edit_form.show()

    def open_add_city(self):
        self.add_form = AddCity()
        self.add_form.show()


class AddCity(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_city.ui', self)
        self.initUI()

    def initUI(self):
        self.add.clicked.connect(self.add_city)

    def add_city(self):
        if len(self.city_name.text()) >= 1:
            open('current_city.txt', 'w', encoding='utf-8').write(self.city_name.text())
            data = open('cityes.txt', 'r', encoding='utf-8').readlines()
            data.append(self.city_name.text())
            new = []
            for city in data:
                if not f'{city.rstrip()}\n' in new:
                    new.append(f'{city.rstrip()}\n')
            open('cityes.txt', 'w', encoding='utf-8').writelines(new)
            self.city_name.setText('')
            self.city_name.setText(' ')
            self.label_3.setText('Город добавлен!')

        else:
            self.label_3.setText('Неккоректный ввод')


class EditCity(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('edit_city.ui', self)
        self.initUI()

    def initUI(self):
        # self.edit.clicked.connect(self.choose_city)
        data_cityes = open('cityes.txt', encoding='utf-8').readlines()
        for i in range(len(data_cityes)):
            self.cityes_list.addItem(str(data_cityes[i]))
        self.cityes_list.itemClicked.connect(self.choose_city)

    def choose_city(self, item):
        self.label.setText("Нажмите Выбрать")
        open('current_city.txt', 'w', encoding='utf-8').write(str(item.text()))
        self.edit.clicked.connect(self.close_form)

    def close_form(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
