import os
import re
import configparser

def clean_po_box(address):
    address = re.sub(r'P.O. Box [0-9]+', '', address)
    address = re.sub(r'PO Box [0-9]+', '', address)
    address = re.sub(r'Box [0-9]+', '', address)
    return address

def get_google_geo_location_api_key():
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini')
    config.read(config_file_path)
    # key = config.get('PROD', 'api_key_google_geo_location')
    key = config.get('DEV', 'api_key_google_geo_location')
    # print(key)
    return key


get_google_geo_location_api_key()

address = '2060 Columbia Ave. Box 940 Rossland, BC  V0G 1Y0'
print(clean_po_box(address))

address = 'PO Box 2160 Quilchena Square, 1800 Garcia St. Merritt, BC  V1K 1B8'
print(clean_po_box(address))

address = 'P.O. Box 940 Stn Fort Langley 100 - 23148 96 Ave Langley, BC  V1M 2S3 CANADA'
print(clean_po_box(address))
