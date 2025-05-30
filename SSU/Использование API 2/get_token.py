import subprocess
import webbrowser
import json

'''
Данный файл позволяет сделать удобное получение "access_token" от Яндекса
Для работы надо вставить 2 токена в константы CLIENT_ID и CLIENT_SECRET

ACHTUNG! Данные ключи НИКОМУ сообщать нельзя :)

Краткий гайд для получения этих 2-х OAuth-токенов:

1.  Зайдите на сайт: https://oauth.yandex.ru/client/new/ и создайте приложение
    Добавьте в поле "Доступ к данным":
    cloud_api:disk.write
    cloud_api:disk.read
    cloud_api:disk.app_folder
    cloud_api:disk.info
    cloud_api.data:app_data
    cloud_api.data:user_data
    cloud:auth
    yadisk:disk

2.  Создайте приложение, и впишите в поле "Redirect URI для веб-сервисов"
    https://oauth.yandex.ru/verification_code
    (Он может стоять там по дефолту)

3.  Копипастните CLIENT_ID и CLIENT_SECRET в константы снизу

P.S. Вся работа программы с диском - работа Сони! Я просто добавил немного косметических изменений и удобное получение токена
'''

def get_token():
    CLIENT_ID = "ВВЕДИТЕ СВОИ ДАННЫЕ"
    CLIENT_SECRET = "ВВЕДИТЕ СВОИ ДАННЫЕ"
    REDIRECT_URI = "https://oauth.yandex.ru/verification_code"

    auth_url = f"https://oauth.yandex.ru/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    print("Откройте ссылку в браузере для авторизации:")
    print(auth_url)
    webbrowser.open(auth_url)

    CODE = input("Введите код: ")

    # Знаю, это стыдный костыль, но иначе яндекс мне выдаёт ответ в HTML-формате
    cmd = [
        'curl', '-X', 'POST', 'https://oauth.yandex.ru/token',
        '-H', 'Content-Type: application/x-www-form-urlencoded',
        '-d', 'grant_type=authorization_code',
        '-d', f'code={CODE}',
        '-d', f'client_id={CLIENT_ID}',
        '-d', f'client_secret={CLIENT_SECRET}'
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        token_data = json.loads(res.stdout)
        access_token = token_data.get("access_token")

        if access_token:
            print('\nАвторизация прошла успешно!')
            return access_token
        else:
            print("\nERR, токен не найден в ответе!\nПолный ответ сервера:")
            print(res.stdout)
            exit()

    except Exception as shit:
        print("\nТут даже Бог не поможет...\nПолный ответ сервера:")
        print(shit)
        print(res.stdout)
        exit()
