# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:38:20 2024

@author: IGNAOLSZ
"""

import wapi
import pandas as pd
import datetime as dt

ID = 'OE7t6tjKJVsFt3.5eNPhtSmXehtbFNeP'
secret = 'sMTOQr5s9gf4Ml95V8OzD9g-PWCy.hhLfCNpQXnZ0jBI2HIS7GQwpEfO9HqXMCxzIF1Wo58S0rrc9SQQZvMb_mHUdcG2uyWCfF4r'
session = wapi.Session(client_id=ID, client_secret=secret, timeout=30000)

# Assuming the area data is stored in a variable named area_data
area_data = session.get_areas()  # Your area data here

# Function to create a mapping from country/region names to their keys
def create_country_name_to_key_map(area_data):
    country_name_to_key = {}
    for area in area_data:
        # Assuming 'name' is a unique identifier for each entry
        country_name_to_key[area['name'].lower()] = area['key']
    return country_name_to_key

# Assuming category_data is your list of categories
category_data = session.get_categories() # Your category data here

def create_category_name_to_key_map(category_data):
    category_name_to_key = {}
    for category in category_data:
        category_name_to_key[category['name'].lower()] = category['key']
    return category_name_to_key

def fetch_curve_by_name_and_category(country_or_region_name, category_name):
    name_to_key_map = create_country_name_to_key_map(area_data)
    category_name_to_key_map = create_category_name_to_key_map(category_data)
    country_or_region_name_lower = country_or_region_name.lower()
    category_name_lower = category_name.lower()
    
    if country_or_region_name_lower in name_to_key_map and category_name_lower in category_name_to_key_map:
        country_code = name_to_key_map[country_or_region_name_lower]
        category_key = category_name_to_key_map[category_name_lower]
        return fetch_volue_with_category(country_code, category_key)
    else:
        print(f"No data found for '{country_or_region_name}' with category '{category_name}'. Please check the name and category and try again.")
        return None

# Updated fetch_volue function to include category
def fetch_volue_with_category(country_code, category_key):
    curve_name = f'{category_key} {country_code} con ec00ens °c cet min15 f'  # Modify as per actual format needed
    curve = session.get_curve(name=curve_name)
    ts = curve.get_instance(issue_date='2018-01-01T00:00', tag='Avg', function='AVERAGE', frequency='D')
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df

def check_curve_type(curve_key):
    curve = session.get_curve(name=curve_key)
    volue_type = curve.curve_type # check the type of the given curve
    return volue_type

def time_series_curve(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency):
    curve_name = curve_key
    curve = session.get_curve(name=curve_name)
    ts = curve.get_data(data_from, data_to)
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df

def instances_curve(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency):
    curve_name = curve_key
    curve = session.get_curve(name=curve_name)
    ts = curve.get_instance(issue_date)
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df

def tagged_curve(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency):
    curve_name = curve_key
    curve = session.get_curve(name=curve_name)
    ts = curve.get_data(tag, data_from, data_to)
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df

def tagged_instance_curve(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency):
    curve_name = curve_key
    curve = session.get_curve(name=curve_name)
    ts = curve.get_instance(issue_date, tag, function, frequency)
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df

def handle_curve_parameters(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency):
    
    curve_type_key = check_curve_type(curve_key)

    if curve_type_key == 'TIME_SERIES':
        # Set parameters for a curve with a single time series
        pd_df = time_series_curve(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)
    elif curve_type_key == 'INSTANCES':
        # Set parameters for a curve with instances
        pd_df = instances_curve(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)
    elif curve_type_key == 'TAGGED':
        # Set parameters for a curve with tagged time series
        pd_df = tagged_curve(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)
    elif curve_type_key == 'TAGGED_INSTANCES':
        # Set parameters for a curve with instances and tags
        pd_df = tagged_instance_curve(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)
    else:
        # Handle unexpected curve type key
        pd_df = {}
        print(f"Unexpected curve type key: {curve_type_key}")

    return pd_df


def fetch_voule(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency):
    
    pd_df = handle_curve_parameters(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)    

    return pd_df

#df = fetch_voule('tt de con ec00 °c cet min15 f')

#df