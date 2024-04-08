# Импорт библиотек
import datetime
import sys
from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt, QSignalBlocker
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QCompleter, QVBoxLayout, QGridLayout, QWidget, \
    QHBoxLayout, QPushButton
import sqlite3
from weather_data import weather_api
from icons import icons_128, icons_256
from time_dict import months, months_short
from main_design import Ui_MainWindow
from current_city import get_current_city, get_current_city_coords
from weather_dict import weather_tr

# Подключение к БД
connection = sqlite3.connect('cities.db')
cur = connection.cursor()

# Чтение избранных городов
with open('favorite.txt', encoding='utf8') as f:
    data_f = f.readlines()
    if len(data_f) == 0:
        initial_city = get_current_city()
        open('favorite.txt', 'w', encoding='utf8').write(initial_city)


# Главный класс приложения
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Инициализация класса
        super().__init__()
        self.setupUi(self)

        # Установка флага для отслеживания нажатия кнопки мыши
        self.mouse_pressed = False
        self.inside_area_future = False
        self.inside_area_hours = False

        # Сохранение начальной позиции курсора при нажатии
        self.last_pos = None
        self.search_city_v = ''
        self.search_btn.clicked.connect(self.check_city_f)
        self.search_le.textChanged.connect(self.on_text_changed)
        self.last_city = ''

        self.initUI()

    # Значение поиска (ввод пользователя)
    def on_text_changed(self, text):
        self.search_city_v = text

    # Действия при запуске
    def initUI(self):
        # Обозначение команд кнопок
        self.homeb.clicked.connect(self.home_page_f)
        self.searchb.clicked.connect(self.search_page_f)
        self.profileb.clicked.connect(self.settings_page_f)
        self.favorite.clicked.connect(self.do_favorite)
        self.favorite_2.clicked.connect(self.do_favorite_2)
        self.stackedWidget.setStyleSheet("background-color: rgba(255, 255, 255, 0)")

        self.home_page_f() # Переход на главную страницу

    def do_favorite(self): # Сделать город избранным
        name = self.city.text()

        with open('favorite.txt', 'r', encoding='utf8') as f:
            data = set([line.strip() for line in f])

        if name in data:
            data.remove(name)
            self.favorite.setIcon(QIcon('icons/free-icon-bookmark-3983871.png'))
        else:
            data.add(name)
            self.favorite.setIcon(QIcon('icons/free-icon-bookmark-3983855.png'))

        with open('favorite.txt', 'w', encoding='utf8') as f:
            for value in data:
                f.write(f'{value}\n')

    def do_favorite_2(self): # Сделать город избранным в поиске
        name = self.city_2.text()

        with open('favorite.txt', 'r', encoding='utf8') as f:
            data = set([line.strip() for line in f])

        if name in data:
            data.remove(name)
            self.favorite_2.setIcon(QIcon('icons/free-icon-bookmark-3983871.png'))
        else:
            data.add(name)
            self.favorite_2.setIcon(QIcon('icons/free-icon-bookmark-3983855.png'))

        with open('favorite.txt', 'w', encoding='utf8') as f:
            for value in data:
                f.write(f'{value}\n')


    def home_page_f(self): # Главная страница приложения
        self.stackedWidget.setCurrentIndex(0)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.profileb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.statusBar().hide()

        with open('last_city', encoding='utf8') as f:
            city = f.readline()
            if city:
                self.last_city = city.strip()
            else:
                self.last_city = get_current_city()
                open('last_city', 'w', encoding='utf8').write(self.last_city)
        self.choose_city.currentIndexChanged.connect(self.on_combo_box_changed)

        lat, lon = get_current_city_coords(cur, self.last_city)

        data = weather_api(lat, lon)

        main_layout_future = QHBoxLayout()
        main_widget_future = QWidget()
        main_widget_future.setLayout(main_layout_future)

        # Добавление погоды в будущие дни
        for i in range(0, 7):
            name = QLabel()
            name.setMaximumSize(128, 40)
            name.setMinimumSize(128, 40)
            name.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 20px;")
            name.setAlignment(Qt.AlignCenter)

            img = QLabel()
            img.setMinimumSize(128, 128)
            img.setMaximumSize(128, 128)
            img.setStyleSheet('background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 15px;')
            img.setAlignment(Qt.AlignCenter)

            max_temp = QLabel()
            max_temp.setMaximumSize(60, 40)
            max_temp.setMinimumSize(60, 40)
            max_temp.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 15px;")
            max_temp.setAlignment(Qt.AlignCenter)

            min_temp = QLabel()
            min_temp.setMaximumSize(60, 40)
            min_temp.setMinimumSize(60, 40)
            min_temp.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 15px;")
            min_temp.setAlignment(Qt.AlignCenter)

            layout = QGridLayout()
            widget = QWidget()
            widget.setLayout(layout)

            date = data["forecasts"][i]["date"]

            if i == 0:
                name.setText("Сегодня")
            elif i == 1:
                name.setText("Завтра")
            else:
                year, month, day = str(date).split('-')
                name_month = months_short[month]

                name.setText(f'{day} {name_month}')

            img.setPixmap(QPixmap(icons_128[data["forecasts"][1]["parts"]["day"]["icon"]]))

            if data["forecasts"][i]["parts"]["day"]["temp_max"] > 0:
                max_temp.setText("+" + str(data["forecasts"][i]["parts"]["day"]["temp_max"]))
            elif int(data["forecasts"][i]["parts"]["day"]["temp_max"]) < 0:
                max_temp.setText(str(data["forecasts"][i]["parts"]["day"]["temp_max"]))
            else:
                max_temp.setText(str(data["forecasts"][i]["parts"]["day"]["temp_max"]))

            if data["forecasts"][i]["parts"]["day"]["temp_min"] > 0:
                min_temp.setText("+" + str(data["forecasts"][i]["parts"]["night"]["temp_min"]))
            elif int(data["forecasts"][i]["parts"]["day"]["temp_min"]) < 0:
                min_temp.setText(str(data["forecasts"][i]["parts"]["night"]["temp_min"]))
            else:
                min_temp.setText(str(data["forecasts"][i]["parts"]["night"]["temp_min"]))

            max_min = QHBoxLayout()
            max_min.addWidget(max_temp)
            max_min.addWidget(min_temp)

            layout.addWidget(name, 0, 0)  # Размещаем name в строке 0, столбце 0
            layout.addWidget(img, 1, 0, 1, 1)  # Размещаем img в строке 1, столбце 0, занимая 2 столбца
            layout.addLayout(max_min, 2, 0)

            main_layout_future.addWidget(widget)

        self.future.setWidget(main_widget_future)

        current_hour = int(str(datetime.datetime.now().time()).split(":")[0])
        main_layout_hours = QHBoxLayout()
        main_widget_hours = QWidget()
        main_widget_hours.setLayout(main_layout_hours)

        # Добавление погоды в будущие 24 часа
        for i in range(0, 25):
            hour = QLabel()
            hour.setMaximumSize(128, 40)
            hour.setMinimumSize(128, 40)
            hour.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 20px;")
            hour.setAlignment(Qt.AlignCenter)
            layout = QVBoxLayout()
            widget = QWidget()
            widget.setLayout(layout)

            img = QLabel()
            img.setMinimumSize(128, 128)
            img.setMaximumSize(128, 128)
            img.setStyleSheet('background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 15px;')
            img.setAlignment(Qt.AlignCenter)

            temp = QLabel()
            temp.setMaximumSize(128, 40)
            temp.setMinimumSize(128, 40)
            temp.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 15px;")
            temp.setAlignment(Qt.AlignCenter)

            if current_hour + i <= 23:
                hour.setText(f'{str(data["forecasts"][0]["hours"][current_hour + i]["hour"]).zfill(2)}:00')
                img.setPixmap(QPixmap(icons_128[data["forecasts"][0]["hours"][current_hour + i]["icon"]]))

                if data["forecasts"][0]["hours"][current_hour + i]["temp"] > 0:
                    temp.setText("+" + str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
                elif int(data["forecasts"][0]["hours"][current_hour + i]["hour"]) < 0:
                    temp.setText(str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
                else:
                    temp.setText(str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
            else:
                hour.setText(f'{str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["hour"]).zfill(2)}:00')
                img.setPixmap(QPixmap(icons_128[data["forecasts"][1]["hours"][(current_hour + i) % 24]["icon"]]))

                if data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"] > 0:
                    temp.setText("+" + str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"]))
                elif int(data["forecasts"][1]["hours"][(current_hour + i) % 24]["hour"]) < 0:
                    temp.setText(str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"]))
                else:
                    temp.setText(str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"]))

            layout.addWidget(hour)
            layout.addWidget(img)
            layout.addWidget(temp)

            main_layout_hours.addWidget(widget)

        main_widget_hours.setLayout(main_layout_hours)
        self.hours.setWidget(main_widget_hours)

        self.city.setText(f'{self.last_city}')

        if data["forecasts"][0]["hours"][current_hour]["temp"] > 0:
            self.now_temp.setText("+" + str(data["forecasts"][0]["hours"][current_hour]["temp"]))
        elif int(data["forecasts"][0]["hours"][current_hour]["hour"]) < 0:
            self.now_temp.setText(str(data["forecasts"][0]["hours"][current_hour]["temp"]))
        else:
            self.now_temp.setText(str(data["forecasts"][0]["hours"][current_hour]["temp"]))
        # =======================================================================================
        s = ''

        if data["forecasts"][0]["parts"]["day"]["temp_max"] > 0:
            s += '+' + f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'
        elif int(data["forecasts"][0]["parts"]["day"]["temp_max"]) < 0:
            s += f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'
        else:
            s += f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'

        if data["forecasts"][0]["parts"]["night"]["temp_min"] > 0:
            s += '+' + f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'
        elif int(data["forecasts"][0]["parts"]["night"]["temp_min"]) < 0:
            s += f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'
        else:
            s += f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'

        self.maxmin.setText(s)

        self.img_now.setPixmap(QPixmap(icons_256[data["forecasts"][0]["hours"][current_hour]["icon"]]))

        self.description.setText(f'{weather_tr[data["forecasts"][0]["hours"][current_hour]["condition"]]}')

        self.label_4.setText(
            f'{data["forecasts"][0]["hours"][current_hour]["wind_dir"]} {data["forecasts"][0]["hours"][current_hour]["wind_speed"]}м/с')
        self.label_5.setText(f'{data["forecasts"][0]["hours"][current_hour]["pressure_mm"]}мм')
        self.label_6.setText(f'{data["forecasts"][0]["hours"][current_hour]["humidity"]}%')

        self.date.setText(
            f'{datetime.datetime.now().day} {months[datetime.datetime.now().month]} {datetime.datetime.now().year}')

        self.favorite.setText('')

        name = self.city.text()

        with open('favorite.txt', 'r', encoding='utf8') as f:
            data = set([line.strip() for line in f])

        if name in data:
            self.favorite.setIcon(QIcon('icons/free-icon-bookmark-3983855.png'))
        else:
            self.favorite.setIcon(QIcon('icons/free-icon-bookmark-3983871.png'))

    def search_page_f(self): # Страница дял поиска
        self.stackedWidget.setCurrentIndex(1)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")
        self.profileb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.statusBar().hide()

        cities = [x[0] for x in list(cur.execute("SELECT Город FROM city").fetchall())] # Все города

        completer = QCompleter(cities, self) # Сетод для подсказок пользователю
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive) # не зависит от регистра

        self.search_le.setCompleter(completer) # добавляем его в строкук поиска

        popup = completer.popup() # стилизуем
        popup.setStyleSheet("background-color: rgba(255, 255, 255, 100); color: black; font-size: 26px;")

        city = self.search_le.text()
        self.search_city_v = city # изменям текст атрибута

    def check_city_f(self): # Страница для просмотра города в режиме поиска
        if self.search_city_v != "" and self.search_city_v.lower() in [str(x[0]).lower() for x in list(cur.execute(
                "SELECT Город FROM city").fetchall())]:
            self.statusBar().hide()
            city = self.search_city_v

            self.stackedWidget.setCurrentIndex(4)

            lat, lon = get_current_city_coords(cur, city)

            data = weather_api(lat, lon)

            main_layout_future = QHBoxLayout()
            main_widget_future = QWidget()
            main_widget_future.setLayout(main_layout_future)

            # Добавление погоды в следующие дни
            for i in range(0, 7):
                name = QLabel()
                name.setMaximumSize(128, 40)
                name.setMinimumSize(128, 40)
                name.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 20px;")
                name.setAlignment(Qt.AlignCenter)

                img = QLabel()
                img.setMinimumSize(128, 128)
                img.setMaximumSize(128, 128)
                img.setStyleSheet('background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 15px;')
                img.setAlignment(Qt.AlignCenter)

                max_temp = QLabel()
                max_temp.setMaximumSize(60, 40)
                max_temp.setMinimumSize(60, 40)
                max_temp.setStyleSheet(
                    "background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 15px;")
                max_temp.setAlignment(Qt.AlignCenter)

                min_temp = QLabel()
                min_temp.setMaximumSize(60, 40)
                min_temp.setMinimumSize(60, 40)
                min_temp.setStyleSheet(
                    "background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 15px;")
                min_temp.setAlignment(Qt.AlignCenter)

                layout = QGridLayout()
                widget = QWidget()
                widget.setLayout(layout)

                date = data["forecasts"][i]["date"]

                if i == 0:
                    name.setText("Сегодня")
                elif i == 1:
                    name.setText("Завтра")
                else:
                    year, month, day = str(date).split('-')
                    name_month = months_short[month]

                    name.setText(f'{day} {name_month}')

                img.setPixmap(QPixmap(icons_128[data["forecasts"][1]["parts"]["day"]["icon"]]))

                if data["forecasts"][i]["parts"]["day"]["temp_max"] > 0:
                    max_temp.setText("+" + str(data["forecasts"][i]["parts"]["day"]["temp_max"]))
                elif int(data["forecasts"][i]["parts"]["day"]["temp_max"]) < 0:
                    max_temp.setText(str(data["forecasts"][i]["parts"]["day"]["temp_max"]))
                else:
                    max_temp.setText(str(data["forecasts"][i]["parts"]["day"]["temp_max"]))

                if data["forecasts"][i]["parts"]["day"]["temp_min"] > 0:
                    min_temp.setText("+" + str(data["forecasts"][i]["parts"]["night"]["temp_min"]))
                elif int(data["forecasts"][i]["parts"]["day"]["temp_min"]) < 0:
                    min_temp.setText(str(data["forecasts"][i]["parts"]["night"]["temp_min"]))
                else:
                    min_temp.setText(str(data["forecasts"][i]["parts"]["night"]["temp_min"]))

                max_min = QHBoxLayout()
                max_min.addWidget(max_temp)
                max_min.addWidget(min_temp)

                layout.addWidget(name, 0, 0)  # Размещаем name в строке 0, столбце 0
                layout.addWidget(img, 1, 0, 1, 1)  # Размещаем img в строке 1, столбце 0, занимая 2 столбца
                layout.addLayout(max_min, 2, 0)

                main_layout_future.addWidget(widget)

            self.future_2.setWidget(main_widget_future)

            current_hour = int(str(datetime.datetime.now().time()).split(":")[0])
            main_layout_hours = QHBoxLayout()
            main_widget_hours = QWidget()
            main_widget_hours.setLayout(main_layout_hours)

            # Добавление погоды в будущие часы
            for i in range(0, 25):
                hour = QLabel()
                hour.setMaximumSize(128, 40)
                hour.setMinimumSize(128, 40)
                hour.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 20px;")
                hour.setAlignment(Qt.AlignCenter)
                layout = QVBoxLayout()
                widget = QWidget()
                widget.setLayout(layout)

                img = QLabel()
                img.setMinimumSize(128, 128)
                img.setMaximumSize(128, 128)
                img.setStyleSheet('background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 15px;')
                img.setAlignment(Qt.AlignCenter)

                temp = QLabel()
                temp.setMaximumSize(128, 40)
                temp.setMinimumSize(128, 40)
                temp.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 15px;")
                temp.setAlignment(Qt.AlignCenter)

                if current_hour + i <= 23:
                    hour.setText(f'{str(data["forecasts"][0]["hours"][current_hour + i]["hour"]).zfill(2)}:00')
                    img.setPixmap(QPixmap(icons_128[data["forecasts"][0]["hours"][current_hour + i]["icon"]]))

                    if data["forecasts"][0]["hours"][current_hour + i]["temp"] > 0:
                        temp.setText("+" + str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
                    elif int(data["forecasts"][0]["hours"][current_hour + i]["hour"]) < 0:
                        temp.setText(str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
                    else:
                        temp.setText(str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
                else:
                    hour.setText(f'{str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["hour"]).zfill(2)}:00')
                    img.setPixmap(QPixmap(icons_128[data["forecasts"][1]["hours"][(current_hour + i) % 24]["icon"]]))

                    if data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"] > 0:
                        temp.setText("+" + str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"]))
                    elif int(data["forecasts"][1]["hours"][(current_hour + i) % 24]["hour"]) < 0:
                        temp.setText(str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"]))
                    else:
                        temp.setText(str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"]))

                layout.addWidget(hour)
                layout.addWidget(img)
                layout.addWidget(temp)

                main_layout_hours.addWidget(widget)

            main_widget_hours.setLayout(main_layout_hours)
            self.hours_2.setWidget(main_widget_hours)

            self.city_2.setText(f'{city}')

            if data["forecasts"][0]["hours"][current_hour]["temp"] > 0:
                self.now_temp_2.setText("+" + str(data["forecasts"][0]["hours"][current_hour]["temp"]))
            elif int(data["forecasts"][0]["hours"][current_hour]["hour"]) < 0:
                self.now_temp_2.setText(str(data["forecasts"][0]["hours"][current_hour]["temp"]))
            else:
                self.now_temp_2.setText(str(data["forecasts"][0]["hours"][current_hour]["temp"]))
            # =======================================================================================
            s = ''

            if data["forecasts"][0]["parts"]["day"]["temp_max"] > 0:
                s += '+' + f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'
            elif int(data["forecasts"][0]["parts"]["day"]["temp_max"]) < 0:
                s += f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'
            else:
                s += f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'

            if data["forecasts"][0]["parts"]["night"]["temp_min"] > 0:
                s += '+' + f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'
            elif int(data["forecasts"][0]["parts"]["night"]["temp_min"]) < 0:
                s += f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'
            else:
                s += f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'

            self.maxmin_2.setText(s)

            self.img_now_2.setPixmap(QPixmap(icons_256[data["forecasts"][0]["hours"][current_hour]["icon"]]))

            self.description_2.setText(f'{weather_tr[data["forecasts"][0]["hours"][current_hour]["condition"]]}')

            self.label_130.setText(
                f'{data["forecasts"][0]["hours"][current_hour]["wind_dir"]} {data["forecasts"][0]["hours"][current_hour]["wind_speed"]}м/с')
            self.label_8.setText(f'{data["forecasts"][0]["hours"][current_hour]["pressure_mm"]}мм')
            self.label_131.setText(f'{data["forecasts"][0]["hours"][current_hour]["humidity"]}%')

            self.date_2.setText(
                f'{datetime.datetime.now().day} {months[datetime.datetime.now().month]} {datetime.datetime.now().year}')

            self.favorite_2.setText('')

            name = self.city_2.text()

            with open('favorite.txt', 'r', encoding='utf8') as f:
                data = set([line.strip() for line in f])

            if name in data:
                self.favorite_2.setIcon(QIcon('icons/free-icon-bookmark-3983855.png'))
            else:
                self.favorite_2.setIcon(QIcon('icons/free-icon-bookmark-3983871.png'))
        else:
            self.statusBar().show()
            self.statusBar().showMessage("Некорректный ввод")
            self.statusBar().setStyleSheet('background-color: rgba(255, 255, 255, 100); font-size: 20px;')

    def settings_page_f(self): # Страница с настройками
        self.stackedWidget.setCurrentIndex(3)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.profileb.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")
        self.statusBar().hide()

        with QSignalBlocker(self.choose_city): # При выполнении следующих действий сигналы отключены
            self.choose_city.clear() # очистка городов для выбора

            self.default_city.setText(f"По умолчанию {self.last_city}") # Надпись с городом по умолчанию

            data_for_ch = []

            # Добавление городов, которые можно выбрать как город по умолчанию
            with open('favorite.txt', 'r', encoding='utf8') as f:
                data = set([line.strip() for line in f])

                for city in data:
                    data_for_ch.append(city)
                data_for_ch.pop(data_for_ch.index(self.last_city))

            self.choose_city.addItems(data_for_ch)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        for c in sorted(data):
            widget = QWidget()
            layout = QHBoxLayout()
            widget.setLayout(layout)
            button = QPushButton()
            button.setText(c)
            button.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px; font-size: 26px;")
            button.setMinimumSize(630, 100)
            button.clicked.connect(lambda checked, city=c: self.on_button_clicked(city))
            layout.addWidget(button)
            main_layout.addWidget(widget)

        self.my_cities.setWidget(main_widget)

    def on_button_clicked(self, city): # Просмотр города из списка пользователей
        self.search_city_v = city
        self.check_city_f()

    def on_combo_box_changed(self, index): # Изменение города по умолчанию
        selected_item = self.choose_city.currentText()
        print(selected_item)

        default_city_text = self.default_city.text().replace("По умолчанию ", "")
        if selected_item != default_city_text:
            self.last_city = selected_item

            self.default_city.setText(f"По умолчанию {self.last_city}")
            with open('last_city', 'w', encoding='utf8') as f:
                f.write(self.last_city)

    def mousePressEvent(self, event): # Следующие три метода отвечают за скроллинг погоды в специальных окошках
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.last_pos = event.pos()

            # Координаты future
            x1, y1 = 640, 290  # Пример координат левого верхнего угла области
            x2, y2 = 640 + 641, 310 + 241  # Пример координат правого нижнего угла области

            # Координаты
            x1_, y1_ = 620, 40  # Пример координат левого верхнего угла области
            x2_, y2_ = 620 + 641, 40 + 241  # Пример координат правого нижнего угла области

            # Координаты
            x1__, y1__ = 590, 140  # Пример координат левого верхнего угла области
            x2__, y2__ = 590 + 641, 140 + 341  # Пример координат правого нижнего угла области

            if (x1 <= event.x() <= x2 and y1 <= event.y() <= y2):
                self.inside_area_future = True
            else:
                self.inside_area_future = False

            if (x1_ <= event.x() <= x2_ and y1_ <= event.y() <= y2_):
                self.inside_area_hours = True
            else:
                self.inside_area_hours = False

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False

    def mouseMoveEvent(self, event):
        if self.stackedWidget.currentIndex() == 0:
            if self.mouse_pressed and self.last_pos:
                delta = event.pos() - self.last_pos
                new_value_future = self.future.horizontalScrollBar().value() - delta.x()
                new_value_hours = self.hours.horizontalScrollBar().value() - delta.x()

                # Координаты future
                x1, y1 = 640, 290  # Пример координат левого верхнего угла области
                x2, y2 = 640 + 641, 310 + 241  # Пример координат правого нижнего угла области

                # Координаты
                x1_, y1_ = 620, 40  # Пример координат левого верхнего угла области
                x2_, y2_ = 620 + 641, 40 + 241  # Пример координат правого нижнего угла области

                if self.mouse_pressed and self.inside_area_future or (x1 <= event.x() <= x2 and y1 <= event.y() <= y2):
                    self.future.horizontalScrollBar().setValue(new_value_future)

                if self.mouse_pressed and self.inside_area_hours or (
                        x1_ <= event.x() <= x2_ and y1_ <= event.y() <= y2_):
                    self.hours.horizontalScrollBar().setValue(new_value_hours)

                self.last_pos = event.pos()
        if self.stackedWidget.currentIndex() == 4:
            if self.mouse_pressed and self.last_pos:
                delta = event.pos() - self.last_pos
                new_value_future = self.future_2.horizontalScrollBar().value() - delta.x()
                new_value_hours = self.hours_2.horizontalScrollBar().value() - delta.x()

                # Координаты future
                x1, y1 = 640, 290  # Пример координат левого верхнего угла области
                x2, y2 = 640 + 641, 310 + 241  # Пример координат правого нижнего угла области

                # Координаты
                x1_, y1_ = 620, 40  # Пример координат левого верхнего угла области
                x2_, y2_ = 620 + 641, 40 + 241  # Пример координат правого нижнего угла области

                if self.mouse_pressed and self.inside_area_future or (x1 <= event.x() <= x2 and y1 <= event.y() <= y2):
                    self.future_2.horizontalScrollBar().setValue(new_value_future)

                if self.mouse_pressed and self.inside_area_hours or (
                        x1_ <= event.x() <= x2_ and y1_ <= event.y() <= y2_):
                    self.hours_2.horizontalScrollBar().setValue(new_value_hours)

                self.last_pos = event.pos()


# Запуск приложения
if __name__ == "__main__": # Если запускают именно из этого файла
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.setFixedSize(1280, 716) # Фиксированное разрешение
    ex.show()
    sys.exit(app.exec_())
