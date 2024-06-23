import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pykrige.ok import OrdinaryKriging
from initialize_basemap import initialize_basemap
import matplotlib.colors as mcolors
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as mcolors
from pykrige.ok import OrdinaryKriging
import matplotlib as mpl
from calculate_ice_concentration import calculate_ice_concentration

def plot_GR(df, variable_name, label_name):
    """
    Plot an interpolated scatter plot of a specified variable on a map of the Southern Hemisphere using kriging.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing columns for 'LAT' (latitude), 'LON' (longitude), and the specified variable.
        variable_name (string): The name of the column in the DataFrame that contains the values to be plotted.
        label_name (string): Label for the colorbar indicating what the variable represents.
        title (string): Title of the plot.
        
    Returns:
        None: Displays an interpolated scatter plot on a stereographic projection of the Southern Hemisphere.
    """
    
    # Extract latitude, longitude, and the variable values from the DataFrame
    LON = df['LON'].values
    LAT = df['LAT'].values
    SIC = df['SIC'].values
    z = df[variable_name].values
    
    
    # Define the grid on which to interpolate the data
    xi = np.linspace(LON.min(), LON.max(),700)
    yi = np.linspace(LAT.min(), LAT.max(), 700)
    xi, yi = np.meshgrid(xi, yi)
    
    # Perform kriging interpolation
    variogram_parameters = [1.0, 10.0, 0.01]
    OK = OrdinaryKriging(LON, LAT, z, variogram_model='spherical', variogram_parameters=variogram_parameters, verbose=False, enable_plotting=False)
    zi, ss = OK.execute('grid', xi[0], yi[:, 0])

    # Reshape zi back to 2D
    zi = zi.reshape(xi.shape)
    
    # Apply a mask to hide data outside the bounding latitude
    mask1 = yi > -50  # Above max altitudd
    zi[mask1] = np.nan
    
    # For the SIC mask, we need to interpolate SIC onto the same grid
    SIC_OK = OrdinaryKriging(LON, LAT, SIC, variogram_model='spherical', variogram_parameters=variogram_parameters, verbose=False, enable_plotting=False)
    SIC_grid, ss = SIC_OK.execute('grid', xi[0], yi[:, 0])
    SIC_grid = SIC_grid.reshape(xi.shape)
  
    mask2 = SIC_grid < 0.3
    zi[mask2] = np.nan
    
    # Initialize Basemap with the Southern Hemisphere stereographic projection
    m = Basemap(projection='spstere', boundinglat=-50, lon_0=0, resolution='l', round=True)
    initialize_basemap()
    
    # Convert the coordinates from centers to edges
    xi_edges = np.linspace(LON.min(), LON.max(), 701)
    yi_edges = np.linspace(LAT.min(), LAT.max(), 701)
    xi_edges, yi_edges = np.meshgrid(xi_edges, yi_edges)
    
    # Plot interpolated data
    x, y = m(*np.meshgrid(xi_edges[0], yi_edges[:, 0]))  # Use meshgrid for coordinates

    cmaplist = ['#bdd2f6','#4358cb','white']
    cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, 3)
    bounds = np.array([-0.001, 0, 0.01,1])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    
     # Convert the grid to map coordinates
    xi_grid, yi_grid = m(xi, yi)
    pcm = m.pcolormesh(x, y, zi, cmap=cmap,norm=norm)

    # Add a colorbar and set its label
    colorbar = plt.colorbar(pcm, ticks=[-0.001+0.001/2,
                                        0+ 0.01/2,
                                        0.01+1/2])
    colorbar.set_label(label_name, fontsize=16, labelpad=15)  # Adjust fontsize as needed
    colorbar.ax.tick_params(labelsize=12)
    colorbar.ax.set_yticklabels(['Type B', 'Type A', 'Other'])

    m.fillcontinents(color='white')
    
    # Adjust layout and add title to the plot
    plt.tight_layout()
    plt.show()