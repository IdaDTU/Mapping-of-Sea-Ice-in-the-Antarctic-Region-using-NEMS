import pandas as pd
import numpy as np
from RTM import scams

def ref_dataframe(df,df_water, variable_name, tp_ice, tp_water):
    """
    This function computes the reference dataframe (bt_ref_df) from data and tie-points.
    """
    # define parameters needed for scams-function
    V = np.mean(df_water['tcwv'])
    W = np.mean(df_water['W'])
    L = np.mean(df_water['L'])
    Ta = np.mean(df_water['t2m'])
    Ts = np.mean(df_water['sst'])
    theta = 0
    Ti_amsrv = np.full(7, 260)
    Ti_amsrh = np.full(7, 260)
    e_icev = np.full(7, 0.9)
    e_iceh = np.full(7, 0.9)

    RTM_Tb_ref = []
    RTM_lats_ref = []
    RTM_lons_ref = []

    for i in range(len(df)):
        bt = df[variable_name].iloc[i]
        c_ice = (bt - tp_water) / (tp_ice - tp_water)
        #c_ice = df['siconc'].iloc[i]
        
        # Call the scams function with the calculated parameters
        try:
            result = scams(V, W, L, Ta, Ts, theta, Ti_amsrv, Ti_amsrh, c_ice, e_icev, e_iceh)
            RTM_Tb_ref.append(result)
            RTM_lats_ref.append(df['LAT'].iloc[i])
            RTM_lons_ref.append(df['LON'].iloc[i])
            
        except Exception as e:
            print(f"Error processing data at index {i}: {e}")

    RTM_Tb_ref_array = np.array(RTM_Tb_ref)
    RTM_lats_ref_array = np.array(RTM_lats_ref)
    RTM_lons_ref_array = np.array(RTM_lons_ref)

    # Create a DataFrame from these arrays
    df2 = pd.DataFrame({
        'TBNEMS_C1': RTM_Tb_ref_array[:,0],
        'TBNEMS_C2': RTM_Tb_ref_array[:,1],
        'LAT': RTM_lats_ref_array,
        'LON': RTM_lons_ref_array,
        'tcwv' : df['tcwv'],
        'v10' : df['v10'],
        'u10' : df['u10'],
        'W' : df['W'],
        'tcw' : df['tcw'],
        'L' : df['L'],
        't2m' : df['t2m'],
        'sst' : df['sst'],
        'siconc' : df['siconc']
    })
    
    # Drop missing values
    bt_ref_df = df2.dropna()
    
    return bt_ref_df


def actual_bt_dataframe(df, variable_name, tp_ice, tp_water):
    """
    This function computes the actual dataframe (bt_akt_df) from data and tie-points.
    """
    # Create empty lists to be filled with scams
    RTM_Tb_akt = []
    RTM_lats_akt = []
    RTM_lons_akt = []

    # loop over df and insert in scams-function
    for i in range(len(df)):
        V = df['tcwv'].iloc[i]
        v = df['v10'].iloc[i]
        u = df['u10'].iloc[i]
        W = np.sqrt(v**2 + u**2)
        L0 = (np.mean(df['tcw']) - np.mean(df['tcwv']))
        L = L0[(L0 >= 0) & (L0 <= 1)]
        Ta = df['t2m'].iloc[i]
        Ts = df['sst'].iloc[i]
        theta = 0
        Ti_amsrv = np.full(7, 260)
        Ti_amsrh = np.full(7, 260)
        bt = df[variable_name].iloc[i]
        #c_ice = df['siconc'].iloc[i]
        c_ice = (bt - tp_water) / (tp_ice - tp_water)
        e_icev = np.full(7, 0.9)
        e_iceh = np.full(7, 0.9)

        # Call the scams function with the calculated parameters
        try:
            result = scams(V, W, L, Ta, Ts, theta, Ti_amsrv, Ti_amsrh, c_ice, e_icev, e_iceh)
            #if not np.isnan(result).any():  # Check if the result does not contain any NaN values
            RTM_Tb_akt.append(result)
            RTM_lats_akt.append(df['LAT'].iloc[i])
            RTM_lons_akt.append(df['LON'].iloc[i])
            
        except Exception as e:
            print(f"Error processing data at index {i}: {e}")

    RTM_Tb_akt_array = np.array(RTM_Tb_akt)
    RTM_lats_akt_array = np.array(RTM_lats_akt)
    RTM_lons_akt_array = np.array(RTM_lons_akt)

    # Create a DataFrame from these arrays
    df = pd.DataFrame({
        'TBNEMS_C1': RTM_Tb_akt_array[:,0],
        'TBNEMS_C2': RTM_Tb_akt_array[:,1],
        'LAT': RTM_lats_akt_array,
        'LON': RTM_lons_akt_array,
        'tcwv' : df['tcwv'],
        'v10' : df['v10'],
        'u10' : df['u10'],
        'W' : df['W'],
        'tcw' : df['tcw'],
        'L' : df['L'],
        't2m' : df['t2m'],
        'sst' : df['sst'],
        'siconc' : df['siconc']
    })
    
    # Drop missing values
    bt_akt_df = df.dropna()
    
    return bt_akt_df

def corrected_dataframe(df,variable_name,delta_bt):
    """
    This function computes the corrected dataframe (corrected_df) from data and delta_bt.
    """
    bt_corrected = df[variable_name] + delta_bt

    # Create a DataFrame
    corrected_df = pd.DataFrame({
        'bt_corrected': bt_corrected,
        'LAT': df['LAT'],
        'LON': df['LON'], 
        'tcwv' : df['tcwv'],
        'v10' : df['v10'],
        'u10' : df['u10'],
        'W' : df['W'],
        'tcw' : df['tcw'],
        'L' : df['L'],
        #'L' : np.full(len(df), 0),
        't2m' : df['t2m'],
        'sst' : df['sst'],
        'siconc' : df['siconc']
    }) 
    
    # Drop missing values
    corrected_df = corrected_df.dropna()
    
    return corrected_df



