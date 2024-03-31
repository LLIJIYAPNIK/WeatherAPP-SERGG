import sys
from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QLabel, QCompleter, QVBoxLayout
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

lat, lon = get_current_coords(cur)

with open('test_1.json', 'w') as f:
    json.dump(weather_api(lat, lon), f, ensure_ascii=False, indent=4)


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

        self.initUI()

    def initUI(self):
        self.homeb.clicked.connect(self.home_page_f)
        self.searchb.clicked.connect(self.search_page_f)
        self.addb.clicked.connect(self.add_page_f)
        self.profileb.clicked.connect(self.profile_page_f)

        self.stackedWidget.setCurrentIndex(0)

        with open('last_city', encoding='utf8') as f:
            city = f.readline()
            if city:
                self.last_city = city
            else:
                self.last_city = get_current_city()

        lat, lon = get_current_city_coords(cur, self.last_city)

        data = weather_api(lat, lon)

        for count_d in range(0, 10):
            with open('test_1.json') as f:
                data = json.load(f)
                if count_d == 0:
                    self.label_54.setText("Сегодня")
                    self.label_55.setPixmap(QPixmap(icons_128[data["forecasts"][0]["parts"]["day"]["icon"]]))
                    self.label_55.setAlignment(Qt.AlignCenter)
                    if data["forecasts"][0]["parts"]["day"]["temp_max"] > 0:
                        self.label_56.setText("+" + str(data["forecasts"][0]["parts"]["day"]["temp_max"]))
                    elif data["forecasts"][0]["parts"]["day"]["temp_max"] < 0:
                        self.label_56.setText("-" + str(data["forecasts"][0]["parts"]["day"]["temp_max"]))
                    else:
                        self.label_56.setText(str(data["forecasts"][0]["parts"]["day"]["temp_max"]))

                    if data["forecasts"][0]["parts"]["day"]["temp_min"] > 0:
                        self.label_57.setText("+" + str(data["forecasts"][0]["parts"]["day"]["temp_min"]))
                    elif data["forecasts"][0]["parts"]["day"]["temp_min"] < 0:
                        self.label_57.setText("-" + str(data["forecasts"][0]["parts"]["day"]["temp_min"]))
                    else:
                        self.label_57.setText(str(data["forecasts"][0]["parts"]["day"]["temp_min"]))

                if count_d == 1:
                    self.label_10.setText("Завтра")
                    self.label_13.setPixmap(QPixmap(icons_128[data["forecasts"][1]["parts"]["day"]["icon"]]))
                    self.label_13.setAlignment(Qt.AlignCenter)
                    if data["forecasts"][1]["parts"]["day"]["temp_max"] > 0:
                        self.label_12.setText("+" + str(data["forecasts"][1]["parts"]["day"]["temp_max"]))
                    elif data["forecasts"][1]["parts"]["day"]["temp_max"] < 0:
                        self.label_12.setText("-" + str(data["forecasts"][1]["parts"]["day"]["temp_max"]))
                    else:
                        self.label_12.setText(str(data["forecasts"][1]["parts"]["day"]["temp_max"]))

                    if data["forecasts"][1]["parts"]["day"]["temp_min"] > 0:
                        self.label_11.setText("+" + str(data["forecasts"][1]["parts"]["day"]["temp_min"]))
                    elif data["forecasts"][1]["parts"]["day"]["temp_min"] < 0:
                        self.label_11.setText("-" + str(data["forecasts"][1]["parts"]["day"]["temp_min"]))
                    else:
                        self.label_11.setText(str(data["forecasts"][1]["parts"]["day"]["temp_min"]))

                if count_d == 2:
                    date = data["forecasts"][2]["date"]
                    year, month, day = list(map(str, str(date).split('-')))
                    self.label_14.setText(f"{str(day).zfill(2)} {months_short[month]}")
                    self.label_17.setPixmap(QPixmap(icons_128[data["forecasts"][2]["parts"]["day"]["icon"]]))
                    self.label_17.setAlignment(Qt.AlignCenter)
                    if data["forecasts"][2]["parts"]["day"]["temp_max"] > 0:
                        self.label_16.setText("+" + str(data["forecasts"][2]["parts"]["day"]["temp_max"]))
                    elif data["forecasts"][2]["parts"]["day"]["temp_max"] < 0:
                        self.label_16.setText("-" + str(data["forecasts"][2]["parts"]["day"]["temp_max"]))
                    else:
                        self.label_16.setText(str(data["forecasts"][2]["parts"]["day"]["temp_max"]))

                    if data["forecasts"][2]["parts"]["day"]["temp_min"] > 0:
                        self.label_15.setText("+" + str(data["forecasts"][2]["parts"]["day"]["temp_min"]))
                    elif data["forecasts"][2]["parts"]["day"]["temp_min"] < 0:
                        self.label_15.setText("-" + str(data["forecasts"][2]["parts"]["day"]["temp_min"]))
                    else:
                        self.label_15.setText(str(data["forecasts"][2]["parts"]["day"]["temp_min"]))

                if count_d == 3:
                    date = data["forecasts"][3]["date"]
                    year, month, day = list(map(str, str(date).split('-')))
                    self.label_26.setText(f"{str(day).zfill(2)} {months_short[month]}")
                    self.label_29.setPixmap(QPixmap(icons_128[data["forecasts"][3]["parts"]["day"]["icon"]]))
                    self.label_29.setAlignment(Qt.AlignCenter)
                    if data["forecasts"][3]["parts"]["day"]["temp_max"] > 0:
                        self.label_28.setText("+" + str(data["forecasts"][3]["parts"]["day"]["temp_max"]))
                    elif data["forecasts"][3]["parts"]["day"]["temp_max"] < 0:
                        self.label_28.setText("-" + str(data["forecasts"][3]["parts"]["day"]["temp_max"]))
                    else:
                        self.label_28.setText(str(data["forecasts"][3]["parts"]["day"]["temp_max"]))

                    if data["forecasts"][3]["parts"]["day"]["temp_min"] > 0:
                        self.label_27.setText("+" + str(data["forecasts"][3]["parts"]["day"]["temp_min"]))
                    elif data["forecasts"][3]["parts"]["day"]["temp_min"] < 0:
                        self.label_27.setText("-" + str(data["forecasts"][3]["parts"]["day"]["temp_min"]))
                    else:
                        self.label_27.setText(str(data["forecasts"][3]["parts"]["day"]["temp_min"]))

                if count_d == 4:
                    date = data["forecasts"][4]["date"]
                    year, month, day = list(map(str, str(date).split('-')))
                    self.label_30.setText(f"{str(day).zfill(2)} {months_short[month]}")
                    self.label_33.setPixmap(QPixmap(icons_128[data["forecasts"][4]["parts"]["day"]["icon"]]))
                    self.label_33.setAlignment(Qt.AlignCenter)
                    if data["forecasts"][4]["parts"]["day"]["temp_max"] > 0:
                        self.label_32.setText("+" + str(data["forecasts"][4]["parts"]["day"]["temp_max"]))
                    elif data["forecasts"][4]["parts"]["day"]["temp_max"] < 0:
                        self.label_32.setText("-" + str(data["forecasts"][4]["parts"]["day"]["temp_max"]))
                    else:
                        self.label_32.setText(str(data["forecasts"][4]["parts"]["day"]["temp_max"]))

                    if data["forecasts"][4]["parts"]["day"]["temp_min"] > 0:
                        self.label_31.setText("+" + str(data["forecasts"][4]["parts"]["day"]["temp_min"]))
                    elif data["forecasts"][4]["parts"]["day"]["temp_min"] < 0:
                        self.label_31.setText("-" + str(data["forecasts"][4]["parts"]["day"]["temp_min"]))
                    else:
                        self.label_31.setText(str(data["forecasts"][4]["parts"]["day"]["temp_min"]))

                if count_d == 5:
                    date = data["forecasts"][5]["date"]
                    year, month, day = list(map(str, str(date).split('-')))
                    self.label_34.setText(f"{str(day).zfill(2)} {months_short[month]}")
                    self.label_37.setPixmap(QPixmap(icons_128[data["forecasts"][5]["parts"]["day"]["icon"]]))
                    self.label_37.setAlignment(Qt.AlignCenter)
                    if data["forecasts"][5]["parts"]["day"]["temp_max"] > 0:
                        self.label_36.setText("+" + str(data["forecasts"][5]["parts"]["day"]["temp_max"]))
                    elif data["forecasts"][5]["parts"]["day"]["temp_max"] < 0:
                        self.label_36.setText("-" + str(data["forecasts"][5]["parts"]["day"]["temp_max"]))
                    else:
                        self.label_36.setText(str(data["forecasts"][5]["parts"]["day"]["temp_max"]))

                    if data["forecasts"][5]["parts"]["day"]["temp_min"] > 0:
                        self.label_35.setText("+" + str(data["forecasts"][5]["parts"]["day"]["temp_min"]))
                    elif data["forecasts"][5]["parts"]["day"]["temp_min"] < 0:
                        self.label_35.setText("-" + str(data["forecasts"][5]["parts"]["day"]["temp_min"]))
                    else:
                        self.label_35.setText(str(data["forecasts"][5]["parts"]["day"]["temp_min"]))

                if count_d == 6:
                    date = data["forecasts"][6]["date"]
                    year, month, day = list(map(str, str(date).split('-')))
                    self.label_38.setText(f"{str(day).zfill(2)} {months_short[month]}")
                    self.label_41.setPixmap(QPixmap(icons_128[data["forecasts"][6]["parts"]["day"]["icon"]]))
                    self.label_41.setAlignment(Qt.AlignCenter)
                    if data["forecasts"][6]["parts"]["day"]["temp_max"] > 0:
                        self.label_40.setText("+" + str(data["forecasts"][6]["parts"]["day"]["temp_max"]))
                    elif data["forecasts"][6]["parts"]["day"]["temp_max"] < 0:
                        self.label_40.setText("-" + str(data["forecasts"][6]["parts"]["day"]["temp_max"]))
                    else:
                        self.label_40.setText(str(data["forecasts"][6]["parts"]["day"]["temp_max"]))

                    if data["forecasts"][6]["parts"]["day"]["temp_min"] > 0:
                        self.label_39.setText("+" + str(data["forecasts"][6]["parts"]["day"]["temp_min"]))
                    elif data["forecasts"][6]["parts"]["day"]["temp_min"] < 0:
                        self.label_39.setText("-" + str(data["forecasts"][6]["parts"]["day"]["temp_min"]))
                    else:
                        self.label_39.setText(str(data["forecasts"][6]["parts"]["day"]["temp_min"]))

                # if count_d == 7:
                #     date = data["forecasts"][7]["date"]
                #     year, month, day = list(map(str, str(date).split('-')))
                #     self.label_42.setText(f"{str(day).zfill(2)} {months_short[month]}")
                #     self.label_45.setPixmap(QPixmap(icons_128[data["forecasts"][7]["parts"]["day"]["icon"]]))
                #     self.label_45.setAlignment(Qt.AlignCenter)
                #     if data["forecasts"][7]["parts"]["day"]["temp_max"] > 0:
                #         self.label_44.setText("+" + str(data["forecasts"][7]["parts"]["day"]["temp_max"]))
                #     elif data["forecasts"][7]["parts"]["day"]["temp_max"] < 0:
                #         self.label_44.setText("-" + str(data["forecasts"][7]["parts"]["day"]["temp_max"]))
                #     else:
                #         self.label_44.setText(str(data["forecasts"][7]["parts"]["day"]["temp_max"]))
                #
                #     if data["forecasts"][7]["parts"]["day"]["temp_min"] > 0:
                #         self.label_43.setText("+" + str(data["forecasts"][7]["parts"]["day"]["temp_min"]))
                #     elif data["forecasts"][7]["parts"]["day"]["temp_min"] < 0:
                #         self.label_43.setText("-" + str(data["forecasts"][7]["parts"]["day"]["temp_min"]))
                #     else:
                #         self.label_43.setText(str(data["forecasts"][7]["parts"]["day"]["temp_min"]))
                #
                # if count_d == 8:
                #     date = data["forecasts"][8]["date"]
                #     year, month, day = list(map(str, str(date).split('-')))
                #     self.label_46.setText(f"{str(day).zfill(2)} {months_short[month]}")
                #     self.label_49.setPixmap(QPixmap(icons_128[data["forecasts"][8]["parts"]["day"]["icon"]]))
                #     self.label_49.setAlignment(Qt.AlignCenter)
                #     if data["forecasts"][8]["parts"]["day"]["temp_max"] > 0:
                #         self.label_48.setText("+" + str(data["forecasts"][8]["parts"]["day"]["temp_max"]))
                #     elif data["forecasts"][8]["parts"]["day"]["temp_max"] < 0:
                #         self.label_48.setText("-" + str(data["forecasts"][8]["parts"]["day"]["temp_max"]))
                #     else:
                #         self.label_48.setText(str(data["forecasts"][8]["parts"]["day"]["temp_max"]))
                #
                #     if data["forecasts"][8]["parts"]["day"]["temp_min"] > 0:
                #         self.label_47.setText("+" + str(data["forecasts"][8]["parts"]["day"]["temp_min"]))
                #     elif data["forecasts"][8]["parts"]["day"]["temp_min"] < 0:
                #         self.label_47.setText("-" + str(data["forecasts"][8]["parts"]["day"]["temp_min"]))
                #     else:
                #         self.label_47.setText(str(data["forecasts"][8]["parts"]["day"]["temp_min"]))
                #
                # if count_d == 9:
                #     date = data["forecasts"][9]["date"]
                #     year, month, day = list(map(str, str(date).split('-')))
                #     self.label_50.setText(f"{str(day).zfill(2)} {months_short[month]}")
                #     self.label_53.setPixmap(QPixmap(icons_128[data["forecasts"][9]["parts"]["day"]["icon"]]))
                #     self.label_53.setAlignment(Qt.AlignCenter)
                #     if data["forecasts"][9]["parts"]["day"]["temp_max"] > 0:
                #         self.label_52.setText("+" + str(data["forecasts"][9]["parts"]["day"]["temp_max"]))
                #     elif data["forecasts"][9]["parts"]["day"]["temp_max"] < 0:
                #         self.label_52.setText("-" + str(data["forecasts"][9]["parts"]["day"]["temp_max"]))
                #     else:
                #         self.label_52.setText(str(data["forecasts"][9]["parts"]["day"]["temp_max"]))
                #
                #     if data["forecasts"][9]["parts"]["day"]["temp_min"] > 0:
                #         self.label_51.setText("+" + str(data["forecasts"][9]["parts"]["day"]["temp_min"]))
                #     elif data["forecasts"][9]["parts"]["day"]["temp_min"] < 0:
                #         self.label_51.setText("-" + str(data["forecasts"][9]["parts"]["day"]["temp_min"]))
                #     else:
                #         self.label_51.setText(str(data["forecasts"][9]["parts"]["day"]["temp_min"]))

    def home_page_f(self):
        self.stackedWidget.setCurrentIndex(0)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.addb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.profileb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")

    def search_page_f(self):
        self.stackedWidget.setCurrentIndex(1)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")
        self.addb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.profileb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")

        self.layout = QVBoxLayout()

        cities = [x[0] for x in list(cur.execute("SELECT Город FROM city").fetchall())]
        print(cities)
        completer = QCompleter(cities)
        completer.popup().setStyleSheet("""
                    QListView {
                        background-color: #f0f0f0;
                        border: 2px solid #333;
                        border-radius: 5px;
                    }
                    QListView:item {
                        padding: 5px;
                        background-color: #000;
                    }
                    QListView:item:selected {
                        background-color: #00f;
                        color: #fff;
                    }
                """)

        self.search_le.setCompleter(completer)
        self.layout.addWidget(self.search_le)

        self.setLayout(self.layout)

    def add_page_f(self):
        self.stackedWidget.setCurrentIndex(2)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.addb.setStyleSheet("background-color: rgba(255, 255, 255, 100);\nborder: none;\nborder-radius: 15px;")
        self.profileb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")

    def profile_page_f(self):
        self.stackedWidget.setCurrentIndex(3)
        self.homeb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.searchb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
        self.addb.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;\nborder-radius: 15px;")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
