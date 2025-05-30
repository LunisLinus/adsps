import requests
import os
import get_token

# Полные пути к файлам для UNIX-систем
# USERNAME = 'ligma'
# TOKEN_FILE = f'/Users/{USERNAME}/Desktop/CS&IT/PythonProject/БД/7 задание/TOKEN.txt'

# Путь для сохранения файла с access_token:
TOKEN_FILE = 'TOKEN.txt'

long = True
TOKEN = ''

if os.path.exists(TOKEN_FILE):
    if input('Я обнаружил файл с токеном, загружаем его? Введите 1 для загрузки, Enter, если не хотите загружать: ') == '1':
        with open(TOKEN_FILE, 'r') as f:
            TOKEN = f.read()
            print('Токен был успешно загружен!')

if TOKEN == '':
    sh = input('Введите свой токен. Если он неизвестен, то введите 1:\n\t ')

    if sh == '1':
        TOKEN = get_token.get_token()
        print(f'Ваш токен: {TOKEN}')
        if input('Хотите ли Вы сохранить токен в файле? Введите 1, чтобы сохранить: ') == '1':
            with open(TOKEN_FILE, 'w') as f:
                f.write(TOKEN)
                print('Токен был успешно записан!')
    elif sh == '':
        try:
            with open(TOKEN_FILE, 'r') as f:
                TOKEN = f.read()
                print('Токен был успешно загружен!')

        except FileNotFoundError:
            exit('Файла с токеном не было!')
    else:
        TOKEN = sh

class YaCloud:
    B_URL = 'https://cloud-api.yandex.net/v1/disk'

    def __init__(self, oauth_token):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'Authorization': f'OAuth {oauth_token}'}

    def get_disk_info(self):
        response = requests.get(f'{self.B_URL}/', headers=self.headers)
        print(f'Информация о диске: {response.json()}')
        return self.response(response)

    def list_files(self, path):
        params = {'path': path}
        response = requests.get(f'{self.B_URL}/resources', headers=self.headers, params=params)
        print(f'Информация о папке {path.strip("/")}: {list(elem["name"] for elem in response.json()["_embedded"]["items"])}')
        return self.response(response)

    def create_folder(self, path):
        params = {'path': path}
        response = requests.put(f'{self.B_URL}/resources', headers=self.headers, params=params)
        return response.status_code == 201 or self.response(response)

    def upload_file(self, file_path, disk_path):
        params = {'path': disk_path, 'overwrite': 'true'}
        response = requests.get(f'{self.B_URL}/resources/upload', headers=self.headers, params=params)
        if response.status_code == 200:
            upload_url = response.json()['href']
            with open(file_path, 'rb') as f:
                upload_response = requests.put(upload_url, files={'file': f})
            return upload_response.status_code == 201 or self.response(upload_response)
        else:
            return self.response(response)

    def download_file(self, disk_path, save_path):
        params = {'path': disk_path}
        response = requests.get(f'{self.B_URL}/resources/download', headers=self.headers, params=params)
        if response.status_code == 200:
            download_url = response.json()['href']
            download_response = requests.get(download_url)
            with open(save_path, 'wb') as f:
                f.write(download_response.content)
        else:
            return self.response(response)

    def move_file(self, source_path, target_path):
        params = {'from': source_path, 'path': target_path, 'overwrite': 'true'}
        response = requests.post(f'{self.B_URL}/resources/move', headers=self.headers, params=params)
        return response.status_code == 201 or self.response(response)

    def delete_file(self, path):
        params = {'path': path}
        response = requests.delete(f'{self.B_URL}/resources', headers=self.headers, params=params)
        return response.status_code == 204 or self.response(response)

    def clear_trash(self):
        response = requests.delete(f'{self.B_URL}/trash/resources', headers=self.headers)
        return response.status_code == 204 or self.response(response)

    def response(self, response):
        try:
            # Краткий экскурс по кодам HTTP:
            # 200 - OK
            # 201 - Создано
            # 204 - Всё прошло успешно, но данных нет
            if response.status_code in [200, 201, 204]:
                return True

            error_info = response.json()
            print(
                f"Ошибка: {error_info.get('message', 'Неизвестная ошибка')} ({error_info.get('error', 'UnknownError')})")
            print(f"Описание: {error_info.get('description', 'Описание отсутствует')}")
        except Exception as shit:
            print(f"Ошибка обработки ответа: {shit}")
            print(f"HTTP статус: {response.status_code}")
            print(f"Ответ: {response.text}")
        return False


disk = YaCloud(TOKEN)

while True:
    if long:
        print("\nВыберите действие:")
        print("1. Информация о диске")
        print("2. Список файлов")
        print("3. Создать папку")
        print("4. Загрузить файл")
        print("5. Скачать файл")
        print("6. Переместить файл")
        print("7. Удалить файл")
        print("8. Очистить корзину")
        print("9. Сократить данное меню")
        print("0. Управление/сохранение токенов")
        print("Enter. Выход")
    else:
        print("1. Инфо ; 2. Список ; 3. Создать ; 4. Загрузить ; 5. Скачать ; 6. Переместить ; 7. Удалить ; 8. Очистить корзину ; 9. Увеличить меню ; 0. Токены ; Enter. Выход")

    ch = input('\t')

    if ch == '1':
        disk.get_disk_info()
    elif ch == '2':
        path = input("Введите путь к папке: ")
        disk.list_files(path)
    elif ch == '3':
        path = input("Введите путь к новой папке: ")
        if disk.create_folder(path):
            print("Папка создана")
        else:
            print("Ошибка создания папки")
    elif ch == '4':
        file_path = input("Введите путь к файлу на компьютере: ")
        disk_path = input("Введите путь к файлу на диске: ")
        if disk.upload_file(file_path, disk_path):
            print("Файл загружен")
        else:
            print("Ошибка загрузки файла")
    elif ch == '5':
        disk_path = input("Введите путь к файлу на диске: ")
        save_path = input("Введите путь для сохранения файла: ")
        if disk.download_file(disk_path, save_path):
            print("Файл скачан")
        else:
            print("Ошибка скачивания файла")
    elif ch == '6':
        source_path = input("Введите путь к файлу для перемещения: ")
        target_path = input("Введите новый путь к файлу: ")
        if disk.move_file(source_path, target_path):
            print("Файл перемещен")
        else:
            print("Ошибка перемещения файла")
    elif ch == '7':
        path = input("Введите путь к файлу для удаления: ")
        if disk.delete_file(path):
            print("Файл удален")
        else:
            print("Ошибка удаления файла")
    elif ch == '8':
        if disk.clear_trash():
            print("Корзина очищена")
        else:
            print("Ошибка очистки корзины")
    elif ch == '9':
        if long:
            long = False
        else:
            long = True
    elif ch == '0':
        print('Что Вы хотите сделать?')
        print('1. Посмотреть токен')
        print('2. Сохранить токен')
        print('3. Удалить токен')
        print('Enter. Выйти')
        sh2 = input('\t')
        if sh2 == '1':
            print('Вот ваш токен, никому его не сообщайте! Его спрашивают ТОЛЬКО мошенники!')
            print(TOKEN)
        elif sh2 == '2':
            with open(TOKEN_FILE, 'w') as f:
                f.write(TOKEN)
                print('Токен был успешно записан!')
        elif sh2 == '3':
            if input('Вы действительно хотите удалить сохранённый токен? Введите 1 для подтверждения: ') == '1':
                try:
                    os.remove(TOKEN_FILE)
                except FileNotFoundError:
                    print('А токен и так не был записан :)')
        elif sh2 == '':
            continue
        else:
            print('Я Вас не понял, простите, можете повторить свой запрос?')
    elif ch == '':
        exit('Пока!')
    else:
        print("Неверный выбор!")

# Убрал if __name__ == "__main__", думаю, что первокурсникам ещё рано писать такие строчки
