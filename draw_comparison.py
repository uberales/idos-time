#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import png
from draw_map_from_data import LoadMap

# Various function for coloring data

def GetRgb_linear_compared2(val_a, val_b, cutoff_t_a, cutoff_t_b):
    dt = 1
    r, g, b = (0, 0, 0)
    if val_a < cutoff_t_a and val_b < cutoff_t_b:
        r = 255 - int(255 * val_a / cutoff_t_a)
        b = 255 - int(255 * val_b / cutoff_t_b)
    elif (val_a >= cutoff_t_a and val_a < cutoff_t_a + dt) or (val_b >= cutoff_t_b and val_b < cutoff_t_b + dt):
        r = 255 - int(255 * (val_a - cutoff_t_a) / dt) if (val_a >= cutoff_t_a and val_a < cutoff_t_a + dt) else 0
        b = 255 - int(255 * (val_b - cutoff_t_b) / dt) if (val_b >= cutoff_t_b and val_b < cutoff_t_b + dt) else 0
    else:
        r, g, b = (0, 0, 0)
    
    return (r, g, b)

def GetRgb_linear_compared3(val_a, val_b, val_c, cutoff_t_a, cutoff_t_b, cutoff_t_c):
    dt = 1
    r, g, b = (0, 0, 0)
    if val_a < cutoff_t_a and val_b < cutoff_t_b and val_c < cutoff_t_c:
        r = 255 - int(255 * val_a / cutoff_t_a)
        g = 255 - int(255 * val_b / cutoff_t_b)
        b = 255 - int(255 * val_c / cutoff_t_c)
    elif (val_a >= cutoff_t_a and val_a < cutoff_t_a + dt) or (val_b >= cutoff_t_b and val_b < cutoff_t_b + dt) or (val_c >= cutoff_t_c and val_c < cutoff_t_c + dt):
        r = 255 - int(255 * (val_a - cutoff_t_a) / dt) if (val_a >= cutoff_t_a and val_a < cutoff_t_a + dt) else 0
        g = 255 - int(255 * (val_b - cutoff_t_b) / dt) if (val_b >= cutoff_t_b and val_b < cutoff_t_b + dt) else 0
        b = 255 - int(255 * (val_c - cutoff_t_c) / dt) if (val_c >= cutoff_t_c and val_c < cutoff_t_c + dt) else 0
    else:
        r, g, b = (0, 0, 0)
    
    return (r, g, b)

def CompareTwo(input_file_a, input_file_b, output_file_name_format, cutoff_t, travel_a, travel_b):
    
    cutoff_t_a = cutoff_t - travel_a
    cutoff_t_b = cutoff_t - travel_b
    
    time_map_a, left_bottom, right_top = LoadMap(input_file_a)
    time_map_b, left_bottom, right_top = LoadMap(input_file_b)
    
    print(left_bottom)
    print(right_top)
    
    res_lon = len(time_map_a[0])
    res_lat = len(time_map_a)
    
    print(res_lon, res_lat)
    
    image_data = [[0 for i in range(3 * res_lon)] for j in range(res_lat)]
    
    for i_lat in range(res_lat):
        for i_lon in range(res_lon):
            i_r = i_lon * 3
            i_g = i_lon * 3 + 1
            i_b = i_lon * 3 + 2
    #        r, g, b = GetRgb_linear(time_map[i_lat][i_lon], stops_map[i_lat][i_lon], max_t)
            r, g, b = GetRgb_linear_compared2(time_map_a[i_lat][i_lon], time_map_b[i_lat][i_lon], cutoff_t_a, cutoff_t_b)
            image_data[i_lat][i_r] = r
            image_data[i_lat][i_g] = g
            image_data[i_lat][i_b] = b
    
    output_file = output_file_name_format.format(res_lon, cutoff_t)
    with open(output_file, 'wb') as f:
        w = png.Writer(res_lon, res_lat, greyscale=False)
        w.write(f, image_data)
    
    print('Done, output written to {0}'.format(output_file))
    
def CompareThree(input_file_a, input_file_b, input_file_c, output_file_name_format, cutoff_t, travel_a, travel_b, travel_c):
    
    cutoff_t_a = cutoff_t - travel_a
    cutoff_t_b = cutoff_t - travel_b
    cutoff_t_c = cutoff_t - travel_c
    
    time_map_a, left_bottom, right_top = LoadMap(input_file_a)
    time_map_b, left_bottom, right_top = LoadMap(input_file_b)
    time_map_c, left_bottom, right_top = LoadMap(input_file_c)
    
    print(left_bottom)
    print(right_top)
    
    res_lon = len(time_map_a[0])
    res_lat = len(time_map_a)
    
    print(res_lon, res_lat)
    
    image_data = [[0 for i in range(3 * res_lon)] for j in range(res_lat)]
    
    for i_lat in range(res_lat):
        for i_lon in range(res_lon):
            i_r = i_lon * 3
            i_g = i_lon * 3 + 1
            i_b = i_lon * 3 + 2
            r, g, b = GetRgb_linear_compared3(time_map_a[i_lat][i_lon], time_map_b[i_lat][i_lon], time_map_c[i_lat][i_lon], cutoff_t_a, cutoff_t_b, cutoff_t_c)
            image_data[i_lat][i_r] = r
            image_data[i_lat][i_g] = g
            image_data[i_lat][i_b] = b
    
    output_file = output_file_name_format.format(res_lon, cutoff_t)
    with open(output_file, 'wb') as f:
        w = png.Writer(res_lon, res_lat, greyscale=False)
        w.write(f, image_data)
    
    print('Done, output written to {0}'.format(output_file))

def main():
         
	# Input:
	# Source: a file produced by fortran utility (matrix n-by-m of the duration to a specified point in a grid)
	# Travel: an additional time needed to get to the destination point from the pivot stop
		 
    input_a = {"source": 'stop-a/time_map.map', "travel": 6}
    input_b = {"source": 'stop-b/time_map.map', "travel": 13}
    input_c = {"source": 'stop-c/time_map.map', "travel": 5}

    output_file_name_format2 = 'comparison-ab-{0}-{1}.png'
    output_file_name_format3 = 'comparison-abc-{0}-{1}.png'
    
    cutoff_times = [30, 35, 40, 45, 50, 55, 60]
    
    for cutoff_t in cutoff_times:
        CompareTwo(input_a["source"], input_b["source"], output_file_name_format2, cutoff_t, input_a["travel"], input_b["travel"])
        CompareThree(input_a["source"], input_b["source"], input_c["source"], output_file_name_format3, cutoff_t, input_a["travel"], input_b["travel"], input_c["travel"])
    
if __name__ == "__main__":
    main()

