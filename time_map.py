#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from connection import GetAvgTime
import unicodedata
import re
import os
import sys



# converts a string to a slug string
def slugify(value):
    value = unicodedata.normalize('NFKD', value)
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value

# Finds the duration of the public transport connection from/to pivot stop to/from all stops in the given list.
# Public API for Prague public transport is used. Documentation for the API can be found here: https://crws.docs.apiary.io/
# Saves backups each 50 stops.
# Allows resume of the download after given number of stops (using id of the last stop).
def ReachStops(pivot_direction, pivot_stop, all_stops, departure_time, output_file_format, skip_up_to_excluding = -1):
    reached_stops = []
    c = 0
    for stop in all_stops:
        c += 1
        if stop["item"]["item"] < skip_up_to_excluding:
            continue
        
        inspected_stop = stop["item"]["name"]
        
        stop_from = inspected_stop
        stop_to = pivot_stop
        
        if (pivot_direction == "to"):
            stop_from = inspected_stop
            stop_to = pivot_stop
        elif (pivot_direction == "from"):
            stop_from = pivot_stop
            stop_to = inspected_stop
        else:
            raise Exception("Unknown direction")            
        
        conn_time, conn_minutes, arrival_times = GetAvgTime(stop_from, stop_to, departure_time)
        if pivot_stop == inspected_stop:
            conn_time = 0
        
        if conn_time >= 0:
            time_from = {"pivot_stop": pivot_stop, "time": conn_time, "minutes": conn_minutes, "arrivals": arrival_times, "direction": pivot_direction}
            if not "time_stats" in stop:
                stop["time_stats"] = [time_from]
            else:
                stop["time_stats"].append(time_from)
            reached_stops.append(stop)
            
            print("From {0} to {1} in {2} minutes".format(stop_from, stop_to, conn_time))
        else:
            print("No connection from {0} to {1}".format(stop_from, stop_to))
        
        if c % 50 == 0:
            file_slug = "{0}-{1}".format(slugify(pivot_stop), str(c))
            output_file = output_file_format.format(file_slug)
            print('Saving temporary output', output_file)
            with open(output_file, mode="w+", encoding="utf-8") as f:
                json.dump(reached_stops, f, indent=2, ensure_ascii=False)
    
    return reached_stops

def main():
	
    all_stops = []
    with open("pid_stops-filtered.json", mode="r", encoding="utf-8") as f:
        all_stops = json.load(f)
    
    pivot_stop = 'Anděl' 
    pivot_direction = 'to'
    departure_time = "5.3.2018 8:45"
    
    if len(sys.argv) == 2:
        pivot_stop = sys.argv[1]
    elif len(sys.argv) == 3:
        pivot_direction = sys.argv[1]
        pivot_stop = sys.argv[2]
    elif len(sys.argv) == 4:
        pivot_direction = sys.argv[1]
        pivot_stop = sys.argv[2]
        departure_time = sys.argv[3]
    
    print(pivot_stop)
    
    pivot_slug = slugify(pivot_stop);
    data_dir = "./" + pivot_slug
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    reached_stops = ReachStops(pivot_direction, pivot_stop, all_stops, departure_time, data_dir + "/arrivals-{0}.json")
    
    file_name = data_dir + "/arrivals-final.json"
    with open(file_name, mode="w+", encoding="utf-8") as f:
        json.dump(reached_stops, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

