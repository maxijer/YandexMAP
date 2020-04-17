from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
import requests
import sys
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import Qt
import math


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
        self.label_1.setFocus()
        self.shema.clicked.connect(self.map)
        self.sputn.clicked.connect(self.sput)
        self.gibr.clicked.connect(self.gibrid)
        self.isk.clicked.connect(lambda: self.poisk(True))
        self.cl.clicked.connect(self.clear)
        self.pochta.stateChanged.connect(self.check_index)

    def check_index(self):
        if not self.post:
            self.post = True
            self.poisk(self.drug)
        else:
            self.post = False
            self.poisk(self.drug)

    def map(self):
        self.typ = 'map'
        self.izobrazhenie()

    def poisk(self, drug):
        if drug:
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
        try:
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
            self.x = float(coordination[1])
            self.y = float(coordination[0])
            self.mesto = f'{self.y},{self.x},pm2rdm'
            self.izobrazhenie()
            self.label_1.setFocus()
        except:
            pass

    def clear(self):
        self.mesto = ''
        self.lineEdit.clear()
        self.lineEdit_2.clear()
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
                    try:
                        if self.post:
                            address += '\nПочтовый индекс: '
                            index = response['response']['GeoObjectCollection']['featureMember'][0][
                                'GeoObject']['metaDataProperty']['GeocoderMetaData']['Address'][
                                'postal_code']
                            address += index
                        self.lineEdit_2.setText(address)
                        self.drug = False
                        self.poisk(self.drug)
                    except:
                        self.lineEdit_2.setText(address)
                        self.drug = False
                        self.poisk(self.drug)
                except:
                    pass
        elif event.button() == Qt.RightButton:
            x_one = event.pos().x()
            y_one = event.pos().y()
            if 0 <= x_one < 600 and 0 <= y_one < 450:
                y = (y_one - 225) * 230 / 2 ** (self.mash + 8)
                x = (x_one - 300) * 360 / 2 ** (self.mash + 8)
                self.y += x
                self.x -= y
                self.mesto = f'{self.y},pm2rdm'
                self.drug = False
                self.rabota()

    def rabota(self):
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
            url = "https://search-maps.yandex.ru/v1/"
            params = {
                "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
                'results': 10,
                "lang": "ru_RU",
                'text': address,
                'spn': '0.005,0.005',
                "type": "biz",
            }
            response = requests.get(url, params=params)
            response = response.json()
            try:
                min_rast = 50
                blizko = ''
                for i in range(12):
                    try:
                        organization = response["features"][i]
                        y, x = organization["geometry"]["coordinates"]
                        rast = self.get_long([float(self.y), float(self.x)], [y, x])
                        if min_rast > rast:
                            min_rast = rast
                            blizko = organization
                    except:
                        pass
                try:
                    address = blizko['properties']['name']
                    print(address)
                    print(blizko['properties']['description'])
                    self.lineEdit_2.setText(blizko['properties']['description'])
                    self.label.setText(address)
                    self.y, self.x = blizko['geometry']['coordinates']
                    self.mesto = f'{self.y},pm2rdm'
                    self.poisk(self.drug)
                except:
                    self.poisk(self.drug)
            except:
                self.poisk(self.drug)
        except:
            self.poisk(self.drug)

    def get_long(self, a, b):  # было в задачах по первому maps API
        degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
        a_lon, a_lat = a
        b_lon, b_lat = b

        # Берем среднюю по широте точку и считаем коэффициент для нее.
        radians_lattitude = math.radians((a_lat + b_lat) / 2.)
        lat_lon_factor = math.cos(radians_lattitude)

        # Вычисляем смещения в метрах по вертикали и горизонтали.
        dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
        dy = abs(a_lat - b_lat) * degree_to_meters_factor

        # Вычисляем расстояние между точками.
        distance = math.sqrt(dx * dx + dy * dy)

        return distance

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
        if self.typ != 'map':
            one = "карта.jpg"
        else:
            one = "карта.png"
        with open(one, "wb") as file:
            file.write(response)
        self.ret_kar(one)

    def ret_kar(self, chto):
        self.pix = QPixmap(chto)
        self.label_1.setPixmap(self.pix)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    n = Maps()
    n.show()
    sys.exit(app.exec())
