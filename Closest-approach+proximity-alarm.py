"""
This is a Python script that uses the ADS-B data of aircraft to calculate the distance
and altitude of aircraft from a fixed location and outputs the closest approaching
aircraft based on certain criteria. The script uses the requests library to get the
ADS-B data from a specified URL and the geopy library to calculate the distance between
two coordinates.
The script also uses the winsound library to produce an alarm beep when an aircraft is
within a certain proximity of the fixed location.

The script sets a home coordinate and specifies certain criteria for selecting aircraft,
such as maximum distance, maximum altitude, proximity distance, and proximity altitude.
The script then loops through the ADS-B data and calculates the distance and altitude of
each aircraft from the home coordinate. If an aircraft meets the specified criteria, it
is added to a dictionary of flights. If the flight is already in the dictionary, its
information is updated if the distance to the home coordinate is shorter than previously
recorded. If an aircraft is within the specified proximity distance and altitude, an alarm
beep is produced, the proximity alarm beep pitch gets higher the closer to the home
coordinates the aircraft get.
Finally, the flights in the dictionary are sorted based on distance,
and the closest approaching aircraft information is written to a text file.

The script runs indefinitely, with a sleep time of 1 second between loops, until an error
occurs. If an error occurs, the error message is printed and the script continues to run.

Script by: MrLunk April-2023
SOurce: https://github.com/mrlunk/Plane-Tracking-ADSB
"""

import requests
from geopy.distance import geodesic
import time
import winsound
from datetime import datetime

home_coords = (52.43362, 4.65424)

MaxDistance = 18 
MaxHeight = 15000 
ProxDist = 2.5 
ProxHeight = 6000 
url = "http://192.168.2.13:8080/data/aircraft.json"

flight_dict = {}

filename = "closest_approach.txt"

# function to determine pitch height for the proximity alarm beeps:
def beep_pitch(distance):
    if distance > 10 or distance < 0:
        print("Distance out of range")
        return
    pitch = int(3000 - 300 * distance)
    duration = 200  # milliseconds
    winsound.Beep(pitch, duration)

while True:
    try:
        #response = requests.get(url)
        response = requests.get(url, timeout=5)
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

                            # proximity alarm beeps when distance is lower then Proximity value:
                            if distance <= ProxDist:
                                if alt <= ProxHeight:
                                    beep_pitch(distance)
                            
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

        # Sort the flight_dict based on the distance value
        sorted_flight_dict = dict(sorted(flight_dict.items(), key=lambda x: x[1]['distance']))

        with open(filename, "w") as f:
            for flight, data in sorted_flight_dict.items():
                closest_approach = (
                    f"Dt: {data['datenow']} | Ti: {data['timenow']} | Hex: {data['hexcode']} | Flt: {flight} | Spd: {data['speed']} | Dist: {data['distance']} mi | Alt: {data['altitude']} ft | Lat: {data['latitude']} | Lon: {data['longitude']}\n"
                )
                f.write(closest_approach)

    except Exception as e:
        print("Error:", e)

    time.sleep(1)
