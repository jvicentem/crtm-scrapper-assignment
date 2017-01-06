import csv
import logging

'''
Given a list of dictionaries, a list of field names and a valid path, generates a csv file with the given field names
as fields and with the dictionaries as rows.

The fields in the dictionaries must match the field names given as argument.
'''


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

'''
Given a valid path of a csv file and a field name from that csv file, it returns a dictionary whose keys are based
on values of the given field name and it belonging rows (as a dictionary each one) as value.
'''


def csv_to_dict(file_path, field_as_key):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        dictionary = {}

        for row in reader:
            dictionary[row[field_as_key]] = row

        return dictionary

'''
Given a valid path of a csv file, it returns a list of the field names of that csv file.
'''


def csv_field_names(file_path):
    with open(file_path, 'r') as csv_file:
        return csv.DictReader(csv_file).fieldnames
