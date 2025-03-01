import requests

AUTH_TOKEN = 'Ваш токен.'


class YandexDisk:
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk'

    def __init__(self, oauth_token):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'Authorization': f'OAuth {oauth_token}'}

    def get_disk_info(self):
        response = requests.get(f'{self.BASE_URL}/', headers=self.headers)
        print(f'Информация о диске: {response.json()}')
        return self._handle_response(response)

    def list_files(self, path):
        params = {'path': path}
        response = requests.get(f'{self.BASE_URL}/resources', headers=self.headers, params=params)
        print(f'Информация о папке {path.strip("/")}: {list(elem["name"] for elem in response.json()["_embedded"]["items"])}')
        return self._handle_response(response)

    def create_folder(self, path):
        params = {'path': path}
        response = requests.put(f'{self.BASE_URL}/resources', headers=self.headers, params=params)
        return response.status_code == 201 or self._handle_response(response)

    def upload_file(self, file_path, disk_path):
        params = {'path': disk_path, 'overwrite': 'true'}
        response = requests.get(f'{self.BASE_URL}/resources/upload', headers=self.headers, params=params)
        if response.status_code == 200:
            upload_url = response.json()['href']
            with open(file_path, 'rb') as f:
                upload_response = requests.put(upload_url, files={'file': f})
            return upload_response.status_code == 201 or self._handle_response(upload_response)
        else:
            return self._handle_response(response)

    def download_file(self, disk_path, save_path):
        params = {'path': disk_path}
        response = requests.get(f'{self.BASE_URL}/resources/download', headers=self.headers, params=params)
        if response.status_code == 200:
            download_url = response.json()['href']
            download_response = requests.get(download_url)
            with open(save_path, 'wb') as f:
                f.write(download_response.content)
        else:
            return self._handle_response(response)

    def move_file(self, source_path, target_path):
        params = {'from': source_path, 'path': target_path, 'overwrite': 'true'}
        response = requests.post(f'{self.BASE_URL}/resources/move', headers=self.headers, params=params)
        return response.status_code == 201 or self._handle_response(response)

    def delete_file(self, path):
        params = {'path': path}
        response = requests.delete(f'{self.BASE_URL}/resources', headers=self.headers, params=params)
        return response.status_code == 204 or self._handle_response(response)

    def clear_trash(self):
        response = requests.delete(f'{self.BASE_URL}/trash/resources', headers=self.headers)
        return response.status_code == 204 or self._handle_response(response)

    def _handle_response(self, response):
        try:
            if response.status_code in [200, 201, 204]:
                return True

            error_info = response.json()
            print(
                f"Ошибка: {error_info.get('message', 'Неизвестная ошибка')} ({error_info.get('error', 'UnknownError')})")
            print(f"Описание: {error_info.get('description', 'Описание отсутствует')}")
        except Exception as e:
            print(f"Ошибка обработки ответа: {e}")
            print(f"HTTP статус: {response.status_code}")
            print(f"Ответ: {response.text}")
        return False


def main():
    disk = YandexDisk(AUTH_TOKEN)

    while True:
        print("\nВыберите действие (0 - 8):")
        print("1. Информация о диске")
        print("2. Список файлов")
        print("3. Создать папку")
        print("4. Загрузить файл")
        print("5. Скачать файл")
        print("6. Переместить файл")
        print("7. Удалить файл")
        print("8. Очистить корзину")
        print("0. Выход")

        choice = input("> ")

        if choice == '1':
            disk.get_disk_info()
        elif choice == '2':
            path = input("Введите путь к папке: ")
            disk.list_files(path)
        elif choice == '3':
            path = input("Введите путь к новой папке: ")
            if disk.create_folder(path):
                print("Папка создана")
            else:
                print("Ошибка создания папки")
        elif choice == '4':
            file_path = input("Введите путь к файлу на компьютере: ")
            disk_path = input("Введите путь к файлу на диске: ")
            if disk.upload_file(file_path, disk_path):
                print("Файл загружен")
            else:
                print("Ошибка загрузки файла")
        elif choice == '5':
            disk_path = input("Введите путь к файлу на диске: ")
            save_path = input("Введите путь для сохранения файла: ")
            if disk.download_file(disk_path, save_path):
                print("Файл скачан")
            else:
                print("Ошибка скачивания файла")
        elif choice == '6':
            source_path = input("Введите путь к файлу для перемещения: ")
            target_path = input("Введите новый путь к файлу: ")
            if disk.move_file(source_path, target_path):
                print("Файл перемещен")
            else:
                print("Ошибка перемещения файла")
        elif choice == '7':
            path = input("Введите путь к файлу для удаления: ")
            if disk.delete_file(path):
                print("Файл удален")
            else:
                print("Ошибка удаления файла")
        elif choice == '8':
            if disk.clear_trash():
                print("Корзина очищена")
            else:
                print("Ошибка очистки корзины")
        elif choice == '0':
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
