# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 14:09:24 2024

@author: IGNAOLSZ
"""

import pandas as pd
from QRLN_Final import merged_df
from transform_5 import transform_data, get_area_name
import numpy as np 
from scipy import stats


data = dict()

merged_df['country_name'] = merged_df['area'].apply(lambda x: get_area_name(x.upper()))
merged_df['PlotDate'] = pd.to_datetime(merged_df[['Year', 'Month', 'Day']])

print('kupa')
#for country_name in merged_df['country_name'].unique():
    
country_name = merged_df['country_name'].unique()

df_country = merged_df[merged_df['country_name'] == 'France']

years = df_country['Year'].drop_duplicates().values
              
dates = pd.date_range(start="2024-01-01", end="2024-12-31")
        
non_zero_anomalies_mask = df_country['Anomaly'] != 0
        
if non_zero_anomalies_mask.any():
    last_non_zero_index = non_zero_anomalies_mask[non_zero_anomalies_mask].index[-1]
    df = df_country.loc[:last_non_zero_index].copy()
            
    most_recent_date = df['PlotDate'].max()
            
    day = most_recent_date.day
    month = most_recent_date.month
    year = most_recent_date.year
            
    anom = round(df['Anomaly'].iloc[-1])
    amon_perc = round((df['Actual'].iloc[-1]/df['Normal'].iloc[-1])*100)
            
    anom_w = round(df['Anomaly'].iloc[-7])
    amon_w_perc = round((df['Actual'].iloc[-7]/df['Normal'].iloc[-7])*100)
            
    tday = df[(df['Day'] == day) & (df['Month'] == month) & (df['Year'] == year)]['PlotDate']
            
    #print("tday length:", len(tday))
    #if not tday.empty:
        #idx = np.where(dates == tday.iloc[0])[0][0]
        #print("Accessing tday")
    #else: 
        #print("tday is empty")
        
    #filtered_df = df[df['Year'].isin(years[:-1])]
                
    #this_week_hist = filtered_df.iloc[idx-7:idx]['Actual', 'Normal'].mean()
    #this_week_hist = []
    
    #for value in years:
        #print('kupa')
        #this_week_hist = df.iloc[idx-7:idx]['Anomaly'][value:+1].mean()
    #this_week_hist = df.iloc[idx-7:idx][years[:-1]].mean()
    
    # Store the results
    this_week_hist = {}

    # Loop through each year
    for year in years:
    # Construct the date for that year using the same month and day as tday
        year_date = pd.Timestamp(year=year, month=month, day=day)
    
    # Ensure the year_date is within the DataFrame's date range
        if year_date in df['PlotDate'].values:
        # Find the index of the year_date in the DataFrame
            date_idx = df[df['PlotDate'] == year_date].index[0]
        
        # Ensure there are at least 7 days prior to the year_date
            if date_idx >= 7:
            # Calculate the mean of 'Anomaly' for the 7 days leading up to the year_date
                mean_anomaly = df.iloc[date_idx-7:date_idx]['Actual'].mean()
                this_week_hist[year] = mean_anomaly
            #else:
                #print(f"Not enough data before {year_date} in year {year}")
        #else:
            #print(f"{year_date} not found in the data range")

    #print("Yearly Anomaly Means:", this_week_hist)
    
    this_week_hist = np.array(list(this_week_hist.values()))
    
    this_week = df.iloc[-8:].Actual.mean()
                
    #quant_one = round(stats.percentileofscore(this_week_hist.values, this_week), 1)
    
    quant_one = round(stats.percentileofscore(this_week_hist, this_week), 1)
                
    data_dict = {
                    'climatology': df, 
                    'anomaly': anom, 
                    'anomaly_percent': amon_perc, 
                    'anomaly_quantile': quant_one,
                    'anomaly_w-1': anom_w, 
                    'anomaly_percent_w-1': amon_w_perc
                }
    
data_dict
                
#data[country_name] = data_dict



#data = process_reservoir_data(merged_df, 3)

#country_name = merged_df['area'].apply(lambda x: get_area_name(x.upper()))

#country_name = country_name.unique()

#for i, country_name in enumerate(country_name): 
#    i = i + 1
    
#    #retrieve data from dict
# country_data = data[country_name]
anom = data_dict['anomaly']
amon_perc = data_dict['anomaly_percent']   
quant_one = data_dict['anomaly_quantile']
anom_w = data_dict['anomaly_w-1']
amon_w_perc = data_dict['anomaly_percent_w-1']
    
#    print(country_name)
print('current anomaly = {}GWh, at {}% of seasonal normal'.format(anom, amon_perc))
print('standing at {}th percentile of the distribution'.format(quant_one)) 
print('last week anomaly = {}GWh, at {}% of seasonal normal'.format(anom_w, amon_w_perc))
print('variation of {}% compared to previous week'.format(amon_perc - amon_w_perc))
#    print('*** \n')