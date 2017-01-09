import rdf_crtm_lines_generator as rdf
import os

CSV_FILE_PATH = '..' + os.sep + 'scrapper' + os.sep + 'info_trans.csv'
RDF_XML_PATH = '.' + os.sep + 'crtm-rdf-graph.xml'


def main():
    rdf.crtm_csv_to_rdf(CSV_FILE_PATH, RDF_XML_PATH)

if __name__ == "__main__":
    main()
