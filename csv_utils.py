import csv
import os
import logging


def write_info_in_csv(rows, fields, file_name):
    file_name = "info_trans.csv"
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


def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        logging.info('File removed successfully')
    else:
        logging.warning('Could not remove file: wrong path')
