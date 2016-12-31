from scrapy.crawler import CrawlerProcess
from crtm_scrapper import CRTMScrapper

CSV_FILE_PATH = 'info_trans.csv'


def main():
    process = CrawlerProcess()
    scrapper_start = CRTMScrapper()
    process.crawl(scrapper_start, csv_file_path=CSV_FILE_PATH)
    process.start()

if __name__ == "__main__":
    main()
