# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:21:33 2024

@author: IGNAOLSZ
"""

import pandas as pd
import numpy as np
from scipy import stats

# Sample DataFrame with random data
# Let's create a DataFrame that simulates the data structure you might be working with
data = {
    'PlotDate': pd.date_range(start='2020-01-01', periods=1000, freq='D'),
    'Actual': np.random.randint(100, 200, size=1000)
}
df = pd.DataFrame(data)

# Assuming tday is a specific date from which month and day should be extracted
tday = pd.Timestamp('2023-01-15')
month = tday.month
day = tday.day

# Sample years to loop through
years = [2020, 2021, 2022, 2023]

# Store the results
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

# Convert yearly mean anomalies to a list
this_week_hist_values = list(this_week_hist.values())

# Assuming this_week is the mean of the last 8 days 'Actual' values
this_week = df.iloc[-8:]['Actual'].mean()

# Calculate the percentile rank of this_week against the historical week means
quant_one = round(stats.percentileofscore(this_week_hist_values, this_week), 1)

# Output the results
print("Yearly Anomaly Means:", this_week_hist)
print("Quantile score of the recent week:", quant_one)