import sys
from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QLabel, QCompleter, QVBoxLayout
import sqlite3
import requests
import json
from weather_data import weather_data
from icons import icons_128, icons_256

connection = sqlite3.connect('cities.db')
cur = connection.cursor()


# with open('test_1.json', 'w') as f:
#     json.dump(response.json(), f, ensure_ascii=False, indent=4)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

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
