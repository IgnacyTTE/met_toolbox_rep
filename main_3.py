# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:24:58 2024

@author: IGNAOLSZ

This code aims to simplify creating curves for volue
"""
from get_volue_5 import fetch_voule
from transform_4 import transform_data
from volue_name import get_name

#Input data for curves eg. 'tt dk con ec00 °c cet min15 f'
primary_category = 'res'
area = 'fr'
secondary_category = 'hydro wtr'
model = ''
freq = 'h'
datatype = 'n'

#Input parameters for your curve type - supply zero if given parameter not required for your curve
tag = 'Ave'
issue_date = '2018-01-01T00:00'
issue_date_from = '2018-01-01T00:00'
issue_date_to = '2018-01-03T00:00'
data_from = '2018-01-01T00:00'
data_to = '2018-01-03T00:00'
function ='AVERAGE'
frequency ='H'


curve_key = get_name(primary_category, area, secondary_category, model, freq, datatype)

df = fetch_voule(curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)

df = transform_data(df, curve_key)

df



