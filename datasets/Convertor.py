import csv
import json


AD = 'ad'
CATEGORY = 'category'
LOCATION = 'location'
USER = 'user'


def convert_file(csv_file, json_file, model):
    result = []
    with open(csv_file, encoding='utf-8') as csv_f:
        for row in csv.DictReader(csv_f):
            to_add = {'model': model, 'pk': int(row['Id'] if 'Id' in row else row['id'])}
            if 'id' in row:
                del row['id']
            else:
                del row['Id']

            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False

            if 'price' in row:
                row['price'] = int(row['price'])

            to_add['fields'] = row
            result.append(to_add)
    with open(json_file, 'w', encoding='utf-8') as jf:
        jf.write(json.dumps(result, ensure_ascii=False, indent=4))


convert_file(f"{AD}.csv", f"{AD}.json", 'ads.ad')
convert_file(f"{CATEGORY}.csv", f"{CATEGORY}.json", 'category.ads')
convert_file(f"{LOCATION}.csv", f"{LOCATION}.json", 'users.location')
convert_file(f"{USER}.csv", f"{USER}.json", 'users.user')

