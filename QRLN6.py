# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:32:56 2024

@author: IGNAOLSZ
"""
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import openpyxl
from scipy import stats
import plotly.graph_objects as go
from tqdm.auto import tqdm


from get_volue_5 import fetch_voule
from transform_5 import transform_data, get_area_name
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

# Transform the 'area' column in merged_df to country names
merged_df['country_name'] = merged_df['area'].apply(lambda x: get_area_name(x))

# Assuming 'merged_df' is your DataFrame and the 'country_name' column is already created
country_names = merged_df['country_name'].unique()

# Initialize a list to hold all the figures for each country
figs = []

# Use tqdm for progress bar
for country_name in tqdm(country_names, desc='Plotting Countries'):
    df_country = merged_df[merged_df['country_name'] == country_name]
    
    # Create figure with secondary y-axis for the anomaly
    fig = go.Figure()
    
    # Add Normal plot
    fig.add_trace(go.Scatter(x=df_country['DateTime'], y=df_country['Normal'], name='Normal', line=dict(color='black', width=2)))
    
    # Add Actual plot
    fig.add_trace(go.Scatter(x=df_country['DateTime'], y=df_country['Actual'], name='Actual', line=dict(color='red', width=2)))
    
    # Add Anomaly bar plot
    fig.add_trace(go.Bar(x=df_country['DateTime'], y=df_country['Anomaly'], name='Anomaly', marker_color='blue', opacity=0.5))
    
    # Set titles and labels
    fig.update_layout(title=f'{country_name} Data Overview', xaxis_title='DateTime', yaxis_title='Values',
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig.update_layout(template="plotly_white")
    
    figs.append(fig)
