import csv
import json
import os


def isLast(itr):
    old = itr.next()
    for new in itr:
        yield False, old
        old = new
    yield True, old


ref_tables = [
    './data/' + filename for filename in os.listdir('./data') if filename.endswith('.csv')]

for table in ref_tables:
    csvfile = open(table, 'rb')
    jsonfile = open(table.replace('.csv', '.json'), 'w')
    json_arr = []
    reader = csv.reader(csvfile)
    headers = reader.next()
    reader = csv.DictReader(csvfile, headers)
    reader.next()

    jsonfile.write('[\n')
    for _, (is_last, row) in enumerate(isLast(reader)):
        json.dump(row, jsonfile)
        if not is_last:
            jsonfile.write(',\n')
        else:
            jsonfile.write('\n')

    jsonfile.write(']')

    csvfile.close()
    jsonfile.close()
