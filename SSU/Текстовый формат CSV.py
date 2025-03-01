import csv


def var1():
    rows = []
    count_belarus, count_turkey, count_egypt, all_cities, average_numbers = 0, 0, 0, 0, []

    with open('var1.csv', 'r', encoding='utf-8') as csv_file:
        print('Ответы для первого варианта')
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            all_cities += 1
            if row['Страна'] == 'Республика Беларусь':
                count_belarus += 1
            elif row['Страна'] == 'Египет':
                count_egypt += 1
            elif row['Страна'] == 'Турция':
                count_turkey += 1
            elif row['Страна'] == 'Россия':
                row.pop('Страна')
                rows.append(row)
            if float(row['Численность населения']) <= 100:
                average_numbers.append(float(row['Численность населения']))

        print(f'Количество городов в Беларуси: {count_belarus}')
        print(f'Cредняя численность населения городов, в которых количество жителей не превышает 100 тыс. человек:'
              f' {sum(average_numbers) / len(average_numbers):.2f}')
        print(
            f'Процентное соотношение количества городов Республики Беларусь: {(count_belarus / all_cities) * 100:.2f}%')
        print(f'Процентное соотношение количества городов Турции: {(count_turkey / all_cities) * 100:.2f}%')
        print(f'Процентное соотношение количества городов Египта: {(count_egypt / all_cities) * 100:.2f}%')

        with open('res1.csv', 'w', encoding='utf-8', newline='') as res_csv:
            writer = csv.DictWriter(res_csv, fieldnames=list(rows[0].keys())[:2])
            writer.writeheader()
            writer.writerows(rows)


def var2():
    rows = []
    precipitation_fall, temperature, count_e, count_ne, count_s, all_winds = [], [], 0, 0, 0, 0

    with open('var2.csv', 'r', encoding='utf-8') as csv_file:
        print('Ответы для второго варианта')
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            all_winds += 1
            if row['Дата'].split(' ')[1] in {'сентября', 'октября', 'ноября'}:
                precipitation_fall.append(float(row['Осадки']))
            if row['Ветер'] == 'С':
                temperature.append(float(row['Температура']))
            elif row['Ветер'] == 'В':
                count_e += 1
            elif row['Ветер'] == 'СВ':
                count_ne += 1
            elif row['Ветер'] == 'ЮВ':
                count_s += 1
            if float(row['Температура']) > 0:
                rows.append(row)

        print(f'Среднее количество осадков выпадало за сутки в осенние месяцы (сентябрь, октябрь, ноябрь): '
              f'{sum(precipitation_fall) / len(precipitation_fall):.2f}')
        print(f'Средняя температура в те дни года, когда дул северный (С) ветер:'
              f' {sum(temperature) / len(temperature):.2f}')
        print(f'Процентное соотношение количества дней, когда дул ветер «В»: {(count_e / all_winds) * 100:.2f}%')
        print(f'Процентное соотношение количества дней, когда дул ветер «СВ»: {(count_ne / all_winds) * 100:.2f}%')
        print(f'Процентное соотношение количества дней, когда дул ветер «ЮВ»: {(count_s / all_winds) * 100:.2f}%')

        with open('res2.csv', 'w', encoding='utf-8', newline='') as res_csv:
            writer = csv.DictWriter(res_csv, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def var3():
    rows = []
    central_english, average_marks, count_w, count_sw, count_c, all_pupils = 0, [], 0, 0, 0, 0

    with open('var3.csv', 'r', encoding='utf-8') as csv_file:
        print('Ответы для третьего варианта')
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            all_pupils += 1
            if row['округ'] == 'Ц' and row['любимый предмет'] == 'английский язык':
                central_english += 1
            if row['округ'] == 'В':
                average_marks.append(int(row['балл']))
            elif row['округ'] == 'З':
                count_w += 1
            elif row['округ'] == 'ЮЗ':
                count_sw += 1
            elif row['округ'] == 'Ц':
                count_c += 1
            if row['любимый предмет'] == 'математика':
                rows.append(row)

        print(f'Cколько учеников в Центральном округе (Ц) выбрали в качестве любимого предмета английский язык: '
              f'{central_english}')
        print(f'Средний тестовый балл у учеников Восточного округа (В):'
              f' {sum(average_marks) / len(average_marks):.2f}')
        print(f'Процентное соотношение числа участников из округов с кодами «З»: {(count_w / all_pupils) * 100:.2f}%')
        print(f'Процентное соотношение числа участников из округов с кодами «ЮЗ»: {(count_sw / all_pupils) * 100:.2f}%')
        print(f'Процентное соотношение числа участников из округов с кодами «Ц»: {(count_c / all_pupils) * 100:.2f}%')

        with open('res3.csv', 'w', encoding='utf-8', newline='') as res_csv:
            writer = csv.DictWriter(res_csv, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def var4():
    rows = []
    сount_products, calories, low_cal, high_cal, all_cal = 0, [], 0, 0, 0

    with open('var4.csv', 'r', encoding='utf-8') as csv_file:
        print('Ответы для четвертого варианта')
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            all_cal += 1
            if float(row['Жиры. г']) < 25 and float(row['Белки. г']) < 25:
                сount_products += 1
            if float(row['Углеводы. г']) > 50:
                calories.append(float(row['Калорийность. Ккал']))
            if float(row['Калорийность. Ккал']) < 500:
                low_cal += 1
            elif float(row['Калорийность. Ккал']) >= 500:
                high_cal += 1
            if float(row['Жиры. г']) < 10:
                rows.append(row)

        print(f'Сколько продуктов в таблице содержат меньше 25 г жиров и меньше 25 г белков: {сount_products}')
        print(f'Cредняя калорийность продуктов с содержанием углеводов более 50 г:'
              f' {sum(calories) / len(calories):.2f}')
        print(f'Процентное соотношение низкокалорийных (менее 500 Ккалорий): {(low_cal / all_cal) * 100:.2f}%')
        print(f'Процентное соотношение высококалорийных продуктов (не менее 500 Ккалорий): '
              f'{(high_cal / all_cal) * 100:.2f}%')

        with open('res4.csv', 'w', encoding='utf-8', newline='') as res_csv:
            writer = csv.DictWriter(res_csv, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def var5():
    rows = []
    mens, girls, average_mens, chemistry, economy, medicine, all_universities = 0, 0, [], 0, 0, 0, 0

    with open('var5.csv', 'r', encoding='utf-8') as csv_file:
        print('Ответы для пятого варианта')
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            all_universities += 1
            if row['пол'] == 'муж':
                mens += 1
                average_mens.append(int(row['баллы']))
            elif row['пол'] == 'жен':
                girls += 1
            if row['факультет'] == 'химический':
                chemistry += 1
            elif row['факультет'] == 'экономический':
                economy += 1
            elif row['факультет'] == 'медицинский':
                medicine += 1
            if row['пол'] == 'жен' and row['факультет'] == 'химический':
                rows.append(row)

        print(f'На сколько число юношей превышает число девушек: {mens - girls}')
        print(f'Средний балл юношей: {sum(average_mens) / len(average_mens):.2f}')
        print(
            f'Процентное соотношение числа учащихся химического факультета: {(chemistry / all_universities) * 100:.2f}%')
        print(
            f'Процентное соотношение числа учащихся экономического факультета: {(economy / all_universities) * 100:.2f}%')
        print(
            f'Процентное соотношение числа учащихся медицинского факультета: {(medicine / all_universities) * 100:.2f}%')

        with open('res5.csv', 'w', encoding='utf-8', newline='') as res_csv:
            writer = csv.DictWriter(res_csv, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


var1()
print('\n')
var2()
print('\n')
var3()
print('\n')
var4()
print('\n')
var5()
