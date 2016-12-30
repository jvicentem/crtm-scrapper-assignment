import scrapy
import re
import logging
import csv_utils


class CRTMScrapper(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(CRTMScrapper, self).__init__(*args, **kwargs)
        self.csv_file_name = kwargs.get('csv_file_path')

    RANDOMIZE_DOWNLOAD_DELAY = True

    name = 'CRTM_scrapper_starter'
    allowed_domains = ['crtm.es']
    BASE_URL = 'http://www.crtm.es'

    start_urls = ['http://www.crtm.es/tu-transporte-publico/metro.aspx',
                  'http://www.crtm.es/tu-transporte-publico/metro-ligero.aspx',
                  'http://www.crtm.es/tu-transporte-publico/cercanias-renfe.aspx']

    scrapped_lines = []

    def parse(self, response):
        lines_page_url = CRTMScrapper._get_lines_page_url(response)
        yield scrapy.Request(lines_page_url, self.parse_lines_page)

    def parse_lines_page(self, response):
        lines_urls = CRTMScrapper._get_lines_urls(response)

        for line in lines_urls:
            yield scrapy.Request(line, self.parse_specific_line_page)

    def parse_specific_line_page(self, response):
        line_name = CRTMScrapper._get_line_name(response)
        line_number = CRTMScrapper._get_line_number(response)
        stations = CRTMScrapper._get_stations_info(response)
        transport_mode = CRTMScrapper._detect_transport_mode(response.url)

        line = {'name': line_name, 'number': line_number, 'stations': [], 'transport': transport_mode}

        for i in range(len(stations)):
            station = stations[i]
            station['order'] = i
            line['stations'].append(station)

        logging.info('%s\'s line %s parsed' % (transport_mode, line_number))

        self._action_to_perform(line)

    def _action_to_perform(self, line):
        self.scrapped_lines.append(line)
        logging.info('Stations info of line %s stored in memory' % line['number'])

    def closed(self, reason):
        header = ['transportmean_name', 'line_number', 'order_number', 'station_id']

        rows_to_save = []

        for line in self.scrapped_lines:
            for station in line['stations']:
                rows_to_save.append({'transportmean_name': line['transport'],
                                     'line_number': line['number'],
                                     'order_number': station['order'],
                                     'station_id': station['id']
                                     })

        csv_utils.write_info_in_csv(rows_to_save, header, self.csv_file_name)

    @staticmethod
    def _get_lines_page_url(response):
        return (CRTMScrapper.BASE_URL +
                (response.css('#menuSecun > ul > li.activo > ul > li:nth-child(2) > a')
                 .xpath('./@href')[0]
                 .extract()))

    @staticmethod
    def _get_lines_urls(response):
        a_objects = response.css('#colCentro > div.listaBotones> ul > li a')
        return [CRTMScrapper.BASE_URL + link.xpath('./@href')[0].extract() for link in a_objects]

    @staticmethod
    def _get_line_name(response):
        possible_name_1 = response.css('#colCentro > div:nth-child(4) > div:nth-child(1) > h4::text')
        possible_name_2 = response.css('#colCentro > div:nth-child(4) > h4::text')

        name = possible_name_1 if len(possible_name_1) > 0 else possible_name_2

        return name[0].extract()

    @staticmethod
    def _get_line_number(response):
        possible_number_1 = response.css('#colCentro > div:nth-child(4) > div:nth-child(1) > h4 > span::text')
        possible_number_2 = response.css('#colCentro > div:nth-child(4) > h4 > span::text')

        number = possible_number_1 if len(possible_number_1) > 0 else possible_number_2

        return number[0].extract()

    @staticmethod
    def _get_stations_info(response):
        rows = (response.css('#colCentro > div:nth-child(4) table > tbody tr'))

        stations_objects = []

        for row in rows:
            station = row.css('td:nth-child(1) > a')

            name = station.xpath('text()')[0].extract()
            url = station.xpath('./@href')[0].extract()
            station_id = re.findall('/tu-transporte-publico/.*/estaciones/(\d+_\d+).aspx', url)[0]

            stations_objects.append({'id': station_id, 'name': name})

        return stations_objects

    @staticmethod
    def _detect_transport_mode(url):
        transport = re.findall('http://www.crtm.es/tu-transporte-publico/([\w-]*)/lineas/.*', url)[0]

        if transport == 'metro':
            return 'METRO'
        elif transport == 'metro-ligero':
            return 'ML'
        else:
            return 'CR'

