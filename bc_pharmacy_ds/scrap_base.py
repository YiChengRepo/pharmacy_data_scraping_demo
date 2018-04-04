import requests
from bs4 import BeautifulSoup
from bc_pharmacy_ds.utils import clean_po_box
from bc_pharmacy_ds.utils import get_google_geo_location_api_key
from bc_pharmacy_ds.address_data_extrator import address_extractor
import json

file_location = '/Users/yi.cheng/Documents/mongdo/spatial/pharmacy_seq.json'
log_location = '/Users/yi.cheng/Documents/mongdo/spatial/scrapping.log'


def write_to_log_file(error):
    log_file = open(log_location, 'a')
    log_file.write(error + '\n')

def append_to_file(pharmacy, file_location):
    pharmacy_str = json.dumps(pharmacy, ensure_ascii=False)
    pharmacy_file = open(file_location, 'a')
    if pharmacy is None:
        write_to_log_file('this pharmacy is null')
    pharmacy_file.write(pharmacy_str + '\n')


def write_to_file(pharmacy_list, file_location):
    with open(file_location, 'a') as outfile:
        json.dump(pharmacy_list, outfile, ensure_ascii=False)
        outfile.write('\n')


def get_google_geocode_url(address):
    api_key = get_google_geo_location_api_key()
    google_geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address=\'{}\'&key={}".format(
        address, api_key)
    return google_geocode_url


def get_geocode_url_from_new_address(pharmacy):
    postcode_province = cleanAddress(address_extractor(pharmacy.get("address")))
    new_address = "{} {}".format(pharmacy.get("name"), postcode_province)
    print("new address is [{}]".format(new_address))
    return get_google_geocode_url(new_address)

def cleanAddress(address):
    return address.strip().replace('\r', ' ').replace('#', '')

def get_listing():
    r = requests.get('http://www.bcpharmacists.org/list-community-pharmacies')
    print(r)
    in_pharmacy_list = []
    soup = BeautifulSoup(r.text, 'html.parser')

    for table_row in soup.select("table.sticky-enabled tr"):
        cells = table_row.findAll('td')
        if len(cells) > 0:
            name = cleanAddress(cells[0].text)
            address = cleanAddress(cells[1].text)
            address = clean_po_box(address)
            phone = cells[3].text.strip()
            fax = cells[4].text.strip()
            pharmacy = create_pharmacy_base(name, address, phone, fax)
            in_pharmacy_list.append(pharmacy)

    print(len(in_pharmacy_list))
    print("================================")
    return in_pharmacy_list

def scrap_new_strategy(pharmacy):
    try:
        print('retry new strategy')
        new_url = get_geocode_url_from_new_address(pharmacy)
        print('new_url is {}'.format(new_url))
        geo_response = requests.get(new_url)
        if geo_response.status_code != 200:
            print('Status:', geo_response.status_code, 'Problem with the request url {}'.format(url))
            return
        print(geo_response)
        geo_data = geo_response.json()
        if len(geo_data['results']) == 0:
            res_json = json.dumps(pharmacy, ensure_ascii=False)
            error = 'this request has gone wrong {0}  and pharmacy is {1} in retry'.format(new_url, res_json)
            print(error)
            write_to_log_file(error)
            print('retrying...')
            # retry with new strategy , pharmacy_name + post code
            print('*****************************************')
            return
        print('recovered !')
        write_to_log_file("recovered!")
        print('*****************************************==========================')
        return geo_data
    except Exception as e:
        print('exception caught ' + str(e))
        write_to_log_file('exception' + str(e))

def scrap(pharmacy):
    url = get_google_geocode_url(pharmacy.get("address"))
    geo_response = requests.get(url)
    print(url)
    if geo_response.status_code != 200:
        print('Status:', geo_response.status_code, 'Problem with the request url {}'.format(url))
        return
    print(geo_response)
    geo_data = geo_response.json()
    if len(geo_data['results']) == 0:
        error = 'this request has gone wrong {0}  and pharmacy is {1}'.format(url, json.dumps(pharmacy, ensure_ascii=False))
        print('*****************************************')
        print(error)
        write_to_log_file(error)
        # retry with new strategy , pharmacy_name + post code
        geo_data = scrap_new_strategy(pharmacy)
        print('*****************************************')
    location = geo_data['results'][0]['geometry']['location']
    print(location)
    geo_json_location = {'type': "Point", 'coordinates': [location['lng'], location['lat']]}
    pharmacy['location'] = geo_json_location
    print(geo_json_location)
    print(pharmacy)
    print("================================")
    if pharmacy is None:
        error = 'pharmacy is None in scrap {}'.format(url)
        print(error)
        write_to_log_file(error)
    return pharmacy


def create_pharmacy_base(name, address, phone, fax):
    return {'name': name, 'address': address, 'phone': phone, 'fax': fax}
