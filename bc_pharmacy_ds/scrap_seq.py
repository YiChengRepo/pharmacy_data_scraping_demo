from timeit import default_timer as timer
import os
from bc_pharmacy_ds.scrap_base import *

start = timer()
print("start with {}".format(start))

try:
    os.remove(file_location)
    os.remove(log_location)
except OSError:
    pass

pharmacy_list = None
pharmacy_list = get_listing()
#for full list scraping, comment out the line below but you prob need a paid good API key
pharmacy_list = pharmacy_list[0:100]
rich_pharmacy_list = []

[rich_pharmacy_list.append(scrap(pharmacy)) for pharmacy in pharmacy_list]

for pharmacy in rich_pharmacy_list:
    append_to_file(pharmacy, file_location)

end = timer()
print("end with {}".format(end))
print(end - start)
