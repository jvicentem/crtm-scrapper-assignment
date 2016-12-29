from scrapy.crawler import CrawlerProcess
from crtm_scrapper import CRTMScrapper
from csv_utils import delete_file_if_exists

CSV_FILE_PATH = 'info_lineas.csv'


def main():
    delete_file_if_exists(CSV_FILE_PATH)
    process = CrawlerProcess()
    scrapper_start = CRTMScrapper()
    process.crawl(scrapper_start, csv_file_path=CSV_FILE_PATH)
    process.start()

if __name__ == "__main__":
    main()
