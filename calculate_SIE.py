import numpy as np
import pandas as pd
from pykrige.ok import OrdinaryKriging
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def calculate_SIE(df, variable):
    # Extract latitude and longitude from the DataFrame
    LON = df['LON'].values
    LAT = df['LAT'].values
    z = variable
    
    # Define the grid on which to interpolate the data
    xi = np.linspace(LON.min(), LON.max(), 100)
    yi = np.linspace(LAT.min(), LAT.max(), 100)
    xi, yi = np.meshgrid(xi, yi)

    # Perform kriging interpolation
    variogram_parameters = [1.0, 10, 0.001]  # Adjust parameters as necessary
    OK = OrdinaryKriging(LON, LAT, z, variogram_model='spherical', variogram_parameters=variogram_parameters, verbose=False, enable_plotting=False)
    zi, ss = OK.execute('grid', xi[0], yi[:, 0])
    
    # Reclassify the raster to 0 = 0-15% cover and 1 = >15% cover
    ice_threshold = 0.3
    reclassified_zi = np.where(zi > ice_threshold, 1, 0)
    
    # Count the "1" pixels
    ice_pixel_count = np.sum(reclassified_zi)
    
    # Initialize Basemap with the Southern Hemisphere stereographic projection
    m = Basemap(projection='spstere', boundinglat=-50, lon_0=0, resolution='l', round=True)

    # Calculate the actual size of one pixel
    lat_min, lat_max = yi.min(), yi.max()
    lon_min, lon_max = xi.min(), xi.max()

    # Define the corner points for distance calculation
    x1, y1 = m(lon_min, lat_min)
    x2, y2 = m(lon_max, lat_min)
    x3, y3 = m(lon_min, lat_max)

    # Calculate distances (in meters) using the Haversine formula
    dx = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    dy = np.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)

    # Calculate pixel area
    pixel_area = (dx / 100) * (dy / 100)  # Divide by grid size (100x100)

    # Calculate the total ice area in km
    total_ice_area = ice_pixel_count * pixel_area/1e6

    return total_ice_area