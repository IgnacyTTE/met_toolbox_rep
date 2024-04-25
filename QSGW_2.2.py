# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 11:44:34 2024

@author: IGNAOLSZ
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math
#import openpyxl
from scipy import stats
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.dates import DateFormatter, MonthLocator
#from openpyxl.drawing.image import Image
import os

from get_volue_6 import fetch_voule
from transform_5 import transform_data, get_area_name
from volue_name import get_name

#Input data for curves eg. 'tt dk con ec00 °c cet min15 f'
primary_category = 'res'
#areas = ['fr','ch','it', 'at' ] #,'np'
secondary_category = 'hydro sgw'
model = ''
freq = 'h'

#number_of_past_years = 10 
areas = ['fr','ch','it', 'at' ]
data_types = ['n', 'sa']
#directory = r"C:\Users\IGNAOLSZ\Documents\Python Scripts\wrapper\hydro_excels"

#Input parameters for your curve type - supply zero if given parameter not required for your curve
tag = 'Ave'
issue_date = '2018-01-01T00:00'
issue_date_from = '2018-01-01T00:00'
issue_date_to = '2018-01-03T00:00'

# Setup the number of years you want to include in the graph
number_of_past_years = 10  # Change this to include a different number of past years


# Define the date range based on the current date and number_of_past_years
today = dt.date.today()
date_max = dt.date(year=today.year, month=12, day=31)
#date_max = today
date_min = dt.date(date_max.year - number_of_past_years + 1, date_max.month, date_max.day)
fx ='AVERAGE'
fq ='D'


#Get the data from voule using the API
def quantify_res_snow_levels(areas, data_types):
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

def process_snow_data(merged_df, number_of_past_years):
    data = dict()

    merged_df['country_name'] = merged_df['area'].apply(lambda x: get_area_name(x.upper()))
    merged_df['PlotDate'] = pd.to_datetime(merged_df[['Year', 'Month', 'Day']])

    for country_name in merged_df['country_name'].unique():
        df_country = merged_df[merged_df['country_name'] == country_name]
        
        years = df_country['Year'].drop_duplicates().values
        
        # First, create a mask of non-zero anomalies
        non_zero_anomalies_mask = df_country['Anomaly'] != 0
        
        # Then, find the index of the last true value in this mask
        last_non_zero_index = non_zero_anomalies_mask[non_zero_anomalies_mask].index[-1]

        # Now, slice the DataFrame to include only up to the last non-zero anomaly
        df = df_country.loc[:last_non_zero_index].copy()
        
        df.reset_index(drop=True, inplace=True)
        
        most_recent_date = df['PlotDate'].max()
        
        day = most_recent_date.day
        month = most_recent_date.month
        
        #calculate delta from norm today and last week
        anom = round(df['Anomaly'].iloc[-1])
        amon_perc = round((df['Actual'].iloc[-1]/df['Normal'].iloc[-1])*100)
                
        anom_w = round(df['Anomaly'].iloc[-7])
        amon_w_perc = round((df['Actual'].iloc[-7]/df['Normal'].iloc[-7])*100)
        
        this_week_hist = {}

        # Loop through each year
        for value in years:
        # Construct the date for that year using the same month and day as tday
            year_date = pd.Timestamp(year=value, month=month, day=day)
        
        # Ensure the year_date is within the DataFrame's date range
            if year_date in df['PlotDate'].values:
            # Find the index of the year_date in the DataFrame
                date_idx = df[df['PlotDate'] == year_date].index[0]
            
            # Ensure there are at least 7 days prior to the year_date
                if date_idx >= 7:
                # Calculate the mean of 'Anomaly' for the 7 days leading up to the year_date
                    mean_anomaly = df.iloc[date_idx-7:date_idx]['Actual'].mean()
                    this_week_hist[value] = mean_anomaly
        
        
        this_week_hist = np.array(list(this_week_hist.values()))
        
        this_week = df.iloc[-8:].Actual.mean()
        
        quant_one = round(stats.percentileofscore(this_week_hist,this_week),1)
        
        data_dict = {'climatology' : df, 'anomaly': anom, 'anomaly_percent': amon_perc, 'anomaly_quantile': quant_one,
                     'anomaly_w-1': anom_w, 'anomaly_percent_w-1': amon_w_perc}
        
        data[country_name] = data_dict

    return data

#Transform the data to this particular use case

def transform_res(areas, data_types):
    df, df_n, df_sa = quantify_res_snow_levels(areas, data_types)

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
        
def plot_snow_levels(merged_df, number_of_past_years):
    current_year = dt.datetime.now().year

    merged_df['country_name'] = merged_df['area'].apply(lambda x: get_area_name(x.upper()))
    merged_df['PlotDate'] = pd.to_datetime(merged_df[['Year', 'Month', 'Day']])
    
    for country_name in merged_df['country_name'].unique():
        fig, ax = plt.subplots(figsize=(15, 10))
        df_country = merged_df[merged_df['country_name'] == country_name]
          
        # Plot data for the selected years in gray (Only 'Actual')
        for year in range(date_min.year, current_year):
            df_year = df_country[df_country['Year'] == year]
            if not df_year.empty:
                plot_dates = pd.to_datetime(dict(year=current_year, month=df_year['Month'], day=df_year['Day']))
                ax.plot(plot_dates, df_year['Actual'], color='gray', lw=1, 
                        label='Past Data' if year == date_min.year else "", alpha=0.5)

        # Plot 'Actual' for the current year, excluding zeros
        df_actual_current_year = df_country[(df_country['Year'] == current_year) & (df_country['Actual'] != 0)]
        ax.plot(df_actual_current_year['PlotDate'], df_actual_current_year['Actual'], color='red', lw=2, label='Actual')

        # Plot 'Anomaly' for the current year, where 'Actual' is not zero
        ax.bar(df_actual_current_year['PlotDate'], df_actual_current_year['Anomaly'], width=1, label='Anomaly', color='blue', alpha=0.5)

        # Plot 'Normal' for the current year for context
        df_normal_current_year = df_country[df_country['Year'] == current_year]
        ax.plot(df_normal_current_year['PlotDate'], df_normal_current_year['Normal'], color='black', lw=2, label='Normal')

        ax.set_title(f'Snow and Grownd Water Level Status: {country_name}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Accumulated GWh')
        ax.legend()
        ax.grid(True)

        ax.set_xlim([pd.to_datetime(f'{current_year}-01-01'), pd.to_datetime(f'{current_year}-12-31')])
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_major_formatter(DateFormatter('%b'))

        plt.xticks(rotation=45)
        plt.tight_layout()  # Adjust layout to make better use of space
        yield fig, country_name
        
#All data saved to excel
def save_and_display_data_and_plots_to_excel(merged_df, number_of_past_years, directory, data):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Filename with current date and time
    timestamp = today 
    excel_filename = os.path.join(directory, f'Snow_and_Grownd_Water_Level_Status_{timestamp}.xlsx')
    
    # Save data to different sheets in the same Excel file
    with pd.ExcelWriter(excel_filename, engine='openpyxl', mode='w') as writer:
        # Save the merged DataFrame to the first sheet
        merged_df.to_excel(writer, index=False, sheet_name='Merged Data')

        # Prepare lists for the second DataFrame
        countries = []
        current_anomalies = []
        current_anomaly_percents = []
        quantiles = []
        last_week_anomalies = []
        last_week_anomaly_percents = []

        # Iterate over the data to populate the lists
        for country_name, country_data in data.items():
            countries.append(country_name)
            current_anomalies.append(country_data['anomaly'])
            current_anomaly_percents.append(country_data['anomaly_percent'])
            quantiles.append(country_data['anomaly_quantile'])
            last_week_anomalies.append(country_data['anomaly_w-1'])
            last_week_anomaly_percents.append(country_data['anomaly_percent_w-1'])

        # Create a DataFrame from the lists
        df_country_data = pd.DataFrame({
            'Country': countries,
            'Current Anomaly (GWh)': current_anomalies,
            'Current Anomaly Percent': current_anomaly_percents,
            'Quantile of Current Anomaly': quantiles,
            'Last Week Anomaly (GWh)': last_week_anomalies,
            'Last Week Anomaly Percent': last_week_anomaly_percents
        })

        # Save the DataFrame to the second sheet
        df_country_data.to_excel(writer, index=False, sheet_name='Country Stat')
        merged_df.to_excel(writer, index=False, sheet_name='Country Data')
    
    
    # Retrieve and prepare the plots
    plots = list(plot_snow_levels(merged_df, number_of_past_years))  # Example: 5 years
    number_of_plots = len(plots)
    
    # Determine the grid size for the subplot
    grid_size = math.ceil(math.sqrt(number_of_plots))
    
    # Define the figure size and layout for combined figure
    fig, axs = plt.subplots(nrows=grid_size, ncols=grid_size, figsize=(15, 10))
    
    # Flatten the axis array for easier iteration if there are multiple axes
    if number_of_plots > 1:
        axs = axs.flatten()
    
    for idx, (country_plot, country_name) in enumerate(plots):
        # Save individual country plots
        image_filename = f'Snow_and_Grownd_Water_Level_Status_{country_name}_{timestamp}.png'
        image_path = os.path.join(directory, image_filename)
        country_plot.savefig(image_path)
        plt.close(country_plot)  # Close the figure to free up memory
        
        # Load and display the plot in the combined figure
        ax = axs[idx]
        ax.imshow(plt.imread(image_path))
        ax.axis('off')  # Hide axes
        ax.set_title(country_name)

    # Turn off unused subplots in the grid
    for ax in axs[idx+1:]:
        ax.axis('off')

    # Display the combined figure interactively
    plt.tight_layout()
    plt.show()

    # Save the combined figure
    combined_image_filename = f'Combined_Snow_and_Grownd_Water_Level_Status_{timestamp}.png'
    combined_image_path = os.path.join(directory, combined_image_filename)
    fig.savefig(combined_image_path)
    plt.close(fig)  # Close the figure to free up memory
    print(f"Data saved to {excel_filename}")
      
def process_and_visualize_snow_data():
    
    number_of_past_years = 10 
    areas = ['fr','ch','it', 'at' ]
    data_types = ['n', 'sa']
    directory = r"C:\Users\IGNAOLSZ\Documents\Python Scripts\wrapper\hydro_excels"
    
    merged_df = transform_res(areas, data_types)
    plot_snow_levels(merged_df, number_of_past_years)
    data = process_snow_data(merged_df, number_of_past_years)
    country_names = merged_df['area'].apply(lambda x: get_area_name(x.upper())).unique()
    save_and_display_data_and_plots_to_excel(merged_df, number_of_past_years, directory, data)
    print(f"Data processing and visualization completed for countries: {country_names}")

process_and_visualize_snow_data()