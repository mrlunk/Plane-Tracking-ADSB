"""
This is a Python script that calculates the distance, view direction,
and viewing angle from a home location to a plane in the sky.

The script uses two Python libraries: geopy and geographiclib.
The geopy library is used to calculate the distance between two
coordinates, and the geographiclib library is used to calculate
the bearing between two coordinates.

The script begins by defining the home coordinates and the plane
coordinates, including the altitude of the plane. It then uses the
geodesic function from the geopy library to calculate the distance
between the home and plane coordinates.

Next, the geographiclib library is used to calculate the bearing
between the home and plane coordinates. This bearing is then
converted to a compass direction by subtracting it from 450 and
taking the modulo 360.

Finally, the script calculates the viewing angle from the ground-plane
to the plane in the sky using the math.atan function.
This angle is printed out along with the distance and compass direction.

Note that the script assumes that the Earth is a perfect sphere and
uses the WGS84 ellipsoid to make calculations.

Script by: MrLunk 2023
Source: https://github.com/mrlunk/Plane-Tracking-ADSB/
"""

import geographiclib.geodesic as geo
from geopy.distance import geodesic
import math

# Home coordinates
home_lat, home_lon = 52.43362, 4.65424

# Plane coordinates
plane_lat, plane_lon, plane_alt = 52.410095, 4.524307, 10675

# Calculate distance between home and plane
distance = geodesic((home_lat, home_lon), (plane_lat, plane_lon)).meters

# Calculate bearing between home and plane
g = geo.Geodesic.WGS84.Inverse(home_lat, home_lon, plane_lat, plane_lon)
bearing = g['azi1']

# Convert bearing to compass degrees
compass = (450 - bearing) % 360

# Calculate viewing angle from ground-plane
viewing_angle = math.degrees(math.atan(plane_alt/distance))

# Print results
print("Distance to plane: {:.2f} meters".format(distance))
print("View direction: {:.2f} degrees".format(compass))
print("Viewing angle from ground-plane: {:.2f} degrees".format(viewing_angle))
