# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 15:08:40 2024

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
areas = ['fr','ch','it', 'at', 'np']
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

#Lets's try to get the data through an API 
#def quantify_res_water_levels(areas, data_types):
    
#    for data_type in data_types: 
#       for area in areas:
#            curve_key = get_name(primary_category, area, secondary_category, model, freq, data_type)
#            df = fetch_voule(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)
#            df = transform_data(df, curve_key)
#    return df
            
#df = quantify_res_water_levels(areas, data_types)        

#df
""""
def quantify_res_water_levels(areas, data_types):
    all_data = []  # List to store data from all areas and data types
    for area in areas:
        # Adjust data_types if the area is 'np' and should only use one data type
        current_data_types = data_types if area != 'np' else ['n']
        
        for data_type in current_data_types:
            try:
                curve_key = get_name(primary_category, area, secondary_category, model, freq, data_type)
                df = fetch_voule(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)
                df = transform_data(df, curve_key)
                all_data.append(df)  # Append the successfully processed dataframe
            except Exception as e:
                print(f"An error occurred for {area} with data type {data_type}: {e}")
                # Optionally, handle specific exceptions or perform a recovery action here

    if all_data:
        # Concatenate all dataframes in the list if there is any data collected
        combined_df = pd.concat(all_data, ignore_index=True)
    else:
        # Create an empty dataframe or perform other actions if no data was collected
        combined_df = pd.DataFrame()
    
    return combined_df

df = quantify_res_water_levels(areas, data_types)       

df
"""   
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
        combined_df.to_excel('res_water_levels2.xlsx', index=False, engine='openpyxl')
    else:
        combined_df = pd.DataFrame()
        
    df_n = combined_df[combined_df['data_type'] == 'n'].copy()
    df_sa = combined_df[combined_df['data_type'] == 'sa'].copy()

    return combined_df, df_n, df_sa

#Now let's tranform this standard combined df into particular needs of this tool 

#def transform_res_water_levels:
    



df, dfb, dfc = quantify_res_water_levels(areas, data_types)       

df

dfb

dfc