from scrapy.crawler import CrawlerProcess
from scrapper.crtm_scrapper import CRTMScrapper
from rdf_graph_generator.rdf_crtm_lines_generator import crtm_csv_to_rdf

CSV_FILE_PATH = './scrapper/info_trans.csv'
RDF_XML_PATH = './rdf_graph_generator/crtm-rdf-graph.xml'


def main():
    process = CrawlerProcess()
    scrapper_start = CRTMScrapper()
    process.crawl(scrapper_start, csv_file_path=CSV_FILE_PATH)
    process.start()

    crtm_csv_to_rdf(CSV_FILE_PATH, RDF_XML_PATH)

if __name__ == '__main__':
    main()

