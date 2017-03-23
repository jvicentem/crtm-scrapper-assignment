from rdflib import URIRef, Literal, Graph

import csv

'''
Parses a csv in gtfs format with crtm public transport info and generates a rdf graph stored in a xml file.

This method takes two arguments: the csv file path and the output xml path.
'''


def crtm_csv_to_rdf(csv_file_path, output_xml_path):
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        g = Graph()

        for row in reader:
            if row['transportmean_name'] == 'METRO':
                uri_transport = 'metro'
                transport_number = 4
            elif row['transportmean_name'] == 'ML':
                uri_transport = 'metro-ligero'
                transport_number = 10
            else:
                uri_transport = 'cercanias-renfe'
                transport_number = 5

            specific_transport_uri = 'http://www.crtm.es/tu-transporte-publico/%s' % uri_transport
            transport = URIRef(specific_transport_uri + '.aspx')
            transportmean_name = Literal(row['transportmean_name'])

            line = URIRef(specific_transport_uri + '/lineas/%d__%s___.aspx' % (transport_number, row['line_number']))
            line_number = Literal(row['line_number'])

            station = URIRef(specific_transport_uri + '/estaciones/%d_%d.aspx' % (transport_number, int(row['stop_code'])))
            stop_id = Literal(row['\ufeffstop_id'])
            stop_code = Literal(row['stop_code'])
            stop_name = Literal(row['stop_name'])
            order_number = Literal(row['order_number'])
            stop_desc = Literal(row['stop_desc'])
            stop_lat = Literal(row['stop_lat'])
            stop_lon = Literal(row['stop_lon'])
            zone_id = Literal(row['zone_id'])
            stop_url = Literal(row['stop_url'])
            location_type = Literal(row['location_type'])
            parent_station = Literal(row['parent_station'])
            stop_timezone = Literal(row['stop_timezone'])
            wheelchair_boarding = Literal(row['wheelchair_boarding'])

            # a transport mean has a name
            g.add((transport, URIRef('http://dbpedia.org/ontology/name'), transportmean_name))
            # a transport mean has lines
            g.add((transport, URIRef(specific_transport_uri + '/lineas.aspx'), line))

            # a transport mean line has a number
            g.add((line, URIRef('http://dbpedia.org/ontology/RailwayLine'), line_number))

            # a stop/station has an id
            g.add((station, URIRef('http://dbpedia.org/ontology/id'), stop_id))
            # a stop/station has a code
            g.add((station, URIRef('http://dbpedia.org/ontology/code'), stop_code))
            # a stop/station has a name
            g.add((station, URIRef('http://dbpedia.org/ontology/name'), stop_name))
            # a stop/station has an order in the line/s it belongs to
            g.add((station, URIRef('http://dbpedia.org/ontology/order'), order_number))
            # a stop/station has an address
            g.add((station,  URIRef('http://dbpedia.org/ontology/address'), stop_desc))
            # a stop/station has a location latitude
            g.add((station, URIRef('http://www.w3.org/2003/01/geo/wgs84_pos#lat'), stop_lat))
            # a stop/station has a location longitude
            g.add((station, URIRef('http://www.w3.org/2003/01/geo/wgs84_pos#lon'), stop_lon))
            # a stop/station has a zone id
            g.add((station, URIRef('http://dbpedia.org/ontology/location'), zone_id))
            # a stop/station has an url
            g.add((station, URIRef('http://www.daml.org/ontologies/396#homepage'), stop_url))
            # a stop/station has location type
            g.add((station,
                   URIRef('http://www.ontologydesignpatterns.org/ont/op/openpolis.owl#location_type'),
                   location_type))
            # a stop/station has a parent station
            g.add((station, URIRef('http://dbpedia.org/ontology/parent'), parent_station))
            # a stop/station has a timezone
            g.add((station, URIRef('http://dbpedia.org/ontology/timezone'), stop_timezone))
            # a stop/station has wheelchair accessibility
            g.add((station, URIRef('http://dbpedia.org/ontology/isHandicappedAccessible'), wheelchair_boarding))

            # a transport mean line has stations
            g.add((line, URIRef(specific_transport_uri), station))

        g.serialize(destination=output_xml_path, format='xml')


if __name__ == "__main__":
    CSV_FILE_PATH = 'info_trans.csv'
    RDF_XML_PATH = 'crtm-rdf-graph.xml'

    crtm_csv_to_rdf(CSV_FILE_PATH, RDF_XML_PATH)
