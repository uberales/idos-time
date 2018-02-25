#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import png
import re
import os

# various functions for conversion of the time duration to RGB

def GetRgb_linear(t_val, stops_val, max_t):
    q = 255 - int(255 * t_val / max_t)
    r = q
    g = q if stops_val == 0 else 0
    b = q if stops_val == 0 else 0
    return (r, g, b)

def GetRgb_linear_with_cutoff(t_val, stops_val, cutoff_t):
    dt = 1 # min
    r, g, b = (0, 0, 0)
    if stops_val > 0:
        r, g, b = (255, 0, 0)
    elif t_val >= cutoff_t + dt:
        r, g, b = (0, 0, 0)
    elif t_val > cutoff_t:
        q = 255 - int(255 * (t_val - cutoff_t) / dt)
        r, g, b = (0, q, 0)
    else:
        q = 255 - int(255 * t_val / cutoff_t)
        r, g, b = (q, q, q)
    return (r, g, b)


def GetG2R_linear_with_cutoff(t_val, stops_val, cutoff_t):
    dt = 1 # min
    r, g, b = (0, 0, 0)
    if stops_val > 0:
        b = 255
    elif t_val > cutoff_t:
        r = 255 - int(255 * (t_val - cutoff_t) / dt)        
    else:
        q = t_val / cutoff_t;
        
        r = int(255 * q / 0.5) if q < 0.5 else 255
        g = 255 if q < 0.5 else 255 - int(255 * (q - 0.5) / 0.5)
        
    return (r, g, b)

# Loads the time map from a file processed by the Fortran utility
	
def LoadMap(file_name):
    grid_data = []
    max_value = 0
    left_bottom = ()
    right_top = ()
    with open(file_name, 'r') as f:
        first_line = [float(s) for s in re.split(r'[;,\s]\s*', f.readline().strip())]
        second_line = [float(s) for s in re.split(r'[;,\s]\s*', f.readline().strip())]
        
		# There was some typo in the fortran program and I was too lazy to re-convert all images.
		# Find the coordinates of the area.
        if len(first_line) == 3 and len(second_line) == 1:
            left_bottom = (first_line[0], first_line[1])
            right_top = (first_line[2], second_line[0])
        elif len(first_line) == 2 and len(second_line) == 2:
            left_bottom = (first_line[0], first_line[1])
            right_top = (second_line[0], second_line[1])
            
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            if not l == '':
                data = [float(t) for t in re.split(r'[;,\s]\s*', l)]
                grid_data.append(data)
                current_max = max(data)
                max_value = max(current_max, max_value)
            
    return (grid_data, left_bottom, right_top)


def main():
            
    
    input_file = 'time_map.map'
    stops_file = 'stops_map.map'
    
    time_map, left_bottom, right_top = LoadMap(input_file)
    stops_map, left_bottom, right_top = LoadMap(stops_file)
    
    print(left_bottom)
    print(right_top)
    
    res_lon = len(time_map[0])
    res_lat = len(time_map)
    max_t = np.amax(time_map)
    
    print(res_lon, res_lat)
    print(max_t)
    
    cutoff_t = 20 # min
        
    image_data = [[0 for i in range(3 * res_lon)] for j in range(res_lat)]
    
    for i_lat in range(res_lat):
        for i_lon in range(res_lon):
            i_r = i_lon * 3
            i_g = i_lon * 3 + 1
            i_b = i_lon * 3 + 2
			# place your own function here
#            r, g, b = GetRgb_linear(time_map[i_lat][i_lon], stops_map[i_lat][i_lon], max_t)
#            r, g, b = GetRgb_linear_with_cutoff(time_map[i_lat][i_lon], stops_map[i_lat][i_lon], cutoff_t)
            r, g, b = GetG2R_linear_with_cutoff(time_map[i_lat][i_lon], stops_map[i_lat][i_lon], cutoff_t)
            image_data[i_lat][i_r] = r
            image_data[i_lat][i_g] = g
            image_data[i_lat][i_b] = b
    
    print("Maximum time: {0}".format(max_t))
    
	output_file_name = os.path.basename(input_file)
    output_file_name += "-{0}-{1}.png".format(res_lon, cutoff_t)
    
    with open(output_file_name, 'wb') as f:
        w = png.Writer(res_lon, res_lat, greyscale=False)
        w.write(f, image_data)

if __name__ == "__main__":
    main()
