import csv
import json

with open('constellations_info.json', 'r', encoding='utf-8') as json_file:
    constellations = json.load(json_file)

stars_data = []

for constellation in constellations:
    for star in constellation['brightest_stars']:
        stars_data.append(
            {
                'name': star['name'],
                'brightness': star['brightness'],
                'constellation': constellation['latin_name'],
                'abbreviation': constellation['abbreviation'],
                'area': constellation['area'],
                'neighboring_constellations': ', '.join(constellation['neighboring_constellations'])
            }
        )
stars_data = sorted(stars_data, key=lambda x: (x['constellation'], x['name']))
fields = ['name', 'brightness', 'constellation', 'abbreviation', 'area', 'neighboring_constellations']
with open('stars_info.csv', 'w', encoding='utf-8', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields, delimiter=';')
    writer.writeheader()
    writer.writerows(stars_data)
