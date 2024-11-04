import pandas as pd
import math
from math import pi, sin, cos, asin, sqrt

#Load county data
file_path = 'Illinois_Counties_Data.csv'
il_counties = pd.read_csv(file_path)

#Code from GIS Distance Calculation
def degrees_to_radians(x):
    return (pi / 180) * x

def lon_lat_distance_miles(lon_a, lat_a, lon_b, lat_b):
    """
    Calculate the distance between two points (latitude and longitude) in miles using the Haversine formula.
    """
    radius_of_earth = 24872 / (2 * pi)  #Radius in miles
    c = sin((degrees_to_radians(lat_a) - degrees_to_radians(lat_b)) / 2) ** 2 + \
        cos(degrees_to_radians(lat_a)) * cos(degrees_to_radians(lat_b)) * \
        sin((degrees_to_radians(lon_a) - degrees_to_radians(lon_b)) / 2) ** 2
    return 2 * radius_of_earth * (asin(sqrt(c)))

#Calculate distances between each pair of counties in Illinois
il_counties = il_counties.reset_index(drop=True)
county_distances = {}

for i, row_a in il_counties.iterrows():
    for j, row_b in il_counties.iterrows():
        if i < j:  #Avoid duplicate pairs and self-distances
            county_a, county_b = row_a["county"], row_b["county"]
            lon_a, lat_a = row_a["lng"], row_a["lat"]
            lon_b, lat_b = row_b["lng"], row_b["lat"]
            dist_miles = lon_lat_distance_miles(lon_a, lat_a, lon_b, lat_b)
            county_distances[(county_a, county_b)] = dist_miles

#Convert distances to a DataFrame for easier review and save it
county_distances_df = pd.DataFrame(
    [(county_a, county_b, dist_miles) for (county_a, county_b), dist_miles in county_distances.items()],
    columns=["County A", "County B", "Distance (miles)"]
)

#Save the distance data to a new CSV file for use
county_distances_df.to_csv("Illinois_County_Distances.csv", index=False)
