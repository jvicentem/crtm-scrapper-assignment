import rdf_crtm_lines_generator as rdf

CSV_FILE_PATH = '../scrapper/info_trans.csv'
RDF_XML_PATH = './crtm-rdf-graph.xml'


def main():
    rdf.crtm_csv_to_rdf(CSV_FILE_PATH, RDF_XML_PATH)

if __name__ == "__main__":
    main()
