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
            if distance <= 5:
                print(f"Flight {flight} | Speed: {speed} | Distance: {distance} miles | Altitude: {alt} ft")

    except Exception as e:
        print("Error:", e)

    time.sleep(1)
