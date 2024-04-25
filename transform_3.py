# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 18:15:51 2024

@author: IGNAOLSZ
"""

from units import get_unit
#from get_volue_2 import fetch_curve_by_name_and_category 
import pandas as pd
import holidays

import wapi
from wapi import Session
ID = 'OE7t6tjKJVsFt3.5eNPhtSmXehtbFNeP'
secret = 'sMTOQr5s9gf4Ml95V8OzD9g-PWCy.hhLfCNpQXnZ0jBI2HIS7GQwpEfO9HqXMCxzIF1Wo58S0rrc9SQQZvMb_mHUdcG2uyWCfF4r'
session = wapi.Session(client_id=ID, client_secret=secret, timeout=30000)


def extract_country_code(api_key):
    # Split the API key by spaces
    parts = api_key.split()
    country_list = session.get_areas()
    # Iterate over parts to find the country code, excluding 'tt'
    for part in parts:
        # Convert both part and country key to lowercase for comparison
        part_lower = part.lower()
        if part_lower != 'tt' and any(country['key'].lower() == part_lower for country in country_list):
            return part
    # Default to 'de' if no valid country code is found
    return 'de'

def transform_data(df, api_key):
    unit = get_unit(api_key)
    
    # Extract country code from the API key
    country_code = extract_country_code(api_key)
    
    country_code_upper = country_code.upper()
    
    # Fetch holidays specific to the country
    country_holidays = holidays.CountryHoliday(country_code_upper)
    
    # Reset index to make the DateTimeIndex a column
    df = df.reset_index()
    # Ensure the new column (assuming named 'index' if not rename accordingly) is recognized as datetime
    df['timestamp'] = pd.to_datetime(df['index'], utc=True)
    df.drop('index', axis=1, inplace=True)  # Remove the redundant column if it's not automatically named 'timestamp'
    
    # At this point, 'timestamp' is definitely a datetime column. We proceed with transformations:
    
    # Convert the datetime to just a date (for holiday comparison)
    df['date'] = df['timestamp'].dt.date
    
    # Filter out February 29
    df = df[~((df['timestamp'].dt.month == 2) & (df['timestamp'].dt.day == 29))]
    
    # Split datetime into components
    df['Year'] = df['timestamp'].dt.year
    df['Month'] = df['timestamp'].dt.month
    df['Day'] = df['timestamp'].dt.day
    df['Hour'] = df['timestamp'].dt.hour
    df['Minute'] = df['timestamp'].dt.minute
    
    # Day of the week and weekend flag
    df['DofW'] = df['timestamp'].dt.weekday
    df['Weekend'] = (df['timestamp'].dt.weekday >= 5).astype(int)
    
    # Holidays
    # Mark holidays
    df['Holiday'] = df['date'].apply(lambda x: x in country_holidays).astype(int)
    
    # Optionally, drop the 'date' column if it's no longer needed
    df.drop('date', axis=1, inplace=True)
    df.drop('timestamp', axis=1, inplace=True)
    
    first_column_name = df.columns[0]  # Get the name of the first column
    df.rename(columns={first_column_name: 'Value'}, inplace=True)
    
    columns = [col for col in df.columns if col != 'Value'] + ['Value']
    
    df = df[columns]
        
    df['Unit'] = unit 
    
    df['Curve_key'] = api_key
    
    return df 

#transformed_df = transform_data(df, 'res fr hydro sgw GWh cet h n')


#transformed_df.head()