import numpy as np
import pandas as pd
from pykrige.ok import OrdinaryKriging
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def haversine(lon1, lat1, lon2, lat2):
    R = 6371.0  # Earth radius in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance

def calculate_SIE(df, variable):
    # Extract latitude and longitude from the DataFrame
    LON = df['LON'].values
    LAT = df['LAT'].values
    z = variable
    
    # Define the grid on which to interpolate the data
    grid_size = 200  # Increase grid size for more accuracy
    xi = np.linspace(LON.min(), LON.max(), grid_size)
    yi = np.linspace(LAT.min(), LAT.max(), grid_size)
    xi, yi = np.meshgrid(xi, yi)

    # Perform kriging interpolation
    variogram_parameters = [1.0, 10, 0.001]  # Adjust parameters as necessary
    OK = OrdinaryKriging(LON, LAT, z, variogram_model='spherical', variogram_parameters=variogram_parameters, verbose=False, enable_plotting=False)
    zi, ss = OK.execute('grid', xi[0], yi[:, 0])
    
    # Reclassify the raster to 0 = 0-30% cover and 1 = >30% cover
    ice_threshold = 0.3
    reclassified_zi = np.where(zi > ice_threshold, 1, 0)
    
    # Count the "1" pixels
    ice_pixel_count = np.sum(reclassified_zi)
    
    # Calculate the actual size of one pixel using the Haversine formula
    lat_min, lat_max = yi.min(), yi.max()
    lon_min, lon_max = xi.min(), xi.max()

    # Calculate distances (in kilometers) using the Haversine formula
    dx = haversine(lon_min, lat_min, lon_max, lat_min) / grid_size
    dy = haversine(lon_min, lat_min, lon_min, lat_max) / grid_size

    # Calculate pixel area
    pixel_area = dx * dy

    # Calculate the total ice area in km²
    total_ice_area = ice_pixel_count * pixel_area

    return total_ice_area
