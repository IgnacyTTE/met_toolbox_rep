# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 13:18:11 2024

@author: IGNAOLSZ
"""
import get_volue_2
import pandas as pd
import holidays

#df = fetch_curve_by_name_and_category("France", "Temperature")

def transform_data(df):
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
    # Generate the list of holidays for the relevant years
    year_min, year_max = df['timestamp'].dt.year.min(), df['timestamp'].dt.year.max()
    us_holidays = holidays.UnitedStates(years=range(year_min, year_max + 1))
    # Mark holidays
    df['Holiday'] = df['date'].apply(lambda x: x in us_holidays).astype(int)
    
    # Optionally, drop the 'date' column if it's no longer needed
    df.drop('date', axis=1, inplace=True)
    df.drop('timestamp', axis=1, inplace=True)
    
    first_column_name = df.columns[0]  # Get the name of the first column
    df.rename(columns={first_column_name: 'Value'}, inplace=True)
    
    columns = [col for col in df.columns if col != 'Value'] + ['Value']
    
    df = df[columns]
    
    return df

# Example usage
# Assuming your DataFrame is named df and your timestamp column is set as the index
#transformed_df = transform_data(df)

#transformed_df.head()

#transformed_df.to_csv('transformed_data4.csv', index=True)


