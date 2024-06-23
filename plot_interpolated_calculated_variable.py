import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pykrige.ok import OrdinaryKriging
from initialize_basemap import initialize_basemap

def plot_interpolated_calculated_variable(df, variable, label_name, colorbar_min, colorbar_max):
    """
    Plot an interpolated scatter plot of a calculated variable on a map of the Southern Hemisphere using kriging.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing columns for 'LAT' (latitude) and 'LON' (longitude).
        variable (array-like): Array containing the calculated variable values to be plotted.
        label_name (string): Label for the colorbar indicating what the variable represents.
        title (string): Title of the plot.
        colorbar_min (float): Minimum value for the colorbar.
        colorbar_max (float): Maximum value for the colorbar.
        
    Returns:
        None: Displays an interpolated scatter plot on a stereographic projection of the Southern Hemisphere.
    """
    
    # Extract latitude and longitude from the DataFrame
    LON = df['LON'].values
    LAT = df['LAT'].values
    z = variable
    
    # Define the grid on which to interpolate the data
    xi = np.linspace(LON.min(), LON.max(), 100)
    yi = np.linspace(LAT.min(), LAT.max(), 100)
    xi, yi = np.meshgrid(xi, yi)
    
    # Perform kriging interpolation
    variogram_parameters = [1.0, 10, 0.001] #maybe sill for GR: 4.5e-05
    OK = OrdinaryKriging(LON, LAT, z, variogram_model='spherical', variogram_parameters=variogram_parameters, verbose=False, enable_plotting=False)
    zi, ss = OK.execute('grid', xi[0], yi[:, 0])
    
    # Initialize Basemap with the Southern Hemisphere stereographic projection
    m = Basemap(projection='spstere', boundinglat=-50, lon_0=0, resolution='l', round=True)
    initialize_basemap()
    
    # Convert the coordinates from centers to edges
    xi_edges = np.linspace(LON.min(), LON.max(), 101)
    yi_edges = np.linspace(LAT.min(), LAT.max(), 101)
    xi_edges, yi_edges = np.meshgrid(xi_edges, yi_edges)

    # Plot interpolated data
    x, y = m(*np.meshgrid(xi_edges[0], yi_edges[:, 0]))  # Use meshgrid for coordinates
    pcm = m.pcolormesh(x, y, zi, cmap=plt.cm.coolwarm, shading='auto', vmin=colorbar_min, vmax=colorbar_max)

    # Add a colorbar and set its label
    colorbar = plt.colorbar(pcm)
    colorbar.set_label(label_name, fontsize=16, labelpad=15)  # Adjust fontsize as needed
    colorbar.ax.tick_params(labelsize=12)
    
    m.fillcontinents(color='white')
    
    # Adjust layout and add title to the plot
    plt.tight_layout()
    plt.show()