import numpy as np
import json
from html_template import html_template
import os
from dotenv import load_dotenv
import requests
import polyline
import shapely
import geojson

load_dotenv()

def calculate_circle_wgs84(lat_center, lon_center, radius, offset_points=0, num_points=100):
    lat_center_rad = np.radians(lat_center)
    lon_center_rad = np.radians(lon_center)
    R_earth = 6371000
    if offset_points > 0:
        offset_rad = (offset_points/num_points)*(2 * np.pi)    
    else:
        offset_rad = 0
    angles = np.linspace(0 + offset_rad, 2 * np.pi + offset_rad, num_points)
    lat_points = []
    lon_points = []

    for angle in angles:
        lat_rad = np.arcsin(np.sin(lat_center_rad) * np.cos(radius / R_earth) +
                            np.cos(lat_center_rad) * np.sin(radius / R_earth) * np.cos(angle))
        lon_rad = lon_center_rad + np.arctan2(np.sin(angle) * np.sin(radius / R_earth) * np.cos(lat_center_rad),
                                              np.cos(radius / R_earth) - np.sin(lat_center_rad) * np.sin(lat_rad))
        
        lat_points.append(np.degrees(lat_rad))
        lon_points.append(np.degrees(lon_rad))

    return list(zip(lon_points, lat_points))

# Example usage
center_lat = 41.336  # Latitude of center
center_lon = -100.000  # Longitude of center
radius_1 = 600000  # Radius in meters
radius_2 = 550000
circle_points_1 = calculate_circle_wgs84(center_lat, center_lon, radius_1)
circle_coords_1 = json.dumps(circle_points_1)

circle_points_2 = calculate_circle_wgs84(center_lat, center_lon, radius_2, 0.5)
circle_coords_2 = json.dumps(circle_points_2)


#Valhalla URL
valhalla_url = os.getenv('VALHALLA_URL')
route_costing = "bicycle"
unit = "miles"

def get_route(start, end):
    data = {
        "locations":[
            {"lat": start[1], "lon": start[0]},
            {"lat": end[1], "lon": end[0]}
        ],
        "costing": route_costing,
        "costing_options":{
            route_costing:{
                "bicycle_type": "Cross", #play with settings
            }
        },
        "directions_options": {
            "units": unit
        }
    }
    response = requests.post(valhalla_url+'route', data=json.dumps(data))
    return response.text

def route2linestring(start, end):
    response = get_route(circle_points_1[i],circle_points_2[i])
    dict = json.loads(response)
    polyline_segment = dict["trip"]["legs"][0]["shape"]
    print("Segment distance {} miles".format(dict["trip"]["legs"][0]["summary"]["length"]))
    route_segment = polyline.decode(polyline_segment, 6, geojson=True)
    return shapely.LineString(route_segment)


segments = []
message = "Requesting route from circle {} point {} to circle {} point {}"

for i in range(len(circle_points_1)):
    if i == len(circle_points_1)-1:
        break
    print(message.format(1,i,2,i))
    linestring = route2linestring(circle_points_1[i],circle_points_2[i])
    segments.append(linestring)
    print(message.format(2,i,1,i+1))
    linestring = route2linestring(circle_points_2[i],circle_points_1[i+1])
    segments.append(linestring)

print(len(segments))
route = shapely.union_all(segments)
route = shapely.line_merge(route)
route_geojson=geojson.Feature(geometry=route, properties={})

route_geojson=geojson.dumps(route_geojson)


# Fill in the HTML template with the circle coordinates and center coordinates

def DIYformat(string, dict):
    for k,v in dict.items():
        string = string.replace(k,str(v))
    return string

branch = "double-circle"

replacement_map = {
    '{center_lat}': center_lat,
    '{center_lon}': center_lon,
    '{circle_coords}': circle_coords_1,
    '{branch}': branch
}

html_content = DIYformat(html_template, replacement_map)

# Save the HTML content to a file
html_file_path = 'index.html'
with open(html_file_path, 'w') as f:
    f.write(html_content)

geojson_path = 'route.geojson'

with open(geojson_path, 'w') as f:
    f.write(route_geojson)