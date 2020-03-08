import requests
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, QEvent

coords = [139.56, 35.56]
scale = [0.005, 0.005]
size = (600, 450)


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def load_map(self):
        geocoder_api_server = "https://static-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "ll": str(coords[0]) + ',' + str(coords[1]),
            "spn": str(scale[0]) + ',' + str(scale[1]),
            "z": "13",
            "l": "map"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        image = response.content
        file = open('new_img_for_yandex_map.png', 'wb')
        file.write(image)
        file.close()
        self.pixmap = QPixmap('new_img_for_yandex_map.png')
        self.label.setPixmap(self.pixmap)

    def initUI(self):

        self.setGeometry(0, 0, size[0], size[1])
        self.setWindowTitle('MainWindow')
        self.label = QLabel('', self)
        self.label.setGeometry(0, 0, size[0], size[1])
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
