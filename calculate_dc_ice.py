import numpy as np

def calculate_dc_ice(ice_concentration, tp_water, tp_ice, uncertainty_water, uncertainty_ice):
    """
    Calculate the uncertainty in the ice concentration measurement (dc_ice).

    Parameters:
    - ice_concentration (float): The concentration of ice.
    - tp_water_corr (float): The temperature correction for water.
    - tp_ice_corr (float): The temperature correction for ice.
    - uncertainty_water (float): The uncertainty in the temperature correction for water.
    - uncertainty_ice (float): The uncertainty in the temperature correction for ice.

    Returns:
    - dc_ice (float): The uncertainty in the ice concentration measurement.
    """
    # Calculate the terms contributing to the uncertainty
    term1 = (-(1 - ice_concentration) * uncertainty_water / (tp_ice - tp_water))**2
    term2 = (-ice_concentration * uncertainty_ice / (tp_ice - tp_water))**2
    
    # Compute the overall uncertainty using the terms
    dc_ice = np.sqrt(term1 + term2)
    
    return dc_ice
