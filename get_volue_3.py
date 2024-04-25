# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 09:43:31 2024

@author: IGNAOLSZ

This code downloads data from Volue for the provided curve key. This version of the code has set values for the 

get.curve() parameters, future versions of this code will enable change of these parameters. 
"""

import wapi
import pandas as pd
import datetime as dt

ID = 'OE7t6tjKJVsFt3.5eNPhtSmXehtbFNeP'
secret = 'sMTOQr5s9gf4Ml95V8OzD9g-PWCy.hhLfCNpQXnZ0jBI2HIS7GQwpEfO9HqXMCxzIF1Wo58S0rrc9SQQZvMb_mHUdcG2uyWCfF4r'
session = wapi.Session(client_id=ID, client_secret=secret, timeout=30000)

def fetch_voule(curve_key):
    curve_name = curve_key
    curve = session.get_curve(name=curve_name)
    ts = curve.get_instance(issue_date='2018-01-01T00:00', tag='Avg', function='AVERAGE', frequency='D')
    pd_s = ts.to_pandas()
    pd_df = pd_s.to_frame()
    return pd_df

#df = fetch_voule('tt fr con ec00ens °c cet min15 f')

#df

#f'{category_key} {country_code} con ec00ens °c cet min15 f'