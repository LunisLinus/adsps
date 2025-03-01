import argparse
import fnmatch
import os
import re
import chardet
import json
import random
import datetime
import string
from tqdm import tqdm
import time
from faker import Faker

PATTERNS = {
    "time": r'\b(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?\b',
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "url": r'\bhttps?://[A-Za-z0-9./_~:?#&=+%,-]+\b',
    "python_variable_names": r'\b[_a-z][_a-z0-9]*\b',
    "dates": r'\b\d{1,2}[-/.]\d{1,2}[-/.]\d{4}\b|\b\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\b',
    "floating_numbers": r'\b\d+\.\d+\b|\b\d+\.\d+e[+-]?\d+\b|\b\d+e[+-]?\d+\b',
    "russian_license_plates": r'[A-ЯA-Z]{1}[0-9]{3}[A-ЯA-Z]{2}|[A-ЯA-Z]{1}[0-9]{3}[A-ЯA-Z]{2}[0-9]{2,3}|[0-9]{4}[A-ЯA-Z]{2}',
}

fake = Faker()


def loading_animation():
    for _ in tqdm(range(100), desc="Loading", ascii=True, ncols=100):
        time.sleep(0.05)


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def generate_time():
    return datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))


def generate_email():
    return fake.email()


def generate_url():
    return fake.url()


def generate_variable_name(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_date():
    return fake.date()


def generate_float():
    return random.uniform(0.0, 100.0)


def generate_vehicle_registration():
    region_code = random.randint(1, 199)
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=3))
    return f"{letters}{digits} {region_code}"


data_generators = {
    'time': generate_time,
    'email': generate_email,
    'url': generate_url,
    'python_variable_names': generate_variable_name,
    'dates': generate_date,
    'floating_numbers': generate_float,
    'russian_license_plates': generate_vehicle_registration
}


def generate_file():
    print('Генерируем файлы...')
    loading_animation()

    if not os.path.exists('task2'):
        os.makedirs('task2')

    os.chdir('task2')
    for i in range(args.count_files):
        with open(f'{args.filename_template}_{random.randint(0, 10000)}{i}.txt', 'w') as file:
            for _ in range(args.count_types):
                data_generator = data_generators[random.choice(args.types)]
                data = data_generator()
                file.write(str(data) + '\n')


parser = argparse.ArgumentParser(description='Generate files with random data.')
parser.add_argument('filename_template', type=str, help='Template for file names.')
parser.add_argument('types', nargs='+', choices=data_generators.keys(), help='Types of objects to generate.')
parser.add_argument('--count_types', type=int, default=100, help='Number of objects to generate for each type.')
parser.add_argument('--count_files', type=int, default=100, help='Number of files to generate for each type.')
args = parser.parse_args()


def analysis_filename():
    files = []
    print('Анализируем папку task2...')
    letter = input('Введите букву: ')
    print('Ищем файлы...')
    loading_animation()
    print('Найденные файлы:')

    for file in os.listdir('.'):
        filename = file.split('.')[0]
        if (filename.lower().startswith(letter.lower()) and filename[-2].isdigit() and len(filename) >= 7 and
                fnmatch.fnmatch(file, '*.txt')):
            print(file)
            files.append(file)
    if not files:
        print('Такой файл не был найден.')
        return None
    else:
        return files


def search_data(files):
    if files:
        print('Ищем данные в найденных файлах...')

        os.chdir('..')

        if os.path.exists('information.json') and os.path.getsize('information.json') > 0:
            with open('information.json', 'r') as file:
                informations = json.load(file)
        else:
            informations = []

        os.chdir('task2')

        for file in files:
            print(f'Ищем данные в файле {file}...')
            loading_animation()

            with open(file, 'r', encoding=detect_encoding(file)) as file_text:
                content = file_text.read()
                information = {key: re.findall(pattern, content) for key, pattern in PATTERNS.items()}
                information['filename'] = file
                informations.append(information)

                for key, value in information.items():
                    if value and key != 'filename':
                        print(f'{key}: {value}')

        os.chdir('..')

        with open('information.json', 'w', encoding='utf-8') as json_file:
            json.dump(informations, json_file, indent=4, ensure_ascii=True)


generate_file()
search_files = analysis_filename()
search_data(search_files)
