import csv
import json
from collections import defaultdict

with open('stars_info.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file, delimiter=';')
    constellation_data = defaultdict(lambda: {
        "latin_name": "",
        "abbreviation": "",
        "area": "",
        "brightest_stars": [],
        "neighboring_constellations": []
    })
    for row in reader:
        constellation = constellation_data[row["constellation"]]
        constellation["latin_name"] = row["constellation"]
        constellation["abbreviation"] = row["abbreviation"]
        constellation["area"] = row["area"]
        constellation["neighboring_constellations"] = row["neighboring_constellations"].split(", ")
        constellation["brightest_stars"].append({"name": row["name"], "brightness": row["brightness"]})

constellation_data = sorted(list(constellation_data.values()), key=lambda x: x['latin_name'])
for constellation in constellation_data:
    constellation['brightest_stars'] = sorted(constellation['brightest_stars'], key=lambda x: -float(x['brightness']))

with open('constellations_recreate.json', 'w', encoding='utf-8') as json_file:
    json.dump(constellation_data, json_file, indent=4, ensure_ascii=False)

'''
Совершенно точно отличается порядок звёзд внутри созвездий в JSON-файле после его воссоздания из CSV,
так как при восстановлении данных мы сортировали звёзды по яркости.
В исходном JSON порядок звёзд мог быть задан иначе, не обязательно по яркости. 
Таким образом, порядок звёзд — это первое и самое заметное отличие.
Второе отличие — это порядок самих созвездий в воссозданном JSON-файле.
 Он зависит от порядка, в котором строки были прочитаны из CSV,
и может не совпадать с исходным порядком созвездий в первом JSON-файле,
 если там созвездия были упорядочены иначе (например, по площади или алфавиту).
'''
