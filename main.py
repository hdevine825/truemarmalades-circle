import numpy as np
import json
from html_template import html_template

def calculate_circle_wgs84(lat_center, lon_center, radius, num_points=100):
    lat_center_rad = np.radians(lat_center)
    lon_center_rad = np.radians(lon_center)
    R_earth = 6371000
    angles = np.linspace(0, 2 * np.pi, num_points)
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
center_lat = 37.7749  # Latitude of center
center_lon = -122.4194  # Longitude of center
radius = 100000  # Radius in meters
circle_points = calculate_circle_wgs84(center_lat, center_lon, radius)
circle_coords = json.dumps(circle_points)

# Fill in the HTML template with the circle coordinates and center coordinates

def DIYformat(string, dict):
    for k,v in dict.items():
        string = string.replace(k,str(v))
    return string

replacement_map = {
    '{center_lat}': center_lat,
    '{center_lon}': center_lon,
    '{circle_coords}': circle_coords
}

html_content = DIYformat(html_template, replacement_map)

# Save the HTML content to a file
html_file_path = 'interactive_maplibre_map.html'
with open(html_file_path, 'w') as f:
    f.write(html_content)