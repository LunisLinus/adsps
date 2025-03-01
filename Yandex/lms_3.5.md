# 3.5. Потоковый ввод/вывод. Работа с текстовыми файлами. JSON
## 1. A+B+...
```python
from sys import stdin

s = 0
for line in stdin:
    s += sum(map(int, line.split()))

print(s)
```
## 2. Средний рост
```python
from sys import stdin

average_height = []
for line in stdin:
    before_height, now_height = map(int, line.split()[1:])
    average_height.append(max(before_height, now_height) - min(before_height, now_height))

print(round(sum(average_height) / len(average_height)))
```
## 3. Без комментариев 2.0
```python
from sys import stdin

for line in stdin:
    if not line.startswith('#'):
        print(line[:line.find('#')])
```
## 4. Найдётся всё 2.0
```python
from sys import stdin

for line in (data := [elem.strip() for elem in stdin])[:-1]:
    if data[-1].lower() in line.lower():
        print(line)
```
## 5. А роза упала на лапу Азора 6.0
```python
from sys import stdin

for symbol in sorted({word for line in stdin for word in line.split()}):
    if symbol.lower() == symbol[::-1].lower():
        print(symbol)
```
## 6. Транслитерация 2.0
```python
LITER = {
    'А': 'A', 'Б': 'B', 'В': 'V',
    'Г': 'G', 'Д': 'D', 'Е': 'E',
    'Ё': 'E', 'Ж': 'ZH', 'З': 'Z',
    'И': 'I', 'Й': 'I', 'К': 'K',
    'Л': 'L', 'М': 'M', 'Н': 'N',
    'О': 'O', 'П': 'P', 'Р': 'R',
    'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'KH', 'Ц': 'TC',
    'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
    'Ы': 'Y', 'Э': 'E', 'Ю': 'IU',
    'Я': 'IA', 'Ь': '', 'Ъ': '',
}

text = ''
with open('cyrillic.txt', 'r', encoding='utf-8') as file:
    for line in file:
        text += line

with open('transliteration.txt', 'a', encoding='utf-8') as file:
    for symbol in text:
        if symbol.upper() in LITER:
            print(LITER[symbol.upper()].lower().capitalize() if symbol.isupper() else LITER[symbol.upper()].lower(),
                  end='', file=file)
        else:
            print(symbol, end='', file=file)
```
## 7. Файловая статистика
```python
name_file = input()

with open(name_file, 'r', encoding='utf-8') as file:
    data = [int(symbol) for line in file.readlines() for symbol in line.split()]

print(len(data))
print(len([elem for elem in data if elem > 0]))
print(min(data))
print(max(data))
print(sum(data))
print(round(sum(data) / len(data), 2))
```
## 8. Файловая разница
```python
first_name_file, second_name_file, answer_name_file = input(), input(), input()
with open(answer_name_file, 'w', encoding='utf-8') as answer_file:
    with open(first_name_file, 'r', encoding='utf-8') as first_file:
        data1 = {word for line in first_file for word in line.split()}
    with open(second_name_file, 'r', encoding='utf-8') as second_file:
        data2 = {word for line in second_file for word in line.split()}
    answer_file.write('\n'.join(sorted((data1.union(data2)) - (data1.intersection(data2)))))
```
## 9. Файловая чистка
```python
first_name_file, second_name_file = input(), input()
with open(second_name_file, 'w', encoding='utf-8') as second_file:
    with open(first_name_file, 'r', encoding='utf-8') as first_file:
        for line in first_file:
            if line.strip():
                second_file.write(' '.join(line.strip().replace('\t', '').split()) + '\n')
```
## 10. Хвост
```python
name_file, n = input(), int(input())
with open(name_file, 'r', encoding='utf-8') as file:
    print(''.join(file.readlines()[-n:]))
```
## 11. Файловая статистика 2.0
```python
import json

filename, filename_json = input(), input()

with open(filename, 'r', encoding='utf-8') as file:
    data = [int(n) for line in file for n in line.split()]

data_json = {
    'count': len(data),
    'positive_count': len([n for n in data if n > 0]),
    'min': min(data),
    'max': max(data),
    'sum': sum(data),
    'average': round(sum(data) / len(data), 2)
}
with open(filename_json, 'w', encoding='utf-8') as file_json:
    json.dump(data_json, file_json, indent=4, ensure_ascii=False)
```
## 12. Разделяй и властвуй
```python
def count_digits(num: str) -> tuple:
    even_count = sum(1 for digit in num if digit in '02468')
    return even_count, len(num) - even_count


filename_numbers, filename_even, filename_odd, filename_eq = input(), input(), input(), input()

with open(filename_numbers, 'r', encoding='utf-8') as file:
    lines = file.readlines()

text_even = [[num for num in line.split() if count_digits(num)[0] > count_digits(num)[1]] for line in lines]
text_odd = [[num for num in line.split() if count_digits(num)[0] < count_digits(num)[1]] for line in lines]
text_eq = [[num for num in line.split() if count_digits(num)[0] == count_digits(num)[1]] for line in lines]

with open(filename_even, 'w', encoding='utf-8') as even_file, \
     open(filename_odd, 'w', encoding='utf-8') as odd_file, \
     open(filename_eq, 'w', encoding='utf-8') as eq_file:
    for even, odd, eq in zip(text_even, text_odd, text_eq):
        even_file.write(' '.join(even) + '\n')
        odd_file.write(' '.join(odd) + '\n')
        eq_file.write(' '.join(eq) + '\n')
```
## 13. Обновление данных
```python
from sys import stdin
import json

data_json = input()

with open(data_json, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    new_data = {line.split(' == ')[0].strip(): line.split(' == ')[1].strip() for line in stdin}
    data.update(new_data)

with open(data_json, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)
```
## 14. Слияние данных
```python
import json

users_json, update_json = input(), input()

with open(users_json, 'r', encoding='utf-8') as json_file:
    data_old = json.load(json_file)
    data = {users['name']: {key: value for key, value in users.items() if key != 'name'} for users in data_old}

with open(update_json, 'r', encoding='utf-8') as json_file:
    data_new = json.load(json_file)
    data_new = {users['name']: {key: value for key, value in users.items() if key != 'name'} for users in data_new}

for name in data:
    if name in data_new:
        for key, value in data_new[name].items():
            if key in data[name]:
                data[name][key] = max(data[name][key], value)
            else:
                data[name][key] = value

with open(users_json, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)
```
## 15. Поставь себя на моё место
```python
from sys import stdin
import json

answers = [answer.strip() for answer in stdin]

with open('scoring.json', 'r', encoding='utf-8') as file:
    data_score = [
        {test['pattern']: test_block["points"] // len(test_block["tests"])}
        for test_block in json.load(file)
        for test in test_block["tests"]
    ]

res = 0
for answer, score in zip(answers, data_score):
    if answer in score:
        res += score[answer]

print(res)
```
## 16. Найдётся всё 3.0
```python
from sys import stdin

search = ' '.join(input().split()).lower()
files = [file.strip() for file in stdin]

output = set()
for file in files:
    with open(file, 'r', encoding='utf-8') as file_search:
        data_file = ' '.join([word.strip() for word in file_search.read().split()]).lower()
        if search in data_file:
            output.add(file)
            print(file)


if not output:
    print('404. Not Found')
```
## 17. Прятки
```python
with open('secret.txt', 'r', encoding='utf-8') as file:
    print(''.join([chr(ord(symbol) % 128) for symbol in file.read()]))
```
## 18. Сколько вешать в байтах?
```python
import os

size = os.path.getsize(input())
size_word = ''
if size > 1024 ** 3 - 1:
    size = size // 1024 ** 3 + 1
    size_word = 'ГБ'
elif size > 1024 ** 2 - 1:
    size = size // 1024 ** 2 + 1
    size_word = 'МБ'
elif size > 1023:
    size = size // 1024 + 1
    size_word = 'КБ'
else:
    size_word = 'Б'

print(size, size_word, sep='')
```
## 19. Это будет наш секрет
```python
shift = int(input())

with open('public.txt', 'r', encoding='utf-8') as file:
    data = file.read()
    res_text = ''
    for char in data:
        if char.isalpha():
            alphabet = ord('A') if char.isupper() else ord('a')
            res_text += chr((ord(char) - alphabet + shift) % 26 + alphabet)
        else:
            res_text += char

with open('private.txt', 'w', encoding='utf-8') as file:
    file.write(res_text)
```
## 20. Файловая сумма
```python
with open("numbers.num", "rb") as file:
    data = file.read()
    print(sum([int.from_bytes(data[i:i + 2], "big") for i in range(0, len(data), 2)]) % 2 ** 16)
```
