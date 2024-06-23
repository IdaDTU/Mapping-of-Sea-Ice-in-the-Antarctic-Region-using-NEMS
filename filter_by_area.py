def filter_by_area(df, LON_min, LON_max, LAT_min, LAT_max):
    """
    Filter the DataFrame by geographic area defined by longitude and latitude bounds.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing 'LAT' (latitude) and 'LON' (longitude) columns.
        LON_min (float): Minimum longitude boundary for filtering.
        LON_max (float): Maximum longitude boundary for filtering.
        LAT_min (float): Minimum latitude boundary for filtering.
        LAT_max (float): Maximum latitude boundary for filtering.
        
    Returns:
        pandas.DataFrame: A DataFrame filtered to only include rows within the specified geographic area.
    """
    # Filtering the DataFrame to include only rows within the specified longitude and latitude bounds
    filtered_df_location = df[(df['LON'] >= LON_min) & (df['LON'] <= LON_max) &
                              (df['LAT'] >= LAT_min) & (df['LAT'] <= LAT_max)]
    
    return filtered_df_location
