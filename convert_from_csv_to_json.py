"""Script to convert csv records from a file (.csv) to array of json object's file (.json)"""
import csv
import json
import os


def is_last(itr):
    """Loop through the records and check if its last
       If yes => return True
       else   => return False

       Purpose is to prevent adding comma to the last row in the json array
    """
    old = itr.__next__()
    for new in itr:
        yield False, old
        old = new
    yield True, old


def main():
    """Convert list of csv files in the data directory to json files"""
    ref_tables = [
        './data/' + filename for filename in os.listdir('./data') if filename.endswith('.csv')]

    for table in ref_tables:
        csvfile = open(table, 'r')
        jsonfile = open(table.replace('.csv', '.json'), 'w')
        reader = csv.reader(csvfile)
        headers = reader.__next__()
        reader = csv.DictReader(csvfile, headers)
        reader.__next__()

        jsonfile.write('[\n')
        for _, (last, row) in enumerate(is_last(reader)):
            json.dump(row, jsonfile)
            if not last:
                jsonfile.write(',\n')
            else:
                jsonfile.write('\n')

        jsonfile.write(']')

        csvfile.close()
        jsonfile.close()


if __name__ == '__main__':
    main()
