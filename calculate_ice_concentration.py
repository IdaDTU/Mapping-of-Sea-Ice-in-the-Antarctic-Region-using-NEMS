import numpy as np

def calculate_ice_concentration(df,variable_name,tp_ice,tp_water):
    """
    Calculate the ice concentration based on brightness temperature (TBNEMS) data.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing the 'TBNEMS' column which represents brightness temperature.
        tp_ice (float): Brightness temperature tiepoint for ice.
        tp_water (float): Brightness temperature tiepoint for water.
        
    Returns:
        numpy.ndarray: Array of ice concentration values, clipped between 0 and 1.
    """
    
    bt = df[variable_name]
    c=(bt-tp_water)/(tp_ice-tp_water)

    c = c.apply(lambda x: 0.0 if x < 0.3 else (1.0 if x > 1.0 else x))
    
    return c