"""
UNDER DEVELOPMENT !!!

This Python script is used to track the flights that are within a certain
distance and altitude of the given home coordinates using ADS-B data.
The script uses the requests module to get the JSON data from a local
dump1090 .json server, which provides information about all the planes in
the vicinity. The geopy module is used to calculate the distance between
the home coordinates and the plane coordinates.

The script sets a maximum distance and a maximum height, within which the
flights will be tracked. The script stores the closest approach of each
flight in a dictionary and writes the data to a text file. The script runs
in a continuous loop, checking for updates every 2 seconds.

The script can be modified to track flights in a different location or
within a different range by updating the home coordinates, maximum distance,
and maximum height.

Script by: MrLunk April 2023
Source: https://github.com/mrlunk/Plane-Tracking-ADSB 
"""

import requests
from geopy.distance import geodesic
import time
from datetime import datetime

# Set your Home-coordinates here as precisely as possible
home_coords = (52.43362, 4.65424)

# Log all planes within MaxDistance and MinHeight.
MaxDistance = 5 # Nautical Miles (1852m = 1 Nm / 0.53995 Nm = 1 km)
MaxHeight = 10000  # Foot (3280 ft = 1km)

# URL for the local ADS-B dump1090 info
url = "http://192.168.2.13:8080/data/aircraft.json"

# Create a dictionary to store the closest approach of each flight
flight_dict = {}

# Define the filename for the output file
filename = "closest_approach.txt"

while True:
    try:
        # Get the JSON data from the URL
        response = requests.get(url)
        data = response.json()

        # Loop through all the aircraft in the JSON data
        for aircraft in data['aircraft']:
            # Get the flight information
            flight = aircraft.get('flight')
            speed = aircraft.get('gs')
            lat = aircraft.get('lat')
            lon = aircraft.get('lon')
            alt = aircraft.get('alt_baro')

            # Calculate the distance from home-coordinates to the plane coordinates
            plane_coords = (lat, lon)
            distance = geodesic(home_coords, plane_coords).miles

            # If the distance is within given MaxDistance miles and under MaxHeight Miles
            if distance <= MaxDistance:
                if alt <= MaxHeight:
                    # Check if the flight already exists in the dictionary
                    if flight in flight_dict:
                        # Check if the current distance is closer than the stored distance
                        if distance < flight_dict[flight]["distance"]:
                            # Update the flight information in the dictionary
                            flight_dict[flight]["speed"] = speed
                            flight_dict[flight]["distance"] = distance
                            flight_dict[flight]["altitude"] = alt
                            flight_dict[flight]["latitude"] = lat
                            flight_dict[flight]["longitude"] = lon
                    else:
                        # Add the flight information to the dictionary
                        flight_dict[flight] = {
                            "speed": speed,
                            "distance": distance,
                            "altitude": alt,
                            "latitude": lat,
                            "longitude": lon,
                        }

        # Add timestamp and date to the output
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write the closest approach of each flight to the output file
        with open(filename, "w") as f:
            for flight, data in flight_dict.items():
                closest_approach = (
                    f"{now} |  Flight {flight} | Spd: {data['speed']} | Dist: {data['distance']} Nm | Alt: {data['altitude']} ft | Lat: {data['latitude']} | Lon: {data['longitude']}\n"
                )
                f.write(closest_approach)
                print(f"{now} |  Flight {flight} | Spd: {data['speed']} | Dist: {data['distance']} Nm | Alt: {data['altitude']} ft | Lat: {data['latitude']} | Lon: {data['longitude']}")

    except Exception as e:
        print("Error:", e)

    time.sleep(1)
