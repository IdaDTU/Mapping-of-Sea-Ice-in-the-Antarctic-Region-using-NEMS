from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from initialize_basemap import initialize_basemap

def scatterplot_on_map_calculated_variable(df, variable, label_name, colorbar_min, colorbar_max):
    """
    Plot a scatter plot of a specified variable on a map of the Southern Hemisphere using data from a DataFrame.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing columns for 'LAT' (latitude), 'LON' (longitude), and the specified variable.
        variable (array): Array containing plotting variable
        label_name (string): Label for the colorbar indicating what the variable represents (e.g., 'Brightness Temperature [K]').
        title (string): Title of the plot.
        
    Returns:
        None: Displays a scatter plot on a stereographic projection of the Southern Hemisphere.
    """
    lats = df['LAT']
    lons = df['LON']
    
    # Initialize Basemap with the Southern Hemisphere stereographic projection
    m = Basemap(projection='spstere', boundinglat=-50, lon_0=0, resolution='l', round=True)
    initialize_basemap()

    # Convert latitude and longitude to map coordinates and create scatter plot
    x, y = m(lons, lats)
    scatter = m.scatter(x, y, c=variable, cmap=plt.cm.coolwarm, vmin=colorbar_min, vmax=colorbar_max, marker='.', s=15, label=label_name)
    
    # Add a colorbar and title to the plot
    #plt.colorbar(scatter, label=label_name)
    colorbar = plt.colorbar(scatter)
    colorbar.set_label(label_name, fontsize=16, labelpad=15)  # Adjust fontsize as needed
    colorbar.ax.tick_params(labelsize=12)
    plt.show()