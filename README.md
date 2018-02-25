# idos-time
A simple tool for visualising Prague public transport time for a selected stop.

IDOS (Chaps) has a public API for Prague public transport (PID; without trains, sadly). You can search for a connection or whatever you'd like. I wanted to see how far can I get from my flat to any place in 30 minutes. So I made this. No guarantee whatsoever is granted.

Public documentation of the aforementioned API can be found here: https://crws.docs.apiary.io

Approximately 1 request per second is permitted by the API. Running multiple scripts communicating with the API won't help anything.

Usage:

- Compile the Fortran utility ;).

- Load stops from IDOS using `stops.py`.
- Optionally: Filter them using `filter_stops.py` (restrict the area by latitude and longitude of left bottom and right top corner).
- Select a stop.
- Run `time_map.py`, for example like this `python time_map.py from "Můstek"`
- Run `draw_map.py`.
- Run the Fortran utility, for example like this `./idos-map -i data/from/draw_map.dat -o time_map.map -s stop_map.map -r 1024`
- Run `draw_map_from_data.py` or `draw_comparison.py`.

Some specification of input files is probably needed inside the script files.