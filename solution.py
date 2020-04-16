from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
import requests
import sys
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5 import uic


class Maps(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('kar.ui', self)
        self.coords = '41.44326,52.73169'
        self.mash = 5
        self.izobrazhenie()

    def keyPressEvent(self, event):
        try:
            if event.key() == QtCore.Qt.Key_PageUp:
                if 0 <= int(self.mash) < 18:
                    self.mash += 1
                    self.izobrazhenie()
            if event.key() == QtCore.Qt.Key_PageDown:
                if 0 < int(self.mash) <= 18:
                    self.mash -= 1
                    self.izobrazhenie()
        except:
            pass

    def izobrazhenie(self):
        url = "http://static-maps.yandex.ru/1.x/"
        params = {'ll': self.coords, 'z': f'{self.mash}', 'l': 'map'}
        response = requests.get(url, params=params).content

        with open("карта.png", "wb") as file:
            file.write(response)
        self.ret_kar()

    def ret_kar(self):
        self.pix = QPixmap("карта.png")
        self.label_1.setPixmap(self.pix)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    n = Maps()
    n.show()
    sys.exit(app.exec())
