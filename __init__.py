from scrapy.crawler import CrawlerProcess
from crtm_scrapper import CRTMScrapper


def main():
    process = CrawlerProcess()
    scrapper_start = CRTMScrapper()
    process.crawl(scrapper_start)
    process.start()

if __name__ == "__main__":
    main()
