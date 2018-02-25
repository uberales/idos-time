#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

all_stops = []

file_name = "pid_stops.json"

with open(file_name, mode="r", encoding="utf-8") as f:
    all_stops = json.load(f)

filtered_stops = []

min_lat = 14.2499750
max_lat = 14.5809381
min_lon = 49.9953133
max_lon = 50.1552786

stop_i = 0
for stop in all_stops:
    if stop["coorX"] >= min_lon and stop["coorX"] <= max_lon and stop["coorY"] >= min_lat and stop["coorY"] <= max_lat:
        stop["item"]["item"] = stop_i
        stop_i += 1
        filtered_stops.append(stop)

file_name = os.path.basename(input_file)
file_name += "-filtered.json"
with open(file_name, mode="w+", encoding="utf-8") as f:
    json.dump(filtered_stops, f, indent=2, ensure_ascii=False) 