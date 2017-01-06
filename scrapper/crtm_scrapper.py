import scrapy
import re
import logging
import csv_utils


class CRTMScrapper(scrapy.Spider):
    name = 'CRTM_scrapper_starter'
    allowed_domains = ['crtm.es']
    BASE_URL = 'http://www.crtm.es'

    start_urls = ['http://www.crtm.es/tu-transporte-publico/metro.aspx',
                  'http://www.crtm.es/tu-transporte-publico/metro-ligero.aspx',
                  'http://www.crtm.es/tu-transporte-publico/cercanias-renfe.aspx']

    scrapped_lines = []

    def __init__(self, *args, **kwargs):
        super(CRTMScrapper, self).__init__(*args, **kwargs)
        self.csv_file_name = kwargs.get('csv_file_path')

    def parse(self, response):
        lines_page_url = CRTMScrapper._get_lines_page_url(response)
        yield scrapy.Request(lines_page_url, self.parse_lines_page)

    '''
    Parse pages with lines info (i.e. http://www.crtm.es/tu-transporte-publico/metro/lineas.aspx)
    '''
    def parse_lines_page(self, response):
        lines_urls = CRTMScrapper._get_lines_urls(response)

        for line in lines_urls:
            yield scrapy.Request(line, self.parse_specific_line_page)

    '''
    Parse a specific line page (i.e. http://www.crtm.es/tu-transporte-publico/metro/lineas/4__1___.aspx)
    '''
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

    '''
    Final actions to execute when the scrapper is about to end
    '''
    def _action_to_perform(self, line):
        self.scrapped_lines.append(line)
        logging.info('Stations info of line %s stored in memory' % line['number'])

    '''
    As described in the official Scrappy documentation, this method is called automatically when all the scrappers
    are finished.

    In this case, it saves the content of scrapped_lines to a csv in gtfs format, now including the order of each
    station in the line it belongs to.
    '''
    def closed(self, reason):
        rows_to_save = []

        metro_dict = csv_utils.csv_to_dict('../assets/METRO/stops.txt', '\ufeffstop_id')
        ml_dict = csv_utils.csv_to_dict('../assets/ML/stops.txt', '\ufeffstop_id')
        cr_dict = csv_utils.csv_to_dict('../assets/CR/stops.txt', '\ufeffstop_id')

        metro_dict = CRTMScrapper._change_ids(metro_dict)
        ml_dict = CRTMScrapper._change_ids(ml_dict)
        cr_dict = CRTMScrapper._change_ids(cr_dict)

        header = (['transportmean_name', 'line_number', 'order_number']
                  +
                  csv_utils.csv_field_names('../assets/METRO/stops.txt'))

        for line in self.scrapped_lines:
            if line['transport'] == 'METRO':
                aux_dict = metro_dict
            elif line['transport'] == 'ML':
                aux_dict = ml_dict
            else:
                aux_dict = cr_dict

            for station in line['stations']:
                if station['id'] in aux_dict:
                    new_info_dict = {'transportmean_name': line['transport'],
                                     'line_number': line['number'],
                                     'order_number': station['order']
                                     }

                    all_info = {**new_info_dict, **aux_dict[station['id']]}

                    rows_to_save.append(all_info)

        csv_utils.write_info_in_csv(rows_to_save, header, self.csv_file_name)

    '''
    Extracts lines site urls from a transport mean page
    '''
    @staticmethod
    def _get_lines_page_url(response):
        return (CRTMScrapper.BASE_URL +
                (response.css('#menuSecun > ul > li.activo > ul > li:nth-child(2) > a')
                 .xpath('./@href')[0]
                 .extract()))

    '''
    Extracts lines urls from a lines page
    '''
    @staticmethod
    def _get_lines_urls(response):
        a_objects = response.css('#colCentro > div.listaBotones> ul > li a')
        return [CRTMScrapper.BASE_URL + link.xpath('./@href')[0].extract() for link in a_objects]

    '''
    Extracts the name of a line
    '''
    @staticmethod
    def _get_line_name(response):
        possible_name_1 = response.css('#colCentro > div:nth-child(4) > div:nth-child(1) > h4::text')
        possible_name_2 = response.css('#colCentro > div:nth-child(4) > h4::text')

        name = possible_name_1 if len(possible_name_1) > 0 else possible_name_2

        return name[0].extract()

    '''
    Extracts the number of a line
    '''
    @staticmethod
    def _get_line_number(response):
        possible_number_1 = response.css('#colCentro > div:nth-child(4) > div:nth-child(1) > h4 > span::text')
        possible_number_2 = response.css('#colCentro > div:nth-child(4) > h4 > span::text')

        number = possible_number_1 if len(possible_number_1) > 0 else possible_number_2

        return number[0].extract()

    '''
    Extracts id and name of a station/stop
    '''
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

    '''
    Given a transport mean name, it returns a kind of abbreviation
    '''
    @staticmethod
    def _detect_transport_mode(url):
        transport = re.findall('http://www.crtm.es/tu-transporte-publico/([\w-]*)/lineas/.*', url)[0]

        if transport == 'metro':
            return 'METRO'
        elif transport == 'metro-ligero':
            return 'ML'
        else:
            return 'CR'

    '''
    In the csv gtfs original file, the ids look like this: par_4_100 or par_4_100_1

    We don't want the substring "par_" nor "... _1" because it doesn't allow us to match the station ids from the website
    with the stations in the csv gtfs file.

    Therefore, we need to extract the portion of ids that looks like this: 4_100
    '''
    @staticmethod
    def _change_ids(dictionary):
        new_dict = {}

        for key, value in dictionary.items():
            real_id = re.findall('[a-z]{3}_(([4-5]|10)_[0-9a-zA-Z]+)(_[0-9]+)?', key)

            station_id = '' if len(real_id) == 0 or real_id[0][2] != '' else real_id[0][0]

            if station_id:
                new_dict[station_id] = value

        return new_dict

