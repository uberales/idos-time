#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request as rq
from urllib.parse import urlencode
import json
import numpy

# Loads the connection from IDOS public API.
# Public API documentation can be found here https://crws.docs.apiary.io/


def GetConnection(station_from, station_to, departure_time):
    
    data = urlencode({'from': station_from, 'to': station_to, 'dateTime': departure_time, 'ttDetails': 3, 'maxCount': 3})
    data.encode('ascii')
    
    connection_data = {}
    
    with rq.urlopen("https://ext.crws.cz/api/ABCz/connections?{0}".format(data)) as response:
        connection_data = json.loads(response.read().decode('utf-8'))    
    
    return connection_data
    
    
def GetAvgTime(station_from, station_to, departure_time):

    conn_avg = 0.0
    arrival_times = []
    conn_minutes = []
    try:
        connection_data = GetConnection(station_from, station_to, departure_time)
        
        conn_lengths = [c["timeLength"] for c in connection_data["connInfo"]["connections"]]
        arrival_times = [c["trains"][-1]["dateTime2"] for c in connection_data["connInfo"]["connections"]]
        for c_l in conn_lengths:
            t = 0
            data = c_l.split(" ")
            data_len = len(data)
            if (data_len >= 2):
                if (data[-1] == 'hod'):
                    t += int(data[-2]) * 60
                else:
                    t += int(data[-2])
            if (data_len >= 4):
                t += int(data[-4]) * 60
            conn_minutes.append(t)
            
        conn_avg = numpy.mean(conn_minutes)
    except:
        conn_avg = -1
    
    return (conn_avg, conn_minutes, arrival_times)


def main():
    
    station_from = "Airport (Terminal 1)"
    station_to = "Roztylské náměstí"
    departure_time = "5.3.2018 8:45"
    conn_time, conn_lengths, arrival_times = GetAvgTime(station_from, station_to, departure_time)
    print(conn_time)
    print(conn_lengths)
    print(arrival_times)

if __name__ == "__main__":
    main()
