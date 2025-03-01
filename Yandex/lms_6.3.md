# 6.3 Модуль requests
## 1. Проверка системы
```python
import requests

print(requests.get('http://127.0.0.1:5000').text)
```
## 2. Суммирование ответов
```python
from requests import get

url = f'http://{input()}'

res = 0
while data := int(get(url).text):
    res += data
print(res)
```
## 3. Суммирование ответов 2
```python
from requests import get

url = f'http://{input()}'

data = get(url).json()
print(sum(elem for elem in data if isinstance(elem, int)))
```
## 4. Конкретное значение
```python
from requests import get

url = f'http://{input()}'
key = input()

data = get(url).json()
print(data.get(key, 'No data'))
```
## 5. Суммирование ответов 3
```python
from requests import get
from sys import stdin

url = f'http://{input()}'
res = 0

for path in stdin:
    res += sum(get(url + path.strip()).json())

print(res)
```
## 6. Список пользователей
```python
from requests import get

url = f'http://{input()}/users'
users = get(url).json()

res = []
for user in users:
    res.append(f"{user['last_name']} {user['first_name']}")

print('\n'.join(sorted(res)))
```
## 7. Рассылка сообщений
```python
from requests import get
from sys import stdin

url = f'http://{input()}/users/{input()}'
pattern_email = ''.join(row for row in stdin)
data = {}

try:
    data = get(url).json()
except ValueError:
    print('Пользователь не найден')
if data:
    for key in data:
        pattern_email = pattern_email.replace('{' + key + '}', str(data[key]))

    print(pattern_email)
```
## 8. Регистрация нового пользователя
```python
from requests import post
from json import dumps

url = f'http://{input()}/users'
username, last_name, first_name, email = input(), input(), input(), input()
data = {'username': username, 'last_name': last_name, 'first_name': first_name, 'email': email}

post(url, data=dumps(data))
```
## 9. Изменение данных
```python
from requests import put
from sys import stdin
from json import dumps

url = f'http://{input()}/users/{input()}'
data = {row.split('=')[0].strip(): row.split('=')[1].strip() for row in stdin}

put(url, data=dumps(data))
```
## 10. Удаление данных
```python
from requests import delete

url = f'http://{input()}/users/{input()}'
delete(url)
```
