# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:25:09 2024

@author: IGNAOLSZ
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import openpyxl
from scipy import stats
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.dates import DateFormatter, MonthLocator


from get_volue_6 import fetch_voule
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

# Setup the number of years you want to include in the graph
number_of_past_years = 3  # Change this to include a different number of past years


# Define the date range based on the current date and number_of_past_years
today = dt.date.today()
date_max = dt.date(today.year, today.month + 8, today.day)
#date_max = today
date_min = dt.date(date_max.year - number_of_past_years, date_max.month, date_max.day)
fx ='AVERAGE'
fq ='D'

#Get the data from voule using the API
def quantify_res_water_levels(areas, data_types):
    all_data = []
    for area in areas:
        current_data_types = data_types if area != 'np' else ['n']
        
        # Optional: you can also wrap this loop with tqdm for more detailed progress, but it might clutter the output
        for data_type in current_data_types:
            try:
                curve_key = get_name(primary_category, area, secondary_category, model, freq, data_type)
                df = fetch_voule(curve_key, tag, issue_date, issue_date_from, issue_date_to, date_min, date_max, fx, fq)
                df = transform_data(df, curve_key)
                
                # Ensure 'area' and 'data_type' are included in df
                df['area'] = area
                df['data_type'] = data_type
                
                all_data.append(df)
            except Exception as e:
                print(f"An error occurred for {area} with data type {data_type}: {e}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
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



def plot_reservoir_levels(merged_df, number_of_past_years):
    current_year = today.year
    past_year = current_year - 1  # This should be used for historical data plotting

    merged_df['country_name'] = merged_df['area'].apply(lambda x: get_area_name(x.upper()))
    merged_df['PlotDate'] = pd.to_datetime(merged_df[['Year', 'Month', 'Day']])
    
    for country_name in merged_df['country_name'].unique():
        fig, ax = plt.subplots(figsize=(15, 10))
        df_country = merged_df[merged_df['country_name'] == country_name]
        
        # Adjusting the logic to use 'past_year' for plotting historical data
        # Plot historical 'Actual' data for years before the current year
        historical_years = range(current_year - number_of_past_years, current_year)
        for year in historical_years:
            if year != past_year:  # Exclude the immediate past year for a specific highlight, if needed
                df_year = df_country[df_country['Year'] == year]
                ax.plot(df_year['PlotDate'], df_year['Actual'], color='lightgray', lw=1, alpha=0.5, label=f'Historical Actual {year}' if year == historical_years[0] else "")

        # Optionally, specifically highlight the 'past_year' data
        df_past_year = df_country[df_country['Year'] == past_year]
        if not df_past_year.empty:
            ax.plot(df_past_year['PlotDate'], df_past_year['Actual'], color='orange', lw=2, label=f'Actual {past_year}')

        # Continuing with plotting current year data and normals
        df_current_year = df_country[df_country['Year'] == current_year]
        ax.plot(df_current_year['PlotDate'], df_current_year['Actual'], color='red', lw=2, label=f'Actual {current_year}')
        ax.bar(df_current_year['PlotDate'], df_current_year['Anomaly'], width=1, label='Anomaly', color='blue', alpha=0.5)
        # Assuming 'Normal' data is consistent across years and plotting it for the whole year
        if not df_current_year.empty:
            ax.plot(df_current_year['PlotDate'], df_current_year['Normal'], color='black', lw=2, label='Normal')

        ax.set_title(f'Reservoir Water Level Status: {country_name}')
        ax.set_xlabel('Date')
        ax.set_ylabel('GWh')
        ax.legend()
        ax.grid(True)

        ax.set_xlim([pd.to_datetime(f'{current_year}-01-01'), pd.to_datetime(f'{current_year}-12-31')])
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_major_formatter(DateFormatter('%b'))

        plt.xticks(rotation=45)
        plt.show()

merged_df = transform_res(areas, data_types)
plot_reservoir_levels(merged_df, number_of_past_years)

