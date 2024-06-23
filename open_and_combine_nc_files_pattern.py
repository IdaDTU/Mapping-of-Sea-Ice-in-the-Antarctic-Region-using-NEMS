import os
import fnmatch
import xarray as xr

def open_and_combine_nc_files_pattern(directory, pattern):
    """
    Open and combine netCDF files in the given directory matching the specified pattern.

    Parameters:
        directory (str): Path to the directory containing the .nc files.
        pattern (str): Pattern to match the files. For example, "m08" for August files.

    Returns:
        combined_ds (xarray.Dataset): Combined dataset along the time dimension.
    """
    try:
        # Get a list of all files in the directory
        files = os.listdir(directory)

        # Filter out only the .nc files that match the pattern
        nc_files = [file for file in files if file.endswith(".nc") and fnmatch.fnmatch(file, f"*{pattern}*.*")]

        # Create an empty list to store the datasets
        datasets = []

        # Loop through each .nc file and open it
        for nc_file in nc_files:
            try:
                file_path = os.path.join(directory, nc_file)
                # Open the dataset
                ds = xr.open_dataset(file_path, decode_times=False)
                
                # Append the dataset to the list
                datasets.append(ds)
            except Exception as e:
                print(f"Error opening file '{nc_file}': {e}")

        # Combine all datasets into a single dataset along the time dimension
        combined_ds = xr.concat(datasets, dim='t')
        return combined_ds
    except Exception as e:
        print(f"An error occurred: {e}")
        return None