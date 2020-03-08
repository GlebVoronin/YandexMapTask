import requests
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtGui import QPixmap

coords = [139.56, 35.56]
scale = [0.005, 0.005]
size = (600, 450)


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, size[0], size[1])
        self.setWindowTitle('MainWindow')
        self.label = QLabel('', self)
        self.label.setGeometry(0, 0, size[0], size[1])
        geocoder_api_server = "https://static-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "ll": str(coords[0]) + ',' + str(coords[1]),
            "spn": str(scale[0]) + ',' + str(scale[1]),
            "z": "13",
            "l": "map"}
        try:
            response = requests.get(geocoder_api_server, params=geocoder_params)
            img = response.content
            file = open('new_img_for_yandex_map.png', 'wb')
            file.write(img)
            file.close()
            self.pixmap = QPixmap('new_img_for_yandex_map.png')
            self.label.setPixmap(self.pixmap)
        except Exception:
            print("error")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())
