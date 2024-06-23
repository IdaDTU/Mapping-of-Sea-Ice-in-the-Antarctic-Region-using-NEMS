from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from initialize_basemap import initialize_basemap

def plot_satellite_paths(combined_ds):
    """
    Plot satellite paths of Nimbus5 (NEMS) on the Southern Hemisphere.

    Parameters:
        combined_ds (xarray.Dataset): Combined dataset containing latitude and longitude.
        title (string): Title of plot
    Returns:
        None
    """
    lats = combined_ds['LAT']
    lons = combined_ds['LON']
    
    m = Basemap(projection='spstere', boundinglat=-50, lon_0=0, resolution='l', round=True)
    initialize_basemap()
    
    
    x, y = m(lons, lats)
    m.scatter(x, y, marker='.', s=20,color='#4358cb')
    plt.show()