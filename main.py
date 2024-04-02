import datetime
import sys
from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QLabel, QCompleter, QVBoxLayout, QGridLayout, QWidget, \
    QHBoxLayout, QFrame, QListView, QStyledItemDelegate
import sqlite3
import requests
import json
from weather_data import weather_api
from icons import icons_128, icons_256
from time_dict import months, months_short
from current_city import get_current_coords
from main_design import Ui_MainWindow
from current_city import get_current_city, get_current_city_coords

connection = sqlite3.connect('cities.db')
cur = connection.cursor()


# lat, lon = get_current_coords(cur)

# with open('test_1.json', 'w') as f:
#     json.dump(weather_api(lat, lon), f, ensure_ascii=False, indent=4)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
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

        self.initUI()

    def on_text_changed(self, text):
        self.search_city_v = text

    def initUI(self):
        self.homeb.clicked.connect(self.home_page_f)
        self.searchb.clicked.connect(self.search_page_f)
        self.profileb.clicked.connect(self.profile_page_f)

        self.stackedWidget.setCurrentIndex(0)

        self.home_page_f()

    def home_page_f(self):
        self.stackedWidget.setCurrentIndex(0)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.profileb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")

        with open('last_city', encoding='utf8') as f:
            city = f.readline()
            if city:
                self.last_city = city
            else:
                self.last_city = get_current_city()

        lat, lon = get_current_city_coords(cur, self.last_city)

        data = weather_api(lat, lon)

        main_layout_future = QHBoxLayout()
        main_widget_future = QWidget()
        main_widget_future.setLayout(main_layout_future)

        for i in range(0, 7):
            name = QLabel()
            name.setMaximumSize(128, 40)
            name.setMinimumSize(128, 40)
            name.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")

            img = QLabel()
            img.setMinimumSize(128, 128)
            img.setMaximumSize(128, 128)
            img.setStyleSheet('background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;')

            max_temp = QLabel()
            max_temp.setMaximumSize(60, 40)
            max_temp.setMinimumSize(60, 40)
            max_temp.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")

            min_temp = QLabel()
            min_temp.setMaximumSize(60, 40)
            min_temp.setMinimumSize(60, 40)
            min_temp.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")

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
            elif data["forecasts"][i]["parts"]["day"]["temp_max"] < 0:
                max_temp.setText("-" + str(data["forecasts"][i]["parts"]["day"]["temp_max"]))
            else:
                max_temp.setText(str(data["forecasts"][i]["parts"]["day"]["temp_max"]))

            if data["forecasts"][i]["parts"]["day"]["temp_min"] > 0:
                min_temp.setText("+" + str(data["forecasts"][i]["parts"]["night"]["temp_min"]))
            elif data["forecasts"][i]["parts"]["day"]["temp_min"] < 0:
                min_temp.setText("-" + str(data["forecasts"][i]["parts"]["night"]["temp_min"]))
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

        for i in range(0, 25):
            hour = QLabel()
            hour.setMaximumSize(128, 40)
            hour.setMinimumSize(128, 40)
            hour.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")
            layout = QVBoxLayout()
            widget = QWidget()
            widget.setLayout(layout)

            img = QLabel()
            img.setMinimumSize(128, 128)
            img.setMaximumSize(128, 128)
            img.setStyleSheet('background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;')

            temp = QLabel()
            temp.setMaximumSize(128, 40)
            temp.setMinimumSize(128, 40)
            temp.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")

            if current_hour + i <= 23:
                hour.setText(f'{str(data["forecasts"][0]["hours"][current_hour + i]["hour"]).zfill(2)}:00')
                img.setPixmap(QPixmap(icons_128[data["forecasts"][0]["hours"][current_hour + i]["icon"]]))

                if data["forecasts"][0]["hours"][current_hour + i]["temp"] > 0:
                    temp.setText("+" + str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
                elif data["forecasts"][0]["hours"][current_hour + i]["hour"] < 0:
                    temp.setText("-" + str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
                else:
                    temp.setText(str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
            else:
                hour.setText(f'{str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["hour"]).zfill(2)}:00')
                img.setPixmap(QPixmap(icons_128[data["forecasts"][1]["hours"][(current_hour + i) % 24]["icon"]]))

                if data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"] > 0:
                    temp.setText("+" + str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"]))
                elif data["forecasts"][1]["hours"][(current_hour + i) % 24]["hour"] < 0:
                    temp.setText("-" + str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"]))
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
        elif data["forecasts"][0]["hours"][current_hour]["hour"] < 0:
            self.now_temp.setText("-" + str(data["forecasts"][0]["hours"][current_hour]["temp"]))
        else:
            self.now_temp.setText(str(data["forecasts"][0]["hours"][current_hour]["temp"]))
        # =======================================================================================
        s = ''

        if data["forecasts"][0]["parts"]["day"]["temp_max"] > 0:
            s += '+' + f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'
        elif data["forecasts"][0]["parts"]["day"]["temp_max"] < 0:
            s += '-' + f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'
        else:
            s += f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'

        if data["forecasts"][0]["parts"]["night"]["temp_min"] > 0:
            s += '+' + f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'
        elif data["forecasts"][0]["parts"]["night"]["temp_min"] < 0:
            s += '-' + f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'
        else:
            s += f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'

        self.maxmin.setText(s)

        self.img_now.setPixmap(QPixmap(icons_256[data["forecasts"][0]["hours"][current_hour]["icon"]]))

        self.description.setText(f'{data["forecasts"][0]["hours"][current_hour]["condition"]}')

        self.label_4.setText(
            f'{data["forecasts"][0]["hours"][current_hour]["wind_dir"]} {data["forecasts"][0]["hours"][current_hour]["wind_speed"]}м/с')
        self.label_5.setText(f'{data["forecasts"][0]["hours"][current_hour]["pressure_mm"]}мм')
        self.label_6.setText(f'{data["forecasts"][0]["hours"][current_hour]["humidity"]}%')

        self.date.setText(
            f'{datetime.datetime.now().day} {months[datetime.datetime.now().month]} {datetime.datetime.now().year}')

    def search_page_f(self):
        self.stackedWidget.setCurrentIndex(1)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")
        self.profileb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")

        cities = [x[0] for x in list(cur.execute("SELECT Город FROM city").fetchall())]

        completer = QCompleter(cities)

        self.search_le.setCompleter(completer)

        popup = completer.popup()
        popup.setStyleSheet("background-color: rgba(255, 255, 255, 100); color: black; font-size: 26px;")

        city = self.search_le.text()
        print(city)
        self.search_city_v = city
        print(self.search_city_v)

    def check_city_f(self):
        city = self.search_city_v
        print(city, self.search_city_v)

        self.stackedWidget.setCurrentIndex(4)

        lat, lon = get_current_city_coords(cur, city)

        data = weather_api(lat, lon)

        main_layout_future = QHBoxLayout()
        main_widget_future = QWidget()
        main_widget_future.setLayout(main_layout_future)

        for i in range(0, 7):
            name = QLabel()
            name.setMaximumSize(128, 40)
            name.setMinimumSize(128, 40)
            name.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")

            img = QLabel()
            img.setMinimumSize(128, 128)
            img.setMaximumSize(128, 128)
            img.setStyleSheet('background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;')

            max_temp = QLabel()
            max_temp.setMaximumSize(60, 40)
            max_temp.setMinimumSize(60, 40)
            max_temp.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")

            min_temp = QLabel()
            min_temp.setMaximumSize(60, 40)
            min_temp.setMinimumSize(60, 40)
            min_temp.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")

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
            elif data["forecasts"][i]["parts"]["day"]["temp_max"] < 0:
                max_temp.setText("-" + str(data["forecasts"][i]["parts"]["day"]["temp_max"]))
            else:
                max_temp.setText(str(data["forecasts"][i]["parts"]["day"]["temp_max"]))

            if data["forecasts"][i]["parts"]["day"]["temp_min"] > 0:
                min_temp.setText("+" + str(data["forecasts"][i]["parts"]["night"]["temp_min"]))
            elif data["forecasts"][i]["parts"]["day"]["temp_min"] < 0:
                min_temp.setText("-" + str(data["forecasts"][i]["parts"]["night"]["temp_min"]))
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

        for i in range(0, 25):
            hour = QLabel()
            hour.setMaximumSize(128, 40)
            hour.setMinimumSize(128, 40)
            hour.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")
            layout = QVBoxLayout()
            widget = QWidget()
            widget.setLayout(layout)

            img = QLabel()
            img.setMinimumSize(128, 128)
            img.setMaximumSize(128, 128)
            img.setStyleSheet('background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;')

            temp = QLabel()
            temp.setMaximumSize(128, 40)
            temp.setMinimumSize(128, 40)
            temp.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")

            if current_hour + i <= 23:
                hour.setText(f'{str(data["forecasts"][0]["hours"][current_hour + i]["hour"]).zfill(2)}:00')
                img.setPixmap(QPixmap(icons_128[data["forecasts"][0]["hours"][current_hour + i]["icon"]]))

                if data["forecasts"][0]["hours"][current_hour + i]["temp"] > 0:
                    temp.setText("+" + str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
                elif data["forecasts"][0]["hours"][current_hour + i]["hour"] < 0:
                    temp.setText("-" + str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
                else:
                    temp.setText(str(data["forecasts"][0]["hours"][current_hour + i]["temp"]))
            else:
                hour.setText(f'{str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["hour"]).zfill(2)}:00')
                img.setPixmap(QPixmap(icons_128[data["forecasts"][1]["hours"][(current_hour + i) % 24]["icon"]]))

                if data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"] > 0:
                    temp.setText("+" + str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"]))
                elif data["forecasts"][1]["hours"][(current_hour + i) % 24]["hour"] < 0:
                    temp.setText("-" + str(data["forecasts"][1]["hours"][(current_hour + i) % 24]["temp"]))
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
        elif data["forecasts"][0]["hours"][current_hour]["hour"] < 0:
            self.now_temp_2.setText("-" + str(data["forecasts"][0]["hours"][current_hour]["temp"]))
        else:
            self.now_temp_2.setText(str(data["forecasts"][0]["hours"][current_hour]["temp"]))
        # =======================================================================================
        s = ''

        if data["forecasts"][0]["parts"]["day"]["temp_max"] > 0:
            s += '+' + f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'
        elif data["forecasts"][0]["parts"]["day"]["temp_max"] < 0:
            s += '-' + f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'
        else:
            s += f'{data["forecasts"][0]["parts"]["day"]["temp_max"]}' + '/'

        if data["forecasts"][0]["parts"]["night"]["temp_min"] > 0:
            s += '+' + f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'
        elif data["forecasts"][0]["parts"]["night"]["temp_min"] < 0:
            s += '-' + f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'
        else:
            s += f'{data["forecasts"][0]["parts"]["night"]["temp_min"]}'

        self.maxmin_2.setText(s)

        self.img_now_2.setPixmap(QPixmap(icons_256[data["forecasts"][0]["hours"][current_hour]["icon"]]))

        self.description_2.setText(f'{data["forecasts"][0]["hours"][current_hour]["condition"]}')

        self.label_130.setText(
            f'{data["forecasts"][0]["hours"][current_hour]["wind_dir"]} {data["forecasts"][0]["hours"][current_hour]["wind_speed"]}м/с')
        self.label_8.setText(f'{data["forecasts"][0]["hours"][current_hour]["pressure_mm"]}мм')
        self.label_131.setText(f'{data["forecasts"][0]["hours"][current_hour]["humidity"]}%')

        self.date_2.setText(
            f'{datetime.datetime.now().day} {months[datetime.datetime.now().month]} {datetime.datetime.now().year}')

    def add_page_f(self):
        self.stackedWidget.setCurrentIndex(2)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.profileb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")

    def profile_page_f(self):
        self.stackedWidget.setCurrentIndex(3)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.profileb.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.last_pos = event.pos()

            # Координаты future
            x1, y1 = 640, 290  # Пример координат левого верхнего угла области
            x2, y2 = 640 + 641, 310 + 241  # Пример координат правого нижнего угла области

            # Координаты
            x1_, y1_ = 620, 40  # Пример координат левого верхнего угла области
            x2_, y2_ = 620 + 641, 40 + 241  # Пример координат правого нижнего угла области

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
