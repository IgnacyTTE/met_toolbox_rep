# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:55:53 2024

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
number_of_past_years = 5  # Change this to include a different number of past years


# Define the date range based on the current date and number_of_past_years
today = dt.datetime.now()
date_max = today + dt.timedelta(days=240)  # Approx. 8 months ahead
date_min = today - dt.timedelta(days=365 * number_of_past_years)  # Years back

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

    merged_df['country_name'] = merged_df['area'].apply(lambda x: get_area_name(x.upper()))
    merged_df['PlotDate'] = pd.to_datetime(merged_df[['Year', 'Month', 'Day']])

    #data = {}
    countries = merged_df['country_name'].unique()

    for country in countries:
        df = merged_df[merged_df['country_name'] == country]

        # Generating a date range for the last year for indexing
        dates = pd.date_range(start=date_max - pd.DateOffset(years=1), end=date_max, freq='D')

        # Historical production excluding the most recent year
        years = df['Year'].drop_duplicates().values
        df_years = pd.DataFrame(index=dates, columns=years[:-1])
        for year in years[:-1]:
            yearly_data = df[df['Year'] == year]
            for date in dates:
                corresponding_day = yearly_data[(yearly_data['Month'] == date.month) & (yearly_data['Day'] == date.day)]
                df_years.at[date, year] = corresponding_day['Actual'].values[0] if not corresponding_day.empty else np.nan

        df_years['Normal'] = df[df['Year'] == years[-1]]['Normal'].values  # Assuming 'norm' is consistent across the years
        df_years['Month'] = df_years.index.month
        df_years['Day'] = df_years.index.day

        this_year = df[df['Year'] == date_max.year]['Actual']
        this_year.index = pd.date_range(start=date_max - pd.DateOffset(months=4), periods=len(this_year), freq='D')

        # Plotting
        plt.figure()
        plt.plot(df_years.index, df_years[years[:-1]], c='grey', lw=0.5)
        plt.plot(df_years.index, df_years['Normal'], c='k', lw=2, label='norm')
        plt.plot(this_year.index, this_year, c='r', lw=2, label=str(date_max.year))
        plt.legend()
        plt.grid()
        plt.title(country + ' Water Levels')
        plt.xlabel('Date of the Year')
        plt.ylabel('Accumulated GWh')
        plt.show()

        # Calculations (anomalies, percentiles, etc.) would follow here, adapted as needed
# Usage example
merged_df = transform_res(areas, data_types)
plot_reservoir_levels(merged_df, number_of_past_years)