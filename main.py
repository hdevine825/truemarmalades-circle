import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

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

    return list(zip(lat_points, lon_points))

# Example usage
center_lat = 37.7749  # Latitude of center
center_lon = -122.4194  # Longitude of center
radius = 1000000  # Radius in meters
circle_points = calculate_circle_wgs84(center_lat, center_lon, radius)
lats, lons = zip(*circle_points)

# Ensure map appears by tting a non-interactive backend
plt.switch_backend('Agg')

# Plotting using Cartopy
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.Mercator())
ax.set_extent([center_lon - 25, center_lon + 25, center_lat - 25, center_lat + 25], crs=ccrs.PlateCarree())
ax.coastlines()

# Add US state borders
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')
ax.add_feature(states_provinces, edgecolor='gray')

# Add the circle points
ax.plot(lons, lats, 'r', transform=ccrs.Geodetic())

# Save the plot as an image file
plt.savefig('circle_on_map.png')

print("The map with has been saved as 'circle_on_map.png'.")