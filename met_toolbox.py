# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 16:23:44 2024

@author: IGNAOLSZ
"""

import pandas as pd
from area_list_module import data 

def transform_original_date(df):
    df.index.name = 'Original Date'
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df['Day'] = df.index.day
    
    # Remove leap year
    mask = (df['Day'] == 29) & (df['Month'] == 2)
    df = df[~mask].copy(deep=True)
    
    return df

import ftplib

def connect_metelogica_ftp():

    # FTP Information:
    HOSTNAME = "ftp.meteologica.com"
    USERNAME = "axpo_IT_variables"
    PASSWORD = "k.qQ533D"

    # Create server connection
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

    return ftp_server

area_list = pd.DataFrame(data)

# Function to get the area key from the area name
def get_area_key(area_name):
    result = area_list[area_list['name'] == area_name]['key']
    if not result.empty:
        return result.iloc[0].lower()
    else:
        return "Area name not found"