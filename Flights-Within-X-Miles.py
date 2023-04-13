"""
This script retrieves information about aircraft from a local flight tracker
(PiAware with FlightAware Pro Stick)
and calculates the distance between the plane's coordinates and a set of home
coordinates. If the plane is within 3 miles of the home coordinates and at an
altitude of 3000 feet or lower, the flight information is printed.
The script continuously runs in an infinite loop, with a 2-second pause between
each iteration. 
The script makes use of the requests library to retrieve data from a URL and the
geopy library to calculate the geodesic distance between two sets of coordinates. 
"""

import requests
from geopy.distance import geodesic
import time

# Home-coordinates
home_coords = (52.43362, 4.65424)

# URL for the local flightaware piaware info
url = "http://192.168.2.13:8080/data/aircraft.json"

while True:
    try:
        # Get the JSON data from the URL
        response = requests.get(url)
        data = response.json()

        # Loop through all the aircraft in the JSON data
        for aircraft in data['aircraft']:
            # Get the flight number, speed, latitude, longitude, and altitude
            flight = aircraft.get('flight')
            speed = aircraft.get('gs')
            lat = aircraft.get('lat')
            lon = aircraft.get('lon')
            alt = aircraft.get('alt_baro')

            # Calculate the distance from home-coordinates to the plane coordinates
            plane_coords = (lat, lon)
            distance = geodesic(home_coords, plane_coords).miles

            # If the distance is within 5 miles, print the flight info
            if distance <= 3:
                if alt <= 3000:
                    print(f"Flight {flight} | Speed: {speed} | Distance: {distance} miles | Altitude: {alt} ft")

    except Exception as e:
        print("Error:", e)

    time.sleep(2)
