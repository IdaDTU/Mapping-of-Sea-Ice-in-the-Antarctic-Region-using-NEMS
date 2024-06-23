def filter_bt_by_interval(df, variable,min_temp, max_temp):
    """
    Filter DataFrame rows where brightness temperature ('TBNEMS') is within a specified range.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing brightness temperature data in the 'TBNEMS' column.
        min_temp (float): Minimum temperature threshold.
        max_temp (float): Maximum temperature threshold.

    Returns:
        pandas.DataFrame: DataFrame filtered to include only rows where 'TBNEMS' values are between min_temp and max_temp.
    """
    # Filter DataFrame based on the 'TBNEMS' column values within the specified range
    filtered_bt_df = df[(df[variable] > min_temp) & (df[variable] < max_temp)]
    
    # Remove NaN values
    filter_bt_by_interval = filtered_bt_df.dropna()
    
    return filter_bt_by_interval
