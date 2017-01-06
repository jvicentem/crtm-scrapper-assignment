from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, FOAF
import csv


def crtm_csv_to_rdf(csv_file_path, output_xml_path):
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        g = Graph()

        for row in reader:
            specific_transport_uri = 'http://example.org/%s/publicTransport' % row['transportmean_name']
            transport = URIRef(specific_transport_uri)
            transportmean_name = Literal(row['transportmean_name'])

            line = URIRef(specific_transport_uri + '/line')
            line_number = Literal(row['line_number'])

            station = URIRef(specific_transport_uri + '/station')
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

            g.add((transport, RDF.type, FOAF.PublicTransport))
            g.add((transport, FOAF.name, transportmean_name))
            g.add((transport, FOAF.has, line))

            g.add((line, RDF.type, FOAF.Line))
            g.add((line, FOAF.line_number, line_number))

            g.add((station, RDF.type, FOAF.Station))
            g.add((station, FOAF.id, stop_id))
            g.add((station, FOAF.code, stop_code))
            g.add((station, FOAF.name, stop_name))
            g.add((station, FOAF.order, order_number))
            g.add((station, FOAF.descr, stop_desc))
            g.add((station, FOAF.lat, stop_lat))
            g.add((station, FOAF.lon, stop_lon))
            g.add((station, FOAF.zone, zone_id))
            g.add((station, FOAF.url, stop_url))
            g.add((station, FOAF.location, location_type))
            g.add((station, FOAF.parent, parent_station))
            g.add((station, FOAF.timezone, stop_timezone))
            g.add((station, FOAF.wheelchair, wheelchair_boarding))

            g.add((line, FOAF.has, station))

        g.serialize(destination=output_xml_path, format='xml')

