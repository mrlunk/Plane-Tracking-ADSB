"""
Basic python code example for Real-time Aircraft notifications within
a specified radius and altitude range. (overhead traffic notification basics)


This script retrieves information about aircraft from a local flight tracker
(PiAware with FlightAware Pro Stick)
and calculates the distance between the plane's coordinates and a set of home
coordinates. If the plane is within X miles of the home coordinates and at an
altitude of Z feet or lower, the flight information is printed to console.
(Later this will be saved to database...) 

Script by: MrLunk April 2023
Source: https://github.com/mrlunk/Plane-Tracking-ADSB 
"""

import requests
from geopy.distance import geodesic
import time
from datetime import datetime

# Home-coordinates
home_coords = (52.43362, 4.65424)

# Log all planes within MaxDistance and MinHeight.
MaxDistance = 5 # Nautical Miles
MaxHeight = 4000  # Foot

# URL for the local flightaware piaware info
url = "http://192.168.2.13:8080/data/aircraft.json"

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

            # If the distance is within 5 miles, print the flight info
            if distance <= MaxDistance:
                if alt <= MaxHeight:
                    # Add timestamp and date to the output
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{now} | Flight {flight} | Speed: {speed} | Distance: {distance} miles | Altitude: {alt} ft | Latitude: {lat} | Longitude: {lon}")
                    

    except Exception as e:
        print("Error:", e)

    time.sleep(2)
