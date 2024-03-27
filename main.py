import sys
from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        # Установка флага для отслеживания нажатия кнопки мыши
        self.mouse_pressed = False
        self.inside_area = False

        # Сохранение начальной позиции курсора при нажатии
        self.last_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.last_pos = event.pos()

            x1, y1 = 640, 290  # Пример координат левого верхнего угла области
            x2, y2 = 640 + 601, 290 + 251  # Пример координат правого нижнего угла области

            if (x1 <= event.x() <= x2 and y1 <= event.y() <= y2):
                self.inside_area = True
            else:
                self.inside_area = False

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False

    def mouseMoveEvent(self, event):
        if self.mouse_pressed and self.last_pos:
            delta = event.pos() - self.last_pos
            new_value = self.scrollArea.horizontalScrollBar().value() - delta.x()

            x1, y1 = 640, 290  # Пример координат левого верхнего угла области
            x2, y2 = 640 + 601, 290 + 251  # Пример координат правого нижнего угла области

            if self.mouse_pressed and self.inside_area or (x1 <= event.x() <= x2 and y1 <= event.y() <= y2):
                self.scrollArea.horizontalScrollBar().setValue(new_value)


            self.last_pos = event.pos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
