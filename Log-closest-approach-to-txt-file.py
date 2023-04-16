"""
UNDER DEVELOPMENT !!!

This Python script uses the requests library to retrieve data from
a Dump1090 ADSB JSON API server, and the geopy library to calculate
distances between coordinates.

The script continuously loops to monitor the data from the API and
looks for nearby aircraft that are within a certain distance and altitude
from a given home location.

It then records the flight data of the closest aircraft and writes it to a text file.

Script by: MrLunk April 2023
Source: https://github.com/mrlunk/Plane-Tracking-ADSB 
"""

import requests
from geopy.distance import geodesic
import time
from datetime import datetime

home_coords = (52.43362, 4.65424)

MaxDistance = 5 
MaxHeight = 10000  # 6561 ft = 2km
 
url = "http://192.168.2.13:8080/data/aircraft.json"

flight_dict = {}

filename = "closest_approach.txt"

while True:
    try:
        response = requests.get(url)
        data = response.json()
        datenow = datetime.now().strftime("%Y-%m-%d")
        timenow = datetime.now().strftime("%H:%M:%S")

        for aircraft in data['aircraft']:
            hexcode = aircraft.get('hex')
            flight = aircraft.get('flight')
            speed = aircraft.get('gs')
            lat = aircraft.get('lat')
            lon = aircraft.get('lon')
            alt = aircraft.get('alt_baro')
             

            plane_coords = (lat, lon)
            distance = geodesic(home_coords, plane_coords).miles

            if distance <= MaxDistance:
                if alt <= MaxHeight:
                    if flight in flight_dict:
                        if distance < flight_dict[flight]["distance"]:
                            flight_dict[flight]["hexcode"] = hexcode
                            flight_dict[flight]["speed"] = speed
                            flight_dict[flight]["distance"] = distance
                            flight_dict[flight]["altitude"] = alt
                            flight_dict[flight]["latitude"] = lat
                            flight_dict[flight]["longitude"] = lon
                            flight_dict[flight]["datenow"] = datenow
                            flight_dict[flight]["timenow"] = timenow
                    else:
                        flight_dict[flight] = {
                            "hexcode": hexcode,
                            "speed": speed,
                            "distance": distance,
                            "altitude": alt,
                            "latitude": lat,
                            "longitude": lon,
                            "datenow": datenow,
                            "timenow": timenow,
                        }

        with open(filename, "w") as f:
            for flight, data in flight_dict.items():
                closest_approach = (
                    f"Dt: {data['datenow']} | Ti: {data['timenow']} | Hex: {data['hexcode']} | Flt: {flight} | Spd: {data['speed']} | Dist: {data['distance']} Nm | Alt: {data['altitude']} ft | Lat: {data['latitude']} | Lon: {data['longitude']}\n"
                )
                f.write(closest_approach)

    except Exception as e:
        print("Error:", e)

    time.sleep(1)
