import os
import xarray as xr

def open_and_combine_num_nc_files(directory, num_files):
    """
    Opens and combines a specified number of NetCDF files from a directory into a single dataset.

    Parameters:
        directory (str): The directory containing the NetCDF files.
        num_files (int): The number of files to consider.

    Returns:
        combined_ds (xarray.Dataset): A single dataset containing data from all input files.
    """
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Filter out only the .nc files
    nc_files = [file for file in files if file.endswith(".nc")]

    # Create an empty list to store the datasets
    datasets = []

    # Only consider the first num_files files
    for nc_file in nc_files[:num_files]:
        try:
            file_path = os.path.join(directory, nc_file)
            # Open the dataset
            ds = xr.open_dataset(file_path)
            
            # Append the dataset to the list
            datasets.append(ds)
        except Exception as e:
            print(f"Error opening file '{nc_file}': {e}")

    # Combine all datasets into a single dataset along the time dimension
    combined_ds = xr.concat(datasets, dim='t')
    return combined_ds