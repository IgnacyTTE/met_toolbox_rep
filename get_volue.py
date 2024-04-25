# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 10:39:51 2024

@author: IGNAOLSZ
"""

import wapi
import pandas as pd
import datetime as dt

ID = 'OE7t6tjKJVsFt3.5eNPhtSmXehtbFNeP'
secret = 'sMTOQr5s9gf4Ml95V8OzD9g-PWCy.hhLfCNpQXnZ0jBI2HIS7GQwpEfO9HqXMCxzIF1Wo58S0rrc9SQQZvMb_mHUdcG2uyWCfF4r'
session = wapi.Session(client_id=ID, client_secret=secret, timeout=30000)

def fetch_volue(country_code):
    curve_name = 'tt {} con ec00ens °c cet min15 f'.format(country_code)
    curve = session.get_curve(name=curve_name)
    ts = curve.get_instance(issue_date='2018-01-01T00:00', tag='Avg')
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    data = pd_df
    return data

# Assuming the area data is stored in a variable named area_data
area_data = session.get_areas()  # Your area data here

# Function to create a mapping from country/region names to their keys
def create_name_to_key_map(area_data):
    name_to_key = {}
    for area in area_data:
        # Assuming 'name' is a unique identifier for each entry
        name_to_key[area['name'].lower()] = area['key']
    return name_to_key

# Function to fetch the curve based on country or region name
def fetch_curve_by_name(country_or_region_name):
    name_to_key_map = create_name_to_key_map(area_data)
    country_or_region_name_lower = country_or_region_name.lower()
    
    if country_or_region_name_lower in name_to_key_map:
        country_code = name_to_key_map[country_or_region_name_lower]
        return fetch_volue(country_code)  # Assuming fetch_volue is your existing function
    else:
        print(f"No data found for '{country_or_region_name}'. Please check the name and try again.")
        return None
