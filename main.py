import matplotlib.pyplot as plt
import scienceplots
import numpy as np
import pandas as pd

# Import modules from folder
from open_and_combine_num_nc_files import open_and_combine_num_nc_files
from plot_satellite_paths import plot_satellite_paths 
from open_and_combine_nc_files_pattern import open_and_combine_nc_files_pattern
from create_dataframe import create_dataframe
from scatterplot_on_map import scatterplot_on_map
from filter_bt_by_interval import filter_bt_by_interval
from plot_interpolated import plot_interpolated
from calculate_ice_concentration import calculate_ice_concentration
from scatterplot_on_map_calculated_variable import scatterplot_on_map_calculated_variable
from plot_interpolated_calculated_variable import plot_interpolated_calculated_variable
from filter_by_area import filter_by_area
from sensitivity_study import plot_sensitivity_studies, calculate_std_sensitivity
from correction_study import ref_dataframe,actual_bt_dataframe, corrected_dataframe
from calculate_dc_ice import calculate_dc_ice
from plot_GR import plot_GR
from SIE import calculate_SIE

# Initialize style parameters
plt.rcParams['figure.dpi'] = 1000
plt.style.use('science')
plt.rc('text', usetex=False)

# Open single .nc file
directory = "C:/Users/idags/Desktop/DTU/Semester4/Fagprojekt/NEMS_colocated"
one_nc_file = open_and_combine_num_nc_files(directory, 1)

# Plot satellite paths
plot_satellite_paths(one_nc_file)

# Usage for august (mid-winter in southeren hemisphere)
pattern = 'm08'

# Open dataset for august
combined_ds_august = open_and_combine_nc_files_pattern(directory, pattern)

# Plots for August
plot_satellite_paths(combined_ds_august)

# Create dataframe for combined august dataset
august_df = create_dataframe(combined_ds_august)

# Filter dataframe by brightness temperature
august_df_filtered_by_interval = filter_bt_by_interval(august_df, 
                                                      variable='TBNEMS_C2',
                                                      min_temp = 90, 
                                                      max_temp = 273.15)
# Filter dataframe by area around south pole
august_df_filtered_by_interval_and_sp=filter_by_area(august_df_filtered_by_interval,
                                                     LON_min=0,
                                                     LON_max=360,
                                                     LAT_min=-90,
                                                     LAT_max=-40)

# Plot brightness temperature as scatter plot
scatterplot_on_map(august_df_filtered_by_interval_and_sp,
                   variable_name='TBNEMS_C2',
                   label_name='Brightness Temperature [K]',
                   colorbar_min=100,
                   colorbar_max=300)

# Interpolate and plot brightness temperature 
plot_interpolated(august_df_filtered_by_interval_and_sp,
                     variable_name='TBNEMS_C2',
                     label_name='Brightness Temperature [K]',
                     colorbar_min=100,
                     colorbar_max=300)

# Find the tiepoints
# Filter dataframe by area over open water
august_df_filtered_by_interval_and_open_water_sp=filter_by_area(august_df_filtered_by_interval_and_sp,
                                                                LON_min=10,
                                                                LON_max=60,
                                                                LAT_min=-55,
                                                                LAT_max=-45)

# Only keep measurements in OW area that have a siconc value between 0-10 (0-0.1)
august_df_filtered_by_interval_and_open_water_sp_siconc = (august_df_filtered_by_interval_and_open_water_sp[(august_df_filtered_by_interval_and_open_water_sp['siconc'] >= 0) & (august_df_filtered_by_interval_and_open_water_sp['siconc'] <= 10)])

# Scatterplot of brightness temperature over open water
scatterplot_on_map(august_df_filtered_by_interval_and_open_water_sp_siconc,
                   variable_name='TBNEMS_C2',
                   label_name='Brightness Temperature [K]',
                   colorbar_min=100,
                   colorbar_max=300)

# Filter dataframe by area over ice
august_df_filtered_by_interval_and_ice_sp=filter_by_area(august_df_filtered_by_interval_and_sp,
                                                         LON_min=305,
                                                         LON_max=340,
                                                         LAT_min=-75,
                                                         LAT_max=-65)

# Only keep measurements in sea ice area that have a siconc value between 90-100 (0.9-1)
august_df_filtered_by_interval_and_ice_sp_siconc = (august_df_filtered_by_interval_and_ice_sp[(august_df_filtered_by_interval_and_ice_sp['siconc'] >= 90) & (august_df_filtered_by_interval_and_ice_sp['siconc'] <= 100)])

# Scatterplot of brightness temperature over ice
scatterplot_on_map(august_df_filtered_by_interval_and_ice_sp_siconc,
                   variable_name='TBNEMS_C2',
                   label_name='Brightness Temperature [K]',
                   colorbar_min=100,
                   colorbar_max=300)

# Find tiepoints for open water and ice
tp_water = august_df_filtered_by_interval_and_open_water_sp_siconc['TBNEMS_C2'].mean()
print(f'Tiepoint for open water: {tp_water}')

tp_ice = august_df_filtered_by_interval_and_ice_sp_siconc['TBNEMS_C2'].mean()
print(f'Tiepoint for ice: {tp_ice}')

# Calculate ice concentration from tiepoints
ice_concentration = calculate_ice_concentration(august_df_filtered_by_interval_and_sp,
                                               variable_name ='TBNEMS_C2',
                                               tp_ice =  tp_ice,
                                               tp_water = tp_water)

# Scatterplot calculated ice concentration
scatterplot_on_map_calculated_variable(august_df_filtered_by_interval_and_sp,
                   variable=ice_concentration*100, #multiplied by 100 to show in percent
                   label_name='Ice Concentration [%]',
                   colorbar_min=0,
                   colorbar_max=100)

# Interpolate calculated ice concentration
plot_interpolated_calculated_variable(august_df_filtered_by_interval_and_sp,
                                      variable=ice_concentration*100,
                                      label_name='Ice Concentration [%]',
                                      colorbar_min=0,
                                      colorbar_max=100)

# Create and plot sensitivity study for W, L, V, Ts and Ta over open water
plot_sensitivity_studies(august_df_filtered_by_interval_and_sp)

# Calcuculate Std for sensitivity study of brigtness temperature for each channel
sensitivity_std = calculate_std_sensitivity(august_df_filtered_by_interval_and_sp)
print(sensitivity_std)

# Create correction study
# Refrence dataframe
ref_df = ref_dataframe(august_df_filtered_by_interval_and_sp,
                       august_df_filtered_by_interval_and_open_water_sp, 
                       variable_name='TBNEMS_C2', 
                       tp_ice =  tp_ice,
                       tp_water = tp_water)

# Actual dataframe
act_df = actual_bt_dataframe(august_df_filtered_by_interval_and_sp,
                             variable_name='TBNEMS_C2', 
                             tp_ice =  tp_ice,
                             tp_water = tp_water)

# Delta_bt (difference)
calculated_delta_bt = ref_df['TBNEMS_C2'] - act_df['TBNEMS_C2']
print('Delta min:', min(calculated_delta_bt), 'New delta max:', max(calculated_delta_bt))

# Corrected dataframe
corr_df = corrected_dataframe(august_df_filtered_by_interval_and_sp,
                              variable_name = 'TBNEMS_C2',
                              delta_bt = calculated_delta_bt)

# Find new tie points
# Filter dataframe by area over open water
corr_df_open_water=filter_by_area(corr_df,
                                  LON_min=10,
                                  LON_max=60,
                                  LAT_min=-55,
                                  LAT_max=-45)

# Only keep measurements in OW area that have a siconc value between 0-10 (0-0.1)
corr_df_open_water_siconc = (corr_df_open_water[(corr_df_open_water['siconc'] >= 0) & (corr_df_open_water['siconc'] <= 10)])

# Scatterplot of brightness temperature over open water
scatterplot_on_map(corr_df_open_water_siconc,
                   variable_name='bt_corrected', 
                   label_name='Brightness Temperature [K]',
                   colorbar_min=100,
                   colorbar_max=300)


# Filter dataframe by area over ice
corr_df_ice=filter_by_area(corr_df,
                           LON_min=305,
                           LON_max=340,
                           LAT_min=-75,
                           LAT_max=-65)

# Only keep measurements in sea ice area that have a siconc value between 90-100 (0.9-1)
corr_df_ice_siconc = (corr_df_ice[(corr_df_ice['siconc'] >= 90) & (corr_df_ice['siconc'] <= 100)])

# Scatterplot of brightness temperature over ice
scatterplot_on_map(corr_df_ice_siconc,
                   variable_name='bt_corrected',
                   label_name='Brightness Temperature [K]',
                   colorbar_min=100,
                   colorbar_max=300)

# Find new tiepoints for OW and ice
tp_water_corr = corr_df_open_water_siconc['bt_corrected'].mean()
print(f'Tiepoint for open water (corrected): {tp_water_corr}')

tp_ice_corr = corr_df_ice_siconc['bt_corrected'].mean()
print(f'Tiepoint for ice (corrected): {tp_ice_corr}')

# Refrence dataframe from new tiepoint 
new_ref_df = ref_dataframe(corr_df, 
                           corr_df_open_water,
                           variable_name='bt_corrected', 
                           tp_ice= tp_ice_corr,
                           tp_water=tp_water_corr)

# Actual dataframe from new tiepoints
new_act_df = actual_bt_dataframe(corr_df,
                                 variable_name='bt_corrected', 
                                 tp_ice= tp_ice_corr,
                                 tp_water=tp_water_corr)

# New delta_bt (difference from new ref and act)
new_calculated_delta_bt = new_ref_df['TBNEMS_C2'] - new_act_df['TBNEMS_C2']

# New corrected dataframe
new_corr_df = corrected_dataframe(corr_df,
                                  variable_name='bt_corrected',
                                  delta_bt= new_calculated_delta_bt)

# Scatterplot of corrected brightness temperature 
scatterplot_on_map(new_corr_df,
                   variable_name='bt_corrected',
                   label_name='Brightness Temperature [K]',
                   colorbar_min=100,
                   colorbar_max=300)

# Interpolated corrected Brightness Temperature
plot_interpolated(new_corr_df, 
                  variable_name='bt_corrected',
                  label_name = 'Brightness Temperature [K]',
                  colorbar_min=100,
                  colorbar_max=300)

# Calculate ice concentrations from new brightness temperature and tie points
new_ice_concentration = calculate_ice_concentration(new_corr_df,
                                                    variable_name ='bt_corrected',
                                                    tp_ice= tp_ice_corr,
                                                    tp_water=tp_water_corr)

# Scatterplot calculated ice concentration
scatterplot_on_map_calculated_variable(new_corr_df,
                   variable=new_ice_concentration*100,
                   label_name='Ice Concentration [%]',
                   colorbar_min=10,
                   colorbar_max=90)

#% Interpolate calculated ice concentration
plot_interpolated_calculated_variable(new_corr_df,
                                      variable=new_ice_concentration*100,
                                      label_name='Ice Concentrationn [%]',
                                      colorbar_min=0,
                                      colorbar_max=100)

# Diffrence between corrected and uncorrected brightness temperatre
diff_bt = august_df_filtered_by_interval_and_sp['TBNEMS_C2']-new_corr_df['bt_corrected']

# Interpolate and plot difference between corrected and uncorrected brightness temperature
plot_interpolated_calculated_variable(new_corr_df,
                                      variable=diff_bt,
                                      label_name='Brightness Temperature [K]',
                                      colorbar_min=-10,
                                      colorbar_max=10)

# Difference between corrected and uncorrected ice concentration
diff_sic = ice_concentration - new_ice_concentration

# Interpolate and plot diffrence in corrected sic
plot_interpolated_calculated_variable(new_corr_df,
                                      variable=diff_sic*100,
                                      label_name='Ice Concentration [%]',
                                      colorbar_min=-3,
                                      colorbar_max=3)

    
#%% Calculate and display standard deviation for corrected brightness temperatures and ice concentrations
bt_std_water=august_df_filtered_by_interval_and_sp['TBNEMS_C2'].std() #measured
new_bt_std_water=corr_df_open_water['bt_corrected'].std() #corrected
ice_std=ice_concentration.std() # measured
new_ice_std=new_ice_concentration.std() #corrected

print('Standard deviation for unfiltered water:', august_df['TBNEMS_C2'].std())
print(f'Standard deviation for uncorrected water: {bt_std_water}')
print(f'Standard deviation for corrected water: {new_bt_std_water}')
print(f'Standard deviation for uncorrected SIC: {ice_std}')
print(f'Standard deviation for corrected SIC: {new_ice_std}')

#%% Find SIC Uncertainties
# Define std for original OW and ice areas
std_water = corr_df_open_water['bt_corrected'].std()
std_ice = corr_df_ice['bt_corrected'].std()

# Calculate uncertainties
ice_error=calculate_dc_ice(ice_concentration = new_ice_concentration,
                           tp_water = tp_water_corr,
                           tp_ice = tp_ice_corr, 
                           uncertainty_water = std_water, 
                           uncertainty_ice = std_ice)

# Plot interpolated uncertainties
plot_interpolated_calculated_variable(new_corr_df,
                                      variable=ice_error*100, 
                                      label_name='Uncertainty [%]',
                                      colorbar_min=5,
                                      colorbar_max=15)


# Corrected brightness temperature for channel 1 
# Find tiepoints for open water and ice
tp_water_C1 = august_df_filtered_by_interval_and_open_water_sp_siconc['TBNEMS_C1'].mean()
print(f'Tiepoint for open water: {tp_water_C1}')

tp_ice_C1 = august_df_filtered_by_interval_and_ice_sp_siconc['TBNEMS_C1'].mean()
print(f'Tiepoint for ice: {tp_ice_C1}')

# Calculate ice concentration from tiepoints
ice_concentration_C1 = calculate_ice_concentration(august_df_filtered_by_interval_and_sp,
                                               variable_name ='TBNEMS_C1',
                                               tp_ice =  tp_ice_C1,
                                               tp_water = tp_water_C1)

# Create correction study
# Refrence dataframe
ref_df = ref_dataframe(august_df_filtered_by_interval_and_sp,
                       august_df_filtered_by_interval_and_open_water_sp, 
                       variable_name='TBNEMS_C1', 
                       tp_ice =  tp_ice_C1,
                       tp_water = tp_water_C1)

# Actual dataframe
act_df = actual_bt_dataframe(august_df_filtered_by_interval_and_sp,
                             variable_name='TBNEMS_C1', 
                             tp_ice =  tp_ice_C1,
                             tp_water = tp_water_C1)

# Delta_bt (difference)
calculated_delta_bt_C1 = ref_df['TBNEMS_C1'] - act_df['TBNEMS_C1']
print('Delta min:', min(calculated_delta_bt_C1), 'New delta max:', max(calculated_delta_bt_C1))

# Corrected dataframe
corr_df_C1 = corrected_dataframe(august_df_filtered_by_interval_and_sp,
                              variable_name = 'TBNEMS_C1',
                              delta_bt = calculated_delta_bt_C1)

# Find new tie points
# Filter dataframe by area over open water
corr_df_open_water_C1=filter_by_area(corr_df_C1,
                                  LON_min=10,
                                  LON_max=60,
                                  LAT_min=-55,
                                  LAT_max=-45)

# Only keep measurements in OW area that have a siconc value between 0-10 (0-0.1)
corr_df_open_water_siconc_C1 = (corr_df_open_water_C1[(corr_df_open_water_C1['siconc'] >= 0) & (corr_df_open_water_C1['siconc'] <= 10)])

# Filter dataframe by area over ice
corr_df_ice_C1=filter_by_area(corr_df_C1,
                           LON_min=305,
                           LON_max=340,
                           LAT_min=-75,
                           LAT_max=-65)

# Only keep measurements in sea ice area that have a siconc value between 90-100 (0.9-1)
corr_df_ice_siconc_C1 = (corr_df_ice_C1[(corr_df_ice_C1['siconc'] >= 90) & (corr_df_ice_C1['siconc'] <= 100)])

# Find new tiepoints for OW and ice
tp_water_corr_C1 = corr_df_open_water_siconc_C1['bt_corrected'].mean()
print(f'Tiepoint for open water (corrected): {tp_water_corr_C1}')

tp_ice_corr_C1 = corr_df_ice_siconc_C1['bt_corrected'].mean()
print(f'Tiepoint for ice (corrected): {tp_ice_corr_C1}')

# Refrence dataframe from new tiepoint 
new_ref_df_C1 = ref_dataframe(corr_df_C1, 
                           corr_df_open_water_C1,
                           variable_name='bt_corrected', 
                           tp_ice= tp_ice_corr_C1,
                           tp_water=tp_water_corr_C1)

# Actual dataframe from new tiepoints
new_act_df_C1 = actual_bt_dataframe(corr_df_C1,
                                 variable_name='bt_corrected', 
                                 tp_ice= tp_ice_corr_C1,
                                 tp_water=tp_water_corr_C1)

# New delta_bt (difference from new ref and act)
new_calculated_delta_bt_C1 = new_ref_df_C1['TBNEMS_C1'] - new_act_df_C1['TBNEMS_C1']

# New corrected dataframe
new_corr_df_C1 = corrected_dataframe(corr_df_C1,
                                  variable_name='bt_corrected',
                                  delta_bt= new_calculated_delta_bt_C1)

# Calculate ice concentrations from new brightness temperature and tie points
new_ice_concentration_C1 = calculate_ice_concentration(new_corr_df_C1,
                                                    variable_name ='bt_corrected',
                                                    tp_ice= tp_ice_corr_C1,
                                                    tp_water=tp_water_corr_C1)

# Find ice type
# Extract the bt_corrected values for T1_C1 and T2_C2
T1 = new_corr_df_C1['bt_corrected']
T2 = new_corr_df['bt_corrected']

# Calculate GR
GR = (T2 - T1)/(T2 + T1)
LAT = august_df_filtered_by_interval_and_sp['LAT']
LON = august_df_filtered_by_interval_and_sp['LON']
SIC = calculate_ice_concentration(new_corr_df, 
                                  variable_name="bt_corrected", 
                                  tp_ice=tp_ice_corr, 
                                  tp_water=tp_water_corr)

# Make new DF containing: LON, LAT, GR and SIC
GR_df = pd.DataFrame({
    'GR': GR,
    'LAT': LAT,
    'LON': LON,
    'SIC': SIC})

plot_GR(GR_df,
        variable_name='GR',
        label_name='Surface Type')


#%% Calculate SIE
print(calculate_SIE(new_corr_df,
              new_ice_concentration)) #Output 18730.46 km^2

# Data from OSI SAD
august_SIE = [18.13767137, 18.2721875, 18.17538306, 18.23471774, 17.57058468, 
              18.22407986, 17.99407258, 17.38740927, 18.03377016, 17.99792339, 17.79076613, 
              17.91877016, 18.10048387, 18.12326613, 17.89542339, 18.22149194, 18.18758065, 
              18.0941129, 17.99034274, 18.21143145, 18.32506048, 18.64534274, 17.74431452, 
              17.47616935, 17.8665121, 18.35294355, 18.2609879, 18.65155242, 18.12667339, 
              18.12487903, 18.64330645, 19.01241935, 18.3222379, 18.50381048, 19.12570565, 
              19.35368952, 18.11108871, 18.38028226, 17.57064516, 17.83772177, 17.92804435, 
              18.16335685, 18.62705645, 17.48441532, 16.01967515]

years_SIE = [1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 
             1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 
             2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 
             2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

# Convert lists to numpy arrays
august_SIE = np.array(august_SIE)
years_SIE = np.array(years_SIE)

# %%Plot
plt.figure(figsize=(10, 6))
plt.plot(years_SIE, august_SIE, color='#bdd2f6', label=' EUMETSAT Data', linewidth=4)
plt.scatter(1972, 18.730, color='#4358cb', label='NEMS',marker='o')
plt.scatter(1972, 18.5, color='#4358cb', label='ESMR',marker='x')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Sea Ice Extent [millions $\mathrm{km}^2$]', fontsize=14)
plt.legend(loc='lower left') 
plt.grid(True)
plt.show()



