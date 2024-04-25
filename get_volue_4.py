# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 10:55:05 2024

@author: IGNAOLSZ
"""

import wapi
import pandas as pd
import datetime as dt

ID = 'OE7t6tjKJVsFt3.5eNPhtSmXehtbFNeP'
secret = 'sMTOQr5s9gf4Ml95V8OzD9g-PWCy.hhLfCNpQXnZ0jBI2HIS7GQwpEfO9HqXMCxzIF1Wo58S0rrc9SQQZvMb_mHUdcG2uyWCfF4r'
session = wapi.Session(client_id=ID, client_secret=secret, timeout=30000)

def check_curve_type(curve_key):
    curve = session.get_curve(name=curve_key)
    volue_type = curve.curve_type # check the type of the given curve
    return volue_type

def time_series_curve(curve_key):
    curve_name = curve_key
    curve = session.get_curve(name=curve_name)
    ts = curve.get_data(data_from='2018-01-01T00:00', data_to='2018-01-02T00:00')
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df

def instances_curve(curve_key):
    curve_name = curve_key
    curve = session.get_curve(name=curve_name)
    ts = curve.get_instance(issue_date='2018-01-01T00:00')
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df

def tagged_curve(curve_key):
    curve_name = curve_key
    curve = session.get_curve(name=curve_name)
    ts = curve.get_data(tag='Avg', data_from='2018-01-01T00:00', data_to='2018-01-02T00:00')
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df

def tagged_instance_curve(curve_key):
    curve_name = curve_key
    curve = session.get_curve(name=curve_name)
    ts = curve.get_instance(issue_date='2018-01-01T00:00', tag='Avg', function='AVERAGE', frequency='D')
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df

def handle_curve_parameters(curve_key):
    
    curve_type_key = check_curve_type(curve_key)

    if curve_type_key == 'TIME_SERIES':
        # Set parameters for a curve with a single time series
        pd_df = time_series_curve(curve_key)
    elif curve_type_key == 'INSTANCES':
        # Set parameters for a curve with instances
        pd_df = instances_curve(curve_key)
    elif curve_type_key == 'TAGGED':
        # Set parameters for a curve with tagged time series
        pd_df = tagged_curve(curve_key)
    elif curve_type_key == 'TAGGED_INSTANCES':
        # Set parameters for a curve with instances and tags
        pd_df = tagged_instance_curve(curve_key)
    else:
        # Handle unexpected curve type key
        pd_df = {}
        print(f"Unexpected curve type key: {curve_type_key}")

    return pd_df


def fetch_voule(curve_key):
    
    pd_df = handle_curve_parameters(curve_key)    

    return pd_df

#df = fetch_voule('tt de con ec00 °c cet min15 f')

#df