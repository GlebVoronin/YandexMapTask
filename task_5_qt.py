import requests
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from map_scale.map_scale import map_scale

coords = [139.56, 35.56]
scale = [0.005, 0.005]
size = (600, 450)
l_list = ['map', 'sat', 'sat,skl']
l_index = 0
geocoder_api_server = "https://static-maps.yandex.ru/1.x/"
map_api_server = "http://static-maps.yandex.ru/1.x/"
point = None


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def _up_l_index(self):
        global l_index
        l_index += 1
        self.load_map()

    def load_map(self):
        global point
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "ll": str(coords[0]) + ',' + str(coords[1]),
            "spn": str(scale[0]) + ',' + str(scale[1]),
            "z": "13",
            "l": l_list[l_index % len(l_list)]}
        if point is not None and not point.isspace():
            geocoder_params["pt"] = "{0},pm2dgl".format(point)
            point = None
        response = requests.get(geocoder_api_server, params=geocoder_params)
        image = response.content
        file = open('new_img_for_yandex_map.png', 'wb')
        file.write(image)
        file.close()
        self.pixmap = QPixmap('new_img_for_yandex_map.png', 'wb')
        self.label.setPixmap(self.pixmap)
        self.setFocus()

    def get_coords(self, name):
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/" \
                           + "?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
                           + f"={name}&format=json"
        response = requests.get(geocoder_request)
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        coords = toponym["Point"]["pos"].split()
        return [float(coords[0]), float(coords[1])], json_response

    def search(self):
        global coords, scale, point
        coords, json_response = self.get_coords(self.search_area.text())
        scale = map_scale(json_response)
        point = "{0},{1}".format(str(coords[0]), str(coords[1]))
        self.load_map()

    def initUI(self):
        self.setGeometry(0, 0, size[0], size[1] + 70)
        self.setWindowTitle('MainWindow')
        self.label = QLabel('', self)
        self.label.setGeometry(0, 0, size[0], size[1])
        self.layer_button = QPushButton('Сменить слой карты', self)
        width = self.layer_button.width()
        self.layer_button.move(size[0] - width - 10, 0)
        self.layer_button.clicked.connect(self._up_l_index)
        self.search_button = QPushButton('Искать', self)
        width = self.search_button.width()
        self.search_button.setGeometry(size[0] - width - 10, size[1] + 10, 100, 50)
        self.search_button.clicked.connect(self.search)
        self.search_area = QLineEdit(self)
        self.search_area.setGeometry(0, size[1] + 10, size[0] - width - 20, 50)
        try:
            self.load_map()
        except Exception:
            print("error")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if scale[0] < 10:
                scale[0] *= 2
                scale[1] *= 2
                self.load_map()
        elif event.key() == Qt.Key_PageDown:
            if scale[0] > 0.0001:
                scale[0] /= 2
                scale[1] /= 2
                self.load_map()
        elif event.key() == Qt.Key_Down:
            if coords[1] - scale[1] * 1.5 > -85:
                coords[1] -= scale[1] * 1.5
                self.load_map()
        elif event.key() == Qt.Key_Up:
            if coords[1] + scale[1] * 1.5 < 85:
                coords[1] += scale[1] * 1.5
                self.load_map()
        elif event.key() == Qt.Key_Right:
            if coords[0] + scale[0] * 1.5 < 180:
                coords[0] += scale[0] * 1.5
                self.load_map()
        elif event.key() == Qt.Key_Left:
            if coords[0] - scale[0] * 1.5 > -180:
                coords[0] -= scale[0] * 1.5
                self.load_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    ex.setFocus()
    ex.show()
    sys.exit(app.exec_())
