import sys
import requests
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QHBoxLayout
)
from PyQt6.QtGui import QPixmap

DADATA_TOKEN = 'Ваш токен.'
DADATA_SECRET_KEY = 'Ваш секретный ключ.'
YANDEX_MAP_APIKEY = 'Ваш API ключ.'


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Geolocation App")
        self.setFixedSize(670, 540)

        layout = QVBoxLayout()
        self.setLayout(layout)

        input_layout = QHBoxLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Address", "City", "Country", "Postal Code"])
        input_layout.addWidget(self.type_combo)

        self.input_field = QLineEdit()
        input_layout.addWidget(self.input_field)
        layout.addLayout(input_layout)

        button_layout = QHBoxLayout()
        self.search_button = QPushButton("Поиск")
        self.search_button.clicked.connect(self.find_location)
        button_layout.addWidget(self.search_button)

        clear_button = QPushButton("Очистить данные")
        clear_button.clicked.connect(self.input_field.clear)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        self.map_label = QLabel()
        layout.addWidget(self.map_label)

        self.setStyleSheet('''
        QWidget {
    font-family: Arial;
    background-color: #f0f0f0;
}

QLabel {
    color: #333;
}

QComboBox, QLineEdit {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px;
}

QPushButton {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 15px;
}
''')

    def find_location(self):
        selected_type = self.type_combo.currentText()
        address_input = self.input_field.text().strip()

        if not address_input:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста введите запрос.")
            return

        try:
            params = self.create_params(selected_type, address_input)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"{e}")
            return

        dadata_api_server = f"http://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Token  " + DADATA_TOKEN,
            "X-Secret": DADATA_SECRET_KEY
        }

        dadata_params = {
            'query': params['query']
        }

        response = requests.get(dadata_api_server, params=dadata_params, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            if json_response["suggestions"]:
                toponym = json_response["suggestions"][0]["data"]
                if toponym["geo_lon"] is not None and toponym["geo_lat"] is not None:
                    toponym_coord = f"{toponym['geo_lon']},{toponym['geo_lat']}"
                    map_api_server = 'https://static-maps.yandex.ru/v1'
                    map_params = {
                        'apikey': YANDEX_MAP_APIKEY,
                        'll': toponym_coord,
                        'size': '650,450',
                        'z': params['z'],
                        'lang': 'ru_RU',
                    }

                    map_response = requests.get(map_api_server, params=map_params)
                    if map_response.status_code == 200:
                        pixmap = QPixmap()
                        pixmap.loadFromData(map_response.content)
                        self.map_label.setPixmap(pixmap)
                        QMessageBox.information(self, "Информация", "Карта создана успешно.")
                    else:
                        QMessageBox.information(self, "Информация", "Не нашли карту под ваш запрос.")
                else:
                    QMessageBox.warning(self, "Ошибка", 'Не хватает информации, дополните запрос.')
                    return
            else:
                QMessageBox.warning(self, "Ошибка", 'Нет данных по вашему запросу.')
                return
        else:
            QMessageBox.warning(self, "Ошибка", f'Ошибка {response.status_code}, попробуйте позже.')
            return

    def create_params(self, selected_type: str, address_input: str) -> dict[str, str]:
        zoom_levels = {
            "Address": "17",
            "City": "13",
            "Country": "4",
            "Postal Code": "17"
        }
        try:
            zoom = zoom_levels[selected_type]
        except KeyError:
            raise ValueError("Invalid address type selected.")
        return {"query": address_input, "z": zoom}


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
