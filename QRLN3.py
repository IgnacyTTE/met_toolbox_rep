# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 13:01:42 2024

@author: IGNAOLSZ
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import openpyxl
from scipy import stats


from get_volue_5 import fetch_voule
from transform_4 import transform_data
from volue_name import get_name

#Input data for curves eg. 'tt dk con ec00 °c cet min15 f'
primary_category = 'res'
areas = ['fr','ch','it', 'at']
secondary_category = 'hydro wtr'
model = ''
freq = 'h'
data_types = ['n', 'sa']

#Input parameters for your curve type - supply zero if given parameter not required for your curve
tag = 'Ave'
issue_date = '2018-01-01T00:00'
issue_date_from = '2018-01-01T00:00'
issue_date_to = '2018-01-03T00:00'
data_from = '2023-01-01T00:00'
data_to = dt.date.today()
function ='AVERAGE'
frequency ='D'

#Get the data from voule using the API
def quantify_res_water_levels(areas, data_types):
    all_data = []
    for area in areas:
        current_data_types = data_types if area != 'np' else ['n']
        
        for data_type in current_data_types:
            try:
                curve_key = get_name(primary_category, area, secondary_category, model, freq, data_type)
                df = fetch_voule(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)
                df = transform_data(df, curve_key)
                
                # Ensure 'area' and 'data_type' are included in df
                df['area'] = area
                df['data_type'] = data_type
                
                all_data.append(df)
            except Exception as e:
                print(f"An error occurred for {area} with data type {data_type}: {e}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        # Save the DataFrame to an Excel file
        #combined_df.to_excel('res_water_levels2.xlsx', index=False, engine='openpyxl')
    else:
        combined_df = pd.DataFrame()
        
    df_n = combined_df[combined_df['data_type'] == 'n'].copy()
    df_sa = combined_df[combined_df['data_type'] == 'sa'].copy()

    return combined_df, df_n, df_sa

#Transform the data to this particular use case

def transform_res(areas, data_types):
    df, df_n, df_sa = quantify_res_water_levels(areas, data_types)

    df_n = df_n.rename(columns={'Value': 'Normal'})
    df_sa = df_sa.rename(columns={'Value': 'Actual'})

    df_n.drop(['data_type', 'Curve_key'], axis=1, inplace=True)
    df_sa.drop(['data_type', 'Curve_key'], axis=1, inplace=True)

    #Merge the dataframes
    merged_df = pd.merge(df_n, df_sa[['Year', 'Month', 'Day', 'Hour', 'Minute', 'area', 'Actual']], 
                         on=['Year', 'Month', 'Day', 'Hour', 'Minute', 'area'], 
                         how='left')


    # Fill missing values in 'Actual' with zeros
    merged_df['Actual'].fillna(0, inplace=True)

    # Now, to ensure the 'Actual' column is right after 'Normal', we'll specify the column order explicitly.
    # First, get all column names as a list
    columns = list(merged_df.columns)

    # Remove 'Actual' to avoid it appearing twice
    columns.remove('Actual')

    # Find the index of 'Normal' to insert 'Actual' right after it
    normal_index = columns.index('Normal')

    # Reinsert 'Actual' at the correct position
    columns.insert(normal_index + 1, 'Actual')

    # Reorder the dataframe using the updated columns list
    merged_df = merged_df[columns]

    # Calculate 'Anomaly' only where 'Actual' is not zero, otherwise set to zero
    merged_df['Anomaly'] = merged_df.apply(lambda row: row['Actual'] - row['Normal'] if row['Actual'] != 0 else 0, axis=1)

    # Now, ensure 'Anomaly' is placed right after 'Actual'
    # Get all column names
    columns = list(merged_df.columns)

    # Remove 'Anomaly' to reinsert it at the correct position
    if 'Anomaly' in columns:
        columns.remove('Anomaly')

    # Find the index of 'Actual' to insert 'Anomaly' right after it
    actual_index = columns.index('Actual')

    # Insert 'Anomaly' right after 'Actual'
    columns.insert(actual_index + 1, 'Anomaly')

    # Reorder the dataframe using the updated column list
    merged_df = merged_df[columns]
    
    return merged_df

# Data presentation part

merged_df = transform_res(areas, data_types)

# Convert 'Year', 'Month', 'Day', 'Hour', 'Minute' to a datetime object for plotting
merged_df['DateTime'] = pd.to_datetime(merged_df[['Year', 'Month', 'Day', 'Hour', 'Minute']])

# Group by 'area' to plot each separately
areas = merged_df['area'].unique()

# Setup the plot - adjust the size, number of subplots, etc., as necessary
fig, axs = plt.subplots(len(areas), 1, figsize=(10, 5*len(areas)))

if len(areas) == 1:
    axs = [axs]  # Ensure axs is iterable

for ax, area in zip(axs, areas):
    # Filter the data for the current area
    df_area = merged_df[merged_df['area'] == area]
    
    # Plot 'Normal', 'Actual', and 'Anomaly'
    ax.plot(df_area['DateTime'], df_area['Normal'], label='Normal', color='black', lw=2)
    ax.plot(df_area['DateTime'], df_area['Actual'], label='Actual', color='red', lw=2)
    
    # For 'Anomaly', we might plot it differently to highlight its significance
    # Here, we're using a bar plot. Adjust the plotting method as necessary.
    ax.bar(df_area['DateTime'], df_area['Anomaly'], width=0.01, label='Anomaly', color='blue', alpha=0.5)
    
    # Adding details to the plot
    ax.set_title(f'{area} Data Overview')
    ax.set_xlabel('DateTime')
    ax.set_ylabel('Values')
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.show()

