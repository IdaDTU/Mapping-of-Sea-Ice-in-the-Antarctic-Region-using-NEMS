from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

def initialize_basemap():
    plt.figure(figsize=(12*1.5/3, 8*1.5/3))
    m = Basemap(projection='spstere', boundinglat=-50, lon_0=0, resolution='l', round=True)
    m.drawcoastlines(linewidth=2)
    m.drawparallels(np.arange(-80., 81., 20.), labels=[1, 0, 0, 0])
    m.drawmeridians(np.arange(-180., 181., 20.), labels=[1, 0, 0, 1])
    m.drawmapboundary(fill_color='white')

    # Everything below is only used for the front page

    # Coordinates for Wendell Sea and Ross Sea
    #weddell_sea_coords = (-73, -45)  # Approximate coordinates for Wendell Sea
    #ross_sea_coords = (-75, 180)     # Approximate coordinates for Ross Sea

    # Convert coordinates to map projection
    #weddell_x, weddell_y = m(weddell_sea_coords[1], weddell_sea_coords[0])
    #ross_x, ross_y = m(ross_sea_coords[1], ross_sea_coords[0])

    # Plot points
    #m.plot(weddell_x, weddell_y, 'ko', markersize=6)
    #m.plot(ross_x, ross_y, 'ko', markersize=6)

    # Add labels
    #plt.text(weddell_x, weddell_y+1500000, 'Weddell Sea', fontsize=12, ha='center', color='black', weight='semibold')
    #plt.text(ross_x, ross_y-650000, 'Ross Sea', fontsize=12, ha='center', color='black', weight='semibold')
    
    return m