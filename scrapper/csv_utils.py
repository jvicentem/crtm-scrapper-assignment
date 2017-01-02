import csv
import logging


def write_info_in_csv(rows, fields, file_name):
    with open(file_name, 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, dialect="excel", lineterminator='\n', fieldnames=fields)

        with open(file_name) as aux:
            first_line = aux.readline()
            csv_without_header = not first_line

            if csv_without_header:
                writer.writeheader()

        for row in rows:
            writer.writerow(row)

        logging.info('Stations info saved in %s' % file_name)


def csv_to_dict(file_path, field_as_key):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        dictionary = {}

        for row in reader:
            dictionary[row[field_as_key]] = row

        return dictionary


def csv_field_names(file_path):
    with open(file_path, 'r') as csv_file:
        return csv.DictReader(csv_file).fieldnames
