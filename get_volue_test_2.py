# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 15:36:01 2024

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

def time_series_curve(curve_key, tag, issue_date, issue_date_from, issue_date_to, date_min, date_max, fx, fq):
    curve_name = curve_key
    curve = session.get_curve(name=curve_name)
    ts = curve.get_data(data_from=date_min, data_to=date_max, function=fx, frequency=fq)
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df


tag = 'Ave'
issue_date = '2018-01-01T00:00'
issue_date_from = '2018-01-01T00:00'
issue_date_to = '2018-01-03T00:00'
date_min = '2018-01-01T00:00'
date_max = '2019-01-03T00:00'
fx ='AVERAGE'
fq ='D'
filt = ''


curve_key = 'res np hydro wtr gwh cet h n'

pd_df = time_series_curve(curve_key, tag, issue_date, issue_date_from, issue_date_to, date_min, date_max, fx, fq)

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
    ts = curve.get_data(tag, data_from, data_to, function, frequency)
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


tag = 'Ave'
issue_date = '2018-01-01T00:00'
issue_date_from = '2018-01-01T00:00'
issue_date_to = '2018-01-03T00:00'
data_from = '2018-01-01T00:00'
data_to = '2018-01-03T00:00'
function ='AVERAGE'
frequency ='H'
filt = ''


curve_key = 'res np hydro wtr gwh cet h n'

df = fetch_voule(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)

df
