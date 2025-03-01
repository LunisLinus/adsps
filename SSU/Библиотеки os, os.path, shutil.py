import os
import shutil


def print_current_directory():
    print('Ищем текущую директорию...')
    print(f'Текущая директория: {os.getcwd()}')
    input('Нажмите Enter для продолжения...')


def print_current_user():
    print('Ищем имя текущего пользователя...')
    print(f'Текущий пользователь: {os.getlogin()}')
    input('Нажмите Enter для продолжения...')


def print_os_type():
    print('Ищем тип операционной системы...')
    os_type = os.name
    if os_type == 'posix':
        print('Тип ОС: Unix/Linux')
    elif os_type == 'nt':
        print('Тип ОС: Windows')
    elif os_type == 'Java':
        print('Тип ОС: Android')
    else:
        print(f'Неизвестный тип ОС: {os_type}')
    input('Нажмите Enter для продолжения...')


def check_file_exists():
    print('Проверяем существует ли файл "test.txt"...')
    if os.path.exists('test.txt'):
        print('Файл "test.txt" существует.')
    else:
        print('Файл "test.txt" не найден.')
    input('Нажмите Enter для продолжения...')


def print_directory_contents():
    current_dir = os.getcwd().split('\\')[-1]
    print(f'Печатем содержимое текущей папки {current_dir}...')
    print('Содержимое текущей папки:')
    for item in os.listdir():
        print(item)
    input('Нажмите Enter для продолжения...')


def print_directory_structure(startpath='.'):
    current_dir = os.getcwd().split('\\')[-1]
    print(f'Печатам файловую структуру текущей директории {current_dir}...')
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')
    input('Нажмите Enter для продолжения...')


def create_test_directory():
    if not os.path.exists('test'):
        os.mkdir('test')
        print('Папка "test" создана.')
    else:
        print('Папка "test" уже существует.')
    input('Нажмите Enter для продолжения...')


def change_to_test_directory():
    current_dir = os.getcwd().split('\\')[-1]
    print(f'Меняем текущую директорию {current_dir} на "test"...')
    os.chdir('test')
    print(f'Текущая директория: {os.getcwd()}')
    input('Нажмите Enter для продолжения...')


def create_user_named_file(filename: str):
    current_dir = os.getcwd().split('\\')[-1]
    print(f'Создаем файл {filename} в текущей директории {current_dir}...')
    with open(filename, 'w') as file:
        file.write('Hey!')
    print(f'Файл {filename} был создан.')
    input('Нажмите Enter для продолжения...')


def check_file_or_directory(filename: str):
    print(f'Проверяем {filename} это папка или файл...')
    if os.path.exists(filename):
        if os.path.isfile(filename):
            print(f'{filename} существует и это файл.')
        elif os.path.isdir(filename):
            print(f'{filename} существует и это папка.')
    else:
        print(f'{filename} не существует.')
    input('Нажмите Enter для продолжения...')


def print_file_path_and_size(filename: str):
    print(f'Печатаем абсолютным путь и размер файла {filename}...')
    if os.path.exists(filename):
        print(f'Абсолютный путь: {os.path.abspath(filename)}')
        print(f'Размер файла: {os.path.getsize(filename)} байт')
    else:
        print(f'Файл {filename} не найден.')
    input('Нажмите Enter для продолжения...')


def copy_file_to_parent_directory(filename: str):
    print(f'Копируем файл на уровень выше с тем же именем {filename}...')
    shutil.copy(filename, "../" + filename)
    print(f'Файл {filename} скопирован на уровень выше.')
    input('Нажмите Enter для продолжения...')


def move_up_and_print_structure():
    print('Поднимаемся на уровень выше и ещё раз печатаем содержимое папки с учётом вложенности...')
    os.chdir(os.pardir)
    print_directory_structure('.')


def print_copied_file_contents(filename: str):
    print(f'Печатаем содержимое скопированного файла {filename}...')
    with open(filename, 'r') as file:
        print(file.read())
    input('Нажмите Enter для продолжения...')


def delete_test_directory():
    print('Удаляем папку "test" со всем содержимым...')
    shutil.rmtree('test')
    print('Папка "test" и все её содержимое удалены.')
    input('Нажмите Enter для продолжения...')


def delete_copied_file(filename: str):
    print(f'Удаляем скопированный файл {filename}...')
    if os.path.exists(filename):
        os.remove(filename)
        print(f'Файл {filename} удалён.')
    else:
        print(f'Файл {filename} не найден для удаления.')
    input('Нажмите Enter для продолжения...')


def final_check(filename: str):
    print(f'Проверяем существует ли папка "test" и "{filename}"...')
    if not os.path.exists('test'):
        print('Папка "test" не найдена.')
    else:
        print('Папка "test" осталась.')
    if not os.path.exists(filename):
        print(f'Файл "{filename}" не найден.')
    else:
        print(f'Файл "{filename}" остался.')
    input("Нажмите Enter для завершения.")


def archive_current_folder():
    print('Архивируем текущую папку... (это может занять время)')
    shutil.make_archive("backup", 'zip', ".")
    print('Архивация завершена.')

    print('Начинаем печатать содержимое папки...')
    current_folder_contents = os.listdir(os.getcwd())
    for root, dirs, files in os.walk('backup_contents'):
        for file in files:
            print(os.path.join(root, file))

    print('Cчитаем размеры до архивации и размер архива...')
    original_folder_size = sum(
        os.path.getsize(os.path.join(os.getcwd(), f)) for f in os.listdir(os.getcwd()))
    archive_size = os.path.getsize('backup.zip')
    print(f'Размер до архивации: {original_folder_size}')
    print(f'Размер архива: {archive_size}')

    print('Сравниваем размеры...')
    if original_folder_size > archive_size:
        print('Размер до архивации больше чем размер архива.')
    elif original_folder_size < archive_size:
        print('Размер архива больше чем размер до архивации.')
    else:
        print('Размеры равны.')

    print('Разархивируем в новую папку... (это может занять время)')
    shutil.unpack_archive("backup.zip", "backup_contents")
    print('Разархивация завершена в папку "backup_contents".')

    extracted_folder_contents = os.listdir('backup_contents')

    print('Проверка содержимого папки...')
    if set(current_folder_contents) == set(extracted_folder_contents):
        print('Содержимое совпадает с исходным.')
    else:
        print('Содержимое не совпадает с исходным.')


if __name__ == '__main__':
    print_current_directory()
    print_current_user()
    print_os_type()
    check_file_exists()
    print_directory_contents()
    print_directory_structure()
    create_test_directory()
    change_to_test_directory()
    file_name = input("Введите имя файла для создания в папке 'test': ") + '.txt'
    create_user_named_file(file_name)
    check_file_or_directory(file_name)
    print_file_path_and_size(file_name)
    copy_file_to_parent_directory(file_name)
    move_up_and_print_structure()
    print_copied_file_contents(file_name)
    delete_test_directory()
    delete_copied_file(file_name)
    final_check(file_name)
    archive_current_folder()
