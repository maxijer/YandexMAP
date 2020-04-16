from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
import requests
import sys
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import Qt


class Maps(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('kar.ui', self)
        self.x = 52.73169
        self.y = 41.44326
        self.mash = 8
        self.mesto = ''
        self.drug = True
        self.post = False
        self.typ = 'map'
        self.izobrazhenie()
        self.shema.clicked.connect(self.map)
        self.sputn.clicked.connect(self.sput)
        self.gibr.clicked.connect(self.gibrid)
        self.isk.clicked.connect(self.poisk)
        self.cl.clicked.connect(self.clear)
        self.pochta.stateChanged.connect(self.check_index)

    def check_index(self):
        if not self.post:
            self.post = True
            self.poisk()
        else:
            self.post = False
            self.poisk()

    def map(self):
        self.typ = 'map'
        self.izobrazhenie()

    def poisk(self):
        if self.drug:
            text = self.lineEdit.text()
        else:
            text = self.lineEdit_2.text()
        url = 'http://geocode-maps.yandex.ru/1.x/'
        params = {
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'geocode': f'{text}',
            'format': 'json'
        }
        response = requests.get(url, params=params)
        response = response.json()
        print(response)
        address = response['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData']['text']
        if self.post:
            address += '\nПочтовый индекс: '
            index = response['response']['GeoObjectCollection']['featureMember'][0][
                'GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
            address += index
        self.lineEdit_2.setText(str(address))
        coordination = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
            'Point']['pos'].split()
        self.x = coordination[1]
        self.y = coordination[0]
        self.mesto = f'{self.y},{self.x},pm2rdm'
        self.izobrazhenie()

    def clear(self):
        self.mesto = ''
        self.lineEdit.clear()
        self.izobrazhenie()

    def sput(self):
        self.typ = 'sat'
        self.izobrazhenie()

    def gibrid(self):
        self.typ = 'sat,skl'
        self.izobrazhenie()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            y_one = event.pos().y()
            x_one = event.pos().x()
            if 0 <= x_one < 600 and 0 <= y_one < 450:
                x = (x_one - 300) * 360 / 2 ** (int(self.mash) + 8)
                y = (y_one - 225) * 230 / 2 ** (int(self.mash) + 8)
                self.x = float(self.x) - y
                self.y = x + float(self.y)
                self.mesto = f'{self.y},{self.x},pm2rdm'
                url = 'http://geocode-maps.yandex.ru/1.x/'
                params = {
                    'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                    'format': 'json',
                    'geocode': f'{self.y},{self.x}'
                }
                response = requests.get(url, params=params)
                try:
                    response = response.json()
                    address = response['response']['GeoObjectCollection'][
                        'featureMember'][0]['GeoObject']['metaDataProperty'][
                        'GeocoderMetaData']['text']
                    if self.post:
                        address += '\nПочтовый индекс: '
                        index = response['response']['GeoObjectCollection']['featureMember'][0][
                            'GeoObject']['metaDataProperty']['GeocoderMetaData']['Address'][
                            'postal_code']
                        address += index
                    self.lineEdit_2.setText(address)
                    self.drug = False
                    self.poisk()
                except BaseException:
                    pass

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
        if event.key() == QtCore.Qt.Key_Up:
            self.x += 0.05
            self.izobrazhenie()

        if event.key() == QtCore.Qt.Key_Down:
            self.x -= 0.05
            self.izobrazhenie()

        if event.key() == QtCore.Qt.Key_Left:
            self.y -= 0.05
            self.izobrazhenie()

        if event.key() == QtCore.Qt.Key_Right:
            self.y += 0.05
            self.izobrazhenie()

    def izobrazhenie(self):
        url = "http://static-maps.yandex.ru/1.x/"
        params = {'ll': f'{self.y},{self.x}', 'z': f'{self.mash}', 'l': f'{self.typ}',
                  'pt': self.mesto}
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
