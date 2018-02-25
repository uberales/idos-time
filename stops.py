# -*- coding: utf-8 -*-

import urllib.request as rq
import json

# Load all stops from public API by Chaps.
# There is a maximum of 100 stops that can be loaded by 1 request.
# Public API documentation can be found here https://crws.docs.apiary.io/

skip_count = 0
max_count = 100

all_stops = [];

while True:
    response_text = ""
    
    with rq.urlopen("https://ext.crws.cz/api/ABCz/timetableObjects/301003?ttInfoDetails=65&searchMode=4&maxCount={0}&skipCount={1}".format(max_count, skip_count)) as response:
        response_text = response.read()
        
    r_obj = json.loads(response_text.decode('utf-8'))
    if (r_obj["data"] == None):
        break
    else:
        all_stops.extend(r_obj["data"])
        skip_count += max_count
        print("Total stops found: {0}".format(len(all_stops)))


with open("pid_stops.json", mode="w+", encoding="utf-8") as f:
    json.dump(all_stops, f, indent=2, ensure_ascii=False)

print("Stops loaded.")