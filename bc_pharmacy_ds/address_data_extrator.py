import re

def address_extractor(full_address):
    try:
       return re.search('.+(BC\s+([A-Z0-9]{3}\s+[A-Z0-9]{3}\s+)CANADA)', full_address).group(1)
    except AttributeError:
        print('extration failed with input: {}'.format(full_address))
        return ""


