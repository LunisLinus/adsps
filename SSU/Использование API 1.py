import requests

DADATA_TOKEN = 'Ваш токен.'
DADATA_SECRET_KEY = 'Ваш секретный ключ.'
YANDEX_MAP_APIKEY = 'Ваш API ключ.'


def maps(coordinates: str, zoom: str):
    from io import BytesIO
    from PIL import Image
    import webbrowser
    map_api_server = 'https://static-maps.yandex.ru/v1'
    map_params = {
        'apikey': YANDEX_MAP_APIKEY,
        'll': coordinates,
        'size': '650,450',
        'z': zoom,
        'lang': 'ru_RU',
    }

    response = requests.get(map_api_server, params=map_params)
    if response.status_code == 200:
        webbrowser.open(response.url)
        Image.open(BytesIO(response.content)).show()
    else:
        print(f'Ошибка: {response.status_code}. Причина: {response.reason}.')


def dadata_api(params: dict):
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
        if json_response['suggestions']:
            toponym = json_response['suggestions'][0]['data']
            if toponym['geo_lon'] is not None and toponym['geo_lat'] is not None:
                toponym_coord = f"{toponym['geo_lon']},{toponym['geo_lat']}"
                maps(toponym_coord, params['z'])
            else:
                print('Уточните ваш запрос.')
        else:
            print('По вашему запросу нет данных.')
    else:
        print(
            f'Ошибка: {response.status_code}. Причина: {response.reason}. Можете попробовать уточнить запрос '
            f'дополнительной информацией.')


def create_params(action: int) -> dict[str, str]:
    def geo_address():
        address = input('Введите адрес: ')
        return address, '17'

    def geo_city():
        city = input('Введите город: ')
        return city, '13'

    def geo_country():
        country = input('Введите страну: ')
        return country, '4'

    def geo_mail_index():
        mail_index = input('Введите почтовый индекс и улицу: ')
        return mail_index, '17'

    actions_dict = {
        1: geo_address,
        2: geo_city,
        3: geo_country,
        4: geo_mail_index
    }

    res = actions_dict[action]()

    return {'query': res[0], 'z': res[1]}


def main():
    while True:
        action = input('''Как вы хотите узнать адрес объекта?
1. Адрес
2. Город
3. Страна
4. Почтовый индекс
5. Завершить работу
Введите одно из 6 действий (1 - 6): ''')

        if action.isdigit():
            action = int(action)

            if 1 <= action <= 4:
                dadata_api(create_params(action))
            elif action == 5:
                print('Успешно завершили работу!')

            else:
                print('Вы ввели цифру не от 1 до 6, попробуйте еще раз.')

        else:
            print('Вы ввели не цифру, попробуйте еще раз.')


main()
