#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import numpy
import png
import sys

def GetDistance(a_lat_phi, a_lon_lambda, b_lat_phi, b_lon_lambda):
    a_phi = numpy.deg2rad(a_lat_phi)
    b_phi = numpy.deg2rad(b_lat_phi)
    delta_phi = numpy.deg2rad(b_lat_phi - a_lat_phi)
    delta_lambda = numpy.deg2rad(b_lon_lambda - a_lon_lambda)
    
    a = numpy.sin(0.5 * delta_phi) * numpy.sin(0.5 * delta_phi) + numpy.cos(a_phi) * numpy.cos(b_phi) * numpy.sin(0.5 * delta_lambda) * numpy.sin(0.5 * delta_lambda)
    c = 2 * numpy.arctan2(numpy.sqrt(a), numpy.sqrt(1 - a))
    d = 6378e3 * c
    return d

def GetTotalTime(lat, lon, stop):
    walking_speed = 70.0 # m/min
    additional_time = GetDistance(lat, lon, stop["lat"], stop["lon"]) / walking_speed
    return additional_time + stop["t"]

def RefineValue(mapped_stop):
    lat = mapped_stop["coorX"]
    lon = mapped_stop["coorY"]
    time_stats = mapped_stop["time_from"][0] if "time_from" in mapped_stop else mapped_stop["time_stats"][0]
    m = time_stats["minutes"]
    t = time_stats["time"]
    
    if len(m) == 3: 
        averages = [numpy.average([m[0], m[1]]), numpy.average([m[0], m[2]]), numpy.average([m[1], m[2]])]
        t = min(averages)
    
    return {"lat": lat, "lon": lon, "t": t}

mapped_stops = []

file_name = "arrivals-final.json"

with open(file_name, mode="r", encoding="utf-8") as f:
    mapped_stops = json.load(f)

time_map = [RefineValue(s) for s in mapped_stops]

output_file_name = os.path.basename(input_file)
output_file_name += "-fortran.dat"

with open(output_file_name, 'w') as f:
    f.write(str(len(time_map)))
    f.write("\n")
    for s in time_map:
        f.write("{0}\t{1}\t{2}\n".format(s["lat"], s["lon"], s["t"]))
