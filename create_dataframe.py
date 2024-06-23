import pandas as pd
import numpy as np

def create_dataframe(ds):
    """
    Create a Pandas DataFrame from specific variables in a given dataset.
    
    Parameters:
    ds (dataset): A dataset containing multiple variables.
    
    Returns:
    new_df (DataFrame): A cleaned DataFrame with selected variables and no missing values.
    """
    # Extract variables from the dataset 
    v10 = ds['v10'][:,1].values
    u10 = ds['u10'][:,1].values
    W = np.sqrt(v10**2 + u10**2)
    tcwv = ds['tcwv'][:,1].values 
    tcw = ds['tcw'][:,1].values
    L = tcw - tcwv
    sst = ds['sst'][:,1].values
    msl = ds['msl'][:,1].values
    TBNEMS_C1 = ds['TBNEMS'][:,0,0].values 
    TBNEMS_C2 = ds['TBNEMS'][:,0,1].values
    LON = ds['LON'][:,1].values
    LAT = ds['LAT'][:,1].values
    siconc = ds['siconc'][:,1].values
    t2m = ds['t2m'][:,1].values
    
    # Apply filter to remove outliers
    filter_condition = (L >= 0) & (L <= 0.3) & (W >= 0) & (W <= 20) & (tcwv >= 0) & (tcwv <= 17)

    # Create a DataFrame from these arrays
    df = pd.DataFrame({
        'tcwv': tcwv,
        'v10': v10,
        'u10': u10,
        'tcw': tcw,
        'W': W,
        'L': L,
        'sst': sst,
        'msl': msl,
        'TBNEMS_C1': TBNEMS_C1,
        'TBNEMS_C2': TBNEMS_C2,
        'LON': LON,
        'LAT': LAT,
        'siconc': siconc*100, #multiplied by 100 so the plots are shown in percentage
        't2m': t2m
    })

    # Filter the DataFrame for L filter
    filtered_df = df[filter_condition]

    # Drop missing values
    new_df = filtered_df.dropna() 
    #new_df = df.dropna() #to be used when creating initial boxplot for L (no filter)

    return new_df

